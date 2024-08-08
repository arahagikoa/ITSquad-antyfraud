import os
import sys
import json
import datetime
import numpy as np
import skimage.draw

from mrcnn.visualize import display_instances, display_top_masks
from mrcnn.utils import extract_bboxes
from mrcnn.utils import Dataset
from matplotlib import pyplot as plt

from mrcnn.config import Config
from mrcnn.model_temp import MaskRCNN

from mrcnn import model_temp as modellib, utils
from PIL import Image, ImageDraw
from mrcnn.model_temp import load_image_gt
from mrcnn.model_temp import mold_image
from mrcnn.utils import compute_ap
from numpy import expand_dims
from numpy import mean
from matplotlib.patches import Rectangle


#!   NEED TO ESTABLISH MODEL SO IT ONLY FINDS FOR ONE CLASS AT THE TIME




# define the prediction configuration
class PredictionConfig(Config):
    # define the name of the configuration
    NAME = "marble_cfg_coco"
    # number of classes (background + Blue Marbles + Non Blue marbles)
    NUM_CLASSES = 1 + 2
    # Set batch size to 1 since we'll be running inference on
    # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
    BATCH_SIZE = 1
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1


# Load and prepare the dataset
#dataset_train = CocoLikeDataset()
#dataset_train.load_data('dataset/train/labels_my-project-name_2024-05-28-08-02-43.json', 'dataset/train')
#dataset_train.prepare()

# calculate the mAP for a model on a given dataset
def evaluate_model(dataset, model, cfg):
    APs = list()
    for image_id in dataset.image_ids:
        # load image, bounding boxes and masks for the image id
        image, image_meta, gt_class_id, gt_bbox, gt_mask = load_image_gt(dataset, cfg, image_id, use_mini_mask=False)
        # convert pixel values (e.g. center)
        scaled_image = mold_image(image, cfg)
        # convert image into one sample
        sample = expand_dims(scaled_image, 0)
        # make prediction
        yhat = model.detect(sample, verbose=0)
        # extract results for first sample
        r = yhat[0]
        # calculate statistics, including AP
        AP, _, _, _ = compute_ap(gt_bbox, gt_class_id, gt_mask, r["rois"], r["class_ids"], r["scores"], r['masks'])
        # store
        APs.append(AP)
    # calculate the mean AP across all images
    mAP = mean(APs)
    return mAP

def get_mask_coordinates(mask):
    # Find the coordinates of non-zero elements
    coords = np.column_stack(np.where(mask))
    return coords


def get_mask_info(coords):
    y_min, x_min = coords.min(axis=0)
    y_max, x_max = coords.max(axis=0)
    centroid = coords.mean(axis=0)
    return {
        'bounding_box': (y_min, x_min, y_max, x_max),
        'centroid': centroid
    }
# Assuming you have already created filtered_masks and filtered_class_ids
mask_coordinates = {}

# create config
cfg = PredictionConfig()
# define the model
model = MaskRCNN(mode='inference', model_dir='logs', config=cfg)
# load model weights
model.load_weights(r'E:\Projekty\for_work\text-extraction\text_extraction\logs\marble_cfg_coco20240729T2136\mask_rcnn_marble_cfg_coco_0006.h5', by_name=True)

# Evaluate model on training dataset
# Uncomment if needed
# train_mAP = evaluate_model(dataset_train, model, cfg)
# print("Train mAP: %.3f" % train_mAP)

# Test on a single image
import skimage
marbles_img = skimage.io.imread(r"E:\Projekty\for_work\text-extraction\text_extraction\data\train\prawko5.png")
input_image = r"E:\Projekty\for_work\text-extraction\text_extraction\data\train\prawko5.png"

detected = model.detect([marbles_img])
results = detected[0]
class_names = ['BG', 'imie', 'nazwisko']


print("class ids", results['class_ids'])
print("scores", results['scores'])

filtered_results = {}
for i, class_id in enumerate(results['class_ids']):
    score = results['scores'][i]
    if class_id not in filtered_results or filtered_results[class_id]['score'] < score:
        filtered_results[class_id] = {'score': score, 'roi': results['rois'][i], 'mask': results['masks'][:, :, i]}

# Extract the filtered results
filtered_class_ids = list(filtered_results.keys())
filtered_scores = [filtered_results[class_id]['score'] for class_id in filtered_class_ids]
filtered_rois = np.array([filtered_results[class_id]['roi'] for class_id in filtered_class_ids])
filtered_masks = np.stack([filtered_results[class_id]['mask'] for class_id in filtered_class_ids], axis=-1)

# Convert lists to NumPy arrays
filtered_class_ids = np.array(filtered_class_ids)
filtered_scores = np.array(filtered_scores)

print("filtered class ids", filtered_class_ids)
print("filtered scores", filtered_scores)
for i, class_id in enumerate(filtered_class_ids):
    mask = filtered_masks[:,:,i]
    coords = get_mask_coordinates(mask)
    mask_coordinates[class_id] = coords



mask_info = {class_id: get_mask_info(coords) for class_id, coords in mask_coordinates.items()}


# display_instances(marbles_img, filtered_rois, filtered_masks, filtered_class_ids, class_names, filtered_scores)



#display_instances(marbles_img, results['rois'], results['masks'], 
#                  ids, class_names, scores)




# Show detected objects in color and all others in B&W    
def color_splash(img, mask):
    """Apply color splash effect.
    image: RGB image [height, width, 3]
    mask: instance segmentation mask [height, width, instance count]
    Returns result image.
    """
    # Make a grayscale copy of the image. The grayscale copy still
    # has 3 RGB channels, though.
    gray = skimage.color.gray2rgb(skimage.color.rgb2gray(img)) * 255
    # Copy color pixels from the original color image where mask is set
    if mask.shape[-1] > 0:
        # We're treating all instances as one, so collapse the mask into one layer
        mask = (np.sum(mask, -1, keepdims=True) >= 1)
        splash = np.where(mask, img, gray).astype(np.uint8)
    else:
        splash = gray.astype(np.uint8)
    return splash

def detect_and_color_splash(model, image_path=None, video_path=None):
    assert image_path or video_path

    # Image or video?
    if image_path:
        # Run model detection and generate the color splash effect
        # Read image
        img = skimage.io.imread(image_path)
        # Detect objects
        r = model.detect([img], verbose=1)[0]
        # Color splash
        splash = color_splash(img, r['masks'])
        # Save output
        file_name = "splash_{:%Y%m%dT%H%M%S}.png".format(datetime.datetime.now())
        skimage.io.imsave(file_name, splash)
    elif video_path:
        import cv2
        # Video capture
        vcapture = cv2.VideoCapture(video_path)
        width = int(vcapture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(vcapture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = vcapture.get(cv2.CAP_PROP_FPS)

        # Define codec and create video writer
        file_name = "splash_{:%Y%m%dT%H%M%S}.avi".format(datetime.datetime.now())
        vwriter = cv2.VideoWriter(file_name,
                                  cv2.VideoWriter_fourcc(*'MJPG'),
                                  fps, (width, height))

        count = 0
        success = True
        while success:
            print("frame: ", count)
            # Read next image
            success, img = vcapture.read()
            if success:
                # OpenCV returns images as BGR, convert to RGB
                img = img[..., ::-1]
                # Detect objects
                r = model.detect([img], verbose=0)[0]
                # Color splash
                splash = color_splash(img, r['masks'])
                # RGB -> BGR to save image to video
                splash = splash[..., ::-1]
                # Add image to video writer
                vwriter.write(splash)
                count += 1
        vwriter.release()
    print("Saved to ", file_name)

# Uncomment if you want to run color splash detection
#detect_and_color_splash(model, image_path=r"E:\Projekty\for_work\text-extraction\text_extraction\Dataset\train\1-12700.jpg")
def display_masks(image, masks, class_ids, class_names, scores=None, title="", figsize=(16, 16), ax=None, show_mask=True, show_bbox=True, colors=None, captions=None):
    """
    masks: [height, width, num_instances]
    class_ids: [num_instances]
    class_names: list of class names of the dataset
    scores: (optional) confidence scores for each box
    title: (optional) Figure title
    show_mask, show_bbox: To show masks and bounding boxes or not
    figsize: (optional) the size of the image
    colors: (optional) An array or colors to use with each object
    captions: (optional) A list of strings to use as captions for each object
    """
    # Number of instances
    N = masks.shape[2] if masks is not None else 0

    # Generate random colors
    colors = colors or random_colors(N)

    # Show area outside image boundaries.
    height, width = image.shape[:2]
    if not ax:
        _, ax = plt.subplots(1, figsize=figsize)

    ax.set_ylim(height + 10, -10)
    ax.set_xlim(-10, width + 10)
    ax.axis('off')
    ax.set_title(title)

    masked_image = image.astype(np.uint32).copy()
    for i in range(N):
        color = colors[i]

        # Bounding box
        if show_bbox:
            y1, x1, y2, x2 = extract_bboxes(masks[:, :, i:i+1])[0]
            p = patches.Rectangle((x1, y1), x2 - x1+30, y2 - y1, linewidth=2,
                                  alpha=0.7, linestyle="dashed",
                                  edgecolor=color, facecolor='none')
            ax.add_patch(p)

        # Mask
        if show_mask:
            mask = masks[:, :, i]
            masked_image = apply_mask(masked_image, mask, color)
        count_ = {"imie": 0, "nazwisko": 0}
        # Label
        if not captions:
            class_id = class_ids[i]
            score = scores[i] if scores is not None else None
            label = class_names[class_id]
            
            caption = "{} {:.3f}".format(label, score) if score else label
        else:
            caption = captions[i]
        ax.text(x1, y1 + 8, caption,
                color='w', size=11, backgroundcolor="none")

    ax.imshow(masked_image.astype(np.uint8))
    plt.show()

# Helper functions

def random_colors(N, bright=True):
    """
    Generate random colors.
    """
    brightness = 1.0 if bright else 0.7
    hsv = [(i / N, 1, brightness) for i in range(N)]
    colors = list(map(lambda c: colorsys.hsv_to_rgb(*c), hsv))
    random.shuffle(colors)
    return colors

def apply_mask(image, mask, color, alpha=0.5):
    """
    Apply the given mask to the image.
    """
    for c in range(3):
        image[:, :, c] = np.where(mask == 1,
                                  image[:, :, c] *
                                  (1 - alpha) + alpha * color[c] * 255,
                                  image[:, :, c])
    return image

# You'll need to import these at the top of your script
import random
import colorsys
import matplotlib.patches as patches


#display_masks(marbles_img, results['masks'], results['class_ids'], 
 #             class_names, results['scores'], 
 #             title="Detected Masks", figsize=(12,12), 
#             show_bbox=False)

# To show only bounding boxes without masks
display_masks(marbles_img, filtered_masks, filtered_class_ids, class_names, filtered_scores, 
              title="Detected Bounding Boxes", figsize=(12,12), 
              show_mask=False)


original_image = Image.fromarray(marbles_img)


output_dir = f"{input_image}_extracted_info"
os.makedirs(output_dir, exist_ok=True)


for i, class_id in enumerate(filtered_class_ids):

    y1, x1, y2, x2 = filtered_rois[i]
    
    class_name = class_names[class_id]
    

    cropped_image = original_image.crop((x1, y1, x2, y2))
    

    filename = f"{class_name}_{i}.png"
    filepath = os.path.join(output_dir, filename)    

    cropped_image.save(filepath)
    
    print(f"Saved {filepath}")



def main(img_dir):
    batch_size = len(img_dir)

    mask_coordinates = {}

    
    cfg = PredictionConfig()
    cfg.BATCH_SIZE = batch_size
    
    model = MaskRCNN(mode='inference', model_dir='logs', config=cfg)
    model.load_weights(r'E:\Projekty\for_work\text-extraction\text_extraction\logs\marble_cfg_coco20240729T2136\mask_rcnn_marble_cfg_coco_0006.h5', by_name=True)
    list_images = [skimage.io.imread(f"{x}") for x in img_dir]
    

    detected = model.detect(list_images)

    for i in detected:
        results = i[0]
        class_names = ['BG', 'imie', 'nazwisko']


        print("class ids", results['class_ids'])
        print("scores", results['scores'])

        filtered_results = {}
        for i, class_id in enumerate(results['class_ids']):
            score = results['scores'][i]
            if class_id not in filtered_results or filtered_results[class_id]['score'] < score:
                filtered_results[class_id] = {'score': score, 'roi': results['rois'][i], 'mask': results['masks'][:, :, i]}

        # Extract the filtered results
        filtered_class_ids = list(filtered_results.keys())
        filtered_scores = [filtered_results[class_id]['score'] for class_id in filtered_class_ids]
        filtered_rois = np.array([filtered_results[class_id]['roi'] for class_id in filtered_class_ids])
        filtered_masks = np.stack([filtered_results[class_id]['mask'] for class_id in filtered_class_ids], axis=-1)

        # Convert lists to NumPy arrays
        filtered_class_ids = np.array(filtered_class_ids)
        filtered_scores = np.array(filtered_scores)

        print("filtered class ids", filtered_class_ids)
        print("filtered scores", filtered_scores)
        for i, class_id in enumerate(filtered_class_ids):
            mask = filtered_masks[:,:,i]
            coords = get_mask_coordinates(mask)
            mask_coordinates[class_id] = coords


        mask_info = {class_id: get_mask_info(coords) for class_id, coords in mask_coordinates.items()}
        display_masks(marbles_img, filtered_masks, filtered_class_ids, class_names, filtered_scores, 
                title="Detected Bounding Boxes", figsize=(12,12), 
                show_mask=False)


        original_image = Image.fromarray(marbles_img)


        output_dir = "./cnn_output"
        os.makedirs(output_dir, exist_ok=True)


        for i, class_id in enumerate(filtered_class_ids):

            y1, x1, y2, x2 = filtered_rois[i]
            
            class_name = class_names[class_id]

            cropped_image = original_image.crop((x1, y1, x2, y2))
            

            filename = f"{class_name}_{i}.png"
            filepath = os.path.join(output_dir, filename)    

            cropped_image.save(filepath)
            
            print(f"Saved {filepath}")