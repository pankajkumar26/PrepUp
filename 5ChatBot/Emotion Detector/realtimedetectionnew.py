import cv2
from keras.models import model_from_json
import numpy as np
import time
from imutils.video import VideoStream
from collections import Counter

# Load the emotion detector model
json_file = open("emotiondetector.json", "r")
model_json = json_file.read()
json_file.close()
model = model_from_json(model_json)
model.load_weights("emotiondetector.h5")

# Load the face cascade classifier
haar_file = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(haar_file)

def extract_features(image):
    feature = np.array(image)
    feature = feature.reshape(1, 48, 48, 1)
    return feature / 255.0

# Get user input for session time
session_time = int(input("Enter the session time in seconds: "))

# Start the webcam
print("Starting session. Smile for the camera!")
webcam = VideoStream(src=0).start()
time.sleep(2.0)  # Allow the camera to warm up

# Labels for emotion classes
labels = {0: 'angry', 1: 'disgust', 2: 'fear', 3: 'happy', 4: 'neutral', 5: 'sad', 6: 'surprise'}

# Variables for tracking facial expression changes
expression_changes = 0
start_time = time.time()

# List to store detected emotions during the session
detected_emotions = []

while time.time() - start_time < session_time:
    # Read a frame from the webcam
    im = webcam.read()
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(im, 1.3, 5)

    try:
        for (p, q, r, s) in faces:
            # Extract and preprocess the face image
            image = gray[q:q + s, p:p + r]
            cv2.rectangle(im, (p, q), (p + r, q + s), (255, 0, 0), 2)
            image = cv2.resize(image, (48, 48))
            img = extract_features(image)

            # Make emotion prediction
            pred = model.predict(img)
            prediction_label = labels[pred.argmax()]

            # Display the predicted emotion
            cv2.putText(im, '%s' % (prediction_label), (p - 10, q - 10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 0, 255))

            # Count facial expression changes
            expression_changes += 1

            # Store detected emotions
            detected_emotions.append(prediction_label)

        # Display the frame
        cv2.imshow("Output", im)
        cv2.waitKey(1)

    except cv2.error:
        pass

# Stop the webcam and calculate session duration
webcam.stop()
cv2.destroyAllWindows()

# Calculate the average facial expression changes per minute
average_changes_per_minute = expression_changes / (session_time / 60)

# Generate and display the report
print("Session Over. Here's your report:")
report = f"Duration: {session_time} seconds\nFacial Expression Changes: {expression_changes}\n" \
         f"Average Changes Per Minute: {average_changes_per_minute:.2f}\n"

# Most frequent emotion during the session
most_frequent_emotion = Counter(detected_emotions).most_common(1)
if most_frequent_emotion:
    report += f"Most Frequent Emotion: {most_frequent_emotion[0][0]}\n"
else:
    report += "No emotions detected during the session.\n"

print(report)
