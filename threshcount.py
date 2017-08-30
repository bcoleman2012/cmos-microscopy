import argparse
import sys

import cv2
import numpy as np

parser = argparse.ArgumentParser(description = "Enhance a microscope image for viewing or further processing.")

# Positionals 
parser.add_argument("filename", metavar = "filename", help = "A filename corresponding to the input image.")

# Optionals 
parser.add_argument("-g","--gridsize", metavar = "gridsize", type = int, default = 32, help = "The tile grid size for adaptive histogram equalization. Default is 512.")
parser.add_argument("-cl","--cliplimit", metavar = "cliplimit", type = int, default = 30, help = "The clip limit for adaptive histogram equaliztion. Default is 30.")
parser.add_argument("-th","--threshold", metavar = "threshold", type = int, default = 127, help = "The threshold for cell detection")

# Flags 
parser.add_argument("-d","--display", action="store_true", help = "Display the marked cells")
parser.add_argument("--debug", action="store_true", help = "Display debug images")

args = parser.parse_args()

# Check for a valid input filename
if args.filename.split(".")[-1] not in ["png","jpg","jpeg"]: 
	print "Error: invalid input filename - use a .png or .jpg extension."
	sys.exit()



src = cv2.imread(args.filename,1)

img = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

clahe = cv2.createCLAHE(clipLimit = args.cliplimit, tileGridSize = (args.gridsize, args.gridsize))
img = clahe.apply(img)

_, cmask = cv2.threshold(img, args.threshold, 255, cv2.THRESH_BINARY)

cmask = cv2.morphologyEx(cmask, cv2.MORPH_OPEN, np.ones((5,5), np.uint8))
cmask = cv2.morphologyEx(cmask, cv2.MORPH_CLOSE, np.ones((5,5), np.uint8))

img_cmap = cv2.bitwise_and(img, img, mask = 255 - cmask)

img_cmap = cv2.merge((img_cmap, img_cmap, img_cmap + cmask))

_, contours, hierarchy = cv2.findContours(cmask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

print len(contours)

if args.display: 
	cv2.namedWindow("cmask", cv2.WINDOW_NORMAL)
	cv2.namedWindow("Output", cv2.WINDOW_NORMAL)

	cv2.imshow("cmask", cv2.resize(src,(1440,900)))
	cv2.imshow("Output", cv2.resize(img_cmap,(1440,900)))
	print "Press any key to continue ..."
	cv2.waitKey(0)

