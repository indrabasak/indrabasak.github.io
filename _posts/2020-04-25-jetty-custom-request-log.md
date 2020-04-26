---
layout: post
title: Custom Logging in Jetty
published: true
comments: true
tags: [Spring Boot, Jetty, Log]

image: /images/entry/jetty-log.svg
---

There're times when an out-of-the-box solution for access log is not enough and one has to customize the logging 
output for various reasons, including security. Recently, I had to redact a part of the 
request URL for requests matching certain. In the request log example shown in Figure 1, the word `rosemont` in the URL 
had to be substituted with the word `REDACTED`.

```bash
10.4.130.26 - - [25/Apr/2020:21:01:23 +0000] "GET /health HTTP/1.1" 200 383 "-" "kube-probe/1.17"
10.4.140.33 - - [25/Apr/2020:21:01:28 +0000] "GET /myservice/tokens/zipcode/97068/rosemont HTTP/1.1" 200 40 "-" "insomnia/7.1.1"
```

{:.image-caption}
Figure 1. Request logs before redaction

In a Spring Boot application running an embedded Jetty, one has to enable the access log property, as shown in
 Figure 2, to generate request logs.
 
```yaml
server:
  jetty:
    accesslog:
      enabled: true
```   

{:.image-caption}
Figure 2. Property to enable Jetty access log  

It used to be a relatively easy task to customize the request log in a Jetty web server by modifying the
 `JettyServletWebServerFactory`. As shown in Figure 3, one had to set the custom request log 
 by adding a server customizer.

```java
@Bean
public JettyServletWebServerFactory jettyEmbeddedServletContainerFactory(
        @Value("${server.port:8080}") final String port) {
    final JettyServletWebServerFactory factory =
        new JettyServletWebServerFactory(Integer.valueOf(port));

    factory.addServerCustomizers(server -> {
        server.setRequestLog(new MyCustomRequestLog(new RequestLogWriter(),
                                                    CustomRequestLog.EXTENDED_NCSA_FORMAT))
    });

    return factory;
}
```

{:.image-caption}
Figure 3. Setting a custom request log inside a Jetty customizer 

The changes shown in Figure 3, no longer works in `2.3.0-M4` version of Spring Boot library. It stopped working as the
Jetty dependency in the new Spring Boot version overwrites the custom requst log set in the customizer. The built-in
Jetty customizer, `JettyWebServerFactoryCustomizer`, gets loaded last thus overwriting any changes I made to add a 
custom request log.

However, there's an alternative approach that I have came across which solved my dilemma. Instead of setting the 
request log directly on the server from the customizer, add a custom configuration and make it the last 
configuration that gets loaded by Jetty. The custom configuration is added to the `WebAppContext`. The new approach
introduced a new `CustomRequestLogConfiguration` class which instantiates and sets my request log, `MyCustomRequestLog`. 
The new approach, as shown in Figure 4, still needs a Jetty customizer. 


```java
@Configuration
public class CustomJettyConfiguration {

    @Bean
    public JettyServletWebServerFactory jettyEmbeddedServletContainerFactory(
            @Value("${server.port:8080}") final String port) {
        final JettyServletWebServerFactory factory =
                new JettyServletWebServerFactory(Integer.valueOf(port));

        factory.addServerCustomizers(server -> {
            WebAppContext context = (WebAppContext) server.getHandler();
            org.eclipse.jetty.webapp.Configuration[] configs = context.getConfigurations();
            org.eclipse.jetty.webapp.Configuration[] modifiedConfigs =
                    new org.eclipse.jetty.webapp.Configuration[configs.length + 1];
            System.arraycopy(configs, 0, modifiedConfigs, 0, configs.length);
            modifiedConfigs[configs.length] = new CustomRequestLogConfiguration();
            context.setConfigurations(modifiedConfigs);
        });

        return factory;
    }

    private static class CustomRequestLogConfiguration extends AbstractConfiguration {

        @Override
        public void configure(WebAppContext context) {
            context.getServer().setRequestLog(
                    new MyCustomRequestLog(new RequestLogWriter(),
                                           CustomRequestLog.EXTENDED_NCSA_FORMAT));
        }
    }
}
```

{:.image-caption}
Figure 4. A new approach to setting a custom Jetty request log 

Figure 5 shows the content of my custom request log which extends from Jetty's `CustomRequestLog`. This class matches
a `GET` request having a `/myservice/tokens/**` URL pattern. If the request matches the criteria, it substitutes
the last segment of the request URL with the word `REDACTED`. My custom log delegates it to its super class if the 
request doesn't match the criteria.

```java
    private static class MyCustomRequestLog extends CustomRequestLog {
        private static final ThreadLocal<StringBuilder> buffers =
                ThreadLocal.withInitial(() -> new StringBuilder(256));

        private static final String MY_URL = "/myservice/tokens/**";

        private final Writer writer;

        private final PathPattern pattern;

        private final DateCache dateCache;

        public MyCustomRequestLog(Writer writer, String formatString) {
            super(writer, formatString);
            this.writer = writer;

            PathPatternParser pp = new PathPatternParser();
            pattern = pp.parse(MY_URL);

            TimeZone timeZone = TimeZone.getTimeZone("GMT");
            Locale locale = Locale.getDefault();
            dateCache = new DateCache(DEFAULT_DATE_FORMAT, locale, timeZone);
        }

        @Override
        public void log(Request request, Response response) {
            String requestURI = request.getRequestURI();
            if (RequestMethod.GET.name().equals(request.getMethod()) &&
                    pattern.matches(PathContainer.parsePath(requestURI))) {
                try {
                    requestURI = requestURI.substring(0, requestURI.lastIndexOf('/'))
                            + "/REDACTED";
                    StringBuilder sb = buffers.get();
                    sb.setLength(0);

                    sb.append(request.getHttpChannel().getEndPoint()
                                      .getRemoteAddress().getAddress()
                                      .getHostAddress())
                            .append(" - - [")
                            .append(dateCache.format(request.getTimeStamp()))
                            .append("] \"")
                            .append(request.getMethod())
                            .append(" ")
                            .append(requestURI)
                            .append(" ")
                            .append(request.getProtocol())
                            .append("\" ")
                            .append(response.getStatus())
                            .append(" ")
                            .append(response.getHttpChannel().getBytesWritten())
                            .append(" \"-\" \"")
                            .append(request.getHeader("User-Agent"))
                            .append("\"");

                    writer.write(sb.toString());
                } catch (Exception e) {
                    LOG.warn("Unable to log request", e);
                }
            } else {
                super.log(request, response);
            }
        }

        @Override
        protected void stop(LifeCycle lifeCycle) throws Exception {
            buffers.remove();
            super.stop(lifeCycle);
        }
    }
```

{:.image-caption}
Figure 5. A custom Jetty request log 

After adding the custom request log, the log from Figure 1 looks like the one shown below,

```bash
10.4.130.26 - - [25/Apr/2020:21:01:03 +0000] "GET /health HTTP/1.1" 200 383 "-" "kube-probe/1.17"
10.4.130.26 - - [25/Apr/2020:21:01:13 +0000] "GET /health HTTP/1.1" 200 383 "-" "kube-probe/1.17"
10.4.130.26 - - [25/Apr/2020:21:01:23 +0000] "GET /health HTTP/1.1" 200 383 "-" "kube-probe/1.17"
10.4.140.33 - - [25/Apr/2020:21:01:28 +0000] "GET /myservice/tokens/zipcode/97068/REDACTED HTTP/1.1" 200 40 "-" "insomnia/7.1.1"
10.4.140.33 - - [25/Apr/2020:21:01:31 +0000] "GET /myservice/strings/zipcode/97068/Ao6bQf1QuJAxw5LovOpGioKnwDKNAR4Dyp5myQ HTTP/1.1" 200 7 "-" "insomnia/7.1.1"
```

{:.image-caption}
Figure 6. Redacted request logs
