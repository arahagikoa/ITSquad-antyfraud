from models_main import MODEL
from flask import Flask, request, send_file, jsonify, send_from_directory
from flask_cors import CORS
import json
import os
import shutil

app = Flask(__name__)
CORS(app, resources={
    "/*": {"origins": ["*"]}
    })


nlp_model_dir = "/saved_model"
cnn_model_dir = "/CNN_MODEL"


model = MODEL(nlp_model_dir, cnn_model_dir)


model.login_hg()
model.initialize_nlp()
model.initialize_cnn()

@app.route('/API/predict', methods=['GET'])
def predict():
    try:
        data = request.json
        images = data.get('images')
        
        predicted_labels = model.main_function(images)
        if predicted_labels is not None:
            return jsonify({"message": "succesfully predicted labels for given images", "labels": predicted_labels}), 200
        else:
            return jsonify({"error": "error during model prediction, please try again"}), 500
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "Error during model prediction"}), 500

@app.route('/API/get_records', methods = ['GET'])
def get_records():
    records = model.get_docs_text_labels()
    if records:
        return jsonify({"message": "Got records from last prediction", "records": records}), 200
    
    else:
        return jsonify({"message": "No records to obtain"}), 204



if __name__ == "__main__":
    app.run(debug=True, port=5000)