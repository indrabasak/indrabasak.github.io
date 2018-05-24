---
layout: post
title: A Blockchain Hello World in Java
published: false
comments: true
tags: [Blockchain, Java]

image: /images/entry/blockchain-java-logo.svg
---

In my last posting, ["Making Sense of Blockchain"]({{ site.baseurl }}/making-sense-of-blockchain/), 
I touched on the basic concepts of blockchain. Now that the concept of 
blockchain is a little bit clearer, we'll take a closer look on how to 
implement a simple blockchain in Java.

A blockchain is implemented as a list of blocks. You can visualize a blockchain 
as a linked list of blocks where each block has the following properties:

1. A blocks has a **unique identifier** know was **hash**. It's calculated 
using a **hash function**.A hash function takes an input of bits and 
produces a fixed size result. Hash functions are also known as **message digest** 
functions and the resulting hash is known as the **digest**. For clarity's 
sake, we will stick with the term from now on. The input of the hash function 
is usually some type of aggregation of data contained within the block.

1. Each block contains the **previous block hash**. It means a block's 
hash is computed using a previous block hash. This way all blocks are guaranteed
to be in **chronological order**. 

1. The first block of a block chain is called the **genesis block**.


Proof of Work (POW) is a way of ensuring that a new block is difficult to build by making the block creation process costly and time consuming. However it must be relatively trivial to check if a blockchain satifies these requriiments. This helps to avoid blockchain tampering.