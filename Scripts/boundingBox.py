from asyncio.windows_events import NULL
import imagesize
import main
import globalVars as gv
import cv2 as cv
import imageManipulation as im
import masking
from skimage.measure import label, regionprops, find_contours
import numpy as np


# # This function allows us to create a descending sorted list of contour areas.
# def contour_area(contours):
     
#     # create an empty list
#     cnt_area = []
     
#     # loop through all the contours
#     for i in range(0,len(contours),1):
#         # for each contour, use OpenCV to calculate the area of the contour
#         cnt_area.append(cv.contourArea(contours[i]))
 
#     # Sort our list of contour areas in descending order
#     list.sort(cnt_area, reverse=True)
#     return cnt_area

# def draw_bounding_box(contours, image, number_of_boxes=1):
#     # Call our function to get the list of contour areas
#     cnt_area = contour_area(contours)
 
#     # Loop through each contour of our image
#     for i in range(0,len(contours),1):
#         cnt = contours[i]
 
#         # Only draw the the largest number of boxes
#         if (cv.contourArea(cnt) > cnt_area[number_of_boxes]):
             
#             # Use OpenCV boundingRect function to get the details of the contour
#             x,y,w,h = cv.boundingRect(cnt)
             
#             # Draw the bounding box
#             image=cv.rectangle(image,(x,y),(x+w,y+h),(0,0,255),2)
 
#     return image

""" Convert a mask to border image """
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

""" Mask to bounding boxes """
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

imageSize = 256

img = main.readFile("RawData/images/Image1.jpg",imageSize)
cv.imshow('Green Screen Armor Plate',img)
mask = masking.mask(img)
cv.imshow('Masked Armor Plate',mask)

bboxes = mask_to_bbox(mask)
for bbox in bboxes:
    maskWithBox = cv.rectangle(mask, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (255, 0, 0), 2)
cv.imshow('Mask With Bounding Box',maskWithBox)

cv.waitKey(0)