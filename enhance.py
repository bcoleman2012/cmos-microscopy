import argparse
import sys

import cv2
import numpy as np

parser = argparse.ArgumentParser(description = "Enhance a microscope image for viewing or further processing.")

# Positionals 
parser.add_argument("filename", metavar = "filename", help = "A filename corresponding to the input image.")

# Optionals 
parser.add_argument("-o","--output", metavar = "output", help = "A filename to save the output. If this is not provided, the image will be displayed but not saved.")
parser.add_argument("-gs","--gridsize", metavar = "gridsize", type = int, default = 512, help = "The tile grid size for adaptive histogram equalization. Default is 512.")
parser.add_argument("-cl","--cliplimit", metavar = "cliplimit", type = int, default = 30, help = "The clip limit for adaptive histogram equaliztion. Default is 30.")

# Flags 
parser.add_argument("-d","--display", action="store_true", help = "Display the original and the resulting image.")
parser.add_argument("-c","--colormap", action="store_true", help = "Apply a colormap")
parser.add_argument("-b","--bar", action="store_true", help = "Apply a scalebar")


args = parser.parse_args()

# Check for a valid input filename
if args.filename.split(".")[-1] not in ["png","jpg","jpeg"]: 
	print "Error: invalid input filename - use a .png or .jpg extension."
	sys.exit()


# Check for a valid output filename, if we have one
if args.output is not None:  
	if args.output.split(".")[-1] not in ["png","jpg","jpeg"]: 
		print "Error: invalid output filename - use a .png or .jpg extension."
		sys.exit()


# Start of algorithm

img = cv2.imread(args.filename,1)
if img is None: 
	print "Error: invalid input filename - file does not exist."
	sys.exit()

imgOut = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

clahe = cv2.createCLAHE(clipLimit = args.cliplimit, tileGridSize = (args.gridsize, args.gridsize))
imgOut = clahe.apply(imgOut)

if args.colormap: 
	imgOut = cv2.applyColorMap(imgOut, cv2.COLORMAP_OCEAN)

if args.display: 
	cv2.namedWindow("Input", cv2.WINDOW_NORMAL)
	cv2.namedWindow("Output", cv2.WINDOW_NORMAL)
	if img.shape[0] > 1440 or img.shape[1] > 900:
		cv2.imshow("Input", cv2.resize(img,(1440,900)))
		cv2.imshow("Output", cv2.resize(imgOut,(1440,900)))
	else: 
		cv2.imshow("Input", img)
		cv2.imshow("Output", imgOut)
	print "Press any key to continue ..."
	cv2.waitKey(0)

if args.bar: 
	cv2.line(imgOut, (30,100),(30+80,100),(0,0,0),thickness = 50)
	cv2.putText(imgOut,"100 um", (30,80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), thickness = 50)


if args.output is not None:  
	cv2.imwrite(args.output, imgOut)



