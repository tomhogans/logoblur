# A simple python script to blur out an object given
# a folder of images and a template file, or, to blur
# everything but the object. Edges of the blurred object
# are feathered to stop the edges looking sharp, which
# is achieved via masking.
#
# NOTE: will over-write folder of images


import sys, os
import cv2
from cv2 import cv2
import numpy as np

flip = 0

if len(sys.argv) < 3:
    print('Usage: logoblur.py <image_folder> <logo_template> <optionalFlip=0|1>')
    exit()

if len(sys.argv) == 4:
    flip = int(sys.argv[3])

method = cv2.TM_SQDIFF_NORMED

# Read the images from the file
templatePath = sys.argv[2]
template = cv2.imread(templatePath)
template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
template = cv2.Canny(template, 50, 200)

def alphaBlend(img1, img2, mask):
    """ alphaBlend img1 and img 2 (of CV_8UC3) with mask (CV_8UC1 or CV_8UC3)
    """
    if mask.ndim==3 and mask.shape[-1] == 3:
        alpha = mask/255.0
    else:
        alpha = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)/255.0
    blended = cv2.convertScaleAbs(img1*(1-alpha) + img2*alpha)
    return blended

# Loop over all images in given folder
directory = sys.argv[1]
for filename in os.listdir(directory):
    if filename.endswith((".jpg",".png")):
        fullPath = os.path.join(directory, filename)

        origImage = cv2.imread(fullPath)
        processedImage = origImage.copy()

        origImage = cv2.cvtColor(origImage, cv2.COLOR_BGR2GRAY)
        origImage = cv2.Canny(origImage, 50, 200)
        result = cv2.matchTemplate(template, origImage, method)
        # Open the image we wnt to process
        # image = Image.open(open(fullPath, 'rb'))
        height,width = origImage.shape[:2]

        # We want the minimum squared difference
        mn,_,mnLoc,_ = cv2.minMaxLoc(result)

        # Draw the rectangle:
        # Extract the coordinates of our best match
        MPx,MPy = mnLoc

        # Get the size of the template. This is the same size as the match.
        trows,tcols = template.shape[:2]

        X,Y = processedImage.shape[:2]
        mask = np.zeros((X,Y), np.uint8)
        cv2.rectangle(mask,(MPx, MPy),(MPx+tcols,MPy+trows),(255,255,255), -1, cv2.LINE_AA)
        mask = cv2.GaussianBlur(mask, (11,11),11)

        processedImageB = processedImage.copy()
        processedImageB = cv2.GaussianBlur(processedImageB, (59,59),11)
        if flip == 0:
            blended = alphaBlend(processedImage, processedImageB, mask);
        else:
            blended = alphaBlend(processedImage, processedImageB, 255-mask);
        cv2.imwrite(fullPath, blended)