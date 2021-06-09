# **Finding Lane Lines on the Road** 
Ryan O'Shea

**Finding Lane Lines on the Road**

The goals / steps of this project are the following:
* Make a pipeline that finds lane lines on the road
* Reflect on your work in a written report


[//]: # (Image References)

[grayscale_ex]: ./test_images_output/solidYellowCurve2_grayBlur.jpg "Grayscale"
[canny_ex]: ./test_images_output/solidYellowCurve2_CannyEdge.jpg "Canny Edges"
[roi_ex]: ./test_images_output/solidYellowCurve2_roi.jpg "ROI"
[hough_ex]: ./test_images_output/solidYellowCurve2_hough.jpg "Hough"
[final_ex]: ./test_images_output/solidYellowCurve2.jpg "Final"

---

### Reflection

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
