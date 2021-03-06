import cv2
import math 
import numpy as np


def grayscale(img):
    """Applies the Grayscale transform
    This will return an image with only one color channel
    but NOTE: to see the returned image as grayscale
    (assuming your grayscaled image is called 'gray')
    you should call plt.imshow(gray, cmap='gray')"""
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # Or use BGR2GRAY if you read an image with cv2.imread()
    # return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
def canny(img, low_threshold, high_threshold):
    """Applies the Canny transform"""
    return cv2.Canny(img, low_threshold, high_threshold)

def gaussian_blur(img, kernel_size):
    """Applies a Gaussian Noise kernel"""
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

def region_of_interest(img, vertices):
    """
    Applies an image mask.
    
    Only keeps the region of the image defined by the polygon
    formed from `vertices`. The rest of the image is set to black.
    `vertices` should be a numpy array of integer points.
    """
    #defining a blank mask to start with
    mask = np.zeros_like(img)   
    
    #defining a 3 channel or 1 channel color to fill the mask with depending on the input image
    if len(img.shape) > 2:
        channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255
        
    #filling pixels inside the polygon defined by "vertices" with the fill color    
    cv2.fillPoly(mask, vertices, ignore_mask_color)
    
    #returning the image only where mask pixels are nonzero
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image


def draw_lines(img, lines, color=[0, 0, 255], thickness=2, vertices=[]):
    """
    NOTE: this is the function you might want to use as a starting point once you want to 
    average/extrapolate the line segments you detect to map out the full
    extent of the lane (going from the result shown in raw-lines-example.mp4
    to that shown in P1_example.mp4).  
    
    Think about things like separating line segments by their 
    slope ((y2-y1)/(x2-x1)) to decide which segments are part of the left
    line vs. the right line.  Then, you can average the position of each of 
    the lines and extrapolate to the top and bottom of the lane.
    
    This function draws `lines` with `color` and `thickness`.    
    Lines are drawn on the image inplace (mutates the image).
    If you want to make the lines semi-transparent, think about combining
    this function with the weighted_img() function below
    """
    # Used to keep track of the two sets of lane lines
    left_lane_lines = []
    right_lane_lines = []

    left_lane_avg_slope = 0
    right_line_avg_slope = 0

    left_lane_avg_x = 0
    left_lane_avg_y = 0
    right_lane_avg_x = 0
    right_lane_avg_y = 0

    width = img.shape[1]

    for line in lines:
        # print(line)
        # continue
        for x1,y1,x2,y2 in line:
            # Find the slope of the line so we can throw out lines that arent nearly vertical
            slope = (y2-y1)/(x2-x1)

            # Check which side of the image the line is on
            # TODO: Find a more robust way to do this
            if (x1 < width/2) and (abs(slope) > .5):
                # cv2.line(img, (x1, y1), (x2, y2), color, thickness)
                left_lane_avg_slope += slope
                left_lane_avg_x += (x1 + x2)/2
                left_lane_avg_y += (y1 + y2)/2
                # avg_point = (int((x1+x2)/2), int((y1+y2)/2))
                left_lane_lines.append(line)
            elif abs(slope) > .5:
                # cv2.line(img, (x1, y1), (x2, y2), [255, 0, 0], thickness)
                right_line_avg_slope += slope
                right_lane_avg_x += (x1 + x2)/2
                right_lane_avg_y += (y1 + y2)/2
                # avg_point = (int((x1+x2)/2), int((y1+y2)/2))
                right_lane_lines.append(line)

    if len(left_lane_lines) > 0:
        left_lane_avg_slope /= len(left_lane_lines)
        left_lane_avg_point = (int(left_lane_avg_x/len(left_lane_lines)), int(left_lane_avg_y/len(left_lane_lines)))
        # cv2.circle(img, (left_lane_avg_point[0], left_lane_avg_point[1]), 10, (0, 255, 0), -1)
        cv2.line(img, left_lane_avg_point, (int(vertices[0][1][0]*1.05), vertices[0][1][1]), [0,0,255], 5)
        cv2.line(img, left_lane_avg_point, (int(vertices[0][0][0]*1.05), vertices[0][0][1]), [0,0,255], 5)
        

    if len(right_lane_lines) > 0:
        right_line_avg_slope /= len(right_lane_lines)
        right_lane_avg_point = (int(right_lane_avg_x/len(right_lane_lines)), int(right_lane_avg_y/len(right_lane_lines)))
        # cv2.circle(img, (right_lane_avg_point[0], right_lane_avg_point[1]), 10, (0, 255, 0), -1)
        cv2.line(img, right_lane_avg_point, (int(vertices[0][2][0]*.95), vertices[0][2][1]), [0,0,255], 5)
        cv2.line(img, right_lane_avg_point, (int(vertices[0][3][0]*.95), vertices[0][3][1]), [0,0,255], 5)


            # First try finding the two farthest apart points on each side and making a line from those
            # This can then be extended to the edge of the region of interest by finding where the line interescts that horizantal line

            # To make the line more robust to curves it might be good to try to connect line segments with similar slopes to any others that are close to them
            # Loop When drawing a line check if there are any other lines close above or below it and connect top of one to bottom of the other and vice versa

    # # Grab the initial values for closest and farthest lane points
    # first_left_line = left_lane_lines[0]

    # # Determines which of the two points is closer to the bottom of the image
    # # TODO: Might need to check x as well but y is far more impactful in terms of distance from the camera
    # if first_left_line[0][1] > first_left_line[0][3]:
    #     closest_left_lane_point = (first_left_line[0][0], first_left_line[0][1])
    #     farthest_left_lane_point = (first_left_line[0][2], first_left_line[0][3])
    # else:
    #     closest_left_lane_point = (first_left_line[0][2], first_left_line[0][3])
    #     farthest_left_lane_point = (first_left_line[0][0], first_left_line[0][1])

    # # Loop through the left lane lines and find the two points that are the farthest apart
    # for line in left_lane_lines:
    #     # Check if the first point in the line is closer or farther than the current best
    #     if line[0][1] > closest_left_lane_point[1]:
    #         closest_left_lane_point = (line[0][0], line[0][1])
    #     elif line[0][1] < farthest_left_lane_point[1]:
    #         farthest_left_lane_point = (line[0][0], line[0][1])
    #     # Check if the second point in the line is closer or farther than the current best
    #     elif line[0][3] > closest_left_lane_point[1]:
    #         closest_left_lane_point = (line[0][2], line[0][2])
    #     elif line[0][3] < farthest_left_lane_point[1]:
    #         farthest_left_lane_point = (line[0][2], line[0][3])

    # # Grab the initial values for closest and farthest lane points
    # first_right_line = right_lane_lines[0]

    # # Determines which of the two points is closer to the bottom of the image
    # # TODO: Might need to check x as well but y is far more impactful in terms of distance from the camera
    # if first_right_line[0][1] > first_right_line[0][3]:
    #     closest_right_lane_point = (first_right_line[0][0], first_right_line[0][1])
    #     farthest_right_lane_point = (first_right_line[0][2], first_right_line[0][3])
    # else:
    #     closest_right_lane_point = (first_right_line[0][2], first_right_line[0][3])
    #     farthest_right_lane_point = (first_right_line[0][0], first_right_line[0][1])

    # # Loop through the right lane lines and find the two points that are the farthest apart
    # for line in right_lane_lines:
    #     # Check if the first point in the line is closer or farther than the current best
    #     if line[0][1] > closest_right_lane_point[1]:
    #         closest_right_lane_point = (line[0][0], line[0][1])
    #     elif line[0][1] < farthest_right_lane_point[1]:
    #         farthest_right_lane_point = (line[0][0], line[0][1])
    #     # Check if the second point in the line is closer or farther than the current best
    #     elif line[0][3] > closest_right_lane_point[1]:
    #         closest_right_lane_point = (line[0][2], line[0][2])
    #     elif line[0][3] < farthest_right_lane_point[1]:
    #         farthest_right_lane_point = (line[0][2], line[0][3])

    # cv2.line(img, closest_left_lane_point, farthest_left_lane_point, color, thickness)
    # cv2.line(img, closest_right_lane_point, farthest_right_lane_point, [255, 0, 0], 5)



def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap, vertices):
    """
    `img` should be the output of a Canny transform.
        
    Returns an image with hough lines drawn.
    """
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)
    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    draw_lines(line_img, lines, vertices=vertices)
    return line_img

# Python 3 has support for cool math symbols.

def weighted_img(img, initial_img, α=0.8, β=1., γ=0.):
    """
    `img` is the output of the hough_lines(), An image with lines drawn on it.
    Should be a blank image (all black) with lines drawn on it.
    
    `initial_img` should be the image before any processing.
    
    The result image is computed as follows:
    
    initial_img * α + img * β + γ
    NOTE: initial_img and img must be the same shape!
    """
    return cv2.addWeighted(initial_img, α, img, β, γ)


if __name__ == "__main__":
    img = cv2.imread("test_images/solidYellowCurve.jpg")

    vid = cv2.VideoCapture("test_videos/challenge.mp4")

    while(1):

        ret, img = vid.read()

        # Get the dimensions of the image
        height = img.shape[0]
        width = img.shape[1]

        cv2.imshow("Original", img)
        cv2.waitKey(0)

        # Make a copy of the original image so we can use it to find the region of interest later
        roi_img = img.copy()

        # Make another copy of the image that we will use to display the final lines on
        display_img = img.copy()

        # Get the grayscale version of the image
        gray_img = grayscale(img)

        # Apply Guassian blur to smooth the image
        blurred_img = gaussian_blur(gray_img, 5)

        # Apply the canny edge detector to get all the lines in the image
        # Uses the standard low to high threshold ratio of 1:3
        edge_img = canny(blurred_img, 50, 150)

        # cv2.imshow("Edges", edge_img)
        # cv2.waitKey(0)

        # Grab the region of interest
        vertices = np.array([[[width*.15, height], [width*.45, height*.60], [width*.55, height*.60], [width*.93, height]]], dtype=np.int32)
        roi_img = region_of_interest(edge_img, vertices)

        cv2.imshow("ROI", roi_img)
        # cv2.waitKey(0)

        # Use Hough voting to get only the strongest lines in the image
        strongest_lines = hough_lines(roi_img, 1, np.pi/180, 20, 20, 15, vertices)
        cv2.imshow("Hough lines", strongest_lines)
        # cv2.waitKey(0)

        # Apply the lines to the original image
        hough_img = (weighted_img(strongest_lines, img))

        cv2.imshow("Hough image", hough_img)
        # cv2.waitKey(0)