from turtle import width
import globalVars as gv
import imageManipulation as im
import masking as mask
import labelGenerator as ig
from skimage.measure import label, regionprops, find_contours
import progressBar as pb
import numpy as np
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
    numTotal = (finalRunAmount+exampleRunAmount)*gv.NUM_IMAGES*gv.NUM_BACKGROUNDS
    if(gv.DEBUGGING): numTotal=exampleRunAmount
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
        modifiedMask = modifyImage(rescaledMask,randx,randy,randrot)
        bboxes = mask_to_bbox(modifiedMask)
        result = mask.applyMask(modifyImage(rescaledImage,randx,randy,randrot),background,modifiedMask)

        xmlParams = {'folder':'placeholder','filename':str((i+1)*numRun),'path':'placeholder','width':str(gv.IMAGE_SIZE),'height':str(gv.IMAGE_SIZE),'color':'red','xmin':str(bboxes[0][0]),'ymin':str(bboxes[0][1]),'xmax':str(bboxes[0][2]),'ymax':str(bboxes[0][3])}
        # Output Data
        saveData(gv.OUTPUT_BLURRY,(i+1)*numRun,im.motionBlur(result,randhorzblur,randvertblur),xmlParams)
        saveData(gv.OUTPUT_SHARP,(i+1)*numRun,result,xmlParams)
        # Example Output Data
        if(i<exampleRunAmount):
            saveData(gv.EXAMPLE_OUTPUT_BLURRY,(i+1)*numRun,im.motionBlur(result,randhorzblur,randvertblur),xmlParams)
            saveData(gv.EXAMPLE_OUTPUT_SHARP,(i+1)*numRun,result,xmlParams)
        currNum = (i+1)*numRun*4
        pb.printProgressBar(currNum,numTotal*4, 'Saving Data: (' + str(currNum) + '/' + str(numTotal*4) + ') ')
    return

def randomNumber(low,high):
    return random.randint(low,high)

def modifyImage(img,randx,randy,randrot):
    translated = im.translate(img,randx,randy)
    rotated = im.rotate(translated,randrot)
    return rotated

def saveData(outputFolderName,numRun,img, xmlParams):
    xmlParams['folder'] = outputFolderName.split('/')[1]
    xmlParams['path'] = outputFolderName + str(numRun)
    cv.imwrite(outputFolderName + str(numRun) + gv.FILE_TYPE,img)
    ig.saveXML(outputFolderName,str(numRun) ,xmlParams)
    return

def mask_to_border(mask):
    h, w = mask.shape
    border = np.zeros((h, w))
    contours = find_contours(mask, 128)
    for contour in contours:
        for c in contour:
            x = int(c[0])
            y = int(c[1])
            border[x][y] = 255

    return border

def mask_to_bbox(mask):
    bboxes = []
    mask = mask_to_border(mask)
    lbl = label(mask)
    props = regionprops(lbl)
    for prop in props:
        x1 = prop.bbox[1]
        y1 = prop.bbox[0]
        x2 = prop.bbox[3]
        y2 = prop.bbox[2]
        bboxes.append([x1, y1, x2, y2])
    return bboxes