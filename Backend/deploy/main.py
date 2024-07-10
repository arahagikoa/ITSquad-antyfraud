from models_main import MODEL
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import shutil
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app, resources={
    "/*": {"origins": ["*"]}
})

nlp_model_dir = r"C:\Users\olekm\OneDrive\Pulpit\ICFraud_github\ITSquad-antyfraud\Backend\saved_model"
cnn_model_dir = r"C:\Users\olekm\OneDrive\Pulpit\ICFraud_github\ITSquad-antyfraud\Backend\CNN_MODEL"

model = MODEL(nlp_model_dir, cnn_model_dir)

@app.route('/API/predict', methods=['POST'])
def predict():
    try:
        unique_dir = f'uploaded_images_{uuid.uuid4()}'
        images_dir = os.path.join(os.getcwd(), unique_dir)
        os.makedirs(images_dir, exist_ok=True)

        files = request.files.getlist('images')
        for file in files:
            filename = secure_filename(file.filename)
            file_path = os.path.join(images_dir, filename)
            file.save(file_path)
        
        predicted_labels = model.main_function(images_dir)
        
        shutil.rmtree(images_dir)

        if predicted_labels is not None:
            return jsonify({"message": "Successfully predicted labels for given images", "labels": predicted_labels}), 200
        else:
            return jsonify({"error": "Error during model prediction, please try again"}), 500
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/API/get_records', methods=['GET'])
def get_records():
    records = model.get_docs_text_labels()
    if records:
        return jsonify({"message": "Got records from last prediction", "records": records}), 200
    else:
        return jsonify({"message": "No records to obtain"}), 204

if __name__ == "__main__":
    app.run(debug=False, port=5000, threaded=True)