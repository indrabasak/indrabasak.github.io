---
layout: post
title: Swagger for the REST of Us
published: true
comments: true
tags: [REST, Spring, Swagger]
image: /images/entry/swagger.png
---

In the last few years, RESTful web services have become as ubiquitous as SOAP in the early 2000s. You look anywhere in the tech community, you will notice someone somewhere is either talking or doing something with REST APIs or microservices. In spite of its immense popularity, REST lacks any type of standard other than a few guiding principles. REST doesn’t have anything similar to Web Service Definition Language (WSDL). WSDL is used for describing SOAP operations, messages, and also for generating client code. 

In absence of any standardization, documenting REST API becomes extremely critical. In one of my earlier projects, we tried to resolve this issue by documenting the REST APIs in the Wiki. You probably guessed it by now, the documentation quickly got out of sync with the latest versions of the APIs. By the time the project reached the testing stage, the documentation was completely out of whack. Getting latest information from the development team is not an easy task as the developer who worked on an API has either moved on or it has been a while since he or she has touched that particular piece of code. Even after you are in possession of the latest API information, you still have to get hold of special tool(s) for testing the API. Overall, it wasn’t a pleasant experience. 

This is the part where Swagger comes to the rescue of REST from eternal neglect and anonymity. You might think that I am getting carried away but it’s the whole truth and nothing but the truth. Swagger will certainly help REST APIs to be more discoverable and usable. APIs will become descriptive enough to be easily used by prospective clients. How is one supposed to use a REST service if one is not even aware of its functionalities? 

Enough of evangelization! So, what is Swagger? 

Swagger is an open source, language agnostic specification for describing REST APIs. Swagger generates API documentation in JSON format by scanning source code looking for special annotations. It is is now part of [Open API Initiative (OAI)](http://swagger.io/introducing-the-open-api-initiative/). The goal of OAI is to make REST APIs more discoverable and usable. Swagger provides easy to use interactive APIs. It is descriptive enough to be easily used by prospective clients. 

Now if your REST service is written in Java and Spring, you can use Swagger [SpringFox](http://springfox.github.io/springfox/) library. It doesn’t require you to modify any existing REST API. It scans API information from existing Spring annotations. 

Swagger JSON documentation is consumed by Swagger UI to generate beautiful, easy to use interactive documentation. I will post a working example in my next posting. Swagger is not only useful for end user, it's even useful for the developer who wrote the service.