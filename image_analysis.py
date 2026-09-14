import cv2
import numpy as np


def analyze_plant_image(image_bytes):

    # Convert uploaded image into OpenCV image
    image_array = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    # Check whether image was loaded correctly
    if image is None:
        return 0, 0, 0

    # Convert BGR image to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Green color range
    lower_green = np.array([25, 40, 40])
    upper_green = np.array([90, 255, 255])

    # Detect green plant areas
    mask = cv2.inRange(
        hsv,
        lower_green,
        upper_green
    )

    # Total image area
    total_pixels = mask.shape[0] * mask.shape[1]

    # Green pixels
    green_pixels = cv2.countNonZero(mask)

    # Green area percentage
    green_percentage = (
        green_pixels / total_pixels
    ) * 100

    # Approximate leaf/plant area
    leaf_area_percentage = green_percentage

    # Average hue of detected green areas
    if green_pixels > 0:

        average_hue = cv2.mean(
            hsv,
            mask=mask
        )[0]

    else:

        average_hue = 0

    return (
        green_percentage,
        average_hue,
        leaf_area_percentage
    )