import cv2

def capture_from_camera(save_path = "captured_food.jpg"):
        # Open a connection to the first webcam (0 = default camera)

    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        raise Exception("Could not access the webcam.")

    print("Camera opened. Point it at your food.")
    print("Press 'c' to capture, or 'q' to quit.")

    captured_path = None  # stays None if the user quits without capturing

    while True:
        # ok is True/False (did the read work?), frame is the image pixels
        ok, frame = cam.read()
        if not ok:
            cam.release()
            raise Exception("Failed to read from webcam.")

        # Show the live preview in a pop-up window
        cv2.imshow("Food Scanner - c to capture, q to quit", frame)

        # Wait 1 ms for a key press
        key = cv2.waitKey(1) & 0xFF

        if key == ord("c"):
            cv2.imwrite(save_path, frame)  # save the current frame to disk
            print(f"Photo captured and saved as {save_path}")
            captured_path = save_path
            break
        elif key == ord("q"):
            print("Capture cancelled.")
            break

    cam.release()            # give the webcam back to Windows
    cv2.destroyAllWindows()  # close the preview window

    return captured_path