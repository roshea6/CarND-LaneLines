# **Finding Lane Lines on the Road** 
[![Udacity - Self-Driving Car NanoDegree](https://s3.amazonaws.com/udacity-sdc/github/shield-carnd.svg)](http://www.udacity.com/drive)

<img src="examples/laneLines_thirdPass.jpg" width="480" alt="Combined Image" />

Overview
---

When we drive, we use our eyes to decide where to go.  The lines on the road that show us where the lanes are act as our constant reference for where to steer the vehicle.  Naturally, one of the first things we would like to do in developing a self-driving car is to automatically detect lane lines using an algorithm.

In this project you will detect lane lines in images using Python and OpenCV.  OpenCV means "Open-Source Computer Vision", which is a package that has many useful tools for analyzing images.  

To complete the project, two files will be submitted: a file containing project code and a file containing a brief write up explaining your solution. We have included template files to be used both for the [code](https://github.com/udacity/CarND-LaneLines-P1/blob/master/P1.ipynb) and the [writeup](https://github.com/udacity/CarND-LaneLines-P1/blob/master/writeup_template.md).The code file is called P1.ipynb and the writeup template is writeup_template.md 

To meet specifications in the project, take a look at the requirements in the [project rubric](https://review.udacity.com/#!/rubrics/322/view)


Creating a Great Writeup
---
For this project, a great writeup should provide a detailed response to the "Reflection" section of the [project rubric](https://review.udacity.com/#!/rubrics/322/view). There are three parts to the reflection:

1. Describe the pipeline

2. Identify any shortcomings

3. Suggest possible improvements

We encourage using images in your writeup to demonstrate how your pipeline works.  

All that said, please be concise!  We're not looking for you to write a book here: just a brief description.

You're not required to use markdown for your writeup.  If you use another method please just submit a pdf of your writeup. Here is a link to a [writeup template file](https://github.com/udacity/CarND-LaneLines-P1/blob/master/writeup_template.md). 


The Project
---

## If you have already installed the [CarND Term1 Starter Kit](https://github.com/udacity/CarND-Term1-Starter-Kit/blob/master/README.md) you should be good to go!   If not, you should install the starter kit to get started on this project. ##

**Step 1:** Set up the [CarND Term1 Starter Kit](https://classroom.udacity.com/nanodegrees/nd013/parts/fbf77062-5703-404e-b60c-95b78b2f3f9e/modules/83ec35ee-1e02-48a5-bdb7-d244bd47c2dc/lessons/8c82408b-a217-4d09-b81d-1bda4c6380ef/concepts/4f1870e0-3849-43e4-b670-12e6f2d4b7a7) if you haven't already.

**Step 2:** Open the code in a Jupyter Notebook

You will complete the project code in a Jupyter notebook.  If you are unfamiliar with Jupyter Notebooks, check out <A HREF="https://www.packtpub.com/books/content/basics-jupyter-notebook-and-python" target="_blank">Cyrille Rossant's Basics of Jupyter Notebook and Python</A> to get started.

Jupyter is an Ipython notebook where you can run blocks of code and see results interactively.  All the code for this project is contained in a Jupyter notebook. To start Jupyter in your browser, use terminal to navigate to your project directory and then run the following command at the terminal prompt (be sure you've activated your Python 3 carnd-term1 environment as described in the [CarND Term1 Starter Kit](https://github.com/udacity/CarND-Term1-Starter-Kit/blob/master/README.md) installation instructions!):

`> jupyter notebook`

A browser window will appear showing the contents of the current directory.  Click on the file called "P1.ipynb".  Another browser window will appear displaying the notebook.  Follow the instructions in the notebook to complete the project.  

**Step 3:** Complete the project and submit both the Ipython notebook and the project writeup

## How to write a README
A well written README file can enhance your project and portfolio.  Develop your abilities to create professional README files by completing [this free course](https://www.udacity.com/course/writing-readmes--ud777).

### Reflection

[//]: # (Image References)

[grayscale_ex]: ./test_images_output/solidYellowCurve2_grayBlur.jpg "Grayscale"
[canny_ex]: ./test_images_output/solidYellowCurve2_CannyEdge.jpg "Canny Edges"
[roi_ex]: ./test_images_output/solidYellowCurve2_roi.jpg "ROI"
[hough_ex]: ./test_images_output/solidYellowCurve2_hough.jpg "Hough"
[final_ex]: ./test_images_output/solidYellowCurve2.jpg "Final"

### 1. Describe your pipeline. As part of the description, explain how you modified the draw_lines() function.

My pipeline consisted of 7 major steps. The first major step is opening and beginning the playthrough of the video file which was done using the moviepy library. The second step was to prepare the photo for the Canny Edge detector. To do this, OpenCV functions were used to first convert the image to grayscale and then apply a blur to the image through the use of a Gaussian filter. The results of this can be seen in the image below. 

![alt text][grayscale_ex]

Once the image has been preprocessed it is run through OpenCV's Canny Edge detector to extract all edges within the image that are valid by the passed in parameters. This is step 3 and its results can be seen in the image below.

![alt text][canny_ex]

The output of the Canny edge detector is great for showing all of the edges in the image but for our purposes we only need a small section of the image. This section is called the region of interest (ROI) and is the area directly in front of the car that is between the left and right lane. To get just this area a quadrilateral is defined using 4 pixel coordinates as the 4 vertices. For step 4, these vertices are then passed into the OpenCV fillPoly function along with the output of the Canny edge detector in order to get only the edges that are within the region of interest. The output of this step can be seen in the image below.

![alt text][roi_ex]

In order to get only the strongest lines, i.e those which are most likely to represent lane lines, the OpenCV houghLines function is used. For step 5, these lines are returned as a list of lists that each contain 4 different values. These values correspond to the two pixel coordinates that represent the end points of the line. For step 6, these lines are passed into the draw_lines function where most of the new logic for finding the fully extended lane lines was added. The first step was to loop through all of the lines returned from the houghLines function and categorize them as left lane lines, right lane lines, or neither which were then ignored from then on. This was done using a fairly simple check which is one of the major areas that can be improved. If the x position of the line was in the left half of the image and the absolute value of the line's slope was greater than .5 it was added to the left lane line list. The slope value check was so that lines that weren't nearly vertical could be thrown away because they most likely from shadows or other undesirable markings on the road. A similar process was used to find the right lane line but the x position of the line had to be on the right side of the image. During this the average x and y position of the left and right lane lines were calculated seperately so that the average position of the lane could be determined. Two lines where then drawn for each lane using the OpenCV drawLine function which takes in two end points for a line. One from the average location to the top corner of the ROI for that side and one from the average location to the bottom corner of the ROI for that side. Two lines were used in attempt to make it more robust to heavily curved roads like those seen in the challenge video. My initial solution considted of drawing one line between the two farthest apart points that were detected for each lane. This partially worked but made the line incredibly jumpy in certain scenarios. The output of the two line solution can be seen in the image below.

![alt text][hough_ex]

For the 7th and final step of the pipeline the 4 generated lines were overlayed onto the original image using the OpenCV addWeighted function which combines two images into one. The output of this can be seen in the image below. More comprehensive examples of the pipeline's output can be found in the test_videos_output folder.

![alt text][final_ex]


### 2. Identify potential shortcomings with your current pipeline


The pipeline I was able to design is far from perfect especially given its poor performance on the challenge video. One of the main shortcomings is its reliance on connecting the line to the vertices of the region of interest even though they may not properly line up with the position of the lanes especially if the car were to begin changing lanes. The current solution also doesn't handle strong curves, shadows, and very light pavement well as shown in its performance on the challenge video. The ROI also seemed to fail in some places based on the car's relative position between the lines. This was especially apparent in the challenge video where the ROI is badly outside the desired lane due to its shape. Overall the pipeline is not very diverse to dynamic situations and poor road conditions.


### 3. Suggest possible improvements to your pipeline

The pipeline almost certainly needs more tuning of some of its parameters to obtain peak performance with the current pipeline setup. More image preprocessing would also likely lead to increased performance especially in the potion of the challenge video that has a yellow line on a light pavement background. This section isn't picked up by the edge detector which is most likely due to there not being a strong enough gradient in that area. One way to fix this would be to dynamically change the parameters for edge detection as the image begins to exhibit more or less total gradient. For example if the image only has weak gradients across the image then the requirments for line edge detection would be lowered so the lanes could still be detected. Another improvement to the system could be to use the average slope of the lane lines to try to propose a line that spans the whole lane. I initially set out to do this but was unable to work out the math for it in the given time frame. I believe that the ideal improvement to the pipeline would involve using the individual lines in the left and right lane to propose a polynomial line that best fits the detected line segments. This would likely greatly improve performance on curved roads. A similar concept could also be applied to make the ROI dynamic which I believe would also improve performance especially in scenrios like the challenge video.

## Acknowledgments
I referred back to the code in previous lessons to get a better understanding of the proper order for the pipeline. I also referred to the documentation for the OpenCV and matplotlib Python libraries a number of times to get a better understanding of how to use their functions.


