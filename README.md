
# AILCAP 

### Synopsis
 An implementation of various deep learning image segmentation models in [digital pathology field](https://en.wikipedia.org/wiki/Digital_pathology). WSI (Whole slide Image) file is the main file extension we are working on by using [openslide](https://openslide.org/api/python/) python library. We utilize openslide by dividing the pathology slides into smaller section so that we can process each section individually. After that, we can train and use models to recognize abnormal features in particular slides and finally merge the result regions together.

### Specification
 We decide to choose non-small cell lung cancer as targeted disease. We further divide the focus to adenocarcinoma which has 5 subtypes and 1 variant including papillary, solid, micropapillary, lepidic, acinar, and mucinous respectively.

<p align="center">
  <img src="./etc/images/adenocarcinoma_subtypes_variant.png" alt="Adenorcarcinoma and it's subtypes and variant" />
  <br>
  <a href="https://www.youtube.com/watch?v=-vtFloUyYpE">Histopathology of Non-Small Cell Lung Cancer (Dr. Sarawut Kongkarnka)
</a>
</p>

<br>

# Challenges
- limited computing power, especially with large files like .svs (~2GB+)
- Models' abilities to comprehend features
- Limited amount of focused cancer WSI which implies to dataset shortages
- Abnormal features that lie across multiple grid sections
- How to actually handle large output segmented images?

<br>

# Model choices
Before tackling those challenges, Let us consider our deep learning segmentation model choices. <br>

Commonly, in segmentation there are various deep learning models which are published with well-written documentation paper. The following models are interesting models for pathology segmentaion tasks.

[Ultralytics YOLO](https://docs.ultralytics.com/)|  [U-net](https://arxiv.org/pdf/1505.04597) | [Detectron](https://github.com/facebookresearch/detectron2)
:----------:|:------:|:------------:|
<img src="./etc/images/ultralytics_yolov8.jpg" height="100"> | <img src="./etc/images/u-net-architecture.png" height="100"> | <img src="./etc/images/detectron2.png" height="100">

Each of them has different pros and cons that we need to test and compare their results.