from flask import Flask, render_template, Response
from camera import VideoCamera
import json

app = Flask(__name__)

@app.route('/api', methods=['GET'])
def api():
    return{
        'video': 'https://www.6connex.com/wp-content/uploads/virtual_events_and_environments_03.jpg'
    }

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route("/history")
def history():
    with open("messages.json", "r") as f:
        data = json.load(f)
    return data

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')