---
layout: post
title: REST API and Error Handling
published: true
comments: true
tags: [REST, Spring]
image: /images/entry/spring.png

---

Most developers don't think of errors and exception handling while designing a REST API. However it is very critical from your API user perspective as the whole logic inside your API code is black boxed from them. If your API returns an error, the API user should be able to make sense of it so as to take any corrective action. If you want your API to be intuitive and useful, you should adhere to following rules:

1.  **Return relevant HTTP status codes**. There are more than [60 status code](http://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml), but lot of them are either confusing or not common. Use a small subset of status codes which are well known. For example, Google GData API uses 10 status codes, Netflix uses 9, and Digg uses 8\. You can find more [here](http://apigee.com/about/blog/technology/restful-api-design-what-about-errors).
2.  **Make you error response as human readable as possible**. The user of your API doesn't want to know about your internal errors. They don't want to see any exception stack or any other gobbledygook.

Here I will explore the second good practice where error responses are human readable. Spring provides a few different ways to handle exceptions but I will restrict my discussion to `@ExceptionHandler` and `@ControllerAdvice`.  It is the continuation of REST with Spring  example. The source code can be found [here](https://github.com/indrabasak/rest-err-helloworld).

### Controller Specific Exception Handling

Any method declared with `@ExceptionHandler` annotation allows one to handle exception at the controller level. It handles any exception thrown by a request handling method, i.e., any method declared with `@RequestMapping` annotation. For example, `handleTypeMismatchException` method in `CustomerServiceController` handles `TypeMismatchException` exception. This method is **not used for handling exceptions at the application level**. Here are the requirements for controller specific exception handling method:

*   Declare the method with `@ExceptionHandler` annotation.

*   `@ResponseStatus` annotation is optional and is usually used for user defined exception.

*   Method signature is flexible. It can take zero parameters or take any servlet related objects as parameters. In this example, the `handleTypeMismatchException` method takes `HttpServletRequest` and `TypeMismatchException` as parameters.

*   The method doesn't have to return a value. If the error message needs to be customized to make it more human readable, the method should return a value. <span style="color:#008000;">@ResponseBody</span> is needed if the method returns a value. Since the return value of the method is serialized and used as a part of the response body, make sure that the returned object class is serializable by using JAXB annotations.

{% gist e117bc119f41aabd037f9fcf4ff19970 %} 

In this example, the error message is localized by using `MessageSource`. The error messages are stored in the properties file based on locale. A single properties file names messages_en_US.properties is stored in locale folder under `resources`.

```
error.customer.id=Customer cannot have id: {0}
error.customer.not.found=Customer not found - {0}
```

`ResourceBundleMessageSource` bean needs to be configured in the `rest-dispatcher-servlet.xml` file to pickup the properties file. 

{% gist a70faf20e076cfae4f77a87cb0ffe97f %}

In the example, the returned object class `ErrorInfo` takes the request URL, response code, error type, and error message as parameters. 

{% gist 8a90b39b8eb89674213196904e26d36b %} 

Now if a wrong format customer id is used while retrieving a customer, e.g. 'abc' instead of a numeric value, the following error message will be displayed in the browser. ![rest-type-error-handling](https://indrabasak.files.wordpress.com/2016/04/rest-type-error-handling.png)

### Application Specific Exception Handling

Any POJO class declared with annotation `@ControllerAdvice` allows one to handle exceptions at the whole application level and is not restricted to any specific controller. In this example, the class <span style="color:#008000;">ExceptionProcessor </span>handles the exceptions at the application level. 

{% gist 12151fedc0e4c266ca23721fac763689 %}

#### Exception Handing Method

The method `handleCustomerNotFoundException` is used to handle `CustomerNotFoundException` exception. This method is **not required to return any value or take any parameters**. However it can return a value and can take parameters if it's needed. Here is a list of requirements for an exception handling method:

*   A method should be annotated with `@ExceptionHandler`. It takes the exception class as a parameter that is to handled by the method. It maps a specific exception to an appropriate exception handling method.

*   `@ResponseStatus` annotation (which supports all the HTTP status codes defined by the HTTP specification) is used if it's not already defined in the exception class. It takes response value and reason as parameters. The reason parameter is optional. It allows one to customize the response code based on the requirements.

*   Method signature is flexible as earlier. It can take zero parameters or take any servlet related objects as parameters. In this example, the `handleCustomerNotFoundException` method takes `HttpServletRequest` and CustomerNotFoundException as parameters.

*   Return value is optional as earlier but having a a return value makes the error response more human readable. 
`@ResponseBody` is needed if the method returns a value.

{% gist 8ca24480cd0fe191995f67c321e592b6 %}

Now if you try to look up a customer which doesn't exist, you will get the error message shown below. 

![rest-customer-not-found-error-handling](https://indrabasak.files.wordpress.com/2016/04/rest-customer-not-found-error-handling.png)