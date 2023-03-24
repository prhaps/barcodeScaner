import cv2
from pyzbar import pyzbar
from time import sleep

# Initialize the camera
cap = cv2.VideoCapture(0)
interval = 1


while True:
    # Capture a frame from the camera
    # ret, frame = cap.read()
    frame = cv2.imread('test.png')

    # Decode the barcode from the frame
    barcodes = pyzbar.decode(frame)

    # Loop through all the barcodes found in the frame
    for barcode in barcodes:
        # Extract the barcode data and type
        barcode_data = barcode.data.decode('utf-8')
        barcode_type = barcode.type

        # Print the barcode data and type
        print(f"Barcode data: {barcode_data}, Barcode type: {barcode_type}")

    # Display the frame
    cv2.imshow('Barcode Scanner', frame)

    # Check for key press
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    sleep(interval)

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()