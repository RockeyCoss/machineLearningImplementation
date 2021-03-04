import numpy as np
import cv2

#feature transforms
def hogFeature(data):
    #extract hog features
    hog=cv2.HOGDescriptor('../config/hogConfig.xml')

    features=[]
    for img in data:
        img=np.reshape(img,(28,28)).astype(np.uint8)
        hog_feature=hog.compute(img)
        features.append(hog_feature)

    features=np.array(features)
    features=features.reshape(features.shape[0:2])
    return features

def binaryFeature(data):
    data[np.where(data<=127.5)]=0
    data[np.where(data>127.5)]=1
    return data


#label transforms
def perceptronLabelTransform(labels):
    labels[np.where(labels != 1)] = -1
    return labels

