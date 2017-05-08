---
layout: post
title: Swagger 2 Integration with Spring REST
published: true
comments: true
tags: [REST, Spring, Swagger]
image: /images/entry/swagger.png
---

This is the continuation of my earlier posting,  [Swagger For the REST of Us](https://indrabasak.github.io/swagger-for-the-rest-of-us/). Here,  I will cover Springfox integration with my REST Hello World project. Though Springfox supports both 1.2 and 2.0 versions of the Swagger specification, I will stick to Swagger 2.0 specification.

Swagger generates metadata including server host name, endpoint URL, mime-types that the API can consume or produce, data types produced and consumed by operations, etc. Swagger exposes API documentation in JSON format by scanning the source code. Swagger UI is part of the Swagger project and consists of a collection of HTML, Javascript, and CSS resources. Swagger UI takes Swagger compliant JSON API documents as input and dynamically generates an interactive UI of the REST services.

I will continue with the ongoing REST Hello World example. You can find the last version of the example in [REST API and Error Handling](https://indrabasak.github.io/rest-api-and-error-handling/) posting. The example source code mentioned in this posting can be found [here](https://github.com/indrabasak/rest-springfox).

### Changes to Maven Dependencies

*   Add <span style="color:#008000;">springfox-swagger2</span> dependency to integrate Swagger Springfox with Spring REST service example.
*   Add <span style="color:#008000;">springfox-swagger-ui</span> dependency to enable Swagger UI.

{% gist 93e0a2b8dfe44e27dc0c21e6a10aee39 %}

### Configure Docket Configuration Bean

Create a new Docket bean to configure Swagger. A Docket bean is a POJO enabled by `@Configuration`, `@EnableSwagger2`, 
and `@Bean` annotations. For Swagger 2.0, use `@EnableSwagger2` annotation. Here is the example Docket bean: 

{% gist 829ace67721b9ea7a81ee118151daa96 %} 

Import the bean by adding the package name (if it's missing) in the component-scan tag of the existing `rest-dispatcher-servlet.xml`. 

{% gist b38af1aa69841eabf87ba4d0294f814d %}

### Verification of Swagger

Once you have the example running, Swagger documentation in JSON format can be viewed at `localhost:8080/rest-swag-simple/api-docs`.

![0](https://indrabasak.files.wordpress.com/2016/04/0.png)

### Enable Swagger UI

Other than the addition of new `springfox-swagger-ui` dependency in the pom.xml, changes need to be made to the 
`rest-dispatcher-servlet.xml` to serve the static UI content of Swagger UI. Here are the changes to `rest-dispatcher-servlet.xml`: 

{% gist 14be82f1fcb9f4230d827aff863e1008 %}

### Verification of Swagger UI

Once you deploy the example in Tomcat, the Swagger UI can be viewed by visiting `http://localhost:8080/rest-springfox/swagger-ui.html` in any browser. In my experience, the behavior of Swagger in Internet Explorer is flaky.

![swag-1](https://indrabasak.files.wordpress.com/2016/04/swag-1.png) 

Once you have access to Swagger UI, you can view all the operations by clicking **Show/Hide**. 

![swag-2.png](https://indrabasak.files.wordpress.com/2016/04/swag-2.png) 

You can play around with any of the operations by clicking the operation link. Once the operation is expanded, you can retrieve data by clicking **Try it out!** button. In this example, try out **getCustomers** operation. It should fetch a list of customers.

![swag-3](https://indrabasak.files.wordpress.com/2016/04/swag-3.png)

### Further Customization of Controller (Optional)

Use Swagger annotation to make the API more descriptive and hide some of the internal information, e.g., a controller's method names, etc. Here are some of the Swagger annotations commonly used to document a controller:

*   `@Api` describes the general responsibility of the controller.
*   `@ApiOperatio`n describes the responsibility of a specific method.
*   `@ApiParam` describes a  method parameter. It also describes whether a parameter is mandatory or not.

{% gist 7dab321b590cea64d89be7a274838733 %}

Swagger UI should look more descriptive if you now visit http://localhost:8080/rest-springfox/swagger-ui.html in your browser. 

![swag-4](https://indrabasak.files.wordpress.com/2016/04/swag-4.png)