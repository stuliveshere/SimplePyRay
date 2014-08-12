#model a shot gather using shey approximations for the zoeppritz equations
#use rough amplitude approximations for refraction and direct
#http://en.wikipedia.org/wiki/Zoeppritz_equations#Shuey_Equation

import numpy as np
import matplotlib.pyplot as pylab

#signal processing 101.  we are going to process some seismic signals.
#but first we are going to build the signal we are going to process.
#I could supply seismic data, but there is advantages to building our 
#own. specifically, we know what the answer should be.  What we will
#be doing is known as scientific modelling. so what model are we going to build?

#earth convolution model. oz yilmaz.

#this is only one type of model.  Another type of model might be a finite difference 
#model, which uses the partial differential wave equation to model seismic
#waves propogating through a medium.

#what is convolution? 
#it is defined as the integral of the product of the two functions
#after one is reversed and shifted
#http://en.wikipedia.org/wiki/Convolution
#succinct, exact, but not very clear
#convolve is to roll together, so convolution in signal processing is 
#rolling together 2 signals. often denoted by *

#The convolutional model of the seismic trace states that 
#the trace we record is the result of the earth's reflectivity 
#(what we want) convolved with the source wavelet the 
#recording system and some noise.

#ie. E * S * R + N

#we are going to build this model!

#so lets start by building E, the earth's reflectivity

#we are going to sample the earth as if there is a seismic array sitting on top of it.
# a seismic array has whats called a geometry. this describes the location of each 
#source and receiver. it can be as simple as a bunch of gps coordinates.

#lets imitate the crystal mountain seismic survey. 
#csv files with crystal mountain geometry have been supplied in the format
# line number , station number, UTMx, UTMy, ASL

#we could manually read in those files, but numpy gives us a function which makes it all very easy

line, s_station, sx, sy, sz = np.loadtxt('Sx_WGS84.csv', unpack=True)
#check to make sure it all came in ok
#~ print sx
line, r_station, rx, ry, rz = np.loadtxt('Rx_WGS84.csv', unpack=True)
#check to make sure it all came in ok
#~ print rx

#so we have a bunch of source and receiver coordinates.  what we want to do now 
#is come up with some kind of model of the earth that we can use to calculate the reflectivity


#~ vp0 = None
#~ vs0 = None
#~ rho0 = None
dz1 = 30.0 #m
dz2 = 40
dz3 = 90
dz4 = 100
#~ vp1 = None
#~ vs1 = None
#~ rho1 = None
#~ dz1 = None
#~ vp2 = None
#~ vs2 = None
#~ rho2 = None
#~ dz2 = None

z1 = np.ones((10,200))*800.
z2 = np.ones((20,200))*3200.
z3 = np.ones((10,200))*1800.
z4 = np.ones((50,200))*3600
z5 = np.ones((100,200))*4000

dz1 = 30.0 #m
dz2 = 40
dz3 = 90
dz4 = 100

layer_model = [z1, z2, z3, z4, z5]

z = np.vstack(layer_model)
#~ print z.shape

#this time calculator works by storing the earth model in a 2d array in memory, effectively drawing a line of points 
#between source and reciever, then finding the velocity nearest to each point.  

sx_coords = np.arange(99)+0.5
rx_coords = np.arange(100)

def linePick(x0=0, x1=3, y0=0, y1=2, num=1000, z=np.ones((3,3),'f')):
	'''allocates each sample to a box by rounding down'''
	x, y = np.linspace(x0, x1, num, endpoint=False), np.linspace(y0, y1, num, endpoint=False) #generate rays
	xint = np.floor(x) #round em down
	yint = np.floor(y) #round em down
	#~ print xint, yint
	return x, y, z[yint.astype(np.int), xint.astype(np.int)] 

for depth in [dz1, dz2, dz3]:
	for sx in sx_coords[:1] :
		for rx in rx_coords:
			offset = np.abs(rx - sx) #calculate shot-reciever offset from coordinates)
			ds = np.sqrt(depth**2 + (offset/2.)**2)/1000. # line step distance
			x, y, model = linePick(x0=rx, x1=rx+offset/2., y0=0, y1=depth,num=1000, z=z)
			traveltime = np.sum(ds/model)*2. #time = distance/speed
			pylab.plot(offset, traveltime, 'b.')
pylab.ylim([0.2,0])
pylab.title('plot of offset vs time')
pylab.xlabel('offset (m)')
pylab.ylabel('time (s)')
pylab.show()
		
		
	




