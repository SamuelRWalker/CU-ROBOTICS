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
    mask = cv.threshold(lab(img)[:,:,1],127,255,cv.THRESH_BINARY+cv.THRESH_OTSU)[1]
    #CONTROL
    cv.imshow('Mask Result',applyMask(img,readFile("RawData/background/Background1.jpg",700),mask))
    ######## 
    return cleanEdges(mask)
    
    

def applyMask(img,background,mask):
    return background - cv.bitwise_and(background,background,mask=mask) + cv.bitwise_and(img,img,mask=mask)

####################
# HELPER FUNCTIONS #
####################
def readFile(filePath,size):
    img = cv.imread(filePath)
    return resize(img,size,size)

def cleanEdges(mask):
    sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    result = cv.filter2D(erode(mask-edges(mask)), -1, sharpen_kernel)
    return cv.filter2D(erode(result-edges(result)), -1, sharpen_kernel)
    
########
# MAIN #
########
def main():
    imageSize = 700
    image = readFile("RawData/images/Image5.jpg",imageSize)
    background = readFile("RawData/background/Background1.jpg",imageSize)

    imgMask = mask(image)
    maskResult = applyMask(image,background,imgMask)
    # blurredMaskResult = bilateralBlur(maskResult,21,30)
    cv.imshow('Mask Result extra',maskResult)
    # cv.imshow('Blur Result',blurredMaskResult)
    # cv.imshow('Sharpened Blur Result', gaussianBlur(sharpenBlurResult,1))
    # cv.imshow('Sharpened Blur Result',sharpenBlurResult)

    cv.waitKey(0)

if __name__ == "__main__":
    main()