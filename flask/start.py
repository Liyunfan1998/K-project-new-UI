from flask import Flask, redirect, url_for, Response, render_template
from python.video2dpose import gen_frames

app = Flask(__name__)


@app.route('/')
def login():
    return render_template('login.php')


@app.route('/home')
def home():
    return render_template('home.php')


@app.route('/exercise')
def exercise():
    return render_template('exercise.php')


@app.route('/history')
def history():
    return 'Hello World'


@app.route('/instruction')
def instruction():
    return render_template('instruction.php')


# CV2 camera capture and mediapipe
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)  # docker
    # app.run(host='127.0.0.1', port='5002', debug=True)  # local
