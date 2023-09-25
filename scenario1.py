#images work with delay, with overlays plays on qbo speakers

import cv2
import cv2.aruco as aruco
import pygame
import time
import numpy as np
import os 

# Define ArUco marker IDs (6x6) and their corresponding actions (text and audio)
aruco_actions = {
    0: {"text": "Marker 0 Text", "audio": "0.mp3"},
    1: {"text": "Marker 1 Text", "audio": "1.mp3"},
    2: {"text": "Marker 2 Text", "audio": "2.mp3"},
}

# Initialize Pygame for audio playback
pygame.mixer.init()

# Initialize the camera
cap = cv2.VideoCapture(0)

# Create an ArUco dictionary
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)

# Dictionary to keep track of the last time audio was played for each marker
last_played = {}

while True:
    ret, frame = cap.read()
    corners, ids, _ = aruco.detectMarkers(frame, aruco_dict)

    current_time = time.time()

    if ids is not None:
        aruco.drawDetectedMarkers(frame, corners)

        for i in range(len(ids)):
            marker_id = ids[i][0]

            if marker_id in aruco_actions:
                action = aruco_actions[marker_id]
                marker_text = action["text"]
                audio_filename = action["audio"]

                print('{}'.format(marker_id))
                # Check if audio is already playing
                if not pygame.mixer.music.get_busy():
                    # Check if enough time has passed since the last time the audio was played
                    if marker_id not in last_played or current_time - last_played[marker_id] >= 10:
                        os.system("mpg123 -a hw:1,0 " + audio_filename)  # Play the audio on Qbo
                        last_played[marker_id] = current_time  # Update the last played time

                # Load the corresponding image for the detected ArUco marker
                overlay_image = cv2.imread('{}.jpg'.format(marker_id))

                # Get the coordinates for the four corners of the ArUco marker
                corner = corners[i][0].astype(np.float32)

                # Define points for warp perspective
                pts_dst = np.array(corner, dtype=np.float32)
                h, w, _ = overlay_image.shape
                pts_src = np.array([[0, 0], [w - 1, 0], [w - 1, h - 1], [0, h - 1]], dtype=np.float32)

                # Calculate the perspective transform matrix
                M = cv2.getPerspectiveTransform(pts_src, pts_dst)

                # Warp the image
                warped_image = cv2.warpPerspective(overlay_image, M, (frame.shape[1], frame.shape[0]))

                # Create a mask for the warped image
                mask = np.zeros((frame.shape[0], frame.shape[1]), dtype=np.uint8)
                cv2.fillConvexPoly(mask, corner.astype(np.int32), 1)
                mask = mask.astype(bool)

                # Overlay the image
                np.copyto(frame, warped_image, where=mask[:, :, None].astype(bool))

    cv2.imshow('ArUco Marker Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


