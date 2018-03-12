---
layout: post
title: A Class of Its Own
published: true
comments: true
tags:
  - JVM
  - Java
# use_math: true  
image: /images/entry/classfile-duke.svg
---

Anyone using Java is familiar with the concept of Java class file. It's the 
artifact generated from a Java source file after a successful compilation. A
class file contains bytecode (instructions) that is interpreted by a Java 
Virtual Machine (JVM) during execution. As shown in Figure 1, the bytecodes 
in a class file follows a strict format described in the JVM specification. 

![classfile-layout](/images/classfile/classfile-layout.svg?style=centerme)

{:.image-caption}
Figure 1. A class file layout

In this posting, I will be exploring different aspects of a Java class file. 
The best way to get familiar with the class file is to start with an
example, `ClassA.java`, as shown in Figure 2. It's a very simple example where 
`methodX` of `ClassA` combines the two input parameters and return them as a
string. Once you compile the class, you will be getting the `ClassA.class` file.

![ClassA.java](/images/classfile/classfile-classA-java.svg?style=centerme)

{:.image-caption}
Figure 2. Example ClassA.java

Our next step is to investigate the bytecode inside the class file. 
Java provides a `javap` command line utility to disassemble a class file.
Its output is dependent on the options used during its usage. In the current example,
`'javap -c -verbose'` command is used to generate the content of the class file
including the constant pool, stack size, etc. You can find the disassembled 
class file [here](https://gist.github.com/indrabasak/22fd48ea12f5acc224482d2c2278c391).
I will be using the disassembled `ClassA.class` as a reference to explain different
parts of a Java class file. So, let's start from the very beginning which is the
magic number of the class file.

### Magic Number

In computer science,  a standard way to identify a file type is to
insert some type of unique metadata at the beginning of a file. This is the 
convention followed by file types such as PNG, JPEG, etc. The unique identifier 
is termed as the **`magic number`** of a file. 

In Java class file, the first four bytes represents the magic number. It 
uniquely identifies the class file format and has the value of `CAFEBABE`
in hexadecimal format.

If the `ClassA` class file is viewed with a Hex editor, 
e.g., [HxD](http://mh-nexus.de/en/hxd/) for Windows or 
[iHex](https://itunes.apple.com/us/app/ihex-hex-editor/id909566003?mt=12) for 
Mac OS, you will notice the magic number as shown in Figure 3.

![class hex layout](/images/classfile/classfile-classA-hex.svg?style=centerme)

{:.image-caption}
Figure 3. Hexadecimal layout of ClassA.class

There is an interesting story behind the origin of `CAFEBABE` moniker. 
James Gosling, the father of Java, and his friends used to visit a restaurant 
where Grateful Dead allegedly played before they became famous. After the death 
of Jerry Garcia, James and his friends started calling the place `Cafe Dead`. 
While James was looking for a magic number for the object file, he decided to 
use `CAFEDEAD`. Going along with the cafe theme, he came up with `CAFEBABE` 
as the magic number of the class file.

### Class File Version

The next four bytes of the class file contain **`major`** and **`minor`** 
**`version numbers`**. It allows the JVM to verify and identify the class file. 
A class file is rejected with a `java.lang.UnsupportedClassVersionError`
exception if the numbers are greater than the versions allowed by a JVM.
In the disassembled `ClassA.class`, the major version shows up as a 
hexadecimal value of `0x00000034` (the second hexadecimal number in Figure 3). 
In terms of decimal, it is ![magic number](/images/classfile/classfile-magic-number.svg). 
This numeric value is associated with a corresponding version of Java SE. In 
this case, the number `52` indicates that the `ClassA` is a `Java SE 8` 
compiled class. You can find more about the mapping 
[here](https://docs.oracle.com/javase/specs/jvms/se9/html/jvms-4.html).

### Constant Pool

All constants related to a class are stored in a **`constant 
pool table`**. The constants include `class names`, `variable names`, 
`interface names`, `method names`, `signature`, `final variable values`, 
`string literals`, etc. They are stored as a variable length
array element in the constant pool. The array of constants are preceded
by its array size known as the **`constant pool count`**. This helps the JVM to know 
the number of constants that are expected while loading the class file.

![constant pool](/images/classfile/classfile-constant-pool.svg?style=centerme)

{:.image-caption}
Figure 4. ClassA's constant pool

A `constant pool table` entry begins with a one byte tag indicating the type
of entry. The type includes `class`, `field`, `method`, `interface`, `string`, 
`int`, etc. The rest of the information stored in the entry varies according to 
the type.

For instance in Figure 4, the constant pool entry at index `4` has a tag value 
of `7` followed by the number `42`. The number `7` indicates that it's an 
entry of type `class`. The number `42` indicates the index entry in the 
constant pool specifying the name of the class. 

At index entry `42`, the tag value of `1` indicates that the entry is of `UTF-8`
type. An UTF-8 table entry has two more fields. The single byte second field
holds the length of the byte array used for storing the string value 
in the third field, `example/simple/app/ClassB`.

### Access Flags

The **`access flags`** follows the constant pool. The flags are stored as 
bit masks in a two byte entry. It contains information related to the type of 
program code template stored in the file. In other words, it indicates if the
file contains a a `class` or an `interface` definition. If it's a class 
definition, extra flags are added to reveal if the class is `public`, 
`abstract` or `final`. All the access flags are retrieved by performing
a bitwise AND operation with various bit masks, e.g., `ACC_PUBLIC`, `ACC_SUPER`, etc.

![access flags](/images/classfile/classfile-access-flags.svg?style=centerme)

{:.image-caption}
Figure 5. Access Flags

In Figure 5, the `ACC_PUBLIC` flag signals that it's a `public` class. The `ACC_SUPER` 
flag is slightly confusing. Let's say a class named, `AnyClass` overrides a 
method named `anyMethod()` from it's super class, `AnySuperClass`. If the 
`ACC_SUPER` is not set, the JVM can skip `AnyClass.anyMethod()` and call
 `AnySuperClass.anyMethod()`. The absence of the `ACC_SUPER` flag is no longer
 honored by the JVM after `Java 7u13` security update. 

### this Class

After the `access flags`, the next two byte entry points refers to **`this class`**.
It points to an entry in the constant pool. In Figure 6, `this class` points to 
a constant pool entry of `15`. The entry `15` points to entry `51` which stores 
the name of the `this class`, i.e., `example/simple/app/ClassA`.

![access flags](/images/classfile/classfile-this-class.svg?style=centerme)

{:.image-caption}
Figure 6. this Class

### super Class

The next two bytes after `this class` is the **`super Class`**. Similar to 
`this class` entry, the `super Class` points to a constant pool entry. As show
in Figure 7, it points to entry `16` which in turn points to entry `52`. The
entry `52` stores the name of the `super class`, i.e., `java/lang/Object`.

![access flags](/images/classfile/classfile-super-class.svg?style=centerme)

{:.image-caption}
Figure 7. super Class

### Interfaces
				
All the interfaces that are implemented by the class (or interface) defined 
in the file goes in the **`interfaces`** section of a class file. It comes
next after the `super class` entry. The starting  two bytes of the interface 
section is the `interface count` which gives the number of direct interfaces 
implemented by this class or interface. The interface count is followed by an 
array of indices pointing to the entries in the constant pool. Each index 
refers to a name of an interface implemented by this class. The interface 
count in the current example is `0` since `ClassA` doesn't 
implement any interface.

### Fields

A field is an instance or a class level variable (property) of the class or 
interface. The **`fields`** section, which comes after the `interface` section,
 contains only those fields that are defined by `this` class or interface and 
 not the fields inherited from the super class or super interface. The first 
 two bytes in the fields section represents the `field count` which gives 
 the total number of fields in the fields section. An array of variable length 
 structure follows the field count. Each array element represents one field. 
 Some of the field information is stored in this array element while other 
 information such as field names are stored in the constant pool.

![fields](/images/classfile/classfile-fields.svg?style=centerme)

{:.image-caption}
Figure 8. ClassA's fields

The Figure 8 shows the structure of a field element. The first two bytes holds
the `access flags` of the field. The next four bytes hold constant pool table 
indexes that point to the `field name` and the `field descriptor` respectively. 

### Methods
The **`methods`** section, which comes afer `fields` section, contains 
information about methods that are explicitly defined by `this` class. 
It doesn't contain any other methods that  are inherited from the `super` 
class. The first two byte holds the **`method count`** of the methods declared 
in the class or the interface. Next is a variable length array with each 
element storing a different method structure. The method data structure, as 
shown in Figure 9, is very similar to that of a field entry except the last 
part of the method element holds the `code` attribute.

![attributes](/images/classfile/classfile-methods.svg?style=centerme)

{:.image-caption}
Figure 9. Methods of ClassA

A method `code` attribute contains several pieces of information including the 
`method argument list`, `return type`, and the `number of stack words` 
required for each of method's `local variables` and `operand stack`, a 
`table for exceptions`, `byte code sequence`, etc.

![access flags](/images/classfile/classfile-operand-stack.svg?style=centerme)

{:.image-caption}
Figure 10. Stack frame of ClassA's methodX's at various stage of operations

The instructions shown in Figure 10, has letter prefixes and numeric suffixes, 
e.g. `aload_0`, `iload_2`. A prefix denotes the type of data that is going to
be handled by the the instruction. The prefix `'a'` means the `opcode` is 
manipulating an object reference. While prefix `'i'` means the opcode is 
manipulating an integer. A numeric suffix preceded by an underscore( `'_'` ) indicates 
the location of the data in the `location variables table`. The instruction 
`aload_0` is going to operate on an object reference stored at position `0` of 
the local variables table while `iload_2` plans to operate on an integer value 
stored at position `2` of the local variables table.

You may also notice some of the instructions accept numeric operands
preceded by a hashtag(`'#'`), e.g., `#1`, `#2`. These numbers are used to 
construct an index into the runtime constant pool of the current class.

Let's consider the first few lines of the bytecode generated by method `methodX`
of `ClassA` in Figure 10. It consists of mulitple opcode instructions. 
The first opcode `aload_0` pushes the value from index `0 `of the local 
variable table into the `operand stack`. For constructors and instance methods, 
reference to `this` object is always stored at location `0` of the local 
variable table.

The next opcode `aload_1` pushes the method's first parameter value, which is 
stored in the index `1` of the local variable table, into the operand stack.
The `putfield #2` opcode points to the index `2` of the constant pool which
in turn points to the `myAttrib1` field. The `putfield` expects the top of the 
stack to be a value and the one below it to be the object reference.
After resolving the class name of the object reference, field name and its type,
the `putfield` assigns the value stored in the last entry of the stack 
(value of the first method parameter `param1` in our case) to `this`'s `myAttrib1`
field. After the assignment of the value, the top two entries are popped from 
the stack.

The next three opcode instructions perform similar tasks except they assign 
integer value from the method parameter `param2` to `this'`s `myAttrib2` field.

### Attributes
				
The **`attributes`** section, which comes after the `methods` section,  contains 
several attributes of a class file. The first two bytes in the attribute 
section is the **`attribute count`** followed by the class attributes. Each 
attribute entry has three different fields: `name index`, `attribute length`, 
and `attribute info`. The `name index` is a two byte entry which points to 
the constant pool index. The constant pool entry at the attribute index 
contains the name of the attribute. The `attribute length` item indicates the 
length of the subsequent `attribute info`. 

The Figure 10 shows the relationship bewteen the attribute and the constant pool
in the `ClassA` example. The attribute shown here is the source code attribute 
which reveals the name of the `source file` from which this class file was compiled.
The `attribute info` entry in this case points to the constant pool index which
is not always the case. A JVM will ignore any attribute that it doesn't recognize.

![attributes](/images/classfile/classfile-attributes.svg?style=centerme)

{:.image-caption}
Figure 11. Attributes of ClassA

I hope that I was able to clear up some of the mystery surrounding the Java class
file. Now that we have a better understanding of a class file format, I will 
try to address the topic of bytecode manipulation in one of my future postings.
