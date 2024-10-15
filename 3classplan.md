# Reduce Object Classes from 6 to 3

Convert classes from [zero, low, medium, high, dead, vcut] to [live, dead, vcut].

## Refactor training set

We will start with these:

```python
DATASET_PATH = '/home/aubrey/Desktop/Guam07-training-set/datasets/active_learning2'
LABELIMG_PATH = '/home/aubrey/labelImg/labelImg.py'
DB_PATH = '/home/aubrey/Desktop/Guam07-training-set/code/active_learning2.sqlite3'
```

Probably makes more sense to save DB within DATASET_PATH.

1. Copy **datasets/active_learning2** to **datasets/3class**

1. Delete all **.txt** files in **datasets/3class**

1. Fix **classes.txt** files  in **datasets/3class** to contain live, dead, vcut

1. Copy **code/active_learning2.sqlite3** to **datasets/3class/3class.sqlite3**

1. Recode object classes in DB
    * 0,1,2,3 -> 0 (live)
    * 4 -> 1 (dead)
    * 5 -> 2 (vcut)
    ```sql
    UPDATE obj SET cls=0 WHERE cls IN (0,1,2,3);
    UPDATE obj SET cls=1 WHERE cls=4;
    UPDATE obj SET cls=2 WHERE cls=5;
    ```

1. Use DB as a datasource for creating .txt files containing bounding boxes in training set.
    * Implemented in [create_3class_dataset.ipynb](code/create_3class_dataset.ipynb)

## Train new model
Run the following in datasets/3class in the folder containing **3class.yaml**.
```
yolo train data=3class.yaml model=yolov8n.pt imgsz=960 epochs=1000 batch=-1
```

### Training results
```
      Epoch    GPU_mem   box_loss   cls_loss   dfl_loss  Instances       Size
   172/1000      9.62G     0.7287     0.5566      1.005         72        960: 100%|██████████| 294/294 [01:53<00:00,  2.58it/s]
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100%|██████████| 16/16 [00:03<00:00,  4.14it/s]
                   all       1018       2258      0.746      0.739      0.812      0.618
EarlyStopping: Training stopped early as no improvement observed in last 100 epochs. Best results observed at epoch 72, best model saved as best.pt.
To update EarlyStopping(patience=100) pass a new patience value, i.e. `patience=300` or use `patience=0` to disable EarlyStopping.

172 epochs completed in 5.650 hours.
Optimizer stripped from runs/detect/train5/weights/last.pt, 6.3MB
Optimizer stripped from runs/detect/train5/weights/best.pt, 6.3MB

Validating runs/detect/train5/weights/best.pt...
Ultralytics YOLOv8.2.14 🚀 Python-3.10.12 torch-2.3.0+cu121 CUDA:0 (NVIDIA GeForce RTX 3080 Laptop GPU, 16110MiB)
/home/aubrey/.local/lib/python3.10/site-packages/torch/nn/modules/conv.py:456: UserWarning: Plan failed with a cudnnException: CUDNN_BACKEND_EXECUTION_PLAN_DESCRIPTOR: cudnnFinalize Descriptor Failed cudnn_status: CUDNN_STATUS_NOT_SUPPORTED (Triggered internally at ../aten/src/ATen/native/cudnn/Conv_v8.cpp:919.)
  return F.conv2d(input, weight, bias, self.stride,
Model summary (fused): 168 layers, 3006233 parameters, 0 gradients, 8.1 GFLOPs
                 Class     Images  Instances      Box(P          R      mAP50  mAP50-95): 100%|██████████| 16/16 [00:04<00:00,  3.58it/s]
                   all       1018       2258      0.762      0.765      0.824       0.63
                  live       1018       1800      0.796      0.942      0.954      0.804
                  dead       1018         27      0.787      0.704      0.787      0.553
                  vcut       1018        431      0.704       0.65      0.731      0.533
Speed: 0.2ms preprocess, 1.7ms inference, 0.0ms loss, 0.8ms postprocess per image
Results saved to runs/detect/train5
```

# Export model in tflite format

Run the following in /home/aubrey/Desktop/Guam07-training-set/datasets/3class/runs/detect/train5/weights
```
yolo export model=best.pt format=tflite imgsz=960
```




