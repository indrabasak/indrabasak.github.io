---
layout: post
title: Docker and Build Failures
published: true
comments: true
tags: [Docker, Maven, Spring Boot, Jetty, Cassandra]

image: /images/entry/docker-invalid.svg
---

I keep on running into interesting problems while migrating applications into our Kubernetes(k8s) environment. 
Recently, a Spring Boot based application started returning invalid characters once it was ported to k8s. Instead of 
returning a `ό`, it returned with a set of garbage characters. 