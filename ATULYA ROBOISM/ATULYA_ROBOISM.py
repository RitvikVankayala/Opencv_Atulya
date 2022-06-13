#imports
import cv2 as cv
import numpy as np

#some empty list for later appending
l3=[]
l4=[]
l5=[]
l6=[]
img=cv.imread("resources/CVtask.jpg")
img_cpy=img.copy()

#This is the function that wraps the task image
#The width is the difference between max x coordinate - min x coordinate
#The height is the difference between max Y coordinate - min y coordinate
#If the sum of coordinates of the image is max then it is the [w,h] coordinate if its min it is [0,0] coordinate
#If the difference of coordinates of image is max [0,h] coordinate if its min it is [w,0] coordinate
def extraction(img,approx):
	#shortens the list
	final_coordinates=np.squeeze(approx)
	#finds the width and the height
	w=np.max(final_coordinates[:,0])-np.min(final_coordinates[:,0])
	h=np.max(final_coordinates[:,1])-np.min(final_coordinates[:,1])
	#finding summation and difference between coordinates
	summation=final_coordinates.sum(1)
	differnce=np.diff(final_coordinates,1)
	#for calculating the surronding box
	boundaries=np.array([final_coordinates[np.argmin(summation)],final_coordinates[np.argmin(differnce)],final_coordinates[np.argmax(summation)],final_coordinates[np.argmax(differnce)]],dtype=np.float32)
	#for making a reference that which point it corresponds
	top_left=[0,0]
	top_right=[0,h]
	bottom_left=[w,h]
	bottom_right=[w,0]
	# perspective_point=np.array([[0,0],[w,0],[w,h],[0,h]],dtype=np.float32)
	perspective_point=np.array([top_left,bottom_right,bottom_left,top_right],dtype=np.float32)
	#for making a transforamtion matrix
	matrix=cv.getPerspectiveTransform(boundaries,perspective_point)
	#wrapping the image
	img_output=cv.warpPerspective(img,matrix,(w,h))
	#The list of wrapped image , boundary box, reference points
	return 	[img_output,boundaries,perspective_point]

#This function helps in overlappping one image with other
#Host is image on which the prey will be overlapped
def overlapping_img(host,prey):
	#defining width,height and no.of channels using shape function
	width=host.shape[0]
	height=host.shape[1]
	channels=host.shape[2]
	#resizing prey to fit in host
	prey=cv.resize(prey,(height,width))
	#pointing where the prey should overlapp in host
	host[:,:]=prey
	#returning the host image
	return host

#This function is for the finding contours on the image
def contour_drawing(img):
	#grey image
	img_grey=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
	#canny image
	img_canny=cv.Canny(img_grey,50,100)
	#using contour function for finding the contours
	#_ means no use of that particular variable 
	contours,_=cv.findContours(img_canny,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
	for contour in contours:
		#for area of any closed surface greater than area 1500
		if cv.contourArea(contour)>1500:
			#for calculating the perimeter
			perimeter=cv.arcLength(contour,True)
			#for finding the coordinates of the contours that are found
			approx=cv.approxPolyDP(contour,0.01*perimeter,True)
			#boundingrect function returns (x,y)[coordinates] and width and height of image
			x,y,width,height=cv.boundingRect(approx)
			#finding aspect ratio
			ar=float(width)/height
			if(len(approx)==4):
			#1.05<aspect ratio of square<0.95
				if(ar>=0.95 and ar<=1.05):
					cv.drawContours(img,[contour],-1,(0,0,0),cv.FILLED)	
#This function returns the copy of the image in which the contours and approx are found
	return img_cpy

#This function helps in realloting the wrapped image to its original image
def inverse_transform(host,prey,boundary,perspective_points):
	#reverse that we have taken in wrappind
	matrix=cv.getPerspectiveTransform(perspective_points,boundary)
	#defining width,height and no.of channels using shape function
	width=host.shape[0]
	height=host.shape[1]
	channels=host.shape[2]
	#reverse using the wrapperspective
	wrap=cv.warpPerspective(prey,matrix,(height,width))
	overlap=cv.addWeighted(wrap,1,host,0,0)
	#returning the image in which the square of task image is again back into its position
	return overlap

#This function is for blending the image
def overlapping(datas):
	#return same shape and datatype passed with blank screen
	blank=np.zeros_like(datas[0])
	for data in datas:
		blank=cv.addWeighted(blank,1,data,1,0)
	blank=blank.astype(np.uint8)
	#return the blank image with changes
	return blank

# function for finding the coordinates i.e approx and detecting the squares from it and appending them to l2 list
def detected_squares(img):
	img_canny=cv.Canny(img,50,100)
	contours,heichery=cv.findContours(img_canny,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE)
	#empty list that to be returned
	l2=[]
	for contour in contours:
		if cv.contourArea(contour)>1500:
		#only the square whose area is greater than 1000 will be detected
			perimeter=cv.arcLength(contour,True)
			approx=cv.approxPolyDP(contour,0.01*perimeter,True)			
			x,y,width,height=cv.boundingRect(approx)
			ar=float(width)/height
 			#finding aspect ratio
			if(len(approx)==4):
			#1.05<aspect ratio of square<0.95
				if(ar>=0.95 and ar<=1.05):
					l2.append(approx)
	#This function returns a list of squares whose area is greater than 1500				
	return l2

#HSV values for different colours
#[low_hue,low_sat,low_val,high_hue,high_sat,high_val]

Green=[37,144,75,118,255,255]
Orange=[0,241,221,255,250,255]
Black=[0,0,0,0,2,0]
Pink_peach=[4,0,228,89,29,235]

#list of the colours
colours=[Green,Orange,Black,Pink_peach]

#This function helps in the colour finding in the image
def colour_detection(img,colours):
	#hsv of the given image
	img_hsv=cv.cvtColor(img,cv.COLOR_BGR2HSV)	
	for colour in range(0,len(colours)):
		#finding the lower threshold of hsv
		lower_bound=np.array(colours[colour][0:3])
		#finding the upper threshold of hsv
		upper_bound=np.array(colours[colour][3:6])
		#masked image using the upper and lower bound
		img_mask=cv.inRange(img_hsv,lower_bound,upper_bound)
		#if any of the colour is matched with the list of colours and that two a square then this function will return its index
		if len(detected_squares(img_mask))>0:
		#colour-1-Green
		#colour-2-Orange
		#colour-3-Black
		#colouR-4-Pink_peach
			return colour

#aruco images
m1=cv.imread("resources/LMAO.jpg")
m2=cv.imread("resources/XD.jpg")
m3=cv.imread("resources/Ha.jpg")
m4=cv.imread("resources/HaHa.jpg")
#list of aruco images whose indexes are their ids		
ids=[m1,m2,m3,m4]
#LAMO -m1
#XD   -m2
#Ha   -m3
#HaHa -m4

#Traversing throughout the no.of aruco images
for loop in range(0,len(ids)):
	#ids array will store the wrapped image of that id image
	ids[loop]=extraction(ids[loop],detected_squares(ids[loop]))[0]

#The detected list of squares will be stored in squares list
squares=detected_squares(img)
#traversing accross all squares
for square in range(0,len(squares)):
	#wrapping squares from the task image
	net_output=extraction(img,squares[square])
	#making the copy of wrapped squares that are found in task image
	copied_image=net_output[0].copy()
	#listing all the wrapped squares in l3
	l3.append(net_output[0])
	#detecting the colours of the squares
	colour_detect=colour_detection(l3[square],colours)
	#listing the aruco on to squares of task_image
	l5.append(overlapping_img(copied_image,ids[square]))
	#retracking the squares of task to its original position
	l6.append(inverse_transform(img,l5[square],net_output[1],net_output[2]))

final_image=overlapping(l6)
imagecopy=contour_drawing(img_cpy)
end_image=cv.addWeighted(final_image,1,imagecopy,1,0)
#for showing the image
cv.imshow("Task",end_image)
#for showing the aruco images
cv.imshow("M1",m1)
cv.imshow("M2",m2)
cv.imshow("M3",m3)
cv.imshow("M4",m4)


cv.waitKey(0)
