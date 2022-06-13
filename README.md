# Opencv_Atulya

## **DESCRIPTION**

### THE MAIN IDEA OF THE PROJECT:-
1. Detection of squares in the Task Image
2. Colour Detection in the Task Image
3. Aruco Marker ID detection
4. Pasting the aruco markers on to the specified position based on colour

### ARUCO ID AND IT'S RESPECTIVE IMAGE:-
    
1. ARUCO ID [1] = LAMO
2. ARUCO ID [2] = XD
3. ARUCO ID [3] = Ha
4. ARUCO ID [4] = HaHa
   
### ARUCO ID AND IT'S RESPECTIVE SQUARE BOX COLOUR IN TASK IMAGE:-

1. ARUCO ID [1] = GREEN
2. ARUCO ID [2] = ORANGE
3. ARUCO ID [3] = BLACK
4. ARUCO ID [4] = PINK-PEACH

## DETECTION OF SQUARES IN TASK IMAGE-

  ### Detected square -
  
In this function the task image is passed as parameter.We use **findcontours()** function to detect the contours in the task image. Later to neglect some of the contours we    make a condition that the area of the closed loop must be greater than 1500. The area can be found by using **contourArea()** function.Then the coordinates of the    closed loop are found using the function **approxPolyDP()**.Now we calculate the coordinates width and height using the **boundingRect()** function. For detecting only the squares the number of coordinates should be equal to 4. So we use an if else statement whether the **len(coordinates)** is equal to 4 or not if yes using    the **aspectratio** which ranges from **(0.95,1.05)** for squares we detect the squares from remaining polygons of 4 sides.And then we create a list of all         coodinates of square and retrun them.

 ### Contour drawing -
 
 In this function the task image is passed as parameter.All the remaining part of this function is same as the **Detected square** function except the drawing of contours.Here instead of listing the coordinates we used **drawContours()** function to draw the contours on the image.This function will return the Copy of the image on which the contours are drawn.
 

## COLOUR DETECTION IN TASK IMAGE-

  ### Colour detection -
  
  In this function the task image and the list of colours that are to be detected are passed as a parameters.First of all the img will be taken in HSV form.Then we use the **inrange()** function for masking the image.The lower and upper threshold values for all 4 colours are taken in the list of colours.After getting the masked image if we found any square using **detected square** function for a paricular colour then the function will return the index of colour in the list of colours. 

## ARUCO MARKER ID DETECTION-
  
  This can be done using the aruco generator as the given markers are of dimension 5*5 so on giving the 5*5 as dimension in generator and mentioning the id's it gives the respective aruco markers.

## PASTING THE ARUCO MARKERS ON THE SPECIFIED COLOURED SQUARE BOXES-



