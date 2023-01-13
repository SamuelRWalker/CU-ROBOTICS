from cmath import pi
import cv2 as cv
import numpy as np
import random
import shutil
import os

########
# TODO #
########
#-Research Image Distortion from cameras and how to implement (openCV)
#-Make console output to watch it make files
#-Data labels for each image
#-Improve upon the readme

###############
# DESCRIPTION #
###############
# Author: Sam Walker
# Creation Date: 9/27/2022
# Date: 10/19/2022
# Purpose: Create a dataset for computer vision AI for CU ROBOTICS
# Description: Given green screened images output random dirty images with backgrounds

####################
# GLOBAL VARIABLES #
####################
# OUTPUT
OUTPUT_ROOT = "OutputData/"
OUTPUT_BLURRY = OUTPUT_ROOT + "Blurry/"
OUTPUT_SHARP = OUTPUT_ROOT + "Sharp/"

EXAMPLE_OUTPUT_ROOT = "ExampleOutputData/"
EXAMPLE_OUTPUT_BLURRY = EXAMPLE_OUTPUT_ROOT + "Blurry/"
EXAMPLE_OUTPUT_SHARP = EXAMPLE_OUTPUT_ROOT + "Sharp/"

# INPUT
DATA_ROOT = "RawData/"
IMAGE_ROOT = DATA_ROOT + "images/"
BACKGROUND_ROOT = DATA_ROOT + "background/"
IMAGE_BASE = "Image"
BACKGROUND_BASE = "Background"
FILE_TYPE = ".jpg"

# CONST GLOBALS
IMAGE_SIZE = 700
NUM_IMAGES = 10
NUM_BACKGROUNDS= 28

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
    if(randomNumber(0,1)==1): vertBlurStrength = -vertBlurStrength
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
    if(mask): 
        background = np.zeros((IMAGE_SIZE, IMAGE_SIZE), dtype="uint8")
        scaleFactor = scaleFactor*.95
    else: background = np.zeros((IMAGE_SIZE, IMAGE_SIZE,3), dtype="uint8")
    foreground = resize(img,round(scaleFactor*IMAGE_SIZE))
    foreground_height = foreground.shape[0]
    foreground_width = foreground.shape[1]
    blended_portion = cv.addWeighted(foreground,1,background[:foreground_height,:foreground_width],0,0,background)
    background[:foreground_height,:foreground_width] = blended_portion
    translated = translate(background,(IMAGE_SIZE-foreground_width)/2,(IMAGE_SIZE-foreground_width)/2)
    return translated

##########################
# MASKS FOR GREEN SCREEN #
##########################
def mask(img):
    mask = cv.threshold(lab(img)[:,:,1],127,255,cv.THRESH_BINARY+cv.THRESH_OTSU)[1]
    return cleanEdges(mask)
    
def applyMask(img,background,mask):
    return background - cv.bitwise_and(background,background,mask=mask) + cv.bitwise_and(img,img,mask=mask)

####################
# HELPER FUNCTIONS #
####################
def readFile(filePath,size):
    img = cv.imread(filePath)
    return resize(img,size)

def cleanEdges(mask):
    sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    result = cv.filter2D(erode(mask-edges(mask)), -1, sharpen_kernel)
    return cv.filter2D(erode(result-edges(result)), -1, sharpen_kernel)

def importFiles(root,base,fileType,numImages):
    arr = []
    for i in range(numImages):
        arr.append(root + base + str(i+1) + fileType)
    return arr

def saveImage(outputFolderName,outputFileName,img):
    cv.imwrite(outputFolderName + outputFileName + FILE_TYPE,img)
    return

def randomNumber(low,high):
    return random.randint(low,high)

#################
# Generate Data #
#################
def generateData(img,background,numRun):
    # Generate Data
    finalRunAmount = 10
    exampleRunAmount = 10
    for i in range(finalRunAmount):
        # Random Vars
        scaleFactor = 4
        randx = randomNumber(-IMAGE_SIZE/scaleFactor,IMAGE_SIZE/scaleFactor)
        randy = randomNumber(-IMAGE_SIZE/scaleFactor,IMAGE_SIZE/scaleFactor)
        randrot = randomNumber(0,360)
        randhorzblur = randomNumber(5,50)
        randvertblur = randomNumber(5, 25)
        randscale = randomNumber(15,100)/100

        rescaledMask = rescale(mask(img),randscale,True)
        rescaledImage = rescale(img,randscale,False)
        result = applyMask(modifyImage(rescaledImage,randx,randy,randrot),background,modifyImage(rescaledMask,randx,randy,randrot))
        # Output Data
        saveImage(OUTPUT_BLURRY,"blurry" + str((i+1)*numRun),motionBlur(result,randhorzblur,randvertblur))
        saveImage(OUTPUT_SHARP,"sharp" + str((i+1)*numRun),result)
        # Example Output Data
        if(i<exampleRunAmount):
            saveImage(EXAMPLE_OUTPUT_BLURRY,"blurry" + str((i+1)*numRun),motionBlur(result,randhorzblur,randvertblur))
            saveImage(EXAMPLE_OUTPUT_SHARP,"sharp" + str((i+1)*numRun),result)
    return

def modifyImage(img,randx,randy,randrot):
    translated = translate(img,randx,randy)
    rotated = rotate(translated,randrot)
    return rotated

########
# MAIN #
########
def main():
    images = importFiles(IMAGE_ROOT,IMAGE_BASE,FILE_TYPE,NUM_IMAGES)
    backgrounds = importFiles(BACKGROUND_ROOT,BACKGROUND_BASE,FILE_TYPE,NUM_BACKGROUNDS)

    if(os.path.exists(EXAMPLE_OUTPUT_ROOT)):
        shutil.rmtree(EXAMPLE_OUTPUT_ROOT)

    # Create Output Folders
    if(not os.path.exists(OUTPUT_ROOT)):
        os.mkdir(OUTPUT_ROOT)
        os.mkdir(OUTPUT_BLURRY)
        os.mkdir(OUTPUT_SHARP)
    os.mkdir(EXAMPLE_OUTPUT_ROOT)
    os.mkdir(EXAMPLE_OUTPUT_BLURRY)
    os.mkdir(EXAMPLE_OUTPUT_SHARP)

    # Final Case
    # numRun = 0
    # for i in range(NUM_IMAGES):
    #     for j in range(NUM_BACKGROUNDS):
    #         numRun+=1
    #         image = readFile(images[i],IMAGE_SIZE)
    #         background = readFile(backgrounds[j],IMAGE_SIZE)
    #         generateData(image,background,numRun)

    # Test Case - TEMP
    numRun = 1 
    image = readFile(images[6],IMAGE_SIZE)
    background = readFile(backgrounds[1],IMAGE_SIZE)
    generateData(image,background,numRun)    

    shutil.make_archive(OUTPUT_ROOT, format="zip", root_dir=OUTPUT_ROOT)
    shutil.rmtree(OUTPUT_ROOT)

if __name__ == "__main__":
    main()