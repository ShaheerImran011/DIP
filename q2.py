import cv2
import numpy as np

def matching(image):
    upper_region_x_coordinate = 331
    upper_region_y_coordinate = 54
    width = 110
    height = 110

    upper_region = image[upper_region_y_coordinate:upper_region_y_coordinate + height, upper_region_x_coordinate:upper_region_x_coordinate + width]

    lower_region_x_coordinate = 50
    lower_region_y_coordinate = 180
    width = image.shape[1]
    height = image.shape[0] - lower_region_y_coordinate

    lower_region = image[lower_region_y_coordinate:lower_region_y_coordinate + height, lower_region_x_coordinate:lower_region_x_coordinate + width]

    threshold = 0.9

    result = cv2.matchTemplate(lower_region, upper_region, cv2.TM_CCOEFF_NORMED)

    locations = np.where(result >= threshold)
    locations = list(zip(*locations[::-1]))

    if locations:
        for location in locations:
            top_left = (location[0] + lower_region_x_coordinate, location[1] + lower_region_y_coordinate)
            h, w, _ = upper_region.shape
            bottom_right = (top_left[0] + w, top_left[1] + h)
            cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 4)

        cv2.imshow('Result with Matches', image)
        cv2.waitKey(0)
    else:
        print("\nNo matches Found")

image = cv2.imread("1-2.jpg")
matching(image)
