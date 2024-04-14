import cv2

def capture_image_from_webcam():
    # Initialize the webcam (0 is the default camera)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    # Capture a single frame
    ret, frame = cap.read()

    if not ret:
        print("Error: Could not read frame from webcam.")
        return

    # Save the captured image to a file
    cv2.imwrite('webcam_capture.jpg', frame)

    # Display the captured image in a window
    cv2.imshow('Captured Image', frame)

    # Wait for a key press and close the window
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Release the webcam
    cap.release()

if __name__ == "__main__":
    capture_image_from_webcam()
