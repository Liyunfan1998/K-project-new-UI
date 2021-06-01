import os
import time

from flask import Flask, Response, render_template, send_from_directory, request, redirect, url_for

from python.video2dpose import run

app = Flask(__name__)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('home'))
    return render_template('login.php', methods=['POST'])


@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.php', methods=['POST'])


@app.route("/change_label")
def change_label():
    print(request.headers.get('accept'))  # == 'text/event-stream':

    def change_text():
        while True:
            yield "data: %s\n\n" % str(time.time())
            time.sleep(.05)

    return Response(change_text(), content_type='text/event-stream')


@app.route('/exercise', methods=['GET', 'POST'])  #
def exercise():
    if request.method == 'POST':
        request.form
        # pain = request.form['pain']
        # imbalance = request.form['imbalance']
        # usingAssistiveDevices = request.form['usingAssistiveDevices']
        # try:
        #     movement = request.form['movement']
        # except:
        #     movement = None
        # print(pain, imbalance, usingAssistiveDevices, movement)
        print(request.form)
        # TODO: make a report and provide csv download links
        return redirect(url_for('home'))
    else:
        return render_template('exercise.php')


@app.route('/history', methods=['GET', 'POST'])
def history():
    return 'Hello World'


# CV2 camera capture and mediapipe
@app.route('/video_feed')
def video_feed():
    return Response(run(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    # app.run(host='0.0.0.0', debug=True)  # docker
    app.run(host='127.0.0.1', port='5002', debug=True)  # local
