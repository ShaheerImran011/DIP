import cv2
import numpy as np

def calculate_scores(image_path):
    original_image = cv2.imread(image_path)
    copy_image = np.zeros_like(original_image)
    gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray_image, 200, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    scores = []
    for c in contours:
        area = cv2.contourArea(c)
        #print(area)
        if area > 40000 and area<70000:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(copy_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            #cv2.imshow("Image", copy_image)
            roi = original_image[y:y+h, x:x+w]
            #cv2.imshow("ROI", roi)
            hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
            lower_blue = np.array([80, 50, 50])
            upper_blue = np.array([130, 255, 255])
            mask = cv2.inRange(hsv_roi, lower_blue, upper_blue)
            blue_area = cv2.countNonZero(mask)
            scores.append(blue_area)
            copy_image[y:y+h, x:x+w] = roi

    for i in range(len(scores)):
        scores[i] = round(scores[i]/area, 1)
        scores[i] = scores[i]*10
        print(scores[i])

    cv2.putText(copy_image, f"Speaking: {scores[0]}", (300, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(copy_image, f"Writing: {scores[1]}", (300, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(copy_image, f"Reading: {scores[2]}", (300, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow('Image with Test Scores', copy_image)
    cv2.waitKey(0)


image_path = "3-1.jpg"
calculate_scores(image_path)

# The code above analyzes an image to calculate test scores for speaking, writing, and reading abilities. 
# It identifies specific regions of interest (ROIs), analyzes their color information, and displays the scores on the image.
# This script is designed for automated test score evaluation from images.
