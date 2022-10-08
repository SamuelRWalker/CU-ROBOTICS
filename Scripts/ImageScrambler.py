import cv2 as cv
import numpy as np
import os
import sys
import random
import glob
import shutil

################################
# SIMPLE COLOR TRANSFORMATIONS #
################################
def rgb(img):
    return cv.cvtColor(img,cv.COLOR_BGR2RGB)

def grayscale(img):
    return cv.cvtColor(img,cv.COLOR_BGR2GRAY)

def hsv(img):
    return cv.cvtColor(img,cv.COLOR_BGR2HSV)

def lab(img):
    return cv.cvtColor(img,cv.COLOR_BGR2LAB)

###################
# SIMPLE BLURRING #
###################
def smoothBlur(img,blurStrength=9):
    return cv.medianBlur(img,blurStrength)

def gaussianBlur(img,blurStrength=9):
    if(blurStrength%2==0):
        blurStrength+=1
    return cv.GaussianBlur(img,(blurStrength,blurStrength),cv.BORDER_DEFAULT)
    
def bilateralBlur(img,radius=10,sigma=30):
    return cv.bilateralFilter(img,radius,sigma,sigma)

##################
# EDGE FUNCTIONS #
##################
def edges(img,threshold1=100,threshold2=150):
    return cv.Canny(img,threshold1,threshold2)

def dilate(img,dilationStrength=7,iterations=3):
    return cv.dilate(img,(dilationStrength,dilationStrength),iterations)

def erode(img,erosionStrength=7,iterations=3):
    return cv.erode(img,(erosionStrength,erosionStrength),iterations)

#################################################
# SIMPLE TRANSFORMATIONS/ROTATIONS/TRANSLATIONS #
#################################################
def resize(img,x,y):
    return cv.resize(img,(x,y))

def crop(img,x,y,w,h):
    return img[x:y,w:h]

def translate(img,x,y):
    transMat = np.float32([[1,0,x],[0,1,y]])
    dimensions = (img.shape[1],img.shape[0])
    return cv.warpAffine(img,transMat,dimensions)

def rotate(img,angle,rotPoint=None):
    (height,width) = img.shape[:2]
    if rotPoint is None:
        rotPoint = (width//2,height//2)
    rotMat = cv.getRotationMatrix2D(rotPoint,angle,1.0)
    dimensions = (width,height)
    return cv.warpAffine(img,rotMat,dimensions)

def flip(img,code):
    return cv.flip(img,code)

##########################
# MASKS FOR GREEN SCREEN #
##########################
def mask(img):
    return cv.threshold(lab(img)[:,:,1],127,255,cv.THRESH_BINARY+cv.THRESH_OTSU)[1]

def applyMask(img,background,mask):
    return background - cv.bitwise_and(background,background,mask=mask) + cv.bitwise_and(img,img,mask=mask)

#DEPRECATED - LOL
# def mask(img):
#     aChannel = lab(img)[:,:,1]
#     threshold = cv.threshold(aChannel,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)[1]
#     mask = cv.bitwise_and(img,img,mask=threshold)
#     mlab=lab(mask)
#     dst = cv.normalize(mlab[:,:,1],dst=None,alpha=0,beta=255,norm_type=cv.NORM_MINMAX,dtype=cv.CV_8U)
#     thresholdValue = 100
#     dstThreshold = cv.threshold(dst,thresholdValue,255,cv.THRESH_BINARY_INV)[1]
#     return dstThreshold+threshold

####################
# HELPER FUNCTIONS #
####################
def readFile(filePath,size):
    img = cv.imread(filePath)
    return resize(img,size,size)
    

########
# MAIN #
########
def main():
    imageSize = 500
    image = readFile("RawData/images/Image2.jpg",imageSize)
    background = readFile("RawData/background/Background1.jpg",imageSize)

    imgMask = mask(resize(image,imageSize,imageSize))
    maskResult = applyMask(image,background,imgMask)
    blurredMaskResult = bilateralBlur(maskResult,21,30)
    # sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    # sharpenBlurResult = cv.filter2D(blurredMaskResult, -1, sharpen_kernel)
    cv.imshow('Mask Result',maskResult)
    cv.imshow('Blur Result',blurredMaskResult)
    # cv.imshow('Sharpened Blur Result', gaussianBlur(sharpenBlurResult,1))
    # cv.imshow('Sharpened Blur Result',sharpenBlurResult)

    cv.waitKey(0)

if __name__ == "__main__":
    main()