import cv2
from cvzone.ColorModule import ColorFinder

# video_speed:
    # lower = faster
    # higher = slower

# video_window_size. Library default = 1, but is very big
    # We can use 0.55 for notebooks
    # or 0.7 for big screen

def detect_colour(input_video, video_speed=20, video_window_size=0.7):
    # Initialize the video capture object
    cap = cv2.VideoCapture(input_video)
    colour_config = ""

    # Create a ColorFinder object for detecting color
    my_color_finder = ColorFinder(True)

    # Loop continuously until the user exits
    while True:
        # Read the next frame from the video
        success, img = cap.read()

        # Check if the frame was read successfully
        if not success:
            # If we've reached the end of the video, reset to the beginning
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue  # Loop the video

        # Update the color detection on the current frame
        img_edit, mask = my_color_finder.update(img, colour_config)

        # Resize the edited frame for display
        img_edit = cv2.resize(img_edit, (0, 0), None, video_window_size, video_window_size)

        # Show the edited frame with color detection
        cv2.imshow('Detect Colour', img_edit)

        # Check if the user pressed 'q' to quit
        if cv2.waitKey(video_speed) & 0xFF == ord('q'):
            break  # Exit the loop

    # Release the video capture object
    cap.release()

    # Close all OpenCV windows
    cv2.destroyAllWindows()
