##rest
from flask import Flask
import numpy as np
import io
import os
from flask import Flask, jsonify, request 
from flask_restful import Resource, Api, reqparse
# from flask_ngrok import run_with_ngrok
from flask_cors import CORS, cross_origin
import logging
from utilities import *
from flask_bcrypt import Bcrypt
from flask_pymongo import PyMongo
from dotenv import load_dotenv


app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
# logging.getLogger('flask_cors').level = logging.DEBUG
app.logger.setLevel('INFO')
CORS(app)

api = Api(app)

load_dotenv()

app = Flask(__name__)
CORS(app)

bcrypt = Bcrypt(app)

app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
mongo = PyMongo(app)

# -----------DB Models start--------------------

Users = mongo.db.users
Transcriptions = mongo.db.transcriptions

# -----------DB Models end--------------------


# -----------APIs start--------------------

@app.route('/register',methods=['POST'])
def registerUser():
    try:
        data = request.get_json()
        obj = Users.find_one({'email': data['email']})
        if obj is None:
            obj = {
                'email': data['email'],
                'password': data['password'],
                'name': data['name'],
                'mobile': data['mobile'],
            }
            Users.insert_one(obj)
            return {
                'email': data['email'],
                'message': 'User Created Successfully'
            }, 200
        return {'message': 'User Alredy Exist'}, 401
    except Exception as e:
        return {'message': 'Server Error' + str(e)}, 500



@app.route('/login',methods=['POST'])
def loginUser():
    try:
        data = request.get_json()
        obj = Users.find_one({'email': data['email']})
        print("User : ",str(obj['_id']))

        if obj is None:
            return {'message': 'User doesn\'t exist.'}
        if obj['password'] == data['password']:
            return {
                'email': obj['email'],
                'user_id': str(obj['_id']),
                'user_name': obj['name'],
                'mobile': obj['mobile']
            }, 200
        return {"message": 'Invalid credentials'}, 401
    except Exception as e:
        return {'message': 'Server Error' + str(e)}, 500

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
    obj = {'title':str(title),'chunks':str(chunks),'summary': str(summarries) }
    Transcriptions.insert_one(obj)
    # Return on a JSON format
    print(obj)
    return obj


#get all users
@app.route('/users', methods=['GET'])
def get_users():
    obj = Users.find_one({'email': 'user@gmail.com'})

    return obj

if __name__ == '__main__':
    app.run(debug=True)