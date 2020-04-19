---
layout: post
title: Docker and Invalid Characters
published: true
comments: true
tags: [Docker, Kubernetes, REST, Spring Boot]

image: /images/entry/docker-invalid.svg
---

I keep on running into interesting problems while migrating applications into our kubernetes environment. 
Recently, a Spring Boot based application started returning invalid characters once it was ported to Kubernetes. Instead of 
returning a `ό`, it returned with a set of garbage characters. In my first attempt to debug the issue, I started the 
application in an IntelliJ IDE, and it returned with a correct response. It was obvious the invalid character problem was 
related to encoding issue; I wasn't sure about the layer which was causing it. I have encountered similar issues 
related to URL encoding but never in a HTTP response body.

Now, if you think a little more closely about this application's new environment; the only variables were the
Kubernetes networking layer and the operating system due to dockerization. Although a kubernetes networking is
a different beast compared to my application's old networking tier, it's normally not a factor that affects encoding. 
While an application's OS is a different story.

A program locale plays a significant role in defining an application's code sets, date and time formatting, monetary 
conventions, and decimal formatting. In a Unix based system such as Linux, the default locale codeset is usually 
set to `UTF-8`, an ASCII compatible 8-bit encoding form of Unicode. This made me realize that the next step in my
investigation should involve comparing the OS locale of the application's old and new environments. I checked the 
locale of each environment by executing the `locale` command from the command line. 

Here's the locale output of my old CentOS KVM environment,

```bash
LANG=en_US.UTF-8
LC_CTYPE="en_US.UTF-8"
LC_NUMERIC="en_US.UTF-8"
LC_TIME="en_US.UTF-8"
LC_COLLATE="en_US.UTF-8"
LC_MONETARY="en_US.UTF-8"
LC_MESSAGES="en_US.UTF-8"
LC_PAPER="en_US.UTF-8"
LC_NAME="en_US.UTF-8"
LC_ADDRESS="en_US.UTF-8"
LC_TELEPHONE="en_US.UTF-8"
LC_MEASUREMENT="en_US.UTF-8"
LC_IDENTIFICATION="en_US.UTF-8"
LC_ALL=
```

To check the docker container locale, I got a shell to a running container of my application by executing the 
`kubectl exec` command (`"kubectl exec -ti myservice-9c8b5ff5f-56gw6 -c myservice-app -n mynamespace sh"`). Here's the
locale output of my application's kubernetes container,

```bash
sh-4.2# locale
LANG=
LC_CTYPE="POSIX"
LC_NUMERIC="POSIX"
LC_TIME="POSIX"
LC_COLLATE="POSIX"
LC_MONETARY="POSIX"
LC_MESSAGES="POSIX"
LC_PAPER="POSIX"
LC_NAME="POSIX"
LC_ADDRESS="POSIX"
LC_TELEPHONE="POSIX"
LC_MEASUREMENT="POSIX"
LC_IDENTIFICATION="POSIX"
LC_ALL=
sh-4.2# 
```

If you compare the two locale outputs, you will notice that the variables in my old KVM are set to `en_US.UTF-8` while
the same variables in the kubernetes container are set to `POSIX` locale, also known as C locale. To match the locale of
the kubernetes with the KVM, I had to set the locale environment variables in my application's `Dockerfile`. Here are 
the changes I made to my application's Dockerfile to set the locale environment.

```dockerfile
FROM docker-registry.iovationnp.com/iovation/java:11

# Set the locale
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
...
``` 

After my changes to the Dockerfile, I rebuilt the docker image and redeployed in the kubernetes environment. Guess what, 
the application response was back to normal.
