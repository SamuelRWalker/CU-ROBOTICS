from cmath import pi
import cv2 as cv
import numpy as np
import globalVars as gv
import random

######################
# IMAGE MANIPULATION #
######################

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

###################
# MOTION BLURRING #
###################
def horizontalMotionBlur(img,blurStrength=5):
    effect = np.zeros((blurStrength,blurStrength))
    effect[1,:] = np.ones(blurStrength)
    effect = effect/blurStrength
    return cv.filter2D(img,-1,effect)

def verticalMotionBlur(img,blurStrength=5):
    effect = np.zeros((blurStrength,blurStrength))
    effect[:,1] = np.ones(blurStrength)
    effect = effect/blurStrength
    return cv.filter2D(img,-1,effect)

def motionBlur(img,horzBlurStrength=5,vertBlurStrength=5):
    if(random.randint(0,1)==1): vertBlurStrength = -vertBlurStrength
    totalBlurStrength = round(np.power(np.power(horzBlurStrength,2) + np.power(vertBlurStrength,2),1/2))
    angle = 90 - (np.arctan(horzBlurStrength/vertBlurStrength)*180)/pi
    effect = np.zeros((totalBlurStrength,totalBlurStrength))
    effect[(totalBlurStrength-1)// 2 , :] = np.ones(totalBlurStrength, dtype=np.float32)
    effect = cv.warpAffine(effect, cv.getRotationMatrix2D((totalBlurStrength / 2 -0.5 , totalBlurStrength / 2 -0.5 ) , angle, 1.0), (totalBlurStrength, totalBlurStrength) )
    effect = effect/totalBlurStrength
    return cv.filter2D(img,-1,effect)


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
def resize(img,size):
    return cv.resize(img,(size,size))

def crop(img,size):
    return img[0:size,0:size]

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

def rescale(img,scaleFactor,mask):
    imageSize = gv.IMAGE_SIZE
    if(mask): 
        background = np.zeros((imageSize, imageSize), dtype="uint8")
        scaleFactor = scaleFactor*.95
    else: background = np.zeros((imageSize, imageSize,3), dtype="uint8")
    foreground = resize(img,round(scaleFactor*imageSize))
    foreground_height = foreground.shape[0]
    foreground_width = foreground.shape[1]
    blended_portion = cv.addWeighted(foreground,1,background[:foreground_height,:foreground_width],0,0,background)
    background[:foreground_height,:foreground_width] = blended_portion
    translated = translate(background,(imageSize-foreground_width)/2,(imageSize-foreground_width)/2)
    return translated