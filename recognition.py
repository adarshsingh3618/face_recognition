import cv2
import face_recognition
import os
import numpy as np
import time
from attendance import mark_attendance

IMAGES_PATH = "images"


def load_known_faces():
    known_encodings = []
    student_names = []

    if not os.path.exists(IMAGES_PATH):
        os.makedirs(IMAGES_PATH)

    for root, dirs, files in os.walk(IMAGES_PATH):
        for file in files:
            if file.endswith(('.jpg', '.png', '.jpeg')):
                img_path = os.path.join(root, file)
                img = cv2.imread(img_path)
                if img is None:
                    continue

                rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                enc = face_recognition.face_encodings(rgb_img)

                if enc:
                    known_encodings.append(enc[0])
                    rel = os.path.relpath(img_path, IMAGES_PATH)
                    parts = rel.split(os.sep)
                    student_name = parts[0] if len(parts) > 1 else os.path.splitext(file)[0]
                    student_names.append(student_name)

    return known_encodings, student_names


def draw_status_panel(frame, messages):
    panel_width = 500   
    h, w, _ = frame.shape
    panel = np.zeros((h, panel_width, 3), dtype=np.uint8)

    y = 40
    for msg in messages[-10:]:
        color = (0, 255, 0) if "✅" in msg else (0, 255, 255)
        cv2.putText(panel, msg, (10, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)  
        y += 40  

    return np.hstack((frame, panel))


if __name__ == "__main__":
    encodings, names = load_known_faces()
    cap = cv2.VideoCapture(0)

    marked = set()
    status_messages = ["System ready..."]

    detected_name = None
    detection_time = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # If already detected, skip detection for 2 seconds
        if detected_name is None:

            small = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)

            locations = face_recognition.face_locations(rgb_small)
            encodings_frame = face_recognition.face_encodings(rgb_small, locations)

            for enc, loc in zip(encodings_frame, locations):
                matches = face_recognition.compare_faces(encodings, enc)
                distances = face_recognition.face_distance(encodings, enc)

                name = "Unknown"
                if len(distances) > 0:
                    best = np.argmin(distances)
                    if matches[best]:
                        name = names[best]

                # draw rectangle & name
                top, right, bottom, left = [v * 4 for v in loc]
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, name, (left, top - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

                if name != "Unknown":
                    detected_name = name
                    detection_time = time.time()      # Start 2-second timer
                    status_messages.append(f"Detected {name}. Holding for confirmation...")

        else:
            # Draw detected name again
            status_messages.append(f"Confirming {detected_name}...")

            # Wait 2 seconds with camera still ON
            if time.time() - detection_time >= 2:

                # Now mark attendance
                if detected_name not in marked:
                    mark_attendance(student_id=detected_name, student_name=detected_name)
                    marked.add(detected_name)
                    status_messages.append(f"Attendance marked for {detected_name} ✅ ")
                else:
                    status_messages.append(f"Attendance already marked for {detected_name} ⚠️")

                # show for 3 seconds
                final_frame = draw_status_panel(frame, status_messages)
                cv2.imshow("Face Recognition Attendance", final_frame)
                cv2.waitKey(3000)
                break

        # show panel
        display = draw_status_panel(frame, status_messages)
        cv2.imshow("Face Recognition Attendance", display)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
