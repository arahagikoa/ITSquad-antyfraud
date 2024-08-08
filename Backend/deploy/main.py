from models_main import MODEL
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import shutil
import uuid
from werkzeug.utils import secure_filename
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
CORS(app, resources={
    "/*": {"origins": ["*"]}
})
auth = HTTPBasicAuth()


users = {
    "bjson64": generate_password_hash("Test1")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username





#nlp_model_dir = r"C:\Users\olekm\OneDrive\Pulpit\ICFraud_github\ITSquad-antyfraud\Backend\saved_model"
#cnn_model_dir = r"C:\Users\olekm\OneDrive\Pulpit\ICFraud_github\ITSquad-antyfraud\Backend\CNN_MODEL"
#cnn_model_dir = r"E:\Projekty\for_work\ai-solution\ITSquad-antyfraud\Backend\CNN_MODEL"
nlp_model_dir = r"E:\Projekty\for_work\ai-solution\ITSquad-antyfraud\Backend\saved_model"
cnn_model_dir = r"C:\Users\kmlkr\OneDrive\Pulpit\praca\documents-ai\docs-det-all-nations\dit-baseDocument_Classification-ids-seria-16"

model = MODEL(nlp_model_dir, cnn_model_dir)

@app.route('/API/predict', methods=['POST'])
@auth.login_required
def predict():
    try:
        unq_id = uuid.uuid4()
        unique_dir = f'uploaded_images_{unq_id}'
        sorted_dir = f'sorted_images_{unq_id}'

        out_dir = os.path.join(os.getcwd(), sorted_dir)
        images_dir = os.path.join(os.getcwd(), unique_dir)

        os.makedirs(images_dir, exist_ok=True)
        os.makedirs(out_dir, exist_ok=True)

        # zapisujemy pliki które model otrzymuje do lokalnego unikalnego folderu
        model.unq_id = unq_id
        files = request.files.getlist('images')
        for file in files:
            filename = secure_filename(file.filename)
            file_path = os.path.join(images_dir, filename)
            file.save(file_path)
        
        # uniklany folder plików przekazujemy do funkcji main z backendu
        predicted_labels = model.main_function(images_dir)
        print("predicted labels (main)", predicted_labels)
        labels = predicted_labels[0]
        ocr_text = predicted_labels[1]
        for label_dict in predicted_labels[0]:
            for img_label, img_name in label_dict.items():
                if not os.path.exists(f"{out_dir}\\{img_label}"):
                    os.makedirs(f"{out_dir}\\{img_label}")
                shutil.move(img_name, f"{out_dir}\\{img_label}")


        shutil.rmtree(images_dir)

        if predicted_labels is not None:
            return jsonify({"message": "Successfully predicted labels for given images", "labels": labels, "ocr data": ocr_text}), 200
        else:
            return jsonify({"error": "Error during model prediction, please try again"}), 500
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/API/get_records', methods=['GET'])
@auth.login_required
def get_records():
    records = model.get_docs_text_labels()
    if records:
        return jsonify({"message": "Got records from last prediction", "records": records}), 200
    else:
        return jsonify({"message": "No records to obtain"}), 204

if __name__ == "__main__":
    app.run(port=5000, threaded=True)