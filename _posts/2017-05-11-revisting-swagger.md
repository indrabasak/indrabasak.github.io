---
layout: post
title: Revisting Swagger
published: false
comments: true
tags:
  - REST
  - Spring
  - Swagger
image: /images/entry/swagger.png
---

Lately, I am getting a few `how to do` inquiries on my last Swagger posting. Most of them involve either renaming or sorting REST controllers. Also, ran into a few interesting Swagger challenges in the last couple of months. Now that it has been over a year since my lasting posting on Swagger, it is a good time to revisit the subject.

To explore different Swagger features, I created an example github project titled [swagger-deepdive](https://indrabasak.github.io/swagger-deepdive/). The project consist of multiple REST controllers involving various animals and birds which are part of a menagerie. A menagerie is a collection of exotic animals and birds that are kept captive for the viewing pleasure for a certain segment of society.

The followings controllers are part of the `menagerie` project: `ElephantController`, `LionController`, `ParrotController`, `TigerController`, and `ToucanController`. The backend services are supported by HSQLDB, a in-memory database, and JPA. It is based on the latest version of Sprigfox - `Springfox 2.6.1`. 

The customization of Springfox and Swagger can be broadly classified into two different categories:

* Changes which directly affect Swagger UI. Renaming and sorting controllers; customizing Swagger UI falls under this category.

* Springfox extensions affecting the Swagger model and in some cases UI. Sprigfox provides hooks, i.e., `plugins`, to extend Swagger functionality. Writing a extension consists of writing a Java class either extending an existing class or implement an interface. In the menagerie project, I covered only a few of the Swagger plugins. 

I have created a [wiki](https://github.com/indrabasak/swagger-deepdive/wiki) for the `menagerie` project where I discuss each of the Swagger customization in detail. 






