---
layout: post
title: Togglz Integration with REST
published: true
comments: true
tags: [Togglz, Spring, REST]
image: /images/entry/toggle.jpg
---

This is the continuation of my previous REST with Spring - Hello World [example]({{ site.baseurl }}/rest-with-spring/). This example integrates Togglz with the REST example. Togglz proxy factory bean pattern is used in this example. Source code for this example can be found [here](https://github.com/indrabasak/togglz-rest-helloworld).

### Changes to Maven Dependencies

Add the Togglz dependencies to the existing pom.xml. 

 {% gist ed0be93b920af758a096a175138f0ccd %}

### Feature Dependencies

VersionFeatures defines the Togglz feature for Hello World REST example. `REST_VERSION_FEATURE`feature switches the REST controller based on the state of the toggle. `@Label` annotation specifies the human readable label used in the Togglz Admin Console. `@EnabledByDefault` annotation makes the `REST_VERSION_FEATURE` enabled by default if no previous state of this flag persisted in the state repository. 

 {% gist 6664b3c60c2918aba2b6beca6086cab7 %}

### Togglz Configuration

`VersionTogglzConfiguration` specifies the Togglz configuration for the example It implements the `TogglzConfig` interface. The methods, declared in `VersionTogglzConfiguration`, serve the following functions:

*   `getFeatureClass` returns the Java enum used in the example application, `CustomerFeatures`.
*   `getStateRepository` returns the type of repository where the state of our toggle will be persisted. In this example, the state is persisted in a file named rest_features.properties located in the temporary directory.
*   `getUserProvider` returns the user who can access Togglz Admin Console to modify the state of the toggle (enabled or disabled). In the example, no security is enabled and anyone can access the admin page.

 {% gist 5042d23816a3aafcad6322eebba9b1b5 %}

### Changes to Business Service Implementation

In the modified REST Hello World example, `CustomerServiceImplv2` is an additional business service implementation. `CustomerServiceImplv2` is similar to the existing class `CustomerServiceImpl` class except the former prepends the number 2 to the customer first name. `@Service` annotation is removed since the automatic bean detection is not required for any of the implementation classes.  {% gist 8ceaf5834ba89a359ad44809afc4594a %}

### A New Business Service Factory

A new service factory class, CustomerServiceFactory, is introduced to abstract the service implementation class from the controller class. CustomerServiceFactory takes advantage of Togglz's `FeatureProxyFactoryBean` to switch the customer service implementing classes. The `FeatureProxyFactoryBean` allows you to create a proxy object, that delegates all calls to one of two beans depending on the state of feature `REST_VERSION_FEATURE`. `FeatureProxyFactoryBean` is marked with the `@Autowired` annotation so that the bean can be dynamically injected into `CustomerServiceFactory` during runtime. `CustomerServiceFactory` is also marked with @Service for automatic bean detection. 

 {% gist 21700f4a15d471473e4c8b11eaf03302 %}

### Changes to Spring REST Controller

Our modified controller now refers to `CustomerServiceFactory` class instead of `CustomerService`. The controller delegates call to the factory instead of the service. 

 {% gist f8a12656a0c8a20f78cbcf9897eecfb2 %}

### Changes to Dispatcher Servlet Configuration

The rest-dispatcher-servlet.xml file is modified to integrate Togglz's FeatureProxyFactoryBean with our REST example. The factory requires two properties active and inactive. They must refer to two alternative implementations of same business interface, which is `CustomerService` in our example. The alternative bean ids are `customerServicev1` and `customerServicev2` where the former is in active state. `rest-dispatcher-servlet.xml`. 

 {% gist 835cb1d6078df0b60a11dc4975895b2b %}

### Demo

*   Once your application is deployed in Tomcat, you can retrieve a list of customers by calling the following URL: `http://localhost:8080/togglz-rest-helloworld/customers`
*   Access **Togglz Admin Console** by typing the following URL in a browser: `http://localhost:8080/togglz-rest-helloworld/togglz`.
*   Since the Rest Version Feature toggle is enabled, the Status shows up as Green. Click the Action button to change the state of the Rest Version Feature toggle.
*   Change the state of the Toggle by disabling the Enabled checkbox and clicking Save.
*   Rest Version Feature toggle state now shows up as Red and disabled.
*   Now try to access the example by typing the following URL in a browser: `http://localhost:8080/togglz-rest-helloworld/customers`. You will notice the '2' prepended to customer names.