# 00 Stochastics for Engineers

# 01 Introduction

## 1.1 What is Stochastics?  
**Definition:**  
Stochastics (Stochastik) is the branch of mathematics dealing with random phenomena. It comprises:
- **Probability theory:** rigorous, axiomatic study of randomness  
- **Statistics:** data collection and inference about real-world events  

**Basic interpretations of probability:**  
- **Laplace** (finite, uniform):  
$$
P(A)=\frac{\#\{\text{favorable cases}\}}{\#\{\text{possible cases}\}}
$$   
- **Frequentist:** long-run relative frequency  
- **Subjective/Bayesian:** degree of belief (“prior”)  

**Kolmogorov’s axioms:**  
1. $(P(\emptyset)=0)$  
2. $(P(\Omega)=1)$  
3. For disjoint events $(A_i)$:  
$(\displaystyle P\Bigl(\bigcup_i A_i\Bigr)=\sum_iP(A_i))$

---

# 02 Introductory Examples

## 2.1 Flipping a Coin  
- **Sample space:** $(\Omega=\{\mathrm{Head},\mathrm{Tail}\})$
- **Fair coin:**  
  $$
    P(\{\mathrm{Head}\})=P(\{\mathrm{Tail}\})=\tfrac12
  $$  
- **Python simulation:**  
  ```python
  import random
  outcomes = [random.choice(["Head","Tail"]) for _ in range(10000)]
  ```

## 2.2 Rolling a dice

- **Sample space:** $(\Omega=\{1, 2, 3, 4, 5, 6\}$
- **Fair die**
  $$
    P(\{i\})=\frac{1}{6}, \forall i \in \{1, ..., 6\}
  $$ 
- **Python simulation:**
```python
import random
dice = [random.randint(1,6) for _ in range(10000)]
```
- **Histogram (matplotlib):**
```python
import matplotlib.pyplot as plt
plt.hist(dice, bins=6)
plt.show()
```

# 03 Discrete probability spaces

## 3.1 Definition

A discrete probability space is $(\omega, P)$ with infinite $\Omega$ and $P$ on all subsets satisfying Kolmogorov's Axioms.

## 3.2 Uniform distribution

On finite $\Omega$:
$$
p(\omega) = \frac{1}{|\Omega|}, P(A) = \frac{|A|}{|\Omega|}
$$

# 04 Common discrete functions

## 4.1 Bernoulli distribution
$$
\Omega = \{0, 1\}, P(1) = q, P(0) = 1 - q
$$

## 4.2 Binomial distribution
$$
P(X = k) = \binom{n}{k}q^k(1-q)^{n-k}, k = 0, \dots, n
$$

## 4.3 Geometric distribution
$$
P(X = k) = q(1 - q)^{k - 1}, k = 1, 2, \dots
$$

## 4.4 Poisson distribution
$$
P(X = k) = \frac{\lambda^k}{k!}e^{-\lambda}, k = 0, 1, 2, \dots
$$

# 05 Conditional probability & Independence

## 5.1 Conditional probability
$$
P(A | B) = \frac{P(A \cap B)}{P(B)}, P(B) > 0
$$

## 5.2 Law of Total probability
$$
If B_1, \dots , B_n partition \Omega: \\
P(A) = \sum_{i=1}^{n}{P(A | B_i)P(B_i)}
$$

## 5.3 Bayes' Theorem
$$
P(B_j | A) = \frac{P(A | B_j)P(B_j)}{\sum_{i=1}^{n}{P(A | B_i)P(B_i)}}
$$

## 5.4 Independence
Events $A$ and $B$ are independent if
$$
P(A \cap B) = P(A)P(B)
$$