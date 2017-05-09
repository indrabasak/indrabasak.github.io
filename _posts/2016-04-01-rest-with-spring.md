---
layout: post
title: REST with Spring
published: true
comments: true
tags: [REST, Spring]
image: /images/entry/spring.png
---

Spring relies on its Spring MVC framework to support REST APIs. The concept of Model-View-Controller (MVC) was introduced in the the seventies at Xerox Parc. MVC pattern makes an attempt to modularize software by isolating different functional units from each other. It separates application domain/data (model) from the display of the application state (view) and the interaction with the model and view (controller). 

![spring-mvc](https://indrabasak.files.wordpress.com/2016/04/spring-mvc.png?w=300)

### Spring MVC

Not let's see how Spring applies the MVC pattern by following the life of a HTTP request. Once a HTTP request reaches the web server, it is intercepted by Spring's DispatcherServlet. The DispatcherServlet is the front controller servlet where a single servlet delegates the responsibility of actual processing to other components. A Spring MVC controller is responsible for actual processing. Since an application may possess more than one controller, the DispatcherServlet relies on handler mappings to route the request to the intended controller. Mapping is based on the request URL.

![spring-mvc](https://indrabasak.files.wordpress.com/2016/04/spring-mvc1.png) 

Once the controller receives the request, it processes the payload (data in the request) or delegates the processing to the other service objects. Once the processing is complete, the controller stores the data model and identify the logical name of the view responsible for rendering the output. The DispatcherServlet relies on view resolver to map the logical view name with the specific view implementation. Finally, the view implementation uses the model data to render the output that is carried back to the client by the response object. Now you know how Spring MVC framework decouples the view from the controller and the model.

### Spring MVC and REST

*   Spring MVC enhanced it's controller to handle all types of HTTP requests including the four primary REST methods: GET, PUT, DELETE, and POST.
*   Controllers can handle requests for parameterized URL - URLs have variable input as part of their path.
*   Controller can now bypass rendering of any type of view (as discussed earlier) by using the `@ResponseBody` annotation and various converters for marshaling and marshal data.
*   Resources can be represented in a variety of ways - XML, JSON, etc.

### Hello World

Let's start with a simple REST Hello World project to give us a better understanding on how Spring MVC integrates with RESTful web service. You must have heard by now that REST API is all about resources. So, what is a resource? A resource is similar to a Java object instance. It comes with its associated data, relationship with other objects, and with a set of methods to manipulate the data. Unlike a Java object, a resource comes with a limited set of methods - HTTP GET, POST, PUT, DELETE, etc. So a resource is the data (model) backing up a REST web service. Since REST is about transferring the state of resources, we are really transferring the state of data model across the HTTP protocol. In our example, Customer and Address constitutes our data model. They are regular POJOs that come with their own attributes and a corresponding set of getters and setters. The complete source code can be found [here](https://github.com/indrabasak/rest-helloworld). 

{% gist 908034e430ae75186d69e3161019d060 %} 

{% gist f3b5aedf0436ed1219ad72ac71dddf88 %} 

However we cannot transfer `Customer` or `Address` objects over the wire without marshalling (serializing) them first. This is where the representational aspect of REST comes into play. A REST resource can be represented by any form, i.e., the marshalled object can be of any form, including XML, JavaScript Object Notation (JSON), etc. In our example, we will consider both XML and JSON representations while marshaling our data objects. Since JAXB has problem marshaling Java collection classes(list in our case), we will have a wrapper class to return a list of customers. 

{% gist 585cad72b6a1852b1bafb3e2673f0d0a %}

#### JAXB Annotations

We will be using Java Architecture for XML Binding (JAXB) framework for marshalling and unmarshalling Java objects into XML. In order for our classes to be ready for XML conversion, we annotate the classes with `javax.xml.bind.annotation` notations. You can find more information about JAXB [here](http://docs.oracle.com/javase/tutorial/jaxb/intro/). Only a few JAXB annotations are used in our example classes.

* `@XmlRootElement` defines the root element of XML. It is declared at the top of our class declaration.
* `@XmlAccessorType` controls whether fields of our Java classes are serialized by default. By declaring `XmlAccessType` as `NONE`, none of the properties in our classes is bound to XML.
* `@XmlElement` maps a property to a XML element derived from property name. Our classes use the `@XmlElement` before the setters.

### Defining Business Service

Though a service is not a requirement for a Spring REST project, we will define a service to keep a level of abstraction (loose coupling) between our Spring controller and the core business logic. According to the author of 'Spring in Action' - "a well-designed controller performs little or no processing itself and instead delegates responsibility for the business logic to one or more service objects." The `CustomerService` interface defines the CRUD operations that can be performed upon the`Customer` data model. 

{% gist 330734f6611bad295e547263216d0510 %} 

`CustomerServiceImpl` implements the service class. It uses a HashMap as an in-memory data repository to store Customer objects.

#### @Service Annotation

`@Service` annotation, declared before `CustomerServiceImpl`, is used for automatic bean detection using classpath scan in Spring framework. Spring automatically scans and identifies all classes that are annotated with @Service annotation and registers them with ApplicationContext. Though other similar Spring annotations can be used for registering with ApplicationContext, `@Service` annotation is usually used for declaring a bean as a service. 

{% gist c08ebfa7ed07f7f74413c8737de391a5 %}

### Defining a Spring REST Controller

In Spring MVC, controller classes are annotated with @Controller and have methods annotated with `@RequestMapping`. Our example controller class is `CustomerServiceController` which is declared a controller class by using `@Controller` annotation. 

{% gist b44c00b4a7f34eb54d14624311118ed3 %}
 
 The @Resource annotation is also used to declare a reference to a resource named customerService. If you recall from last section, we annotated `CustomerServiceImpl` class with @Service with customerService as its name . The Spring container will inject the resource referred to by `@Resource` annotation, CustomerService, into the component, CustomerServiceController, during runtime. Though CustomerServiceController class doesn't implement the `CustomerService` interface, it exposes all the methods declared by CustomerService. All the methods are mapped to different URLs and HTTP operations. We will discuss a few of the annotations used in our controller in more detail in the following sections.

#### @Controller Annotation

The `@Controller` annotation indicates that an annotated class is a Spring web controller. It is auto-detected by Spring container through classpath scanning.

#### @RequestMapping Annotation

`@RequestMapping` is used to map HTTP requests onto specific handler classes/methods which will handle the request. Various elements within the `@RequestMapping` annotation are used to customize the behavior of the handler.

*   Use value element to specify the URI pattern for which handler method will be used. For example,` @RequestMapping(value = "/customers")`.
*   Use method element to narrow down the HTTP methods (GET, POST, PUT, DELETE, etc.) for which this method will be invoked. For example, `@RequestMapping(value = "/{id}" ), method = RequestMethod.GET)`.
*   Use produce element to indicate the response mime type (representation) the method is capable of producing.For example, `@RequestMapping(value = "/{id}"), method = RequestMethod.GET, produces = {MediaType.APPLICATION_XML_VALUE, MediaType.APPLICATION_JSON_VALUE})`. The method is capable of producing both XML and JSON response content type. The Accept request-header field can be used to specify certain media types which are acceptable for the response, e.g,. `Accept: application/json`.
*   Similarly use consume element to indicate the content type accepted by the method.  For example, `@RequestMapping(value = "/{id}"), method = RequestMethod.GET, consumes = {MediaType.APPLICATION_XML_VALUE, MediaType.APPLICATION_JSON_VALUE})`. The Content-Type entity-header field indicates the media type of the entity-body sent to the recipient, e.g., `Content-Type: application/xml.`

#### @ResponseBody and @RequestBody Annotations

The `@ResposeBody` and `@RequestBody` annotations are used in Spring framework to implement object serialization and deserialization respectively. If a method is annotated with @ResponseBody, Spring serializes the return value to HTTP response into the format specified in the Accept request-header field  in the HTTP request. Similarly Spring deserializes the HTTP request body to a method parameter if the parameter is annotated with the  @RequestBody parameter. The conversion type is specified in the Content-Type entity-header field of the HTTP request. Spring delegates the responsibility of conversion to a HttpMessageConverter. Spring maintains a list of HttpMessageConverters which are registered via the configuration file (discussed later). Depending on a predefined mime type, a HttpMessageConverter  converts the request body to a specific class and back to the response body again. Whenever Spring encounters a @RequestBody or @ResponseBody annotation while processing a HTTP request, it loops through all the registered HttpMessageConverters and selects the first one that matches the given mime type and class. The selected HttpMessageConverter is used for conversion.

#### @PathVariable Annotation

The @PathVariable annotation allows a controller to map a parameterized URL (variable input as part of the URL path) to a method parameter. For example in the getCustomer method of our example controller, the method parameter id is mapped to the parameter id of the URL path `customers/{id}` .

### Configuring the Spring DispatcherServlet

Spring DispatcherServlet is responsible for routing the HTTP request through all other components. It is registered in the WEB-INF/web.xml file by using a URL mapping. Upon initialization of rest-dispatcher DispatcherServlet, the Spring framework will try to load the application context from a file named `[servlet-name]-servlet.xml` located in the application's WEB-INF directory. In our example, the application context file is named `rest-dispatcher-servlet.xml`. You can customize this file name and location by adding the servlet listener ContextLoaderListener and the context parameter `contextConfigLocation`. The servlet-mapping tag indicates the URLs patterns handled by the `DispatcherServlet`. In our example, all HTTP requests ending will be handled by the rest-dispatcher DispatcherServlet. The following example shows the declaration and mapping for rest-dispatcher DispatcherServlet: 

{% gist 41610a8b38d6dfbabf11d1d67ffb4408 %}
 
 Here is the example required configuration for rest-dispatcher-servlet.xml file located in WEB-INF directory: 
 
 {% gist 8a33527fea683ea48ec72bfd0016b4a2 %} 
 
 Following tags are used in the `rest-dispatcher-servlet.xml` file:

*   `context:annotation-config` tag is used to activate annotations in beans already registered in the application context (no matter if they were defined with XML or by package scanning).
*   `context:component-scan` tag is used to activate Spring MVC annotation scanning capability which allows to make use of annotations like @Controller, @Service, and @RequestMapping etc. It can do what context:annotation-config does but also scans packages to find and register beans within the application context.
*   `mvc:default-servlet-handler` tag tallows for mapping the DispatcherServlet to "/" (thus overriding the mapping of the container's default Servlet), while still allowing static resource requests to be handled by the container's default Servlet. This is to pickup the welcome file from web.xml. Though it is not required by Tomcat, WebSphere needs it.
*   `mvc:annotation-driven` tag gives you greater control over the inner workings of Spring Controller, e.g., to register HttpMessageConverters and message validators.
*   `mvc:message-converters` tag used for registering HttpMessageConverters . In our example, Jackson and JAXB converters are registered for converting to JSON and XML types respectively.

### Building Maven Project

To build our Maven project, open a console and change directory to the project root. Once you are in the project root, execute the following command:

```
mvn clean install
```

If the project builds successfully, it should create a `rest-helloworld.war` file in the target directory.

### Deploying in Tomcat

Here we will only talk about deploying the WAR file directly to a web server (instead of deploying it form Eclipse):

*   Make sure you have started Tomcat by executing startup.sh script in the bin folder under Tomcat installed directory.
*   Tomcat should start at port 8080.
*   Copy the `rest-helloworld.war` to the `webapps` folder under Tomcat installed directory.
*   To make sure our example application is running, open a browser and type the following URL, `http://localhost:8080/rest-helloworld/`
*   This should bring up the following welcome page.

### Testing

*   RESTClient from WizTools is a good tool for testing tool for testing REST API. You can download it from [here](https://github.com/wiztools/rest-client). Example README explains how to test the example application.
*   If you are using Chrome browser, [Postman](https://chrome.google.com/webstore/detail/postman/fhbjgbiflinjbdggehcddcbncdddomop?hl=en) extension is a good utility for testing REST API.