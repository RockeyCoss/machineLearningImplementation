import numpy as np
import json
import sklearn
from models import ModelBaseClass
# refer to Statistical Learning Methods and
# paper Sequential Minimal Optimization:A Fast Algorithm for Training Support Vector Machines

class SVM(ModelBaseClass):
    def __init__(self):
        self.rbfGamma:float = 0
        self.sampleNum:int = 0
        self.C:float = 1
        self.epsilon:float = 1e-3
        self.alhpa:np.ndarray=None
        self.features=None

    def rbf(self, x1, x2):
        """
        以sklearn “auto” 方式确定gamma
        """
        return np.exp(-np.sum(np.power((x1 - x2), 2)) / self.rbfGamma)

    def getKernelMatrix(self, features: np.ndarray, kernel) -> np.ndarray:
        """
        计算K(xi,xj)矩阵
        :param features: 测试样例
        :param kernel: 核函数
        :return: K(xi,xj)矩阵。考虑到训练集中样例较少，因此matrix暂不用cache方式而是整体储存
        """
        kernelMatrix = np.zeros((self.sampleNum, self.sampleNum))
        for i in range(self.sampleNum):
            for j in range(i + 1):
                kernelMatrix[i, j] = kernelMatrix[j, i] = kernel(features[i], features[j])
        return kernelMatrix

    def train(self, features: np.ndarray, labels: np.ndarray, *args, **dicts):
        self.rbfGamma = features.shape[1] if features.shape[1] > 0 else 1
        self.sampleNum = features.shape[0]
        self.C = dicts['C'] if 'C' in dicts.keys() else 1
        self.alhpa=np.zeros(self.sampleNum)
        self.features=features

    def predict(self, features: np.array):
        super().predict(features)

        sklearn.svm()

    def loadPara(self):
        super().loadPara()

    def __trainer(self):
        examineAll:bool=True
        changedNum=0
        while changedNum>0 or examineAll==True:
            changedNum=0
            if examineAll:

