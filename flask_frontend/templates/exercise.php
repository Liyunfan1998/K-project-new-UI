<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css"
          integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
    <title>Exercise</title>
    <style>
        div {
            display: table;
            margin-right: auto;
            margin-left: auto;
        }

        table, th, td {
            border: 1px solid black;
            border-collapse: collapse;
        }
    </style>
    <script type="text/javascript">
        function setVideoLink(movementName) {
            let pose_url_dict = new Map();
            pose_url_dict.set("squat", "{{ url_for('static', filename='Assets/0002深蹲测试（deep squat）[1080P].h264.mp4') }}");
            pose_url_dict.set("hurdle", "{{ url_for('static', filename='Assets/0003跨栏测试（hurdle step）[1080P].h264.mp4') }}");
            pose_url_dict.set("raiseLeg", "{{ url_for('static', filename='Assets/0006主动直腿抬高（active straight leg raise）[1080P].h264.mp4') }}");
            document.getElementById("instructionVideo").src = pose_url_dict.get(movementName);
        }

        if (!!window.EventSource) {
            let source = new EventSource('/change_label');
            source.onmessage = function (e) {
                // console.log(e.data);
                document.getElementById("time").innerHTML = e.data;
            }
        }
    </script>

</head>
<body>
<!--<div style="width:1280px; margin:0 auto;">-->
<!--</div>-->
<div>
    <table>
        <tr>
            <td>
                <form action="{{ url_for('exercise') }}" name="reportIssues" method="post"
                      id="reportIssues">
                    <table>
                        <tr>
                            <td width="50%">
                                <h4>Choose FMS movement:</h4><br>
                                <input type="radio" id="squat" name="movement" value="squat"
                                       onclick="setVideoLink('squat')" checked>
                                <label for="squat">Squat</label><br>
                                <input type="radio" id="hurdle" name="movement" value="hurdle"
                                       onclick="setVideoLink('hurdle')">
                                <label for="hurdle">Hurdle</label><br>
                                <input type="radio" id="raiseLeg" name="movement" value="raiseLeg"
                                       onclick="setVideoLink('raiseLeg')">
                                <label for="raiseLeg">Raise Leg</label><br>
                            </td>
                            <td width="50%">
                                <h4>Report the following:</h4><br>
                                <input type="checkbox" id="pain" name="pain" value="pain">
                                <label for="pain">Pain</label><br>
                                <input type="checkbox" id="imbalance" name="imbalance" value="imbalance">
                                <label for="imbalance">Imbalance</label><br>
                                <input type="checkbox" id="usingAssistiveDevices" name="usingAssistiveDevices"
                                       value="usingAssistiveDevices">
                                <label for="usingAssistiveDevices">Using Assistive Devices</label><br>

                            </td>
                        </tr>
                        <tr>
                            <td>
                                <input type="submit" value="Report">
                            </td>
                        </tr>
                    </table>
                </form>
            </td>
            <td>
                <label id="time">
                    {{ url_for('change_label') }}
                </label>
            </td>
        </tr>
        <tr>
            <td>
                <div>
                    <h3 class="mt-5">Live Streaming</h3>
                    <img src="{{ url_for('video_feed') }}" height=550px>
                </div>
            </td>
            <td>
                <div>
                    <h3 class="mt-5">Video Instructions</h3>
                    <video height=550px controls id="instructionVideo" autoplay>
                        <source src="{{ url_for('static', filename='Assets/0002深蹲测试（deep squat）[1080P].h264.mp4') }}"
                                type="video/mp4">
                    </video>
                </div>
            </td>
        </tr>
    </table>
</div>

</body>
</html>