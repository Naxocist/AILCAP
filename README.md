
# AILCAP 

### Synopsis
 An implementation of various deep learning image segmentation models in [digital pathology field](https://en.wikipedia.org/wiki/Digital_pathology). WSI (Whole slide Image) file is the main file we are working on by using [openslide](https://openslide.org/api/python/) python library. We utilize openslide by dividing the pathology slides into smaller section so that we can process each section individually. After that, we can train and use models to recognize abnormal features in particular slides and finally merge the result regions together.

### Specification
 We decide to choose non-small cell lung cancer as targeted disease. We further divide the focus to adenocarcinoma which has 5 subtypes and 1 variant including papillary, solid, micropapillary, lepidic, acinar, and mucinous respectively.

<p align="center">
  <img src="./etc/images/adenocarcinoma_subtypes_variant.png" alt="Adenorcarcinoma and it's subtypes and variant" />
  <br>
  <a href="https://www.youtube.com/watch?v=-vtFloUyYpE">Histopathology of Non-Small Cell Lung Cancer (Dr. Sarawut Kongkarnka)
</a>
</p>

<!-- <br> -->

# Challenges
- limited computing power, especially with large files like .svs (~2GB+)
- Models' abilities to comprehend features
- Limited amount of focused cancer WSI which implies to dataset shortages
- Abnormal features that lie across multiple grid sections
- How to actually handle large output segmented images?

<!-- <br> -->

# Model choices
Before tackling those challenges, Let us consider our deep learning segmentation model choices. <br>

Commonly, in segmentation there are various deep learning models which are published with well-written documentation paper. The following models are interesting models for pathology segmentaion tasks.

<div align="center">

[Ultralytics YOLO](https://docs.ultralytics.com/)|  [U-net architecture](https://arxiv.org/pdf/1505.04597) | [Detectron2](https://github.com/facebookresearch/detectron2)
:----------:|:------:|:------------:|
<img src="./etc/images/ultralytics_yolov8.jpg" height="100"> | <img src="./etc/images/u-net-architecture.png" height="100"> | <img src="./etc/images/detectron2.png" height="100">

</div>

Each of them has different pros and cons that we need to test and compare their results and appropriately adapt to challenges.

<br>

# Tackling Challenges
Let us elaborate solutions to previously mentioned challenges 

We can easily divide WSI file into large amount of tiles. The number of tiles obviously depends on the size of extracted tiles. In this case we choose 256px * 256px tiles as it is small enough for our models to work on. Additionally, we need to add overlaps between tiles to ensure that each image provides decent context for certain region.

By using data augmentation techniques which are processes of rotating, cropping, flipping data to gain another data out of available data. These images will be given to models to ensure ability of generalizing images.

When the abnormal features are lying across multiple tiles, we can't use "object detection model" easily as it frames the features with boxes so it is hard to merge boxes from each tile. Instead, we use segmentation model to "color" interested features so we can easily merge grids together.
