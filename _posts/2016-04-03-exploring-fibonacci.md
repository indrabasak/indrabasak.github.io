---
layout: post
title: Exploring Fibonacci
published: true
comments: true
tags: [Algorithm, Fibonacci]
---

We all are familiar with Fibonacci numbers in the field of computer science. It is a sequence of integers which follows the pattern:

```
0, 1, 1, 2, 3, 5, 8, 13, 21, ...
```

The first two numbers in the sequence are 0 and 1. Any other number in the sequence is defined as: H~2~O 

$$
\begin{align*}
F_n = F_{n-1} + F_{n-2}
\end{align*}
$$

Here, I will explore the different ways of solving the Fibonacci numbers and the complexity associated with each of the algorithm.

### Fibonacci Recursion

The easiest way of solving the Fibonacci is by recursion. Here is an example code snippet:

```java
public int fib(int n) {
    if (n <= 1) {
        return 1;
    } else {
        return fib(n-1) + fib(n-2);
    }
}
```

#### Complexity Analysis of Fibonacci Recursion

The time complexity of the Fibonacci recursive algorithm is measured by designating value of 1 to constant operations. 
1 for comparing _(n <= 1)_; 1 for _fib1(n-1)_; 1 for _fib2(n-2)_; and 1 for addition operation - _fib1(n-1) + fib1(n-2)_.

Here is equation (1), 

$$
\begin{equation}
\begin{aligned}
T(0) = 1 \\
T(1) = 1 \\
T(n) = T(n-1) + T(n-2) + 4 \\
T(n) = T(n-1) + T(n-2) + C 
\end{aligned}
\end{equation}
$$ 

To find the _lower bound of time complexity_, let's assume

$$
\begin{align*}
T(n-1) ≈ T(n-2)
\end{align*}
$$

then equation (1) can be simplified to equation (2),

$$
\begin{equation}
\begin{aligned}
T(n) = 2T(n-2) + C \\
T(n) = 2\{2T(n-4) + C\} + C \\
T(n) = 4T(n-4) + 3C
\end{aligned}
\end{equation}
$$   

then equation (2) can be simplified to equation (3),

$$
\begin{equation}
\begin{aligned}
T(n) = 4{2T(n-6) + C} + 3C \\
T(n) = 8T(n-6) + 7C
\end{aligned}
\end{equation}
$$

then equation (3) can be simplified to equation (4),

$$
\begin{equation}
\begin{aligned}
T(n) = 16T(n-8) + 15C
\end{aligned}
\end{equation}
$$

The equation (4) can be re-written as equation (5),

$$
\begin{equation}
\begin{aligned}
T(n) = 2^kT(n-2k) + (2^k-1)C 
\end{aligned}
\end{equation}
$$

Let's verify if the expression holds true for all cases. In equation(2), k = 2; in equation(3), k = 3. Now if we 
want to apply equation (5) for n = 0:

$$
\begin{align*}
T(n-2k)= T(0) \\
n-2k = 0 \\
k = n/2
\end{align*}
$$

Equation (5) can now be reduced to equation (6),

$$
\begin{equation}
\begin{aligned}
T(n) = 2^{n/2}T(0) + (2^{n/2}-1)C \\
T(n) = (1+C)2^{n/2} + C
\end{aligned}
\end{equation}
$$

Now in equation (7), we can say that the _lower bound of time complexity_ is proportional to:

$$
\begin{equation}
\begin{aligned}
T(n) ∝ 2^{n/2}
\end{aligned}
\end{equation}
$$

Similarly, we can find the _upper bound of time complexity_ by assuming

$$
\begin{align*}
T(n-2) ≈ T(n-1)
\end{align*}
$$

then equation (7),

$$
\begin{equation}
\begin{aligned}
T(n) = 2T(n-1) + C \\
T(n) = 2\{2T(n-2) + C\} + C \\
T(n) = 4T(n-2) + 3C
\end{aligned}
\end{equation}
$$
 
equation (7) can be reduced to equation (8),

$$
\begin{equation}
\begin{aligned}     
T(n) = 4\{2T(n-3) + C\} + 3C \\
T(n) = 8T(n-3) + 7C
\end{aligned}
\end{equation}
$$   

The equation (8) can be re-written as equation (9),

$$
\begin{equation}
\begin{aligned}
T(n) = 2^kT(n-k) + (2^k-1)C 
\end{aligned}
\end{equation}
$$  

For,

$$
\begin{align*}
T(n - k) = T(0) \\
n - k = 0 \\
k = n
\end{align*}
$$

Equation (9) now can be reduced to equation (10),

$$
\begin{equation}
\begin{aligned}
T(n) = 2^nT(0) + (2^n-1)C \\
T(n) = (1+C)2^n - C 
\end{aligned}
\end{equation}
$$ 

Now we can say in equation (11) that the _upper bound of time complexity_ is proportional to:

$$
\begin{equation}
\begin{aligned}
T(n) ∝ 2^n
\end{aligned}
\end{equation}
$$ 

So the time complexity of recursive Fibonacci algorithm is somewhere is between lower and upper bound of time complexity. However in Big-O terms, it is the upper bound of time complexity. In Big-O notation, the complexity of recursive Fibonacci algorithm is:

$$
\begin{align*}
O(2^n)
\end{align*}
$$

The recursive algorithm takes exponential time to compute the value. That's a lot of time to derive a value. The Fibonacci recursion algorithm can be improved upon by applying the principle of dynamic programming.

### Dynamic Programming

Dynamic Programming is a technique for solving problems which exhibit the characteristic of overlapping sub-problems. Let's take the example of Fibonacci numbers. _fib(n)_ is dependent on _fib(n-1)_ and _fib(n-2)_. To calculate _fib(5)_, here is the number of times fib is called:

![fibonacci](https://indrabasak.files.wordpress.com/2016/04/fibonacci.png) 

You noticed that _fib(3)_  and _fib(2)_ are called multiple times. We could have reused the value of _fib(3)_ and _fib(2)_ if we had stored the values during the first call. There are couple ways of storing the values. We will talk about it in the next couple of sections.

### Memoization

It is similar to the recursive algorithm but with a small change. Now there is lookup table which the algorithm looks up before it computes a value. If the value exists, it doesn't compute. Otherwise the value is computed and stored in the lookup table for later reuse. It's the top down approach. Following is the memoized version of the Fibonacci number. I am restricting the array size to 1001\. Any number bigger than 1000, will return a value of -1.

```java 
public class Fibonacci {
    public static int MAX = 1000;
    private int[] lookupTable = new int[MAX + 1];

    static {
        for (int i = 0; i <= MAX; i++) {
            lookupTable[i] = -1;
        }
        lookupTable[0] = 0;
        lookupTable[1] = 1;
    }

    public int fib2(int n) { 
        if (n > MAX) {
            return -1;
        }

        if (lookupTable[n] == -1) {
            lookupTable[n] = fib2(n-1) + fib2(n-2);
        } else {
            return lookupTable[n];
        }
    }
```    

#### Complexity Analysis of Fibonacci Memoization

Though the complexity of memoized Fibonacci is still $$ \begin{align*} O(2^n) \end{align*} $$, it is much faster than regular Fibonacci recursion since we have reduced the time by defining the recursive algorithm in terms of overlapping sub-problems.

### Tabulation

It is the bottom-up approach of solving a problem by building a table that returns the last entry from the table. In memoized version, the lookup table is filled on demand while all the entries in the tabulated version is filled up at once. The lookup table in memoized is not necessary filled up at a given instance.

```java
public int fib3(int n) {
   int[] fib = new int[n + 1];
   fib[0] = 0;
   fib[1] = 1;

   for (int i = 2; i <= n; i++) {
       fib[i] = fib[i-1] + fib[i-2];
   } 
   return fib[n];
}
```

#### Complexity Analysis of Fibonacci Tabulation

The complexity is linear time, i.e, the amount of times around the loop is equal to the size of number, n, we are trying to calculate. The complexity is shown as **O(n)**.