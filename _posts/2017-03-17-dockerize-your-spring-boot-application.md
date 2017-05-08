---
layout: post
title: Dockerize Your Spring Boot Application
published: true
comments: true
tags: [Docker, Maven, Spring, Spring Boot]
image: /images/entry/spring-boot-docker.png
---

It has been nearly a year since my last posting on [Docker](https://indrabasak.wordpress.com/2016/04/05/dockerize-your-rest-api/). The popularity of Docker has since grown by leaps and bounds. In this posting, I will show you how to create a Docker image of a Spring Boot application using a Maven Docker [plugin](https://github.com/spotify/docker-maven-plugin). 

It's the  continuation of my Book API example. The book REST service provides functionality to create, search, update, and delete a book item. To keep the example simple, the persistence layer is an in-memory Java HashMap. The full example can be found [here](https://github.com/indrabasak/docker-example). Here is the example book controller. 

{% gist 6f71cedd8ae5ee60e37363a1538115a4  %}

### Maven Docker Plugin

Spotify's Maven plugin has simplified the creation of Docker image from a Maven project artifacts. The example Maven project consists of two child projects (model and service). Here are the changes to the parent POM.

#### Parent POM

{% gist a2ca9b6550218b0c4715a0ba89b0af8f  %} 

The `skipDockerBuild` tag is set to <span style="color: #000000;">true</span> in order to skip the Docker build process in the parent project when your run the Docker build from the parent project folder.

#### Service POM

The `skipDockerBuild` tag is overridden in the service POM by setting it to `false`. Here is the snippet of the service POM. 

{% gist c4ac5a0a3694a2f596273e65e0f1e369  %}

##### Configuration Tags

*   `imageName`: specifies the name of the example Docker image, e.g., _docker-example_.
*   `dockerDirectory`: specifies the location of the `Dockerfile`. In our example, the location is `/src/main/docker` folder. The contents of the dockerDirectory will be copied into the `${project.build.directory}/docker` folder.
*   `resources`: includes a list of `resource` elements. Each resource describes the files/resources be included with the Docker image.
*   `targetPath`: specifies the directory structure to place the build resources.  In our example, it defaults to the base project (_docker-example-service_) directory.
*   `directory`: specifies the location of resource. In our example, it's the _${project.build.directory}_.
*   `include`: specifies the resources to be included in the Docker image, which in this case is the _docker-example-service-1.0.jar_.

### Dockerfile

A [`Dockerfile`](https://docs.docker.com/engine/reference/builder/) specifies all the instructions to be read by a Docker engine while building the image. 

{% gist dd7b768f078eb32014059850550712f0  %}

#### Instruction

*   `FROM` instruction sets the Base Image for subsequent instructions. FROM must be the first non-comment instruction in the Dockerfile.
*   `VOLUME` instruction creates a mount point with the specified name.
*   `ADD` instruction copies from and adds them to the filesystem of the image at the path.
*   `RUN` instruction executes the command on top of the current image.
*   `EXPOSE` instruction informs Docker that the container listens on the specified network ports at runtime.
*   `ENV` instruction sets the environment variable
*   `ENTRYPOINT` allows you to configure a container that will run as an executable.
*   `LABEL` instruction adds metadata to an image.

You can find more about Docker instructions [`here`](https://docs.docker.com/engine/reference/builder/#usage)

### Docker Build

Assuming you have already installed Docker in your computer. If you haven't, [here](https://docs.docker.com/docker-for-mac/install/#what-to-know-before-you-install) is the instruction for installing Docker for Mac. Once you have Docker installed and running, it should show up as a `whale` in the top status bar. Execute the following maven command from the directory of the parent project, `docker-example`:

```
    mvn clean package docker:build
```

This should create a Docker image named `docker-example`. You will notice maven executing the instructions specified in the Dockerfile.

```bash
ibasa$ mvn clean package docker:build
[INFO] Scanning for projects...
[INFO]
[INFO] ------------------------------------------------------------------------
[INFO] Building Docker Example Service 1.0
[INFO] ------------------------------------------------------------------------
…
[INFO] Building image docker-example
Step 1 : FROM frolvlad/alpine-oraclejdk8:slim
---> 00d8610f052e
Step 2 : VOLUME /tmp
---> Using cache
---> 73a7ca0c26ba
Step 3 : ADD docker-example-service-1.0.jar app.jar
---> a18050579c6d
Removing intermediate container 620985e0927e
Step 4 : RUN sh -c 'touch /app.jar'
---> Running in 6a41b2b6aa83
---> 20331fa49094
Removing intermediate container 6a41b2b6aa83
Step 5 : EXPOSE 8080
---> Running in 82ed746dc381
---> 7d4464042f2a
Removing intermediate container 82ed746dc381
Step 6 : ENV JAVA_OPTS ""
---> Running in cc6469042859
---> e08d3943dbfe
Removing intermediate container cc6469042859
Step 7 : ENTRYPOINT java -Djava.security.egd=file:/dev/./urandom -Dapp.port=${app.port} -jar /app.jar
---> Running in 14f08b15e3c7
---> 01e87692e479
Removing intermediate container 14f08b15e3c7
Step 8 : LABEL maintainer "Indra Basak"
---> Running in b017e600dc45
---> dbbcbdfaecf9
Removing intermediate container b017e600dc45
Successfully built dbbcbdfaecf9
[INFO] Built docker-example
[INFO] ------------------------------------------------------------------------
[INFO] Reactor Summary:
[INFO]
[INFO] Docker Examples .................................... SUCCESS [ 1.837 s]
[INFO] Docker Example Model ............................... SUCCESS [ 2.002 s]
[INFO] Docker Example Service ............................. SUCCESS [ 8.970 s]
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time: 16.138 s
[INFO] Finished at: 2017-03-17T14:01:01-07:00
[INFO] Final Memory: 50M/486M
[INFO] ------------------------------------------------------------------------
```

###  Docker Run

Run (deploy) the newly created Docker image, `docker-example`, by executing the [`docker run`](https://docs.docker.com/engine/reference/run/) command from the terminal:

    docker run --rm -p 8080:8080  --name=cheetos docker-example

#### [](https://github.com/indrabasak/docker-example#options)Options

*   `--rm` option automatically clean up the container and remove the file system when the container exit.
*   `--name` option names the Docker container as `cheetos`. In absence of the `--name` option, the Docker generates a random name for your container.
*   [`-p 8080:8080`](https://docs.docker.com/engine/reference/run/#expose-incoming-ports) option publishes all exposed ports to the host interfaces. In this example, port `8080` is both `hostPort` and `containerPort`

This should start up the example application and it can be accessed at `http://localhost:8080`

```bash
basak$ docker run --rm -p 8080:8080 --name=cheetos docker-example

..
:: Spring Boot :: (v1.4.5.RELEASE)
…

2017-03-17 21:15:28.493 INFO 1 --- [ main] c.b.example.docker.boot.BookApplication : Starting BookApplication on 233c21816a84 with PID 1 (/app.jar started by root in /)
…
2017-03-17 21:20:26.510 INFO 1 --- [ main] o.s.b.a.e.mvc.EndpointHandlerMapping : Mapped "{[/info || /info.json],methods=[GET],produces=[application/json]}" onto public java.lang.Object org.springframework.boot.actuate.endpoint.mvc.EndpointMvcAdapter.invoke()
2017-03-17 21:20:26.580 INFO 1 --- [ main] o.s.b.a.e.mvc.EndpointHandlerMapping : Mapped "{[/autoconfig || /autoconfig.json],methods=[GET],produces=[application/json]}" onto public java.lang.Object org.springframework.boot.actuate.endpoint.mvc.EndpointMvcAdapter.invoke()
2017-03-17 21:20:28.441 INFO 1 --- [ main] s.w.s.m.m.a.RequestMappingHandlerAdapter : Looking for @ControllerAdvice: org.springframework.boot.context.embedded.AnnotationConfigEmbeddedWebApplicationContext@41975e01: startup date [Fri Mar 17 21:15:28 GMT 2017]; root of context hierarchy
2017-03-17 21:20:29.758 INFO 1 --- [ main] o.s.w.s.handler.SimpleUrlHandlerMapping : Mapped URL path [/webjars/**] onto handler of type [class org.springframework.web.servlet.resource.ResourceHttpRequestHandler]
2017-03-17 21:20:29.758 INFO 1 --- [ main] o.s.w.s.handler.SimpleUrlHandlerMapping : Mapped URL path [/**] onto handler of type [class org.springframework.web.servlet.resource.ResourceHttpRequestHandler]
2017-03-17 21:20:30.070 INFO 1 --- [ main] .m.m.a.ExceptionHandlerExceptionResolver : Detected @ExceptionHandler methods in exceptionProcessor
2017-03-17 21:20:30.766 INFO 1 --- [ main] o.s.w.s.handler.SimpleUrlHandlerMapping : Mapped URL path [/**/favicon.ico] onto handler of type [class org.springframework.web.servlet.resource.ResourceHttpRequestHandler]
2017-03-17 21:26:19.385 INFO 1 --- [ main] o.s.j.e.a.AnnotationMBeanExporter : Registering beans for JMX exposure on startup
2017-03-17 21:26:19.400 INFO 1 --- [ main] o.s.c.support.DefaultLifecycleProcessor : Starting beans in phase 0
2017-03-17 21:26:19.514 INFO 1 --- [ main] o.s.c.support.DefaultLifecycleProcessor : Starting beans in phase 2147483647
2017-03-17 21:26:19.516 INFO 1 --- [ main] d.s.w.p.DocumentationPluginsBootstrapper : Context refreshed
2017-03-17 21:26:19.573 INFO 1 --- [ main] d.s.w.p.DocumentationPluginsBootstrapper : Found 1 custom documentation plugin(s)
2017-03-17 21:26:19.636 INFO 1 --- [ main] s.d.s.w.s.ApiListingReferenceScanner : Scanning for api listing references
2017-03-17 21:26:21.079 INFO 1 --- [ main] s.b.c.e.t.TomcatEmbeddedServletContainer : Tomcat started on port(s): 8080 (http)
2017-03-17 21:26:21.124 INFO 1 --- [ main] c.b.example.docker.boot.BookApplication : Started BookApplication in 654.396 seconds (JVM running for 309.048)
```


### Docker Commands

Here is a list Docker commands which will come handy.

#### List Container

Run the [`docker ps`](https://docs.docker.com/v1.11/engine/reference/commandline/ps/) to list 
all the containers. To see all running containers, execute the following command:

```bash
bash-3.2$ docker ps
CONTAINER ID      IMAGE                 COMMAND                    CREATED           STATUS             PORTS                NAMES
d03854fb7779      docker-example   "java -Djava.security"     7 seconds ago     Up 6 seconds    0.0.0.0:8080->8080/tcp      cheetos
```

To see all running containers including the non-running ones, execute the following command:

```bash
bash-3.2$ docker ps -a
CONTAINER ID   IMAGE COMMAND                                     CREATED                         STATUS                              PORTS                             NAMES
d03854fb7779   docker-example "java -Djava.security"   About a minute ago                   Up About a minute         0.0.0.0:8080->8080/tcp                         cheetos
28b2cff9e7e6   docker-example "java -Djava.security"    About an hour ago        Exited (0) About an hour ago                                                         indra1
d2720676c932            nginx "nginx -g 'daemon off"         4 months ago              Exited (0) 4 months ago                                                     webserver
```


#### Remove Container

To remove a Docker container, execute [`docker rm`](https://docs.docker.com/v1.11/engine/reference/commandline/rm/) command. This will remove a non-running container.

```bash
bash-3.2$ docker rm indra1
indra1
```

To forcefully remove a running container,

```bash
bash-3.2$ docker rm -f cheetos
cheetos
```

#### [](https://github.com/indrabasak/docker-example#stop-container)Stop Container

To stop a container, execute [`docker stop`](https://docs.docker.com/v1.11/engine/reference/commandline/stop/) command:

```bash
bash-3.2$ docker stop cheetos
cheetos
```

