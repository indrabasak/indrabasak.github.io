---
layout: post
title: Togglz Integration with JSF and Spring
published: true
comments: true
tags: [Togglz]
image: /images/entry/toggle.jpg
---

This example covers Togglz integration which JSF, Primefaces, and Spring. The example web application displays customer information based on the state of the toggle/flag. The customer's address is only displayed if the toggle/flag is enabled. The flag can be enabled and disabled from the Togglz administration console. You can find the source code [here](https://github.com/indrabasak/togglz-jsf-example).

### Maven Togglz Dependencies

Since our example is Maven based, the Togglz dependencies are declared in `pom.xml`. Our application uses Togglz's Spring integration module (and not CDI). 

{% gist 2908b660002841bc5dceeaaa35f48feb %}

### Feature Definition

Our example application's Togglz feature definition is described in a Java enum file named `CustomerFeatures` which implements the `Feature` interface. Our example declares only one feature named `FEATURE_ADDRESS`. The optional `@Label` is used to specify a human readable label for the feature which is used in the Togglz Admin Console. While the `@EnabledByDefault` annotation is used to indicate the feature, `FEATURE_ADDRESS`, is enabled by default if no previous state of the feature toggle is persisted in the state repository. 

{% gist 2f45557e5fb1a807f63955f579e52867 %}

### Togglz Configuration

The example Togglz configuration is specified in a Java class named `ToggleConfiguration`. It implements the `TogglzConfig` interface. This particular class configures the FeatureManager which is the central Togglz component that manages the state of our features. The methods, declared in `ToggleConfiguration`, serve the following functions:

*   `getFeatureClass`: Returns the Java enum used in our example application, `CustomerFeatures`.
*   `getStateRepository`: Returns the type of repository where the state of our toggle will be persisted. In our example, the state is persisted in a file named features.properties located in a temporary directory.
*   `getUserProvider`: Returns the user who can access Togglz Admin Console to modify the state of the toggle (enabled or disabled). In our example, no security is enabled and anyone can access the admin page.

{% gist f5561217ffe3d54f949e8ebd5734dfcd %}

### Data Models

In this example, `Customer` and `Address` constitutes our data model. They are regular POJOs that come with their own attributes and a corresponding set of getters and setters. 

{% gist 62fa67c8909558789969869f4dc45bc2 %}

{% gist 013e2c414c9afe524aeb41f3995ee0f4 %}

### Backing Bean

In our example a Java bean named, `ViewCustomersManagedBean`, is used for storing data. It is accessed by our example JSF page, `index.xtml`, for displaying customer information. Since our example uses Spring for managing Togglz configuration, we use Spring annotations (`@Controller` and `@Scope`) instead of JSF annotations (`@ManagedBean` and `@SessionScoped`). Using `@ManagedBean` annotation with Spring causes problems in certain application containers. 

{% gist 90100161a6642d684b0169c426e9a238 %}

### JSF Page

The example JSF page, `index.xhtml`, displays customer name and address based on the toggle FEATURE_ADDRESS. If the toggle FEATURE_ADDRESS is enabled, customer is address otherwise not. The check for the toggle is performed by the following snippet. 

{% gist 6644f4267f69429ce87523077a97c658 %}

### Configuration

Since we are using Servlet 3.0 (make sure your app/web server supports Servlet 3.0), no Togglz specific configuration changes are need in WEB-INF/web.xml file. The following web.xml contains configuration related to JSF and Spring. [gist]03817e97abe1b38fece32800bc6224d0[/gist] <span style="color: #000080;">Now if you container which doesn't support Servlet 3.0 specification, you have to add the following declaration in your web.xml:` 

{% gist 453e1ad8ccd68eaff76c3d7cff391294 %} 

We specify the Spring configuration in a `applicationContext.xml`, located in `WEB-INF`. The name and the location of the Spring configuration file are specified in a `context-param` tag named `contextConfigLocation`. The `context:annotation-config` tag is used to activate annotations in beans already registered in the application context. While context:component-scan tag is used to activate Spring annotation scanning capability which allows to make use of annotations like `@Controller`, `@Component`, etc. Here is our example `applicationContext.xml`. 

{% gist 5b356b05b7c5eef21b802e98b4d28d56 %} 

Standard `face-config.xml` doesn't contain any information related to Togglz. 

{% gist e7a12bf8b4d118cc616fd47e22de024e %}

### Building Maven Project

To build our Maven project, open a console and change directory to the project root. Once you are in the project root, execute the following command:

```
mvn clean install
```

If the project builds successfully, it should create a `rest-helloworld.war` file in the target directory.

### Deploying in Tomcat

Here we will only talk about deploying the WAR file directly to a web server (instead of deploying it form Eclipse):

*   Make sure you have started Tomcat by executing `startup.bat` script in the bin folder under Tomcat installed directory.
*   Tomcat should start up at port 8080.
*   Copy the `togglz-jsf-example.war` to the `webapps` folder under Tomcat installed directory.

### Demo

*   Access our example from http://localhost:8080/togglz-jsf-example

![togglz-jsf-example-1](https://indrabasak.files.wordpress.com/2016/03/togglz-jsf-example-1.png)

*   Access **Togglz Admin Console** from http://localhost:8080/togglz-jsf-example/togglz

![togglz-jsf-example-2](https://indrabasak.files.wordpress.com/2016/03/togglz-jsf-example-2.png)

*   Since the **Address Feature** toggle is enabled, its status is <span style="color: #008000;">green</span>. Click the action button (gear) to change the state of the **Address Feature** toggle.

*   Change the state by unchecking the **Enabled** checkbox and clicking **Save**.

![togglz-jsf-example-3](https://indrabasak.files.wordpress.com/2016/03/togglz-jsf-example-3.png)

*   The state of the **Address Feature** toggle is <span style="color: #ff0000;">red</span> and disabled. 

![togglz-jsf-example-5](https://indrabasak.files.wordpress.com/2016/03/togglz-jsf-example-5.png)

*   Now access or example again from `http://localhost:8080/togglz-jsf-example/`

*   You will notice the address column is missing.

![togglz-jsf-example-6](https://indrabasak.files.wordpress.com/2016/03/togglz-jsf-example-6.png)