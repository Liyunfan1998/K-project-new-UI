<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.1.0/css/bootstrap.css'>
    <link rel='stylesheet' href='https://maxcdn.bootstrapcdn.com/font-awesome/4.1.0/css/font-awesome.min.css'>
    <link rel="stylesheet" href="{{ url_for('static',filename='Styles/home.css') }}">
    <link rel="shortcut icon" href="{{ url_for('static', filename='favicon.ico') }}">
    <title>Home</title>
    <style>
        div {
            display: table;
            margin-right: auto;
            margin-left: auto;
        }
    </style>
</head>
<body>
<div style="text-align:center">
    <table style="width:200%;margin:auto">
        <tr>
            <td><h3 class="mt-5">Home</h3><br><br></td>
        </tr>
        <tr>
            <td>
                <div class="calendar calendar-first" id="calendar_first">
                    <div class="calendar_header">
                        <button class="switch-month switch-left"><i class="fa fa-chevron-left"></i></button>
                        <h2></h2>
                        <button class="switch-month switch-right"><i class="fa fa-chevron-right"></i></button>
                    </div>
                    <div class="calendar_weekdays"></div>
                    <div class="calendar_content"></div>
                </div>
            </td>
        </tr>
        <tr>
            <td>
                <br><br><br>
                <br><br><br>
                <a href="{{ url_for('exercise') }}">
                <button style="width:200px;margin:auto">exercise</button>
                </a>
                <br><br><br>
                <a href="{{ url_for('history') }}">
                <button style="width:200px;margin:auto">history</button>
                </a>
                </td>
        </tr>
    </table>
</div>

<script src='https://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.3/jquery.min.js'></script>
<script src='https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.1.0/js/bootstrap.min.js'></script>
<script src="{{ url_for('static',filename='Js/home.js') }}"></script>
</body>
</html>