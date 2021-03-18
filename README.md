# Implementation of Some ML Algorithms 
Implementation of the algorithms in the book *Statistical Learning Methods*  

《统计学习方法》python实现

Use the MNIST dataset to validate the algorithms.

>  This repository is still in the process of updating.

----

### Already Implemented:

* [Perceptron](https://github.com/RockeyCoss/machineLearningImplementation/blob/main/models/Perceptron.py)

* [Naive Bayesian](https://github.com/RockeyCoss/machineLearningImplementation/blob/main/models/NaiveBayesian.py)

* [KNN](https://github.com/RockeyCoss/machineLearningImplementation/blob/main/models/KNN.py)

  > kd-tree is used to implement KNN

* [Logistic](https://github.com/RockeyCoss/machineLearningImplementation/blob/main/models/Logistic.py)

  > 1. Use either SGD or quasi-Newton to optimize the target function.
  >
  > 2. When using quasi-Newton, some numerical problems may be encountered. This bug has not been fixed yet. （以后再说吧呜呜呜）

* [Maximum Entropy](https://github.com/RockeyCoss/machineLearningImplementation/blob/main/models/MaximumEntropy.py)

  > 1. Use quasi-Newton to optimize the target function.
  >
  > 2. The derivative of the likelihood function is different from that written in *Statistical Learning Methods* . For MNIST dataset, the derivative is:
  >
  > <img src="https://github.com/RockeyCoss/machineLearningImplementation/blob/main/README.assets/derivative.png" alt="derivative" style="zoom:40%;" />

* [SVM](https://github.com/RockeyCoss/MachineLearningAlgos/blob/main/models/SVM.py)

  > 1. Refer to paper  *Sequential Minimal Optimization:A Fast Algorithm for Training Support Vector Machines*
  > 2. Store the whole kernel function matrix in the memory. To save memory, I may use a LRU cache to store the kernel function matrix in the future. 
  > 3. Since computing w\*x is time consuming, I store the value of w\*x  of every sample in the memory(as a list) . When updating this list, instead of computing w\*x, I use linear approximation as follows:
  >
  > <img src="https://github.com/RockeyCoss/MachineLearningAlgos/blob/main/README.assets/wxupdate.png" alt="derivative" style="zoom:20%;" />
  >
  > Then, the computation of w\*x can be completely avoided.
  >
  > 

  

