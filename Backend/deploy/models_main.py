import torch
from huggingface_hub import login
import os
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoFeatureExtractor, AutoModelForImageClassification, LlamaForSequenceClassification
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
from pdf_ocr import extract_text_from_images
from peft import PeftModel, PeftConfig
import tempfile
import uuid
from torchvision.transforms import Resize, ToTensor, Normalize, Compose
import predict_new
import ocr
from pdf_ocr import extract_text_from_images
import shutil
class MODEL:
    def __init__(self, nlp_model_dir, cnn_model_dir) -> None:
        self.hg_login = "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"
        self.NLP_MODEL_DIR = nlp_model_dir
        self.CNN_MODEL_DIR = cnn_model_dir
        self.tokenizer_nlp = None
        self.cnn_feature_extractor = None
        self.cnn_model = None
        self.nlp_tokenizer = None
        self.nlp_model = None
        self.list_text_class = None
        self.tokenizer = None
        self.unq_id = None
        self.login_hg()
        # self.initialize_nlp()
        self.initialize_cnn()

    def login_hg(self)->None:
        login(self.hg_login)

    def initialize_nlp(self)->None:
        if os.name =='nt':
            local_path = r"C:\Users\olekm\OneDrive\Pulpit\ICFraud_github\ITSquad-antyfraud\Backend\saved_model"
            local_path = r"C:\Users\olekm\OneDrive\Pulpit\ICFraud_github\ITSquad-antyfraud\Backend\saved_model"

            peft_config = PeftConfig.from_pretrained(local_path)
            offload_dir = "./model_offload"
            base_model = AutoModelForSequenceClassification.from_pretrained(
                peft_config.base_model_name_or_path,
                num_labels=4,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                device_map="auto" if torch.cuda.is_available() else None,
                offload_folder=offload_dir
            )

            tokenizer = AutoTokenizer.from_pretrained(peft_config.base_model_name_or_path)

            # Set the padding token
            tokenizer.pad_token = tokenizer.eos_token
            base_model.config.pad_token_id = tokenizer.eos_token_id

            nlp_model = PeftModel.from_pretrained(base_model, local_path)
            nlp_model.eval()

            self.nlp_model = nlp_model
            self.tokenizer = tokenizer
        
        else:
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.bfloat16
            )
            peft_config = PeftConfig.from_pretrained(self.NLP_MODEL_DIR)

            nlp_model = AutoModelForSequenceClassification.from_pretrained(
                peft_config.base_model_name_or_path,
                num_labels=4,
                quantization_config=bnb_config,
                device_map="auto"
            )

            tokenizer = AutoTokenizer.from_pretrained(peft_config.base_model_name_or_path)

            # Set the padding token
            tokenizer.pad_token = tokenizer.eos_token
            nlp_model.config.pad_token_id = tokenizer.eos_token_id

            self.tokenizer = tokenizer

            nlp_model = PeftModel.from_pretrained(nlp_model, self.NLP_MODEL_DIR)

            nlp_model.eval()

            self.nlp_model = nlp_model

        self.nlp_model.eval()

    def initialize_cnn(self) ->None:
        model = AutoModelForImageClassification.from_pretrained(self.CNN_MODEL_DIR)
        feature_extractor = AutoFeatureExtractor.from_pretrained(self.CNN_MODEL_DIR)
        self.cnn_model = model
        self.cnn_feature_extractor = feature_extractor

    def cnn_model_function(self, images_dir) -> list:
        if not os.path.exists(images_dir):
            print("Provided path is incorrect")
            return []

        image_paths = [os.path.join(images_dir, filename) for filename in os.listdir(images_dir)]
        output_list = []
        document_labels = []

        # Define image preprocessing
        preprocess = Compose([
            Resize((224, 224)),
            ToTensor(),
            Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        ocr_dir = f"./data_extraction_{self.unq_id}"
        sorted_dir = f"./sorted_images_{self.unq_id}"


        if not os.path.exists(ocr_dir):
            os.makedirs(ocr_dir)
        if not os.path.exists(sorted_dir):
            os.makedirs(sorted_dir)


        for path in image_paths:
            try:
                image = Image.open(path).convert('RGB')
                
                # Preprocess the image
                input_tensor = preprocess(image)
                input_batch = input_tensor.unsqueeze(0)  # Create a mini-batch as expected by the model

                # Move the input to the same device as the model
                input_batch = input_batch.to(next(self.cnn_model.parameters()).device)

                # Forward pass
                with torch.no_grad():
                    outputs = self.cnn_model(input_batch)

                logits = outputs.logits
                predicted_label = logits.argmax(-1).item()

                label_mapping = {0: 'id', 1: 'idObcy', 2: 'inne', 3: 'paszport', 4: 'paszportObcy', 5: 'prawoJazdy', 6: 'prawoJazdyObce'}
                predicted_class_name = label_mapping[predicted_label]

                document_labels.append({predicted_class_name: path})
            
                
                
                
                for json_obj in document_labels:
                    for key, value in json_obj.items():
                        if key == "idObcy" or key == "id":

                            image = Image.open(value)
                            
                            img_save_path = os.path.join(ocr_dir, os.path.basename(value))
                            image.save(img_save_path)

            
            except Exception as e:
                print(f"Error processing {path}: {e}")


            print(ocr_dir)
            predict_new.main(ocr_dir, self.unq_id)
            # zapisane

            #perform OCR
            cnn_dir = f"./extracted_data_{self.unq_id}"
            ocr_images = os.listdir(cnn_dir)
            for image in ocr_images:
                image_path = os.path.join(cnn_dir, image)
                # os.makedirs("./preprocessed_images")
                ocr.preprocess_image_for_ocr(image_path, f"./preprocessed_images/{image}")
            
            list_with_data = ocr.perform_ocr_on_preprocessed_images("./preprocessed_images")
            print(list_with_data)
            # document_labels.append(list_with_data)

            for img in os.listdir(ocr_dir):
                img_path = os.path.join(ocr_dir, img)
                if os.path.isfile(img_path):
                    os.remove(img_path)

            os.rmdir(ocr_dir)
        output_list.append(document_labels)
        output_list.append(list_with_data)
        return output_list


    def predict_sentiment(self, text)->int:
        
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512, padding=True)
        
        inputs = {k: v.to(self.nlp_model.device) for k, v in inputs.items()}

        with torch.no_grad():
            outputs = self.nlp_model(**inputs)
            logits = outputs.logits

        predicted_class_id = logits.argmax().item()

        return predicted_class_id

    def nlp_model_function(self, images_dir)->list:
        document_labels = self.cnn_model_function(images_dir)
        #print(document_labels)
        
        values_for_unknown_label = [entry for entry in document_labels if 'inne' in entry]
        #print(values_for_unknown_label)

        nlp_dictionary = []
        list_text = []
        label_mapping = {0: 'notatka_policyjna', 1: 'Oswiadczenie_kolizyjne', 2: 'ekspertyza_likwidatora', 3: 'Nieznany'}

        if len(values_for_unknown_label) > 0:
            for entry in values_for_unknown_label:
                path = list(entry.values())[0]
                #print(path)
                text_from_image = extract_text_from_images([path])
                #print(text_from_image)
                #predicted_class = self.predict_sentiment(text_from_image)
                #list_text.append((text_from_image, predicted_class))
                #print(predicted_class)
                #nlp_dictionary.append({
                #    label_mapping[predicted_class]:path
                #})

            document_labels_new = [entry for entry in document_labels if 'inne' not in entry]

            for item in nlp_dictionary:
                document_labels_new.append(item)

            self.list_text_class = document_labels_new

            return document_labels_new

        else:
            return document_labels
        
    def get_docs_text_labels(self)->list:
        if self.list_text_class is not None:
            return self.list_text_class
        
        return None
    def main_function(self, images_dir)->list:
        dane = self.nlp_model_function(images_dir)
        print(dane)
        return dane