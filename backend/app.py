##rest
from flask import Flask
import numpy as np
import io
from flask import Flask, jsonify, request 
from flask_restful import Resource, Api, reqparse
# from flask_ngrok import run_with_ngrok
from flask_cors import CORS, cross_origin
import logging
from utilities import *

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
# logging.getLogger('flask_cors').level = logging.DEBUG
app.logger.setLevel('INFO')
CORS(app)

api = Api(app)

@app.route('/caption', methods=['POST'])
def infer_image():
    pass
    
@app.route('/create_notes', methods=['POST'])
def create_notes():
    # Catch the image file from a POST request
    
    video_url = request.form.get("video_url")
    print(video_url)

    transcription,title = get_transcription(video_url)
    chunks = get_chunks(transcription['text'])

    summarries = []

    for para in chunks:
      summary = get_summary(para)
      summarries.append(summary)    

    # Return on a JSON format
    return {'transcription': transcription['text'],'title':title,'chunks':chunks,'summary': summarries }

@app.route('/', methods=['GET'])
def index():
    return 'Machine Learning Inference'

if __name__ == '__main__':
    app.run()