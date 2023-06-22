from flask import Flask, request, make_response
from flask_cors import CORS, cross_origin
import subprocess as sb
from datetime import datetime as dt
import os
import json

app = Flask(__name__)


@app.route('/api', methods=['POST'])
def post():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "http://nak-13:3000")
    # response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
    try:
        form_type = request.form["type"]
        
        if form_type == "upscaler":
            scale_amount = request.form["scaleAmount"]
            coordinates = request.files["coordinateFile"]
            time = dt.now().strftime("%d-%m-%Y_%H:%M:%S")
            coordinates_name = f"coordinates_{time}.txt"
            coordinates.save(coordinates_name)


            
            result = sb.run(["python3", "../virtual_microscope.py", "upres", coordinates_name, "out_file.txt", scale_amount])
            # todo: async calls with subproccess.Popen? or raw with exec
            if result.returncode == 0:
                result = sb.run(["python3", "../virtual_microscope.py", "viewer", "out_file.txt"])
                
                if os.path.isfile("../test.html"):
                    with open("../test.html", "r") as html:
                        text = "".join(html.readlines())
                        response.data = json.dumps({"html": text})
                        response.content_type = "application/json"
                        
                    os.remove(coordinates_name)
                        
            
        elif form_type == "generator":
            config = request.files["configFile"]
            time = dt.now().strftime("%d-%m-%Y_%H:%M:%S")
            config_name = f"config_{time}"
            config.save(config_name)

            result = sb.run(["python3", "../virtual_microscope.py", "generator", config_name])
            if result.returncode == 0:
                pass
            # async call the generator
            
            # should call the viewer?
            
        elif form_type == "viewer":
            coordinates = request.files["coordinateFile"]
            
            # async call viewer
    except KeyError as e:
        response.status_code = 400
        return response
    response.status_code = 200
    return response

if __name__ == '__main__':
    app.run(debug=True, port=5000)