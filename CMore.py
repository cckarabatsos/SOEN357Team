import cv2
import numpy as np
from sklearn.cluster import KMeans
from collections import Counter
import webcolors

def bgr2rgb(color_bgr):
    return tuple(reversed(color_bgr))

def detect_dominant_colors(image, k=5):
    original_shape = image.shape
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    image = image.reshape((image.shape[0] * image.shape[1], 3))

    kmeans = KMeans(n_clusters=k, n_init=10)
    labels = kmeans.fit_predict(image)

    count_labels = Counter(labels)
    label_color_dict = {label: kmeans.cluster_centers_[label] for label in range(k)}
    dominant_colors = [color for _, color in sorted(label_color_dict.items(), key=lambda x: count_labels[x[0]], reverse=True)]

    reshaped_labels = labels.reshape(original_shape[0], original_shape[1])
    color_centroids = {label: np.mean(np.argwhere(reshaped_labels == label), axis=0) for label in range(k)}

    return [tuple(map(int, color)) for color in dominant_colors], color_centroids

def get_color_name(rgb_color):
    try:
        color_name = webcolors.rgb_to_name(rgb_color)
    except ValueError:
        min_colors = {}
        for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
            r_c, g_c, b_c = webcolors.hex_to_rgb(key)
            rd = (r_c - rgb_color[0]) ** 2
            gd = (g_c - rgb_color[1]) ** 2
            bd = (b_c - rgb_color[2]) ** 2
            min_colors[(rd + gd + bd)] = name
        color_name = min_colors[min(min_colors.keys())]

    return color_name

def process_frame(frame):
    dominant_colors, color_centroids = detect_dominant_colors(frame, k=5)

    for i, color in enumerate(dominant_colors):
        rgb_color = bgr2rgb(color)
        color_name = get_color_name(rgb_color)
        text_position = (10, 40 * (i + 1))
        cv2.putText(frame, f"{color_name}", text_position, cv2.FONT_HERSHEY_SIMPLEX, 1, rgb_color, 2)

        centroid_x, centroid_y = color_centroids[i]
        centroid_x = int(centroid_x)
        centroid_y = int(centroid_y)
        cv2.circle(frame, (centroid_y, centroid_x), 50, rgb_color, 3)

    return frame


def main():

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    frame_count = 0
    last_processed_frame = None
    while True:
        ret, frame = cap.read()
        frame_count += 1

        if not ret:
            break

        if frame_count % 10 == 0:
            last_processed_frame = process_frame(frame)

        if last_processed_frame is not None:
            cv2.imshow('Color Detection', last_processed_frame)
        else:
            cv2.imshow('Color Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()"