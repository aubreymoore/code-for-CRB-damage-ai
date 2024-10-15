# code-for-CRB-damage-ai

Local folder: Guam07-training-set

GitHub repository: <https://github.com/aubreymoore/code-for-CRB-damage-ai.git>

Note: The git repository contains only files from the Guam07-training-set/code folder.

## Introduction

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

Furhter details and background can be found in [this unfunded preproposal](https://aubreymoore.github.io/serdp-crb-damage/preproposal.pdf).

## Work plan
