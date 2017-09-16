CXX = g++

CXXFLAGS = -c -Wall -O2 -std=c++11
LXXFLAGS = -Wall

SRC = ./src

LIB = ./lib
DYNAMICS = $(LIB)/cwo.dll $(LIB)/libfftw3f-3.dll

TARGET = dfrasm
BIN = ./bin

.PHONY: all clean

all: dfrasm.o cwo.o
	$(CXX) dfrasm.o cwo.o -o $(TARGET).exe $(LXXFLAGS) $(DYNAMICS)

dfrasm.o: $(SRC)/dfrasm.cpp $(SRC)/dfrasm.h $(LIB)/cwo.h 
	$(CXX) $(CXXFLAGS) $(SRC)/dfrasm.cpp -I$(LIB) -I$(SRC)

cwo.o: $(LIB)/cwo.cpp $(LIB)/cwo.h $(LIB)/cwo_lib.h $(LIB)/fftw3.h 
	$(CXX) $(CXXFLAGS) $(LIB)/cwo.cpp -I$(LIB)

clean: 
	rm *.o || true
	rm $(TARGET).exe || true

install: $(BIN)
	cp $(LIB)/cwo.dll $(BIN)/cwo.dll
	cp $(LIB)/libfftw3f-3.dll $(BIN)/libfftw3f-3.dll
	cp $(TARGET).exe $(BIN)/$(TARGET).exe

$(BIN): 
	mkdir $(BIN)
	