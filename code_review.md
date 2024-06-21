# Code Review

Updated June 16, 2024

<!-- TOC -->

- [Code Review](#code-review)
    - [Software Tools](#software-tools)
        - [VS Code](#vs-code)
        - [labelImg](#labelimg)
    - [Jupyter Notebooks](#jupyter-notebooks)
        - [detect_crb_damage.ipynb](#detect_crb_damageipynb)
        - [train_Guam07v1.ipynb](#train_guam07v1ipynb)
        - [build_new_dataset.ipynb](#build_new_datasetipynb)
        - [detect_objects.ipynb](#detect_objectsipynb)
        - [make-labels.ipynb](#make-labelsipynb)
        - [subset.ipynb](#subsetipynb)
        - [yolo-to-label-studio.ipynb](#yolo-to-label-studioipynb)
        - [clean_dataset.ipynb](#clean_datasetipynb)
        - [display_annotated_image.ipynb](#display_annotated_imageipynb)
        - [split_data.ipynb](#split_dataipynb)
    - [Initial training](#initial-training)
        - [Settings](#settings)
        - [Results](#results)
        - [Notes](#notes)

<!-- /TOC -->
## Software Tools

### VS Code

Start in terminal with:
```
code --in-process-gpu
```

### labelImg

Start in terminal using:
```
python3 ~/labelImg/labelImg.py
```

Install by clonining GitHub repo:
```
cd ~
clone https://github.com/HumanSignal/labelImg.git
```

## Jupyter Notebooks

### detect_crb_damage.ipynb
DOCS NEED UPDATING

https://github.com/aubreymoore/Majuro01_updated


### train_Guam07v1.ipynb
DOCS NEED UPDATING

### build_new_dataset.ipynb  
```
ORIGINAL_IMAGE_DIR = '/home/aubrey/Desktop/Guam07-training-set/rawdata'
NEW_DATASET_DIR = '/home/aubrey/Desktop/Guam07-training-set/datasets/Guam07v2'
MODEL='/home/aubrey/Desktop/Guam07-training-set/datasets/Guam07v1/runs/detect/train5/weights/best.pt'
```
### detect_objects.ipynb   
empty
### make-labels.ipynb  
This notebook constructs a YOLOv8 training set. 

INPUT: A **rawdata** folder containing images and pickle files constructed by **detect_rb_damage.ipynb**.

OUTPUT: A training set folder.
### subset.ipynb
```
IMAGES_DIR =  '/home/aubrey/Desktop/Guam07-training-set/datasets/Guam07v2/images' # Original images (*.jpg)
LABELS_DIR =  '/home/aubrey/Desktop/Guam07-training-set/datasets/Guam07v2/labels' # Original labels (*.txt; bounding boxes in YOLO annotation format)
SUBSETS_DIR = '/home/aubrey/Desktop/Guam07-training-set/datasets/Guam07v3/images' # Output directory structure (images/023/<*.jpg and *.txt files>)
IMAGES_PER_SUBSET = 100
```
### yolo-to-label-studio.ipynb
```
os.system('label-studio-converter import yolo -h')
```
### clean_dataset.ipynb
This Jupyter workbook cleans a YOLOv8 dataset by removing bounding boxes from label (*.txt) files where:
* a bounding box classed as zero, low, medium or high [0 .. 3] overlaps another bounding box with class [0..3] with an intersection over union value (IOU) greater than a specified threshold (IOU_THRESHOLD)
* a bounding box classed as vcut which does not overlap another bounding box

### display_annotated_image.ipynb
documentation needed
### split_data.ipynb
This workbook splits raw data in a folder containing images (\*.jpg) and labels (\*.txt) into the folder structure expected by YOLO (See https://docs.ultralytics.com/datasets/detect/#ultralytics-yolo-format).

Note that images which do not have annotated objects are not included in the dataset. In other words, only images (\*.jpg) with a corresponding labels file (\*.txt) are included.

## Initial training

### Settings
```
%%writefile /home/aubrey/Desktop/Guam07-training-set/datasets/Guam07vx/data.yaml
path: /home/aubrey/Desktop/Guam07-training-set/datasets/Guam07vx
train: images/train
val: images/val
test: images/test
names:
  0: zero
  1: low
  2: medium
  3: high
  4: fatal
  5: vcut
```
```
# Load a pretrained YOLO model (recommended for training)
model = YOLO("yolov8n.pt")
```
```
# Train the model using the 'data.yaml' dataset for 3 epochs
results = model.train(
    data="/home/aubrey/Desktop/Guam07-training-set/datasets/Guam07vx/data.yaml", 
    epochs=1000,
    imgsz=960,
    batch=-1,    # auto mode; 60% of GPU memory  
    name='imgsz960',
    )
```
### Results
Results are saved in /home/aubrey/Desktop/Guam07-training-set/code/runs/detect/imgsz9603. 176 epochs completed in 3.264 hours.Best model  at 76 epochs. (Suggest changing patience from 100 to 30.)

### Notes

#### Dataset structure

- test
    - data.yaml
    - train
        - classes.txt
        - *.img
        - *.txt
    - val
        - classes.txt
        - *.img
        - *.txt
    - test
        - classes.txt
        - *.img
        - *.txt

data.yaml
```
path: /home/aubrey/Desktop/Guam07-training-set/datasets/test
train: train
val: val
test: test
names:
  0: zero
  1: low
  2: medium
  3: high
  4: fatal
  5: vcut
```

classes.txt
```
zero
low
medium
high
fatal
vcut
```

- Looks like it is possible to create a dataset where images (\*.jpg) and labels(\*.txt) occur in the same folder. See https://github.com/ultralytics/ultralytics/issues/3087. This is great because this is the data structure used by labelImg. Will test this idea. Note that labelImg silently rejects *.txt files a confidence value has been added. This means we need to store confidence values elsewhere.
```
1 0.358854 0.488889 0.229167 0.964815 is OK
1 0.358854 0.488889 0.229167 0.964815 0.123 will cause rejection of the *.txt file
```
