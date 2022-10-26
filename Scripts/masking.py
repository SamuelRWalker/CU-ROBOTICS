import cv2 as cv
import numpy as np
import imageManipulation as im

###########
# MASKING #
###########
def mask(img):
    mask = cv.threshold(im.lab(img)[:,:,1],127,255,cv.THRESH_BINARY+cv.THRESH_OTSU)[1]
    return cleanEdges(mask)
    
def applyMask(img,background,mask):
    return background - cv.bitwise_and(background,background,mask=mask) + cv.bitwise_and(img,img,mask=mask)

def cleanEdges(mask):
    sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    result = cv.filter2D(im.erode(mask-im.edges(mask)), -1, sharpen_kernel)
    return cv.filter2D(im.erode(result-im.edges(result)), -1, sharpen_kernel)