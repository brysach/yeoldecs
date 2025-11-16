import cv2
#import numpy as np
from flask import Flask, render_template, Response, request

import gemini_api
from gemini_api import generateFantasyStory

app = Flask(__name__)

# Initialize the camera
# Using 0 for the default webcam. Change this if you have multiple cameras.
camera = cv2.VideoCapture(0)

image = 0
i = 0

def generate_frames():
    """Generator function to capture frames from the camera and yield them."""
    while True:
        # Read a frame from the camera
        success, frame = camera.read()
        if not success:
            print("Failed to grab frame")
            break
        else:
            # Encode the frame in JPEG format
            # .jpg is used for streaming as it's efficient
            frame = cv2.flip(frame, 1)
            ret, buffer = cv2.imencode('.jpg', frame)
            global image 
            image = frame

            if not ret:
                print("Failed to encode frame")
                continue
            
            # Convert the buffer to bytes
            frame_bytes = buffer.tobytes()
            
            # Yield the frame in the format required for multipart_x_mixed_replace
            # This format includes the boundary and content type
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            
def take_picture():
    global image, i
    print("taking a picture")
    output_path = "./images/img" + str(i) + ".png"
    success = cv2.imwrite(output_path, image)
    i += 1

def process_and_save():
    result = "TEMPORARY TESTING" #replace with actual data from AI
    with open("output.txt") as f:
        data = f.read()
    return render_template("index.html", storyData=data)



@app.route('/')
def index():
    """Serves the main HTML page that will display the video stream."""
    # render_template looks for files in the 'templates' folder
    return process_and_save()

@app.route('/video_feed')
def video_feed():
    """This is the endpoint that provides the video stream."""
    # Response is a special Flask object that can handle streams.
    # We pass our generator function to it.
    # The mimetype tells the browser this is a multipart stream.
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/take_picture_func")
def picture_taking_function():
    print("running")
    take_picture()
    return "pictures taken"

@app.route("/generate_story_func")
def story_generating_function():
    print("running")
    generateFantasyStory()
    return "story generated"


if __name__ == '__main__':
    # Run the app
    # host='0.0.0.0' makes it accessible on your network
    app.run(host='0.0.0.0', port=5002, debug=True)

# Note: When the Flask app stops, it doesn't automatically release the camera.
# You might need to handle this more gracefully in a production app,
# but for a simple demo, this is fine.
# A simple way to release is to add a shutdown route or use a context manager.
# For this example, restarting the script will release and re-acquire the camera.
