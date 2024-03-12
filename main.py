import cv2
import pytesseract
from colorama import Fore

# mention the installed location of Tesseract-OCR in your system.
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


def main():
    print("Starting the program...")

    # List of images
    image = ['label1.png', 'label2.png', 'label3.png']

    # Output text
    text_list = []

    # Finished Loading OpenCV
    print("Finished loading OpenCV.")

    # Number
    i = 0

    # Read the images
    for img in image:
        text = read_image(img)

        text_list.append(text)
        print(text_list[i])
        if i != len(image) - 1:
            print(f'{Fore.RED}New label:{Fore.WHITE}\n')
        i += 1


def read_image(img):
    image = cv2.imread(img)

    # Convert the image to gray scale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Remove the noise from the image
    noise = cv2.medianBlur(gray, 3)

    # Threshold the image
    thresh = cv2.adaptiveThreshold(noise, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY,11,2)

    cv2.imwrite("thresh.jpg", thresh)

    # Configuration
    config = '-l eng --oem 3 --psm 3'

    # Use the Tesseract library to read the text from the image
    text = pytesseract.image_to_string(thresh, config=config)

    return text


if __name__ == "__main__":
    main()

