import cv2
import numpy as np
import math

image = cv2.imread('2-1.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
edges = cv2.Canny(blurred, 50, 150)
lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=90)

if lines is not None and len(lines) >= 2:
    lines = sorted(lines, key=lambda line: line[0][0])
    minute_hand = lines[1][0]   
    hour_hand = lines[0][0]
    minute_angle = minute_hand[1]
    hour_angle = hour_hand[1]
    angle_between_hands = math.degrees(abs(minute_angle - hour_angle))
    angle_between_hands %= 360
    angle_between_hands = 180 - angle_between_hands
    print(f"Angle between clock hands: {angle_between_hands:.2f} degrees")
    total_minutes = angle_between_hands * 2
    hour = int(total_minutes // 60)
    minute = int(total_minutes % 60)
    print(f"Time: {hour:02d}:{minute:02d}")
else:
    print("No clock hands detected.")

for line in lines:
    rho, theta = line[0]
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    x1 = int(x0 + 1000 * (-b))
    y1 = int(y0 + 1000 * (a))
    x2 = int(x0 - 1000 * (-b))
    y2 = int(y0 - 1000 * (a))
    cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)

cv2.imshow('Clock Hands', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# The code above loads an image and processes it to detect clock hands using Hough Line Transformation.
# It calculates the angle between the clock hands and displays the result, along with the time shown by the clock.
# Detected clock hands are highlighted in the displayed image.
