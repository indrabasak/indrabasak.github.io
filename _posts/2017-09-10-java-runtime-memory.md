---
layout: post
title: Memories of a Java Runtime
published: true
comments: true
tags:
  - JVM
  - Java
  - Memory
image: /images/entry/jvm-runtime.png
---
 
It's been a while since I wrote anything about Java Virtual Machine (JVM). 
I have been using Java for quite some time, yet my understanding of the inner 
workings of JVM seems to fade if I don't refresh it once in a while. This 
posting is an attempt to renew my memories while trying to add something new. 
I plan to post a series of articles exploring different aspects of JVM.

The Java memory seems to be the part which trips most folks. What better way 
to start than exploring the JVM’s runtime memory? The JVM runtime memory can be 
broadly classified into two groups: _common memory areas_ and _exclusive areas_. 
The common memory areas are created during JVM startup and shared across all 
threads. They are destroyed during JVM exit.

Exclusive areas are created during new thread instantiations. A thread 
specific area is only accessible by the thread responsible for its creation.
It's destroyed during the thread exits. Figure 1 shows different
groups of JVM runtime memory.

![memory model](/images/jvmruntime/jvm-runtime-memory.png?style=centerme)

{:.image-caption}
Figure 1. JVM runtime memory

The _method area_ and _heap_ falls under common memory areas while _JVM stack_, 
_stack frame_, _operand stack_, _native stack_, _local variables_, and 
_program counter (PC) register_ are grouped under thread specific memory areas.

### Common Memory Areas

#### Method Area

Once a class bytecode is loaded by a JVM class loader, it's passed to the JVM 
for further processing. The JVM creates an internal representation of the class and 
stores it in the _method area_. An example of a class method area is shown in 
Figure 2. The following data areas are contained within 
the internal representation of a class:

* **Runtime Constant Pool** contains constants used in a particular class. 
The constants can be of types int, float, double, and UTF-8. It also contains
references to methods and fields.

* **Method Code** is the implementation (opcodes) of all class methods.

* **Attribute and Field Values** contain all named attributes and field 
values of a class. A field value points to a value stored in the runtime 
constant pool.

![memory model](/images/jvmruntime/jvm-method-area.png?style=centerme)

{:.image-caption}
Figure 2. A class method area

A method area can be part of a heap. It's created during runtime and
available to all threads. Its size can be fixed or changed dynamically.
Providing a garbage collection mechanism for the method area is optional. 
A JVM throws a _OutofMemoryError_ if the method area runs out of allocation space.

#### Heap

A heap, shown in Figure 3, is created during JVM startup time and used for 
storing instances of classes and arrays. The size of a heap can be fixed or dynamic. 
A heap must provide _garbage collection_ mechanism to reclaim unused space.
However, a garbage collection implementation scheme is not specified and
it is configurable. A heap area is shared across all threads.
A JVM throws an _OutofMemoryError_ if the heap runs out of allocation space.

![memory model](/images/jvmruntime/jvm-heap.png?style=centerme)

{:.image-caption}
Figure 3. JVM heap

### Exclusive Memory Areas

#### JVM Stack

Every thread has a private JVM stack. A stack is created during a thread 
startup time and its size can be static or dynamic. A JVM stack is used 
for storing _stack frames_ as shown in Figure 4. A new stack frame is created 
and pushed into a thread stack every time a method is invoked. A frame is popped 
when a method returns. Thought there may be multiple frames on a stack from nested 
method calls, only one frame is active at a given time for a thread.

![memory model](/images/jvmruntime/jvm-stack.png?style=centerme)

{:.image-caption}
Figure 4. JVM stack

A JVM throws a _StackOverflowError_ when a thread needs a stack area larger
than permitted or memory available. If a JVM stack is dynamically allocated, 
a JVM may throw an _OutofMemoryError_ if insufficient memory is available to 
meet stack size increase request. It may also throw a _OutofMemoryError_ if 
insufficient memory is available during initial stack allocation.


#### Stack Frame

A new stack frame is allocated and pushed into a JVM stack every time a method 
is invoked. A frame is popped from the stack and destroyed upon the completion
of method invocation irrespective of whether the completion is normal or
abrupt (uncaught exception). As shown in Figure 5, each frame has its own operand 
stack, an array of local variables, and a reference to the runtime constant pool.

![memory model](/images/jvmruntime/jvm-stack-frame.png?style=centerme)

{:.image-caption}
Figure 5. A stack frame

* **Local Variables**: A JVM uses local variables to pass around method 
parameters. Each frame contains an array of local variables. The 
size of the table is determined at class compile time. It can store values
of type boolean, byte, char, short, int, float, reference, or return address. 
A long or a double value occupies two consecutive local variables.

    For all instance methods including constructors, the local variable at index 0
always refers to _this_ object. Subsequent indexes, starting at position 1, 
stores method parameters.

* **Operand Stack**: Each frame contains an operand stack and the stack's 
maximum depth is determined at compile time. An operand stack consists of 
JVM instructions (opcodes) to load local or field variables. The JVM may also
instruct to take operands from the operand stack, operate on them, and 
push the result back on the operand stack. An operand stack is used for preparing
parameters required to invoke a method. It's also used for receiving the
 result back from an invoked method.
						
* **Reference to Runtime Constant Pool**: A reference to the runtime constant 
pool of the method’s class which is stored in the method area.

#### PC Register

Each thread has its own pc (program counter) register. If the method is nonnative, 
a pc register points to the address of the JVM instruction currently being executed
 by the thread. The content of a PC register is not defined for a native method.


#### Native Method Stack

A native method gets its own stack called _C-Stack_.

In my future postings, I plan to address Java memory model and its management.
