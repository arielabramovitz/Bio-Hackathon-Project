from flask import Flask, request, make_response, jsonify
from flask_cors import CORS, cross_origin
import subprocess as sb

app = Flask(__name__)

@app.route('/', methods=['GET'])
def test():
    response = make_response()
    response.status_code = 200
    return response

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
            coordinates.save("input_file.txt")


            
            result = sb.run(["python3", "../virtual_microscope.py", "upres", "input_file.txt", "out_file.txt", scale_amount])
            # todo: async calls with subproccess.Popen? or raw with exec
            if result.returncode == 0:
                result = sb.run(["python3", "../virtual_microscope.py", "viewer", "out_file.txt"])
            # async call the upscaler
            
            # async call the viewer with results of upscaler
            
            # parse generated html
            
        elif form_type == "generator":
            config = request.files["configFile"]
            
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