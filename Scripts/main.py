import cv2 as cv
import globalVars as gv
import dataGenerator as dg
import imageManipulation as im
import shutil
import os

########
# TODO #
########
#-Research Image Distortion from cameras and how to implement (openCV)
#-Make console output to watch it make files
#-Create multiple armor plates on one image
#-Get more source data (Different Colored Armor Plates)
#-Create a GUI for selecting amount of files

###############
# DESCRIPTION #
###############
# Author: Sam Walker
# Creation Date: 9/27/2022
# Date: 10/25/2022
# Purpose: Create a dataset for computer vision AI for CU ROBOTICS
# Description: Given green screened images output random dirty images with backgrounds

########
# MAIN #
########
def main():
    images = importFiles(gv.IMAGE_ROOT,gv.IMAGE_BASE,gv.FILE_TYPE,gv.NUM_IMAGES)
    backgrounds = importFiles(gv.BACKGROUND_ROOT,gv.BACKGROUND_BASE,gv.FILE_TYPE,gv.NUM_BACKGROUNDS)

    if(os.path.exists(gv.EXAMPLE_OUTPUT_ROOT)):
        shutil.rmtree(gv.EXAMPLE_OUTPUT_ROOT)

    # Create Output Folders
    if(not os.path.exists(gv.OUTPUT_ROOT)):
        os.mkdir(gv.OUTPUT_ROOT)
        os.mkdir(gv.OUTPUT_BLURRY)
        os.mkdir(gv.OUTPUT_SHARP)
    os.mkdir(gv.EXAMPLE_OUTPUT_ROOT)
    os.mkdir(gv.EXAMPLE_OUTPUT_BLURRY)
    os.mkdir(gv.EXAMPLE_OUTPUT_SHARP)

    # Final Case
    # numRun = 0
    # for i in range(gv.NUM_IMAGES):
    #     for j in range(gv.NUM_BACKGROUNDS):
    #         numRun+=1
    #         image = readFile(images[i],gv.IMAGE_SIZE)
    #         background = readFile(backgrounds[j],gv.IMAGE_SIZE)
    #         generateData(image,background,numRun)

    # Test Case - TEMP
    numRun = 1 
    image = readFile(images[6],gv.IMAGE_SIZE)
    background = readFile(backgrounds[1],gv.IMAGE_SIZE)
    dg.generateData(image,background,numRun)    

    shutil.make_archive(gv.OUTPUT_ROOT, format="zip", root_dir=gv.OUTPUT_ROOT)
    shutil.rmtree(gv.OUTPUT_ROOT)

####################
# HELPER FUNCTIONS #
####################
def readFile(filePath,size):
    img = cv.imread(filePath)
    return im.resize(img,size)

def importFiles(root,base,fileType,numImages):
    arr = []
    for i in range(numImages):
        arr.append(root + base + str(i+1) + fileType)
    return arr

if __name__ == "__main__":
    main()