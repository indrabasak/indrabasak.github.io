---
layout: post
title: A Blockchain Hello World in Java
published: false
comments: true
tags: [Blockchain, Java]

image: /images/entry/classfile-duke.svg
---

### Blockchain Implementation

Now that the concept of blockchain is a little bit clear, we'll take a closer 
look at how a blockchain is implemented. 

#### Blockchain Data Structure

A blockchain is implemented as a list of blocks. You can visualize a blockchain 
as a linked list of blocks. Each block has the following properties:

1. A blocks has a **unique identifier** know was **hash**. It's calculated 
using a **hash function**.A hash function takes an input of bits and 
produces a fixed size result. Hash functions are also know as **message digest** 
functions and the resulting hash is also known as the **digest**. A hash is 
typically used as **digital signature**. The input of the hash function in 
blockchain is usually the summation of information contained within the block.

1. Each block contains the **hash of the previous block**. It means a block's 
hash is computed using a previous block hash. This way all blocks are guaranteed
to be in **chronological order**. This makes **tampering** of a block 
**computationally impractial** since hash of every subsequent block has to be 
regenerated. 

1. The first block of a block chain is called the **genesis block**.


Proof of Work (POW) is a way of ensuring that a new block is difficult to build by making the block creation process costly and time consuming. However it must be relatively trivial to check if a blockchain satifies these requriiments. This helps to avoid blockchain tampering.