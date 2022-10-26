from turtle import width
import globalVars as gv
import imageManipulation as im
import masking as mask
import labelGenerator as ig
import cv2 as cv
import random

#################
# Generate Data #
#################
def generateData(img,background,numRun):
    imageSize = gv.IMAGE_SIZE
    # Generate Data
    finalRunAmount = 10
    exampleRunAmount = 10
    for i in range(finalRunAmount):
        # Random Vars
        scaleFactor = 4
        randx = randomNumber(-imageSize/scaleFactor,imageSize/scaleFactor)
        randy = randomNumber(-imageSize/scaleFactor,imageSize/scaleFactor)
        randrot = randomNumber(0,360)
        randhorzblur = randomNumber(5,50)
        randvertblur = randomNumber(5, 25)
        randscale = randomNumber(15,100)/100

        rescaledMask = im.rescale(mask.mask(img),randscale,True)
        rescaledImage = im.rescale(img,randscale,False)
        result = mask.applyMask(modifyImage(rescaledImage,randx,randy,randrot),background,modifyImage(rescaledMask,randx,randy,randrot))
        # Output Data
        saveImage(gv.OUTPUT_BLURRY,"blurry" + str((i+1)*numRun),im.motionBlur(result,randhorzblur,randvertblur))
        saveImage(gv.OUTPUT_SHARP,"sharp" + str((i+1)*numRun),result)
        ig.saveXML(gv.OUTPUT_BLURRY,"blurry" + str((i+1)*numRun))
        ig.saveXML(gv.OUTPUT_BLURRY,"sharp" + str((i+1)*numRun))
        # Example Output Data
        if(i<exampleRunAmount):
            saveImage(gv.EXAMPLE_OUTPUT_BLURRY,"blurry" + str((i+1)*numRun),im.motionBlur(result,randhorzblur,randvertblur))
            saveImage(gv.EXAMPLE_OUTPUT_SHARP,"sharp" + str((i+1)*numRun),result)
            ig.saveXML(gv.EXAMPLE_OUTPUT_BLURRY,"blurry" + str((i+1)*numRun))
            ig.saveXML(gv.EXAMPLE_OUTPUT_SHARP,"sharp" + str((i+1)*numRun))
    return

def randomNumber(low,high):
    return random.randint(low,high)

def modifyImage(img,randx,randy,randrot):
    translated = im.translate(img,randx,randy)
    rotated = im.rotate(translated,randrot)
    return rotated

def saveImage(outputFolderName,outputFileName,img):
    cv.imwrite(outputFolderName + outputFileName + gv.FILE_TYPE,img)
    return