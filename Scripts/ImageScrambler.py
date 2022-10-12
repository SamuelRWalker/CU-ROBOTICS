import cv2 as cv
import numpy as np
import random
import shutil
import os

########
# TODO #
########
#-Research Image Distortion from cameras and how to implement (openCV)
#-Research Motion Blur and how to implement (OpenCV)
#-Rescale while maintaining aspect ratio (using zeroes and cv.bitwiseAnd)

###############
# DESCRIPTION #
###############
# Author: Sam Walker
# Date: 10/11/2022
# Purpose: Created a dataset for computer vision AI
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
    # Random Vars
    scaleFactor = 4
    randx = randomNumber(-IMAGE_SIZE/scaleFactor,IMAGE_SIZE/scaleFactor)
    randy = randomNumber(-IMAGE_SIZE/scaleFactor,IMAGE_SIZE/scaleFactor)
    randrot = randomNumber(0,360)
    randblur = randomNumber(5,100)

    # Create Output Folders
    os.mkdir(OUTPUT_ROOT)
    os.mkdir(OUTPUT_BLURRY)
    os.mkdir(OUTPUT_SHARP)
    os.mkdir(EXAMPLE_OUTPUT_ROOT)
    os.mkdir(EXAMPLE_OUTPUT_BLURRY)
    os.mkdir(EXAMPLE_OUTPUT_SHARP)

    # Generate Data
    finalRunAmount = 5
    exampleRunAmount = 3
    for i in range(finalRunAmount):
        transrotated = applyMask(rotate(translate(img,randx,randy),randrot),background,rotate(translate(mask(img),randx,randy),randrot))
        # Output Data
        saveImage(OUTPUT_BLURRY,"blurry" + str((i+1)*numRun),transrotated)
        saveImage(OUTPUT_SHARP,"sharp" + str((i+1)*numRun),gaussianBlur(transrotated,randblur))
        # Example Output Data
        if(i<exampleRunAmount):
            saveImage(EXAMPLE_OUTPUT_BLURRY,"blurry" + str((i+1)*numRun),transrotated)
            saveImage(EXAMPLE_OUTPUT_SHARP,"sharp" + str((i+1)*numRun),gaussianBlur(transrotated,randblur))
    return

########
# MAIN #
########
def main():
    images = importFiles(IMAGE_ROOT,IMAGE_BASE,FILE_TYPE,NUM_IMAGES)
    backgrounds = importFiles(BACKGROUND_ROOT,BACKGROUND_BASE,FILE_TYPE,NUM_BACKGROUNDS)

    shutil.rmtree(EXAMPLE_OUTPUT_ROOT)

    # Final Case
    # numRun = 0
    # for i in range(NUM_IMAGES):
    #     for j in range(NUM_BACKGROUNDS):
    #         numRun+=1
    #         image = readFile(images[i],IMAGE_SIZE)
    #         background = readFile(backgrounds[j],IMAGE_SIZE)
    #         generateData(image,background,numRun)

    # Test Case
    numRun = 1 
    image = readFile(images[3],IMAGE_SIZE)
    background = readFile(backgrounds[5],IMAGE_SIZE)
    generateData(image,background,numRun)    

    shutil.make_archive(OUTPUT_ROOT, format="zip", root_dir=OUTPUT_ROOT)
    shutil.rmtree(OUTPUT_ROOT)

if __name__ == "__main__":
    main()