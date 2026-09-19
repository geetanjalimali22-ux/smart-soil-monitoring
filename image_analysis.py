import cv2
import numpy as np
def check_image_quality(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    brightness = np.mean(gray)
    sharpness = cv2.Laplacian(gray, cv2.CV_64F).var()

    if brightness < 35:
        return False, "Image is too dark."

    if sharpness < 50:
        return False, "Image is too blurry."

    return True, "Image quality is acceptable."


def analyze_plant_image(image_bytes):

    # Convert uploaded image into OpenCV image
    image_array = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    # Check whether image was loaded correctly
    if image is None:
        return 0, 0, 0
        quality_ok, quality_message = check_image_quality(image)

    # Resize large images for faster processing
    max_width = 1000

    height, width = image.shape[:2]

    if width > max_width:
        scale = max_width / width
        new_height = int(height * scale)

        image = cv2.resize(
            image,
            (max_width, new_height)
        )

    # Convert BGR to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Green color range
    lower_green = np.array([25, 40, 40])
    upper_green = np.array([90, 255, 255])

    # Detect green regions
    mask = cv2.inRange(
        hsv,
        lower_green,
        upper_green
    )

    # Remove small noise
    kernel = np.ones((5, 5), np.uint8)

    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_OPEN,
        kernel
    )

    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_CLOSE,
        kernel
    )

    # Find connected green regions
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(
        mask,
        connectivity=8
    )

    # Keep the largest green region
    leaf_mask = np.zeros_like(mask)

    if num_labels > 1:

        largest_label = 1
        largest_area = stats[1, cv2.CC_STAT_AREA]

        for label in range(2, num_labels):

            area = stats[label, cv2.CC_STAT_AREA]

            if area > largest_area:
                largest_area = area
                largest_label = label

        leaf_mask[labels == largest_label] = 255

    # Total image area
    total_pixels = leaf_mask.shape[0] * leaf_mask.shape[1]

    # Detected plant/leaf pixels
    leaf_pixels = cv2.countNonZero(leaf_mask)

    # Estimated visible plant area
    leaf_area_percentage = (
        leaf_pixels / total_pixels
    ) * 100

    # Overall green coverage
    green_pixels = cv2.countNonZero(mask)

    green_percentage = (
        green_pixels / total_pixels
    ) * 100

    # Average hue of detected plant region
    if leaf_pixels > 0:

        average_hue = cv2.mean(
            hsv,
            mask=leaf_mask
        )[0]

    else:

        average_hue = 0

    return (
        green_percentage,
        average_hue,
        leaf_area_percentage
    )