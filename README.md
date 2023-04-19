Dominant Color Detection README

This script detects the dominant colors in a video feed and displays the color names and their approximate locations. The script uses OpenCV for video processing, NumPy for numerical calculations, scikit-learn for clustering, and webcolors for mapping RGB values to color names.
Installation

To run this script, you will need to have Python 3 installed on your system. You can download Python from the official website: https://www.python.org/downloads/

Next, you will need to install the required packages. You can do this by running the following command:

pip install opencv-python numpy scikit-learn webcolors

This will install the required packages:

    opencv-python: OpenCV library for image and video processing
    numpy: NumPy library for numerical calculations
    scikit-learn: Scikit-learn library for machine learning and clustering
    webcolors: Webcolors library for converting RGB values to color names

Running the script

Once the dependencies are installed, you can run the script using the following command in your terminal or command prompt:

python dominant_color_detection.py

Make sure the script (dominant_color_detection.py) is in your current working directory.
How it works

The script captures video from the default camera (usually the built-in webcam on a laptop or an external webcam). It processes the video frames, detecting the dominant colors in the image using the K-means clustering algorithm. The detected colors are then mapped to their closest CSS3 color names using the webcolors library. Finally, the color names and approximate locations are displayed on the video feed.

Press 'q' to quit the script.
