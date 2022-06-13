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

## PASTING THE ARUCO MARKERS ON THE SPECIFIED COLOURED SQUARES-

### Extraction -
  
  This function helps in wrapping the square boxes from the task image.Here we will give image and coordinates as the parameters.We make a transformation matrix using the function **getPerspectiveTransform()** function. We will give the reference points for the wrapped imaged on which it has to be oriented.using **wrapPerspective()** we will get an new image in which the square is wrapped.We return this image in this function.

### Overlapping_img-
    
   This function helps in overlapping the prey image on to the host image.We will give host and prey images as the parameters.Firstly we calculate the size of the host that is width height and channels using **shape()**. Then we will resize the prey image to the host's width and the height using **resize()** function.Later we overlap entire prey on to the host.

### Inversetransform-
   
   This function will help in the dewrapping the image that is replacing the wrapped image into its old position after all neccessary operations are done on wrapped image.It is exact opposite of extraction.Host,prey,boundaryrectangle and transformation points are passed as parameters in the function.The process is same except the the order of parameters in the **getPerspectiveTransform()** and **wrapPerspective()**.
    
  BY USING THESE FUNCTION AND PASSING THE CVtask IMAGE IT WILL RETURN THE FINAL IMAGE ON WHICH THE MARKERS ARE ATTACHED AT THE SPECIFIED COLOURED BOXES.
  
 A loop is used to traverse accross the id's of the markers in which at each index the extracted (**extraction()**) image of the markers will be alloted in the id's list.Later all the squares are detected from the task image using **detected_squares()** function.Later a loop will be runned for all 4 squares in which the squares from the task image is extracted using **extraction** function.We will append them in an empty list.Now the colour detection will be checked using **colour_detection()** function.Then we append all overlapping images and unwrapped images into two empty lists using **overlapping_img()** and **inverse_transformation()** respectively.Now finally we pass list of unwrapped images into **overlapping** function and then make a copy of that and display using **imshow()** function.
