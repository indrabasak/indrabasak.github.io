---
layout: post
title: Toying with Togglz
published: true
comments: true
tags: [Togglz]
image: /images/entry/toggle.jpg
---

Any non-trivial software is composed of many different parts. Some of these parts can be grouped together to form a software feature – a unit of functionality that satisfies a requirements or business needs. 

In today’s agile environment, a release cycle is decomposed into multiple sprints. The basic premise of sprint is to build a product which is ready to be shipped at the end of each sprint cycle – doesn’t matter if the product has only a few basic functionalities. What happens to those features which take multiple sprints to build and are not ready to be released yet? It's important to remember that the incomplete features are still part of the same codebase. 

The above question is especially true in a software company where a product might have to be released in the middle of a release cycle. These types of situations usually arise when a company is running out of money (especially in the case of a startup); to fix major bugs or due to market conditions (think of a startup hot on the heels of an established company). So coming back to our earlier question, what do we do when we are faced with a situation when a product has to be released and has a slew of incomplete features? 

First you should try to design your product in modules where a module can be easily removed without affecting the rest of the product. Yes, a software product can be designed that way – think of Eclipse, any application or web servers. However in most cases, it’s easier said than done. So, what are you supposed to do if your product belongs to the other camp? Martin Fowler proposed the features toggle pattern to handle these types of situations. 

The basic notion of features toggle pattern is to control the flow of software - whether a feature is used during an application runtime based on a set of flags (toggles). Toggles state can be stored either in a file, database, or even memory (not very practical).

Consider the feature toggle example shown below in pseudocode. If toggle FEATURE_ADDRESS  is true, display customer name and address or otherwise display customer name. 

**Feature Toggle Pseudocode**
```
IF FEATURE_ADDRESS IS true THEN
    Display customer name and address
ELSE
    Display customer name
ENDIF
```

Togglz is a Java implementation of Features Toggle pattern. You can find more about Togglz [here](http://www.togglz.org/). I played around with Togglz recently and wanted to share my experience. In order to make your application Togglz enabled, you have to implement a couple of classes:

*   A **Feature enum** (must implement _Feature_ interface) defining all the feature flags that you plan to use in your application.
*   A **Togglz configuration class** (must implement _TogglzConfig_ interface) storing information related to the **Feature enum** class where the feature flags are declared (described earlier), repository (file system, memory, database, etc.) for storing the state of the feature flags (enabled or disabled state), and the users who are authorized to modify the feature flags.

In my next few postings, I will explain Togglz in more details including a few working examples. Does Togglz have any use case for a product which doesn’t have to be released in the middle of a release cycle? Yes, I can think of a few:

*   Releasing a product for testing even though all the features are not ready yet.
*   Releasing a product with incomplete features turned off (time ran out).
*   Change an implementation of an interface or a REST service on the fly without the consumer being aware of it.
*   Same software exhibiting different behavior (different UI screens, etc.) based on the server they are deployed, i.e., turn on or off functionalities based on deployed server.
*   Switching from one version of REST service to another (client tier) on the fly.

Remember Togglz is not a silver bullet – it cannot replace good design. However it can help ease some of the pain associated with designing a product with many competing interests. Toggle flags should be used with restrain. Toggle flags in most cases are temporary Band-Aid and should be removed as soon as the wound heal – in our case when a feature gets completed or becomes obsolete.