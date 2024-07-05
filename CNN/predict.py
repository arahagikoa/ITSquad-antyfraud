import os
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoFeatureExtractor, AutoModelForImageClassification
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


#model_dir = os.path.join(parent_dir, "dit_baseDocument_Classification_ids")
model_dir = "E:\\Projekty\\for_work\\docs-det-all-nations\\dit-baseDocument_Classification-ids-seria-21"


if not os.path.exists(model_dir):
    raise ValueError(f"The directory '{model_dir}' does not exist.")

model = AutoModelForImageClassification.from_pretrained(model_dir)
feature_extractor = AutoFeatureExtractor.from_pretrained(model_dir)

id_ = "E:\\Projekty\\for_work\\docs-det-all-nations\\dataset\\train\\idObcy\\3.jfif"
paszport = "E:\\Projekty\\for_work\\docs-det-all-nations\\Dataset\\train\\paszportObcy\\qqqww.jfif"
prawko = "E:\\Projekty\\for_work\\docs-det-all-nations\\Dataset\\train\\prawoJazdy\\15.jfif"
inne = "E:\\Projekty\\for_work\\docs-det-all-nations\\dataset\\train\\inne\\43.jfif"
zdj = "E:\\Projekty\\for_work\\docs-det-all-nations\\test\\id\\1.jfif"



pred_img = paszport

true_label = "paszport Obcy"

image = Image.open(pred_img)

inputs = feature_extractor(images=image, return_tensors="pt")

outputs = model(**inputs)
logits = outputs.logits
predicted_label = logits.argmax(-1).item()



label_mapping = {0: 'id', 1: 'idObcy', 2: 'inne', 3: 'paszport', 4: 'paszportObcy', 5: 'prawoJazdy', 6: 'prawoJazdyObce'}



predicted_class_name = label_mapping[predicted_label]
print(predicted_class_name)

img = mpimg.imread(pred_img)
plt.title(f"Model prediction for category: {true_label} = {predicted_class_name}")
plt.axis('off')
imgplot = plt.imshow(img)
plt.show()
