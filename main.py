import cv2
import pytesseract

# mention the installed location of Tesseract-OCR in your system.
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


def main():
    print("Starting the program...")

    # Start Capturing the camera feed
    start_feed = True

    # Output text
    text = None

    # Get the camera port
    cam_port = 0

    # Open the camera
    cam = cv2.VideoCapture(cam_port)

    # Start a OpenCV window to display the camera feed
    cv2.namedWindow('Preview Feed')

    # Set the window size
    cv2.resizeWindow('Preview Feed', 640, 480)

    # Wait For Key Press
    cv2.waitKey(0)

    # Finished Loading OpenCV
    print("Finished loading OpenCV.")

    while True:
        # Read the camera feed
        ret, frame = cam.read()

        # If the camera feed is empty, break the loop
        if not ret:
            break

        # Start the camera feed
        if cv2.waitKey(1) & 0xFF == ord('s'):
            start_feed = not start_feed

        # Display the camera feed
        if start_feed:
            cv2.imshow('Preview Feed', frame)

        # Capture the image
        if cv2.waitKey(1) & 0xFF == ord('c'):
            image = capture_image(cam)
            cv2.imshow('Preview Feed', image)
            text = read_image()
            start_feed = False

        # Wait for the Q key to be pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    #  Destroy the window.
    cv2.destroyAllWindows()

    # Release the camera.
    cam.release()

    # Print the text
    print(text)


def capture_image(cam):
    result, image = cam.read()

    cv2.imwrite("label.jpg", image)

    if result:
        return image

    return None


def read_image():
    # Read the image
    image = cv2.imread("label.jpg")

    # Convert the image to gray scale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Remove the noise from the image
    noise = cv2.medianBlur(gray, 3)

    # Threshold the image
    thresh = cv2.threshold(noise, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    cv2.imwrite("thresh.jpg", thresh)

    # Configuration
    config = '-l eng --oem 3 --psm 3'

    # Use the Tesseract library to read the text from the image
    text = pytesseract.image_to_string(thresh, config=config)

    return text


if __name__ == "__main__":
    main()

