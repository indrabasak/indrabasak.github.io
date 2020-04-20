---
layout: post
title: Docker and Build Failures
published: false
comments: true
tags: [Docker, Maven, Spring Boot, Jetty, Cassandra]

image: /images/entry/docker-mvn-build.svg
---

I keep on running into interesting problems while migrating applications into our Kubernetes(k8s) environment. 
Recently, a Spring Boot based application started returning invalid characters once it was ported to k8s. Instead of 
returning a `ό`, it returned with a set of garbage characters. 

```yaml
spring:
  data:
    cassandra:
      keyspace-name: mykeyspace
      contact-points: localhost
      port: 9242
      ssl: false
      records: 300000
      read-timeout: 200000
```