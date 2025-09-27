import cv2

win = next(w for w in gw.getAllTitles() if "Chrome" in w or "Firefox" in w or "Brave" in w)
w = gw.getWindowsWithTitle(win)[0]
left, top, right, bottom = w.left, w.top, w.right, w.bottom
bbox = {"left": left, "top": top, "width": right-left, "height": bottom-top}

# 2) Grab frames and feed to OpenCV.
sct = mss.mss()
fps_ts = time.time()
frames = 0

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        # Extract the face ROI
        face_roi = frame[y:y+h, x:x+w]

        # Process the extracted face (e.g., save it, draw rectangle)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        # cv2.imwrite(f"face_{count}.jpg", face_roi) # Example: save each face

    cv2.imshow('Face Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()