# code-for-CRB-damage-ai

Local folder: Guam07-training-set/code

GitHub repository: <https://github.com/aubreymoore/code-for-CRB-damage-ai>

GitHub pages: <https://aubreymoore.github.io/code-for-CRB-damage-ai>

## Background

This repository contains code and documentation for object detectors which scan images to detect coconut palms and distinctive damage to these palms (v-shaped cuts) caused coconut rhinoceros beetles. 

Detection models for CRB damage were originally trained using a RCNN model in 2020.
These models detected coconut palms in images, placed bounding boxes around them, and classified damage using a five point index (none, low, medium, high, and dead).
An additional detector detected v-shaped cuts and placed polygons around these.
These models were tested in roadside surveys on Guam. 
Survey images were acquired by a smartphone fixed to the outside of a vehicle which was driven along all major roads on Guam. 
In the first surveys, the smart phone was used to record a continuous HD video an open source app was used to record waypoints using the phone's GPS chip.
Video frames were later georeferenced using timestamps.
In later surveys we used an open source app called OpenCamera programmed to record still frames (1080 pixels high x 1920 pixels wide) at a rate of one frame per second.
Custom software was used to convert survey data into survey results into interactive web maps. 
Ten island-wide CRB damage surveys were performed on Guam between October 2020 and September 2023.
Inteactive maps and data are publicly available in a [GitHub repository](https://aubreymoore.github.io/Guam-CRB-web-maps/).
Roadside surveys were also performed to help delineate new CRB populations on Rota Island and Majuro Atoll.

Further details and background can be found in [this unfunded preproposal](https://aubreymoore.github.io/serdp-crb-damage/preproposal.pdf).

## Current status

* I retrained the object detectors using YOLOv8. 
This change vastly improved performance, allowing the model to run in real time.
* I wrote an Android smartphone app and submitted it to Google Play Store to demonstrate real time 
detection of CRB damage.
* I retrained the object detectors after reducing the class count from 6 to 3 by merging 
none, low, medium and high into live.

original classes | new classes
------ |-----
none   | live
low    | live
medium | live
high   | live
dead   | dead
vcut   | vcut

* The current 3-class model is stored in /home/aubrey/Desktop/Guam07-training-set/datasets/3class/runs/detect/train5/weights/best.pt.<br>[confusion matrix](models/3class/train5/confusion_matrix.png)<br>[normalized confusion matrix](models/3class/train5/confusion_matrix_normalized.png)

## Current objectives

* The training data suffer from a class imbalance with 1800 **live** palms, 27 **dead** palms and 431 **vcuts**. I will correct this by adding additional images containing dead trees and vcuts from Guam surveys.

* I will improve detection precision using active learning.

* I will improve the smart phone app by:
    * allowing the app to scan images stored on the cell cell phone in addition to scanning images streamed from the phone's camera
    * adding storage of detection results in an embedded database 

* I will publish an online version of the object detector on Google Colab which can be used for scanning uploaded images or images available on the internet.

* I will write a user guide for the smart phone app.

* I will document how to create interactive web maps using QGIS.
 