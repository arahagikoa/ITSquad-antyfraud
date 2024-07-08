import torch
from huggingface_hub import login
import os
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoFeatureExtractor, AutoModelForImageClassification, LlamaForSequenceClassification
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
from pdf_ocr import extract_text_from_images



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

    def login_hg(self)->None:
        login(self.hg_login)

    def initialize_nlp(self)->None:
        tokenizer = AutoTokenizer.from_pretrained(self.NLP_MODEL_DIR)
        self.tokenizer_nlp = tokenizer
        # Load model with memory optimizations
        nlp_model = LlamaForSequenceClassification.from_pretrained(
            self.NLP_MODEL_DIR,
            num_labels=4,
            #device_map="auto",
            #load_in_8bit=True,
            torch_dtype=torch.float16,
            low_cpu_mem_usage=True,
            offload_folder="offload",
            offload_state_dict=True
        )

        nlp_model.eval()

        self.nlp_model = nlp_model

    def initialize_cnn(self) ->None:
        model = AutoModelForImageClassification.from_pretrained(self.CNN_MODEL_DIR)
        feature_extractor = AutoFeatureExtractor.from_pretrained(self.CNN_MODEL_DIR)
        self.cnn_model = model
        self.cnn_feature_extractor = feature_extractor

    def cnn_model_function(self, images_dir) ->list:

        if os.path.exists(images_dir):
            image_paths = [os.path.join(images_dir, filename) for filename in os.listdir(images_dir)]
        else:
            print("Provided path is incorrect")
            image_paths = []

        document_labels = []

        for path in image_paths:
            image = Image.open(os.path.join(images_dir, path))
            try:
                inputs = self.cnn_feature_extractor(images=image, return_tensors="pt")
                outputs = self.cnn_model(**inputs)
                logits = outputs.logits
                predicted_label = logits.argmax(-1).item()

                label_mapping = {0: 'id', 1: 'idObcy', 2: 'inne', 3: 'paszport', 4: 'paszportObcy', 5: 'prawoJazdy', 6: 'prawoJazdyObce'}
                predicted_class_name = label_mapping[predicted_label]

                document_labels.append({predicted_class_name: path})
            
            except Exception as e:  
                print(f"Error processing {path}: {e}")
        
        return document_labels


    def predict_sentiment(self, text)->int:
        # Force CPU usage
        device = torch.device("balanced")
        self.nlp_model.to(device)

        # Tokenize the input text
        inputs = self.nlp_tokenizer(text, return_tensors="pt", truncation=True, max_length=512 ,padding=True)
        inputs = {k: v.to(device) for k, v in inputs.items()}

        # Make predictions
        with torch.no_grad():
            outputs = self.nlp_model(**inputs)
            logits = outputs.logits

        # Get the predicted class
        predicted_class_id = logits.argmax().item()

        return predicted_class_id


    def nlp_model_function(self, images_dir):
        document_labels = self.cnn_model_function(images_dir)
        print(document_labels)
        
        values_for_unknown_label = [entry for entry in document_labels if 'inne' in entry]
        print(values_for_unknown_label)

        nlp_dictionary = []
        list_text = []
        if len(values_for_unknown_label) > 0:
            for entry in values_for_unknown_label:
                path = list(entry.values())[0] #filrs element of every entry which is a one key:value pair dictionary
                print(path)
                text_from_image = extract_text_from_images([path])
                print(text_from_image)
                predicted_class = self.predict_sentiment(text_from_image)
                list_text.append((text_from_image, predicted_class))
                print(predicted_class)
                nlp_dictionary.append({
                    predicted_class:path
                })


            self.list_text_class = list_text
            document_labels.append(nlp_dictionary)
            return document_labels

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
