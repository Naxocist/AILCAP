# AILCAP

An implementation of [YOLOv9](https://docs.ultralytics.com/models/yolov9/) in pathology field. ".svs" file is the main file extension we are working on using [openslide](https://openslide.org/api/python/) python library. We utilize openslide in dividing the pathology slides into smaller section so that we can process each section individually. After that, we can finally train YOLOv9, a powerful object detection model, to recognize abnormal features in particular slides.
