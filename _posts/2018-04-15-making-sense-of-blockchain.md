---
layout: post
title: Making Sense of Blockchain
published: true
comments: true
tags: [Blockchain, Bitcoin]
  
image: /images/entry/blockchain-logo.svg
---

I got a call from my friend, a few Sundays back, and he started 
asking me about bitcoin and mining. Though I had a vague notion of bitcoins
and the technology behind it, I wasn't familiar with all the terms. 
As you've probably guessed, I wasn't able to carry out any meaningful 
discussion on the bitcoin topic. This post is my first attempt at making 
sense of blockchain, the technology at the heart of digital currency.

### Why Blockchain?

Before we dig too deep into blockchain, we need to understand the problem
blockchain is trying to solve. Let's take the example of money transfer where 
an entity sends an amount of money to a designated recipient through a
trusted third party, e.g., Western Union or any bank. In Figure 1, 
the trusted third party charges a fee of $5 for transferring $100 and takes a 
couple of days to transfer the funds.

![money transfer](/images/blockchain-concept/money-transfer.svg?style=centerme)

{:.image-caption}
Figure 1. Money transfer between A and B via a trusted third party

As shown in Figure 2, the blockchain attempts to transfer money by doing away 
with the third party. In the process, it lowers fees and time (close to real time) 
 to move funds around. The money moved by blockchain is often 
 referred to as  **digital currency** or **cryptocurrency** or 
 **virtual currency**. Examples of digital currencies include **bitcoin**, 
 **ether**, etc. 

![money transfer](/images/blockchain-concept/money-transfer-blockchain.svg?style=centerme)

{:.image-caption}
Figure 2. Money transfer between A and B without a trusted third party

Though the idea behind blockchain is not new, bitcoin is the first implementation
of blockchain technology by [Satoshi Nakamoto](https://bitcoin.org/bitcoin.pdf).

### What is Blockchain?

The broader aim of blockchain is to provide a platform for recording transactions
between two parties in an **open**, **efficient**, **verifiable**, and 
 **secure** manner. In the next few sections, I will go over the basic concepts
 of blockchain and how it achieves the aforementioned goals.

#### Open Ledger

The blockchain solves the problem of money transfer by introducing the concept of an
**open ledger**. An open ledger keeps track of all money transfers and makes them
 **visible** to everyone. Let's take an example where four parties _A_,
 _B_, _C_, and _D_ are in a blockchain network. At the beginning, 
 there is a single entry (_A = $100_) in the ledger where _A_ has _$100_. 
 The first entry in the ledger is called the **genesis** entry. In plain 
 English, genesis means start or origin. 
 
 ![open ledger](/images/blockchain-concept/open-ledger.svg?style=centerme)
 
 {:.image-caption}
 Figure 3. Open ledger entries in a blockchain
 
 A new entry (_A &rarr; B = $30_) is made in the ledger when _A_ transfers 
 _$30_ to _B_. This new transaction is not only recorded but also 
 linked with the previous transaction (_A = $100_). Another entry 
 (_B &rarr; C = $20_) is recorded in the ledger when _B_ transfers _$20_ to 
 _C_. Similarly, the new transaction (_B &rarr; C = $20_) is linked with 
 the previous transaction (_A &rarr; B = $30_).
 
 Now if you look at Figure 3(c) again, you will notice the open ledger is just a 
 **chain** of transactions visible to every node in the blockchain
 network. Every node knows the balance of every node, i.e., how much digital
 currency each node has. They can also determine the **validity of a transaction**.
 Let's take the case where  _C_ tries to transfer _$40_ to _D_. Everyone in
 the network would immediately know from the open ledger that the new 
 transaction (_C &rarr; D = $40_) is invalid since _C_ has insufficient 
 funds. The invalid transaction will be rejected right away 
 and will not be entered in the open ledger. 
 
  ![invalid open ledger txn](/images/blockchain-concept/invalid-open-ledger-txn.svg?style=centerme)
  
  {:.image-caption}
  Figure 4. Invalid transaction in a blockchain 
  
#### Distributed Open Ledger

You will notice a centralized ledger if you refer to Figure 3. However, a 
blockchain's goal is a decentralized open ledger in order to remove any single 
point of failure and also to do away with any central authority (big brother). 
The blockchain achieves this goal by **distributing** copies of the open ledger 
among participating nodes in the network.

![distributed open ledger](/images/blockchain-concept/distributed-open-ledger.svg?style=centerme)
  
  {:.image-caption}
  Figure 5. Distributed open ledger
  
This means, _A_ has a copy of the ledger, _B_ has a copy of the ledger, etc. 
A distributed ledger removes the need for a centralized ledger. 
A distributed ledger, however, introduces the added complexity of keeping all 
the ledgers in sync where all transactions are visible to all the nodes in
the blockchain network immediately.

**Q. How does a node join a blockchain network?** 
  
Any computer (process) that connects to a blockchain network is a node. 
It's a **peer-to-peer** network. A node can leave and rejoin the network at will.

#### Miners

The challenge of keeping nodes in sync is mitigated by advancing the concept 
of **miners**. A miner is a special node in a blockchain network which has 
access to the ledger. Any node can be a potential miner.

Let's take the earlier example of _B_ transferring _$20_
to _C_. The transaction (_B &rarr; C = $20_) is not entered in the 
distributed open ledger until it's validated. The blockchain network makes the new 
transaction available to all its nodes. Miners nodes then compete 
against each other to be the first one to **validate** the transaction 
(_B &rarr; C = $20_) and **record** it in the ledger. The winning miner is 
**rewarded financially** with digital currency while the losing miners get
nada. 

![mining](/images/blockchain-concept/mining.svg?style=centerme)
  
  {:.image-caption}
  Figure 6. Example of blockchain mining

To validate the transaction (_B &rarr; C = $20_), the winning miner has to 
first ensure that _B_ has enough funds. The miner has to then find a 
**key** that allows it to link the new transaction with the previous transaction 
(_A &rarr; B = $30_). Finding a key is rather difficult as it's random and 
takes a lot of computational power and time. 

Once a miner records the transaction, it publishes the result to the 
network. The result includes the key used for linking the new transaction. Once
the other nodes see the result, they add the new entry to their own ledgers 
after verifying the entry. Any tampering of the entry will be rejected. 
This way a consensus is reached among different nodes about the new ledger 
entry. Other miners find no incentive in wasting computational resources in 
recreating the key of this verified transaction. The miners now 
wait for the next unvalidated transaction and a chance to win digital coins.

To reiterate, a distributed open ledger is replicated across many nodes in a 
blockchain network. Any new entry in one ledger results in simultaneous
updates in other ledgers. A ledger entry is recorded by a miner with the
incentive of receiving financial rewards in the form of digital currency. The
cost of entering a ledger entry is computationally expensive and is termed
 **proof-of-work** or **mining**. 

### Blockchain Security

The concept of a distributed open ledger and miners help make blockchain 
**open**, **efficient**, and **verifiable**. It also solves the issue of 
**security** partially by making all ledger entries permanent. Permanency in 
the sense that it'll not be easy for an entity to delete or modify a previously 
recorded transaction in the ledger. 

**Q. How's the permanency of open ledger entry achieved?**

We briefly touched upon the subject of **key** earlier. The key is also
termed as **hash** and can be considered as the **fingerprint** of an entry
 which is unique to the entry. Each hash depends not only on the data contained 
in the ledger entry but also on the hash of the previous entry. This makes all 
ledger entries **chronological** in order and **tamperproof**. 
Any change in a ledger entry will result in redoing
the proof-of-work. It will generate a new hash which in turn will have a 
cascading effect of invalidating subsequent entries' hash. Since proof-of-work
is an expensive process, it makes open ledger virtually immune to modifications.  

![security](/images/blockchain-concept/blockchain-security.svg?style=centerme)
  
  {:.image-caption}
  Figure 7. Any change in an open ledger entry will result in recalculation of its hash

Another way blockchain provides security is by having a distributed ledger and
thus preventing a single entity (think government) from manipulating the ledger.

**Q. In our earlier example, how do you prevent _B_ from spending _A's_ money?**

Blockchain takes advantage of **asymmetric-key encryption** which is also
known as **public-key encryption**. In this type of encryption, there is a 
 **public key** and a **private key**. The private key is used to create
 a digital signature while the public key is used to verify that signature.

In blockchain, each node has a public key and a private key. The public key serves
 as the address of a node and is visible to everyone. Every ledger entry has a 
 **sender address (public key)**, a **receiver address (public key)**, 
 **amount transferred**, and a **digital signature**. 
 
 When _A_ wants to transfer funds to _B_, _A_ computes a signature using its
 private key and then sends the transfer request. _B_ or anyone
 else can verify the signature using _A's_ public key. In order for _B_ to 
 steal _A's_ money, _B_ has to possess _A's_ private key. _A_ is vulnerable 
 to theft only if it loses its private key.

### Implications of Blockchain

According to ["The Truth About Blockchain"](https://hbr.org/2017/01/the-truth-about-blockchain)
 article published in the Harvard Business Review, the blockchain can be 
 considered more of a **foundational** technology. It's not disruptive 
 in the sense of cell phones replacing landline telephones or the take over of 
 35mm film cameras by digital cameras. The blockchain technology
 has the potential to have an enormous effect on societies and economies but the 
 process of adoption will be slow. Beyond cryptocurrency, blockchain can be used
 in electronic medical records, notary, real estate, etc.
 
 I hope you have a slightly better understanding of blockchain now. I plan 
 to address other aspects of blockchain in my next few postings. 