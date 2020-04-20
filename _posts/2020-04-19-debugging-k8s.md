---
layout: post
title: Debugging Kubernetes
published: false
comments: true
tags: [Kubernetes, Docker, TCP]

image: /images/entry/debug-k8s.svg
---

I keep on running into interesting problems while migrating applications into our Kubernetes(k8s) environment. 
Recently, a Spring Boot based application started returning invalid characters once it was ported to k8s. Instead of 
returning a `ό`, it returned with a set of garbage characters. 