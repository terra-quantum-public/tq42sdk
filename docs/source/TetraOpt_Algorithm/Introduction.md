# Introduction

## Optimization Algorithms
Optimization is the process of refining and improving systems and operations to make them more efficient, effective, and profitable. All companies aim to reduce their costs and increase their productivity but doing this in intuitive ways is insufficient. Modern companies are formulating these goals as mathematical optimization problems that are amenable to algorithmic solutions.  

The success of classical optimization algorithms is limited in several ways. The search space is huge, often growing factorially with the number of variables. This is faster than exponential growth! The problems are incredibly intricate – every variable matters and they all depend on each other in complex ways.

## Tensor Trains
Tensor networks are a new approach to linear algebra, emerging from quantum physics, for very efficient solutions to high-dimensional problems. The main idea is to decompose a huge tensor into a product of small ones. This decomposition can be visualized in a network diagram. Tensor trains (TT) are a type of tensor network that have a simple, linear structure. They are the most well-studied of all tensor networks.

## TetraOpt
TetraOpt (short for Tensor Trains Optimization) is a global optimization library based on tensor train decomposition. A variety of practical applications require finding the maximum or minimum value of a function, but in many cases the function is non-convex and has a lot of local extrema. This is an example of a global optimization problem.

TetraOpt is a black-box optimization algorithm, meaning that it can optimize an objective function for which we have very little specific knowledge. Black-box optimization is required when you don’t have access to an analytic function or its derivatives. Furthermore, you often only have a small budget of function evaluations. TetraOpt is our universal black-box optimizer.  

Key benefits: 
- It is universal, simple, intuitive, supports high levels of parallelization and is compatible with quantum implementations. 
- It reaches lower values of the cost function in less time than alternative algorithms.

## Basic Math
TetraOpt is a global optimization library based on tensor train (TT) decomposition. A variety of practical applications require finding the maximum or minimum value of a function, but in many cases the function is non-convex and has a lot of local extrema. This is an example of a global optimization problem.

This can be considered a problem-specific method, as for some problems it guarantees that global optimum will be found. But, unlike a majority of such methods, it can be used as a black-box non-deterministic method.

Tetra Opt uses the tensor train (TT) mathematical model of functional (or of its discretized version in case of a continuous problem). It guarantees that the global optimum will be found if:
- The considered optimization problem is a problem of finding value with maximal magnitude.
- The tensor of functional values has a good enough approximation with tensor train of small ranks.