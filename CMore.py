import cv2
import numpy as np
from sklearn.cluster import KMeans
from collections import Counter
import webcolors

#this function converts from BGR to RGB format 
def bgr2rgb(color_bgr):
    return tuple(reversed(color_bgr))

#detects the 'k' dominant colors in an image using clustering. Returns a list of RGB tuples representing the dominant colors and dictionary of the color centroids
def detect_dominant_colors(image, k=5):
    original_shape = image.shape
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # reshape image to 1D array of pixels
    image = image.reshape((image.shape[0] * image.shape[1], 3))

    kmeans = KMeans(n_clusters=k, n_init=10)
    labels = kmeans.fit_predict(image)

    count_labels = Counter(labels)
    label_color_dict = {label: kmeans.cluster_centers_[label] for label in range(k)}
    dominant_colors = [color for _, color in sorted(label_color_dict.items(), key=lambda x: count_labels[x[0]], reverse=True)]

    reshaped_labels = labels.reshape(original_shape[0], original_shape[1])
    color_centroids = {label: np.mean(np.argwhere(reshaped_labels == label), axis=0) for label in range(k)}

    return [tuple(map(int, color)) for color in dominant_colors], color_centroids


#Converts an RGB color tuple to a color name. Uses the WEBCOLORS library to initiiate the conversion
def get_color_name(rgb_color):
    try:
        color_name = webcolors.rgb_to_name(rgb_color)
    except ValueError:
        # if the color is not recognized, find the closest color name
        min_colors = {}
        for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
            r_c, g_c, b_c = webcolors.hex_to_rgb(key)
            rd = (r_c - rgb_color[0]) ** 2
            gd = (g_c - rgb_color[1]) ** 2
            bd = (b_c - rgb_color[2]) ** 2
            min_colors[(rd + gd + bd)] = name
        color_name = min_colors[min(min_colors.keys())]

    return color_name


#Detects the dominant colors and displays their color names on the frame in a single video frame
def process_frame(frame):
    # detect the dominant colors and centroids in the frame
    dominant_colors, color_centroids = detect_dominant_colors(frame, k=5)

    # loop through each dominant color and display its name and centroid on the frame
    for i, color in enumerate(dominant_colors):
        rgb_color = bgr2rgb(color)
        color_name = get_color_name(rgb_color)
        # set the text position for the color name
        text_position = (10, 40 * (i + 1))
        cv2.putText(frame, f"{color_name}", text_position, cv2.FONT_HERSHEY_SIMPLEX, 1, rgb_color, 2)

        centroid_x, centroid_y = color_centroids[i]
        centroid_x = int(centroid_x)
        centroid_y = int(centroid_y)
        cv2.circle(frame, (centroid_y, centroid_x), 50, rgb_color, 3)

    return frame

#Main function of the script. Captures video frames, processing them using function proccess_frame above.
def main():

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    frame_count = 0
    last_processed_frame = None
    while True:
        ret, frame = cap.read()
        frame_count += 1
        
        # If the frame was not read successfully, break out of the loop
        if not ret:
            break

        if frame_count % 10 == 0:
            last_processed_frame = process_frame(frame)

        if last_processed_frame is not None:
            cv2.imshow('Color Detection', last_processed_frame)
        else:
            cv2.imshow('Color Detection', frame)

         # Exit the loop if the user presses 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
