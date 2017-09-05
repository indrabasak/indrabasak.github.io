---
layout: post
title: Anatomy of a Bug - Part I
published: true
comments: true
tags:
  - Zuul
  - Log4J
  - Bug
image: /images/entry/bug-anatomy2.png
---

Recently, I came across a production issue where a [_Zuul_](https://github.com/Netflix/zuul/wiki) (Spring Cloud Brixton.SR3)
edge service became unresponsive to HTTP requests. Even the health REST endpoint, which provides basic health
 information, of the affected service failed to respond. The [_Eureka_](https://github.com/Netflix/eureka/wiki/Eureka-at-a-glance) 
 registry service also advertised the unresponsive service as up. It was a _Spring Boot_ (1.3.4.RELEASE) 
 application with an embedded _Jetty_ (9.3.0.v20150612 ) web container running on 
 _Red Hat Linux VM_ with _Oracle JVM_ (1.8.0_31).

### Investigation

The affected service showed up as running while checking the status of the application using the following command:

`service zuul status`

Also, no error message was found in any of the application log files. However, [VisualVM](https://visualvm.github.io/) was 
able to connect with the affected JVM. VisualVM is a tool for monitoring real time 
JVM statistics including CPU, memory, and thread usage. 

The _heap dump_, which was collected with VisualVM, didn't show anything out of the ordinary. The _CPU_ and 
_memory usage_ were normal and on the lower side. A separate heap dump was also collected using the _jmap_ tool
by exeuting the following command:

`sudo jmap -F -dump:format=b,file=/tmp/zuul_heapdump <pid>`

It was a different story when the _thread usage_ was investigated. There were 285 live and 68 
daemon threads and most of the Jetty QTP threads were in _parked_ state.
Upon close inspection of the thread dumps, it was observed that 198 of the Jetty threads were in waiting state. 
All were waiting for the same thread id _455344ba_.  The following command was used to count the number of threads:

`cat threaddump_1_pre-restart.log | grep '<455344ba>' | wc -l`. 

Yet, no information on the thread with id _455344ba_ was found in the thread dumps.
Note, the thread dumps were captured using VisualVM and _jstack_ tool. Here is an example of a
jstack command for obtaining a thread dump:

`sudo jstack -l -F <pid> > ~/2017_08_30.tdump`
 
The thread ids in the thread dump collected with _jstack_ were mangled. 
Fortunately, the VisualVM thread dump had all the ids present. 
Here is a partial stack trace from the thread dump collected with VisualVM:

```sh
"qtp84113073-285" - Thread t@285
   java.lang.Thread.State: WAITING
	at sun.misc.Unsafe.park(Native Method)
	- parking to wait for <455344ba> (a java.util.concurrent.locks.AbstractQueuedSynchronizer$ConditionObject)
	at java.util.concurrent.locks.LockSupport.park(LockSupport.java:175)
	at java.util.concurrent.locks.AbstractQueuedSynchronizer$ConditionObject.await(AbstractQueuedSynchronizer.java:2039)
	at java.util.concurrent.ArrayBlockingQueue.put(ArrayBlockingQueue.java:353)
	at org.apache.logging.log4j.core.appender.AsyncAppender.append(AsyncAppender.java:156)
	at org.apache.logging.log4j.core.config.AppenderControl.tryCallAppender(AppenderControl.java:152)
	at org.apache.logging.log4j.core.config.AppenderControl.callAppender0(AppenderControl.java:125)
	at org.apache.logging.log4j.core.config.AppenderControl.callAppenderPreventRecursion(AppenderControl.java:116)
	at org.apache.logging.log4j.core.config.AppenderControl.callAppender(AppenderControl.java:84)
	at org.apache.logging.log4j.core.config.LoggerConfig.callAppenders(LoggerConfig.java:390)
	at org.apache.logging.log4j.core.config.LoggerConfig.processLogEvent(LoggerConfig.java:378)
	at org.apache.logging.log4j.core.config.LoggerConfig.log(LoggerConfig.java:362)
	at org.apache.logging.log4j.core.config.LoggerConfig.log(LoggerConfig.java:352)
	at org.apache.logging.log4j.core.config.AwaitCompletionReliabilityStrategy.log(AwaitCompletionReliabilityStrategy.java:63)
	at org.apache.logging.log4j.core.Logger.logMessage(Logger.java:143)
	at org.apache.logging.log4j.spi.AbstractLogger.logMessage(AbstractLogger.java:1016)
	at org.apache.logging.log4j.spi.AbstractLogger.logIfEnabled(AbstractLogger.java:964)
	at org.apache.logging.slf4j.Log4jLogger.info(Log4jLogger.java:178)
	at com.abc.cloud.zuul.service.RequestLogger.logRequest(RequestLogger.java:79)
	at com.abc.cloud.zuul.filter.post.RequestLoggingFilter.run(RequestLoggingFilter.java:52)
	at com.netflix.zuul.ZuulFilter.runFilter(ZuulFilter.java:112)
```

While comparing the thread usage of the uresponsive service with an unaffected Zuul service, it was noticed that 
 the live thread usage of the latter was substantially lower. The unaffected service had 88 live and 63 daemon threads
 compared to 285 live and 68 daemon threads for the unresponsive one.
 
### Analysis

The offending line (line 16 in the code sample below) in the Java code was easily identified by looking at the 
stack trace in the thread dump. The affected piece of code writes HTTP response to a log file. 
One of the custom Zuul post filters writes every HTTP request and response to their 
respective logs. The post filter is executed once the Zuul service receives a response back from an 
internal service. A Zuul service is responsible for routing HTTP requests to one of the internal REST services. A Jetty 
thread used for processing a request and response is also responsible for writing the logs. This thread was 
blocked while trying to log a response.

{% gist 909e85ce95c5bc3481aeb2134675f8b8 %}

When a thread tries to write to an asynchronous Log4J logger, the log message is serialized and inserted into a `BlockingQueue`. 
An blocking queue is a bounded (fixed size) queue where a new message is inserted at the tail. Any attempt to insert a message in a 
queue, when it is full, will result in a thread being blocked until there is adequate space available in the queue. 
In the case of a Zuul service, one of the Jetty threads is responsible for inserting a message in the blocking queue. 
A second Log4J logger thread `AsyncThread` is responsible for dequeuing the message and writing it to a log file. There is 
one thread for each asynchronous Log4J appender. The version of Log4J library used in the Zuul application was _2.4.1_.

It was suspected that the Jetty threads were in _waiting_ state due to the Log4J response queue being full.
To prove the initial assumption, the request log appender MBean (e.g., _org.apache.logging.log4j2:type=4144933788,component=AsyncAppenders,name=asyncResponseLog_) was inspected in the VisualVM. The queue capacity attribute 
_QueueCapacity_ was found to be 128 while the remaining 
capacity attribute _QueueRemaingCapacity_  was 0. The suspicion that the queue was full turned out to be true. 
Note, the name of the _asyncResponseLog_ MBean comes from the response appender name declared in the Log4J 
configuration file shown below.

{% gist eaafb0eb305072a5bab7d40493655961 %}

However, the remaining queue capacity of the request log appender MBean was 128. 
In other words, the request queue was empty. The last response log entry was 
_2017-08-30 09:25:30_ which was slightly older than the request log entry _2017-08-30 09:27:21_. 

According to [Log4j documentation](https://logging.apache.org/log4j/2.0/manual/appenders.html#BlockingQueueFactory) on _AsyncAppender_, 
the default size of the blocking queue is 128 which matched the size in the MBean.

This led to a couple of intial hypothesis as to why the offending thread with id _455344ba_ was not returning:

#### 1. Waiting for a Lock
**The offending thread was waiting to acquire a write lock to the response log file.**
To confirm that the response log file descriptor (handle) was still open, _lsof_ tool was used
to obtain a of open files in the unresponsive Zuul server. Here is an usage of _lsof_ command: 

`sudo lsof -i | grep java | grep -v TCP`. 

Since application name was known, the following command was executed to narrow down the list of
open files. The output was piped to a file for further evaluation.

`pgrep -f 'java.*zuul' | xargs -i sudo lsof -p {} > /tmp/zuul.lsof.$( date +%Y%m%d_%H%M%S ).out`

Once the output file was created, it was grepped to find out the status of response log file using the
command shown below:

`cat /tmp/zuul.lsof.20170830_*.out | grep 'response.log'`

The output shown below confirmed that the response log file was open and a Java process 
with PID _30667_ owned the write lock. 

```bash
COMMAND   PID    USER    FD      TYPE             DEVICE   SIZE/OFF       NODE NAME
java    30667    zuul   18w      REG               253,2     4935360    34894563 /var/log/abc/zuul/response.log
```

The thread dumps were inspected again to confirm there were no deadlocks. Luckily,
the _jstack_ thread dump, shown below, stated no deadlocks were detected. However, no such information 
was available in the VisualVM thread dump. **This ruled out the 
wait for a lock hypothesis**.

```bash
Attaching to process ID 30667, please wait...
Debugger attached successfully.
Server compiler detected.
JVM version is 25.131-b11
Deadlock Detection:

No deadlocks found.
``` 

#### 2. Death of a Thread

**The offending thread died upon encountering an exception.** First, the threads of both responsive and 
unresponsive Zuul services were compared in the VisualVM. Other than the obvious difference in the thread count, 
a thread named _AsyncAppender-asyncResponseLog_ was found missing in the unresponsive Zuul JVM.
The thread suffix (_asyncResponseLog_) matched the asynchronous name of log appender in the Log4J configuration file.
It led to the conclusion that **the response log blocking queue was filled due to the death of
 _AsyncAppender-asyncResponseLog_** thread. **It also confirmed the death thread hypothesis**. 

Now that one of the initial hypothesis was confirmed, the system logs were investigated for error messages. 
Remember, no error messages were found earlier in the application logs. Lo and behold, something interesting turned up
in the system logs. The _AsyncAppender-asyncResponseLog_ thread encountered a _java.lang.OutOfMemoryError_ at _Aug 30 09:25:33_. 
It approximately matched the last entry in the response log at _2017-08-30 09:25:30_. 
This confirmed that the **Log4J _AsyncAppender-asyncResponseLog_ thread died at 
_Aug 30 09:25:33_ due to memory starvation**.

Here is the exception entry in the system log:

```bash
Aug 30 09:25:33 pdxzuul02 java[30667]: Exception in thread "AsyncAppender-asyncResponseLog" java.lang.OutOfMemoryError: Java heap space
Aug 30 09:25:33 pdxzuul02 java[30667]: at java.util.Arrays.copyOf(Arrays.java:3332)
Aug 30 09:25:33 pdxzuul02 java[30667]: at java.lang.AbstractStringBuilder.ensureCapacityInternal(AbstractStringBuilder.java:124)
Aug 30 09:25:33 pdxzuul02 java[30667]: at java.lang.AbstractStringBuilder.append(AbstractStringBuilder.java:448)
Aug 30 09:25:33 pdxzuul02 java[30667]: at java.lang.StringBuilder.append(StringBuilder.java:136)
```

The system log entry was detected using the _journalctl_ utility:

`sudo journalctl -u zuul -n1000 | grep -A30 'java.lang.OutOfMemoryError'`

Note _-A30_ prints 30 lines of trailing context after the matching line.

### Summary

The Log4J _AsyncAppender-asyncResponseLog_ thread died approximately at _Aug 30 09:25:33_ due to memory starvation. 
As the dead thread was responsible for dequeing, it resulted in the response blocking queue to fill up.
Once the response blocking queue was full, all subsequent Jetty HTTP request threads were blocked and were put in waiting state. 
It resulted in the Zuul service becoming unresponsive. The version of Log4J library having the issue was _2.4.1_.
Overall, **the Zuul service failed to respond to 198 client requests**.

In most cases, a _java.lang.OutOfMemoryError_ will not kill a JVM. It usually occurs when a JVM fails to allocate memory blocks 
with the available heap resource. A JVM may recover from an out of memory exception if enough memory space is available after the next
garbage collection. However, there is no guarantee that a JVM will recover after an out of memory exception. 
In the case of unresponsive Zuul service, it recovered from the memory exception which killed the 
Log4J asynchronous log appender thread.
 
Even after the Zuul service became unresponsive, it was still able to accept incoming HTTP requests and route them to internal 
services. It was still able to comunicate with the Eureka server. It broadcasted the _UP_ status without being aware of 
the response logging thread's demise. 

To be continued...



