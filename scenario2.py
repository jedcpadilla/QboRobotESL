import cv2
import serial
import time
from QboCmd import Controller  # Import Controller from QboCmd module

port = '/dev/serial0'

# Open serial port
ser = serial.Serial(port, baudrate=115200, bytesize=serial.EIGHTBITS, stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE, rtscts=False, dsrdtr=False, timeout=0)
print("Opened serial port successfully.")
print(ser.name)

QBO = Controller(ser)

# Initialize the camera
camera = cv2.VideoCapture(0)

# Initialize ArUco parameters and dictionary for 6x6 markers
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
parameters = cv2.aruco.DetectorParameters_create()

try:
    while True:
        # Capture a frame from the camera
        ret, frame = camera.read()

        if not ret:
            print("Failed to capture image")
            break

        # Detect ArUco markers
        corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(frame, aruco_dict, parameters=parameters)

        if ids is not None:
            for i, id in enumerate(ids):
                if id[0] == 0:
                    print("Detected Marker UP")
                    QBO.SetServo(2, 380, 100)
                    time.sleep(1)
                    QBO.SetServo(2, 530, 100)
                    time.sleep(1)
                    QBO.SetServo(1, 500, 100)
                    time.sleep(1)
                elif id[0] == 2:
                    print("Detected Marker RIGHT")
                    QBO.SetServo(1, 725, 100)
                    time.sleep(1)
                    QBO.SetServo(2, 530, 100)
                    time.sleep(1)
                    QBO.SetServo(1, 500, 100)
                    time.sleep(1)
                elif id[0] == 1:
                    print("Detected Marker LEFT")
                    QBO.SetServo(1, 210, 100)
                    time.sleep(1)
                    QBO.SetServo(2, 530, 100)
                    time.sleep(1)
                    QBO.SetServo(1, 500, 100)
                    time.sleep(1)
                elif id[0] == 3:
                    print("Detected Marker SMILE")
                    QBO.SetMouth(0x110E00)
                    time.sleep(2)
                    QBO.SetMouth(0)
                    time.sleep(1)
                    QBO.SetServo(1, 500, 100)
                    time.sleep(1)

        # Display the image
        cv2.imshow('frame', frame)

        # Press 'q' to quit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    camera.release()
    cv2.destroyAllWindows()
    ser.close()
