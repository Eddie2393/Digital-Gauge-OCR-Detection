import os
import cv2
import time
from picamera2 import Picamera2

#---- CONFIGURATION ----
save_base = "dataset"
class_id = 1  # 0 = measured, 1 = not_measured
classes = {
    0: "measured",
    1: "not_measured"
}
capture_interval = 1  # seconds
image_size = (640, 480)

# Prepare folders
label = classes[class_id]
image_folder = os.path.join(save_base, label, "images")
label_folder = os.path.join(save_base, label, "labels")
os.makedirs(image_folder, exist_ok=True)
os.makedirs(label_folder, exist_ok=True)

# Initialize camera
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"size": image_size}))
picam2.start()
time.sleep(1)

paused = False
print(f"Capturing '{label}' images every {capture_interval}s.")
print("Press 'p' to pause/resume, 'q' to quit.")

try:
    while True:
        frame = picam2.capture_array()
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        cv2.imshow("Capture Preview", frame_bgr)

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break
        elif key == ord("p"):
            paused = not paused
            state = "Paused" if paused else "Resumed"
            print(f"{state} capturing.")

        if not paused:
            # Determine next filename
            count = len([f for f in os.listdir(image_folder) if f.endswith(".jpg")])
            filename_base = f"{label}_{count+1:04d}"
            image_path = os.path.join(image_folder, f"{filename_base}.jpg")
            label_path = os.path.join(label_folder, f"{filename_base}.txt")

            # Save image and YOLO label
            cv2.imwrite(image_path, frame_bgr)
            with open(label_path, "w") as f:
                f.write(f"{class_id} 0.5 0.5 1.0 1.0\n")

            print(f"Saved: {image_path}")
            time.sleep(capture_interval)

finally:
    picam2.stop()
    cv2.destroyAllWindows()
    print("Stopped image capture.")
