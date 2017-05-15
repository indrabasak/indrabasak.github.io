---
layout: post
title: Revisting Swagger
published: true
comments: true
tags:
  - REST
  - Spring
  - Swagger
image: /images/entry/menagerie.jpg
---

Lately, I am getting a few `'how to do'` inquiries on my last Swagger posting. Most questions involve either renaming or sorting REST controllers. I also ran into a few interesting Swagger challenges in the last couple of months. Now that it has been over a year since my lasting posting on Swagger, it is a good time to revisit the subject.

To explore different Swagger customizations, I created an example Github project titled [swagger-deepdive](https://indrabasak.github.io/swagger-deepdive/). The project consists of multiple REST controllers involving various animals which are part of a `menagerie`. A menagerie is a collection of exotic animals and birds that are kept in captivity for the viewing pleasure of certain segments of society.

The following controllers are part of the `menagerie` project: `ElephantController`, `LionController`, `ParrotController`, `TigerController`, and `ToucanController`. The backend services are supported by HSQLDB, an in-memory database, and JPA. The project is based on `2.6.1` version of Springfox. 

The customization of Springfox and Swagger in the `menagerie` example can be broadly classified into two different categories:

* **Custom Swagger UI:** It consists of changes directly affecting the Swagger UI. It involves manipulation of Swagger annotations or HTML pages. _Renaming_ and _sorting_ controllers, _rearranging_ controllers, _custom images_, and _skinning_ Swagger UI all fall under this category.
 
 <center>
    <img src="https://github.com/indrabasak/swagger-deepdive/wiki/img/skinned-swagger-feeling-blue.png" width="500">
 </center>
  
  {:.image-caption}
  Figure 1. Skinned Swagger UI
  
* **Springfox Extensions:** Springfox provides hooks, i.e., _plugins_, to extend Swagger functionality. Creating a Springfox extension primarily consists of writing a Java class extending a known class or interface. An extension usually affects the Swagger model and in some cases UI as well. In the `menagerie` project, a few of the Swagger plugins are explored. 

```json
tags:[  
   {  
      name:"Classification(phylum=Chordata, 
           genus=Loxodonta,
           species=Loxodonta africana,
           family=Elephantidae, 
           clazz=Mammalia, 
           kingdom=Animalia, 
           order=Proboscidea)",
      description:"Elephant API"
   },
   {  
      name:"A3",
      description:"Elephant API"
   }
]
```

{:.image-caption}
  Figure 2. Changes to Elephant Swagger model from custom API Listing Plugin
  
A [wiki](https://github.com/indrabasak/swagger-deepdive/wiki) exists for the `menagerie` project where I explain each of the Swagger customizations in detail. Incorporating these ideas into your project is a great way to increase the usability of your REST APIs. 






