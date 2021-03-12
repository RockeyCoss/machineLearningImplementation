import os
from collections import deque
import collections

import numpy as np
from models import ModelBaseClass
import heapq as hq
from utilities import loadConfigWithName


class KNN(ModelBaseClass):
    def __init__(self):
        self.tree=kdTree()
        self.k=int(loadConfigWithName("KNNConfig", "k"))

    def train(self, features: np.array, labels: np.array, *args, **dicts):
        newFeature=np.insert(features,features.shape[1],labels,axis=1)
        self.tree.createKdTree(newFeature)

    def predict(self, features: np.array):
        if self.tree.root==None:
            newFeature=self.loadPara()
            self.tree.createKdTree(newFeature)
        result=[]
        for feature in features:
            nearestPoints=self.tree.search(feature,self.k)
            labels=np.nearestPoints[:,nearestPoints.shape[1]-1]
            label=collections.Counter(labels).most_common(1)
            result.append(label)
        return np.array(result)

    def save(self, para):
        if not os.path.exists(f"../parameters"):
            os.mkdir("../parameters")
        np.save(f"../parameters/{self.__class__.__name__}Para.npy",para)

    def loadPara(self):
        return np.load(f"../parameters/{self.__class__.__name__}Para.npy")


# -----------------------UTILITIES-----------------------#

class DisPPair:
    def __init__(self, dis: float, point: np.ndarray):
        self.pair = (dis, point)

    @property
    def dis(self):
        return self.pair[0]

    @property
    def point(self):
        return self.pair[1]
    # compare
    def __eq__(self, other):
        if self.pair[0] == other.pair[0]:
            return True
        else:
            return False

    def __ne__(self, other):
        if self.pair[0] != other.pair[0]:
            return True
        else:
            return False

    def __lt__(self, other):
        if self.pair[0] < other.pair[0]:
            return True
        else:
            return False

    def __gt__(self, other):
        if self.pair[0] > other.pair[0]:
            return True
        else:
            return False

    def __le__(self, other):
        if self.pair[0] <= other.pair[0]:
            return True
        else:
            return False

    def __ge__(self, other):
        if self.pair[0] >= other.pair[0]:
            return True
        else:
            return False

    # computation
    def __neg__(self):
        newPair = DisPPair(-self.pair[0], self.pair[1].copy())
        return newPair


class maxHeapWithLength:
    def __init__(self, length):
        self.heap = []
        self.length = length

    def push(self, element: DisPPair) -> bool:
        """
        The return value indicates whether the heap is updated
        """
        if len(self.heap) < self.length:
            hq.heappush(self.heap, -element)
            return True
        else:
            if -self.heap[0] <= element:
                return False
            else:
                hq.heappop(self.heap)
                hq.heappush(self.heap, -element)
                return True

    def pop(self) -> DisPPair:
        return -hq.heappop(self.heap)

    def isEmpty(self) -> bool:
        return True if len(self.heap) == 0 else False

    def isFull(self) -> bool:
        return True if len(self.heap) == self.length else False

    def peek(self) -> DisPPair:
        if self.isEmpty():
            raise Exception("The heap is empty")
        else:
            return -self.heap[0]

    def extractPoints(self)->np.ndarray:
        pointList=[pair.point.reshape(1,-1) for pair in self.heap]
        return np.concatenate(pointList,axis=0)

    def __len__(self):
        return len(self.heap)

class Stack(deque):
    def push(self,element):
        super(Stack,self).append(element)

    @property
    def isEmpty(self):
        return not bool(self)

class Node:
    def __init__(self, points: np.ndarray = None, father=None, lChild=None, rChild=None, axis: int = None):
        self.points: np.ndarray = points
        self.father: Node = father
        self.lChild: Node = lChild
        self.rChild: Node = rChild
        self.axis: int = axis


class kdTree:
    def __init__(self, root=None):
        self.root = root

    def __medianSplit(self, features: np.ndarray, axis: int):
        if features.shape[0] == 1:
            return None, features, None
        sortedData = np.array(sorted(features, key=lambda x: x[axis]))
        medianIndex = sortedData.shape[0] // 2
        leftSame, rightSame = True
        leftStep = 1
        rightStep = 1
        medianValue = sortedData[medianIndex, axis]

        while leftSame or rightSame:
            if medianIndex - leftStep < 0 or sortedData[medianIndex - leftStep, axis] < medianValue:
                leftSame = False
            else:
                leftStep += 1

            if medianIndex + rightStep >= sortedData.shape[0] or sortedData[
                medianIndex + rightStep, axis] > medianValue:
                rightSame = False
            else:
                rightStep += 1

        leftData = sortedData[:medianIndex - leftStep + 1]
        medianData = sortedData[medianIndex - leftStep + 1:medianIndex + rightStep]
        rightData = sortedData[medianIndex + rightStep:]

        if leftData.shape[0] == 0:
            leftData = None
        if rightData.shape[0] == 0:
            rightData = None

        return leftData, medianData, rightData

    def createKdTree(self, features: np.ndarray):
        """
        Attention:The features here is actually [feature,label]
        """
        self.root = Node()
        assert type(features) == np.ndarray and len(features.shape) == 2
        self.__createChild(features, self.root, 0)

    def __createChild(self, features: np.ndarray, currentNode: Node, depth: int):
        axis = depth % (features.shape[1] - 1)
        currentNode.axis = axis
        leftData, medianData, rightData = self.__medianSplit(features, axis=axis)
        assert len(medianData.shape) == 2
        currentNode.points = medianData
        if leftData == None:
            currentNode.lChild = None
        else:
            currentNode.lChild = Node(father=currentNode)
            self.__createChild(leftData, currentNode.lChild, depth + 1)

        if rightData == None:
            currentNode.rChild = None
        else:
            currentNode.rChild = Node(father=currentNode)
            self.__createChild(rightData, currentNode.rChild, depth + 1)

        return

    def __calDis(self, currentPoint: np.ndarray, point: np.ndarray) -> float:
        """
        :param currentPoint: point with label in its last column
        :param point:
        :return: Euclidean distance
        """
        return np.linalg.norm(currentPoint[:currentPoint.shape[0] - 1] - point)

    def search(self, point: np.ndarray, k: int) -> np.ndarray:
        if self.root == None:
            return np.array([])

        pointHeap = maxHeapWithLength(k)
        stack=Stack()
        currentNode =self.__searchAlongTheTree(self.root,point,pointHeap,stack)
        logNode=None
        # kd树是平衡树，不确定当一个节点只有左子节点/右子节点的时候还要不要搜索下去
        # 这里选择无视判断去叶节点。反正是平衡树顶多深了一层
        while not stack.isEmpty:
            toSearch=False
            fatherNode=stack.pop()
            if fatherNode==self.root:
                logNode=currentNode
            fatherNodeAxis = fatherNode.axis
            for aPoint in fatherNode.points:
                newPair = DisPPair(self.__calDis(aPoint, point), aPoint)
                pointHeap.push(newPair)
            disWithSuperRectangle = np.abs(fatherNode.points[0, fatherNodeAxis] - point[fatherNodeAxis])
            # circle intersect with rectangle
            if pointHeap.peek().dis > disWithSuperRectangle:
                if fatherNode.lChild == currentNode:
                    nextNode = fatherNode.rChild
                else:
                    nextNode = fatherNode.lChild
                currentNode=nextNode
                toSearch=True
            #如果要退出搜索了heap还没满，则去root的另一子树
            elif currentNode==self.root and not pointHeap.isFull():
                if logNode==self.root.lChild:
                    nextNode=self.root.rChild
                else:
                    nextNode=self.root.lChild
                currentNode=nextNode
                toSearch=True
            else:
                currentNode=fatherNode
            if toSearch:
                currentNode=self.__searchAlongTheTree(currentNode,point,pointHeap,stack)

        return pointHeap.extractPoints()


    def __searchAlongTheTree(self, currentNode: Node, point: np.ndarray, pointHeap: maxHeapWithLength,stack:Stack)->Node:
        if currentNode==None:
            return None
        stack.push(currentNode)
        while True:
            judgeValue = currentNode.points[0, currentNode.axis]
            if point[currentNode.axis] < judgeValue:
                if currentNode.lChild == None:
                    if currentNode.rChild != None:
                        currentNode = currentNode.rChild
                    else:
                        break
                else:
                    currentNode = currentNode.lChild

            else:
                if currentNode.rChild == None:
                    if currentNode.lChild != None:
                        currentNode = currentNode.lChild
                    else:
                        break
                else:
                    currentNode = currentNode.rChild
            stack.push(currentNode)
        for currentPoint in currentNode.points:
            newPair = DisPPair(self.__calDis(currentPoint, point), currentPoint)
            pointHeap.push(newPair)
        return stack.pop()