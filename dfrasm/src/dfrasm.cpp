/* 
dfrasm.cpp: 

Computes the diffraction of an image using the angular spectrum method. Currently is only supported
on Windows because the closed-source library dependency is not available for Linux. 


To compile on windows with g++: 

g++ -c cwo.cpp // -> cwo.o
g++ -c main.cpp // -> main.o 

g++ cwo.o main.o -o out.exe -L/. libfftw3f-3.dll cwo.dll // -> out.exe

Then, run out.exe

Application requires graphicsmagick (gm.exe) to import png, jpeg, etc. 

To convert to pngs for whatever purpose: 
mogrify -format png *.bmp

With FFMPEG in the tools section, to make a video: 
ffmpeg -framerate 10 -i %04d.png -s:v 1280x720 -c:v libx264 -profile:v high -crf 20 -pix_fmt yuv420p testout.mp4

*/
#include "dfrasm.h"
#include "cwo.h"
#include <iostream> 
#include <iomanip>
#include <string> 

#include <cstring> 
#include <cstdlib> 



int main(int argc, char *argv[])
{
	float d = 0.0229; 
	switch(argc)
	{
		case 2: // in this case, we expect -h (and nothing else, no other valid argc == 2 situations are valid) 
			if (strcmp(argv[1],"-h") != 0)
			{
				std::cout << "Error: unrecognized argument. Try " << argv[0] <<" -h for help." << std::endl; 
				return -1; 
			}
			else 
			{
				std::cout << "Usage: dfrasm inputfile outputname [-d distance]" << std::endl; 
				std::cout << "   inputfile\tThe grayscale input image (including extension).\n"
						  << "            \tSupports .bmp, .png, and .jpg" << std::endl; 
				std::cout << "   outputname\tThe output name with extension. Output will be <outputname>-\n"
						  << "             \t<imagetype>.<outputname extension>, where <imagetype> = {real, imag, \n"
						  << "             \tintensity, amplitude, phase}" << std::endl; 
				std::cout << "   distance\tThe diffraction distance for ASM. For holographic\n"
						  << "           \tback-propagation, use a negative value. Default is "<< d << std::endl; 
			}
			break; 
		case 3: 
			if (checkImageFilename(argv[1]) && checkImageFilename(argv[2]))
			{
				//If we get here, the extensions are valid. But consider checking that the input file exists
			}
			else
			{
				std::cout << "Error: unsupported input file format. Supported formats are .bmp, .png, and .jpg" << std::endl; 
				return -1; 
			}
			break;
		case 5: 
			if (checkImageFilename(argv[1]) && checkImageFilename(argv[2]))
			{
				// If we get here, the extensions are valid. But consider checking that the input file exists here. 
			}
			else
			{
				std::cout << "Error: unsupported input file format. Supported formats are .bmp, .png, and .jpg" << std::endl; 
				return -1; 
			}
			if (strcmp(argv[3],"-d")!=0)
			{
				std::cout << "Error: unrecognized argument. Try " << argv[0] <<" -h for help." << std::endl; 
				return -1; 
			}
			d = atof(argv[4]); 
			if (d == 0)
			{
				std::cout << "Error: invalid value - d must be a nonzero floating-point value" << std::endl; 
				return -1; 
			}
			break; 
		default: 
			std::cout << "Error: Incorrect number of arguments. Try " << argv[0] <<" -h for help." << std::endl; 
			return -1; 
			break; 
	}

	CWO a;
	a.Load(argv[1]);
	std::cout << "Image loaded." << std::endl;

	char * filename = new char [strlen(argv[2]) + 16]; 
	char * extension = getFileExtension(argv[2]); 
	*strrchr(argv[2], '.') = '\0'; 

	a.Diffract(d, CWO_ANGULAR); //calculate diffraction from the image using the angular spectrum method
	std::cout << "Diffraction complete" << std::endl << std::endl; 

	strcpy(filename, argv[2]);
	strcat(filename, "-real");
	strcat(filename, extension);
	a.SaveAsImage(filename, CWO_SAVE_AS_RE); 
	
	strcpy(filename, argv[2]); 
	strcat(filename, "-imag");
	strcat(filename, extension);
	a.SaveAsImage(filename, CWO_SAVE_AS_IM);

	strcpy(filename, argv[2]); 
	strcat(filename, "-intensity");
	strcat(filename, extension);
	a.SaveAsImage(filename, CWO_SAVE_AS_INTENSITY);

	strcpy(filename, argv[2]); 
	strcat(filename, "-amplitude");
	strcat(filename, extension);
	a.SaveAsImage(filename, CWO_SAVE_AS_AMP);

	strcpy(filename, argv[2]); 
	strcat(filename, "-phase");
	strcat(filename, extension);
	a.SaveAsImage(filename, CWO_SAVE_AS_ARG);

	delete [] filename;
	return 0; 
}

bool checkImageFilename(const char * filename)
{	
	char * dotptr = strrchr(filename, '.');
	if (dotptr == nullptr)
		return false; 

	bool condition = (strcmp(dotptr, ".png") == 0) || (strcmp(dotptr, ".jpg") == 0) ||
					 (strcmp(dotptr, ".jpeg") == 0) || (strcmp(dotptr, ".bmp") == 0);
	return condition; 
}

char* getFileExtension(const char * filename)
{
	// the extension cannot be longer than the filename itself
	char * extension = new char [strlen(filename)+1]; 

	char * dotptr = strrchr(filename, '.');
	if (dotptr == nullptr)
	{ // if there is no extension, return an empty string 
		extension[0] = '\0'; 
		return extension; 
	}
	return strcpy(extension, dotptr); 
}










