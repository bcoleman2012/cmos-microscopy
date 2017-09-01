import argparse
import sys
import numpy as np
import scipy.signal
import cv2

parser = argparse.ArgumentParser(description = "Enhance holographic diffraction patterns with the Prewitt compass filters, then apply histogram equalization.")

# Positionals 
parser.add_argument("filename", metavar = "filename", help = "A filename corresponding to the input image.")

# Optionals 
parser.add_argument("-o","--output", metavar = "output", help = "A filename to save the output. If this is not provided, the image will be displayed but not saved.")

# Flags 
parser.add_argument("-d","--display", action="store_true", help = "Display the original and the resulting image.")
parser.add_argument("-v","--verbose", action="store_true", help = "Display progress and debug information.")

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


K1 = np.array([ 
	[-1, 1, 1],
	[-1,-2, 1],
	[-1, 1, 1],
	])
K2 = np.array([ 
	[ 1, 1, 1],
	[-1,-2, 1],
	[-1,-1, 1],
	])
K3 = np.array([ 
	[ 1, 1, 1],
	[ 1,-2, 1],
	[-1,-1,-1],
	])
K4 = np.array([ 
	[ 1, 1, 1],
	[ 1,-2,-1],
	[ 1,-1,-1],
	])
K5 = np.array([ 
	[ 1, 1,-1],
	[ 1,-2,-1],
	[ 1, 1,-1],
	])
K6 = np.array([ 
	[ 1,-1,-1],
	[ 1,-2,-1],
	[ 1, 1, 1],
	])
K7 = np.array([ 
	[-1,-1,-1],
	[ 1,-2, 1],
	[ 1, 1, 1],
	])
K8 = np.array([ 
	[-1,-1, 1],
	[-1,-2, 1],
	[ 1, 1, 1],
	])

K = [K1,K2,K3,K4,K5,K6,K7,K8]

img = cv2.imread(args.filename,1)

if img is None: 
	print "Error: invalid input filename - file does not exist."
	sys.exit()

img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

img = cv2.GaussianBlur(img, (7, 7), 0) # Debatable - consider removing this filter

img = img.astype('float32')

Y = []
for k in K: 
	if args.verbose: 
		print "Processing with kernel \n",k
	Y.append(scipy.signal.convolve2d(img,k,mode = 'same', boundary = 'fill'))

out = np.zeros_like(img, dtype = 'float32')

for y in Y: 
	out += np.power(y,2)

out = np.sqrt(out)
out = out.astype('uint8')

out = cv2.equalizeHist(out)

if args.display: 
	cv2.namedWindow("Output", cv2.WINDOW_NORMAL)
	if out.shape[0] > 1440 or out.shape[1] > 900:
		cv2.imshow("Output", cv2.resize(out,(1440,900)))
	else: 
		cv2.imshow("Output", out)
	print "Press any key to continue ..."
	cv2.waitKey(0)


if args.output is not None:
	cv2.imwrite(args.output, out)

