---
layout: post
title: Anatomy of a Bug - Part II
published: true
comments: true
tags:
  - Zuul
  - Log4J
  - Bug
image: /images/entry/bug-anatomy.png
---

In my last [posting]({{ site.baseurl }}/anatomy-of-a-bug/), I wrote about a
[_Zuul_](https://github.com/Netflix/zuul/wiki) service becoming unresponsive 
due to the death of a Log4J thread.
Here, I will continue our discussion and try to arrive at a resolution to prevent the reoccurence
of the bug in the future.

### Bug Reproduction

Fixing a bug starts with reproducing it. If a bug cannot be reproduced, then it can't be fixed.
A bug reproduction starts with repeating the steps which led to the problem in the first place.

The process started with checking the source code out, matching the version in production, 
from the code repository. 
To reproduce the bug faster, _log4j2.xml_ file was modified to reduce the size of response appender
 blocking queue from 128 to 5. The changes to the _log4j2.xml_ file is shown below:

{% gist 8694890e9d01a81ce945acc51669350b %}

For debugging the application, the IDE of choice was [IntelliJ](https://www.jetbrains.com/idea/). 
Once the Zuul application started in debug mode, the response queue capacities were monitored
 using VisualVM. As expected, the queue's total and remaining capacities were 5 and 5 respectively.
If you recall from the previous post, the name of the log appender MBean was _asyncResponseLog_ and
the corresponding attributes were _QueueCapacity_ and _QueueRemaingCapacity_.

![mbean browser](/images/buganatomy/mbean-browser.png)

To ensure the application was working properly, a Zuul endpoint was invoked several times 
from [Postman](https://www.getpostman.com/). Postman is a GUI tool for testing REST endpoints.
While the endpoint was exercised , a close eye was kept on the response logger MBean. As expected, 
the response queue wasn't backing up.

To recreate the unresponsive Zuul scenario, the _AsyncAppender-asyncResponseLog_ thread
was suspended from IntelliJ. This thread is responsible for dequeing the response log
message queue and writing it to a file. From the application perspective, the suspended thread
might as well be dead.

![suspended thread](/images/buganatomy/suspended-thread.png) 

The same Zuul endpoint was exercised once more. 
After each invocation, the response logger queue's remaining capacity decremented by one until
it was completely full. Remember, the queue size was set to 5. 
Once the queue was full, the Zuul service stopped responding to any further requests. 
This helped us to successfully reproduce the bug in the dev environment.

### Search for a Resolution

#### Log4J Upgrade

The next step was to find a resolution for the bug. A quick search on Google, 
led us to a [LOG4J2-1324 issue](https://issues.apache.org/jira/browse/LOG4J2-1324) which seemed similar
to the problem in hand. It mentioned a asynchronous Log4J thread dying 
after encountering an exception. The issue was encountered in Log4J _2.2.0_ version and 
resolved in version _2.6.0_.

After the upgrade of Log4J version to _2.6.2_, there was no change in the behavior of the Zuul service.
As the simulation of _java.lang.OutOfMemoryError_ wasn't feasible, the exeption behavior was mimicked in 
the IntelliJ debug mode by throwing a _java.lang.NullPointerException_. The
null pointer exception didn't have any implications on both versions of Log4J. Any further consideration of 
**upgrading the Log4J library was dropped.**

#### Log4J Appender Changes
 
As shown below, Log4J allows for an asynchronous appender to be non-blocking by changing its 
[_blocking_](https://logging.apache.org/log4j/2.0/manual/appenders.html#BlockingQueueFactory) property. 
If the blocking property is set to false, the messages will be written to an error appender if present.

{% gist 8a936bb15e920572060c0e21647b91ef %}
 
Following the same testing steps as discussed earlier, the _AsyncAppender-asyncResponseLog_ thread
was suspended once the Zuul application was started in debug mode. 
Invoking the Zuul endpoint multiple times didn't have any adverse effect even after the 
response logger queue was full. As expected, entries were missing in the response log file.
 
If one wishes to avoid missing any log entries when the response appender queue is full, one can add an error appender. 
The response entries will be logged in the error log once the response log appender queue fills up.
An example of a Log4J configuration with an error appender is shown below:
 
 {% gist a785a74ceb5692236603ff64019a2454 %}
 
### Validation

Once it was proved that a non-blocking Log4J asynchronous appender will resolve the 
unresponsive Zuul issue, we went forward with validating the changes in a non-production environment. 
The Zuul service was restarted after making changes to _log4j2.xml_.
As shown below, JVM flags were also changed to attach a remote debugger 
from IntelliJ:

`-Xdebug -Xrunjdwp:transport=dt_socket,server=y,suspend=n,address=5005`

From IntelliJ, a remote debugger was started to connect with the remote JVM. Once the debugger
was attached, the _AsyncAppender-asyncResponseLog_ thread was suspended. Same tests were repeated 
as earlier while monitoring the _asyncResponseLog_ MBean from the VisualVM. The validation was successful in the 
non-prod environment. Here is an example of IntelliJ remote debug configuration: 

![remote config](/images/buganatomy/intellij-remote-debug.png) 

### Resolution

#### Heap Size Increase

Since the initial cause of Zuul service failure was memory starvation, increasing the 
heap size was an obvious choice. The following changes were made to the heap
sizes:

| Heap  Size         | JVM Flag       | New Value     | Old Value  |
| ------------------ | :-------------:| -------------:| ----------:|
| Initial            | -Xms           | 2 GB          | 256 MB     |
| Maximun            | -Xmx           | 2 GB          | 512 MB     |
| Young Generation   | -Xmn           | 512 MB        | 200 MB     |

#### Non-Blocking Log4J Appender

Increasing the heap size is not a guarantee that the asynchronous Log4J appender will not encounter an out of memory
exception in the future. To mitigate this scenario, it is prudent to make the 
**asynchronous Log4J appender non-blocking** for both request and response. 

If the queue is full, the Jetty thread will return immediately without writing any message to the queue. 
This would help the Zuul service to respond even if any of the aynchronous logger threads dies.

{% gist 5f2233827e66228caecbb58b182b82a4 %}
