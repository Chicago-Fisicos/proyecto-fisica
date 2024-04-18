import cv2
import cvzone
from cvzone.ColorModule import  ColorFinder

# Initialize the video
cap = cv2.VideoCapture('videos/1.mp4')

def detect_colour():
    hsvVals = 'red'
    myColorFinder = ColorFinder(True)
    while True:
        img = cv2.imread("basket.png")
        img_edit, mask = myColorFinder.update(img, hsvVals)

        # Show the photo
        cv2.imshow('Detect Colour', img_edit)

        # Speed of video
        cv2.waitKey(30)


def analyze_video():
    myColorFinder = ColorFinder(False)
    while True:
        success, img = cap.read()

        # Find the color ball
        imgColor, mask = myColorFinder.update(img, hsvVals)
        # Find location of the ball
        imgContours, contours = cvzone.findContours(img, mask, minArea=300, maxArea=900)


        # Display
        # Resize
        imgContours = cv2.resize(imgContours, (0,0), None, 1.5, 1.5)
        #cv2.imshow('Image', img)
        cv2.imshow('ImageColor', imgContours)

        # Speed of video
        cv2.waitKey(40)


#detect_colour()
hsvVals = {'hmin': 110, 'smin': 0, 'vmin': 62, 'hmax': 179, 'smax': 110, 'vmax': 115}

analyze_video()