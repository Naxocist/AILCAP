# AILCAP 

### Synopsis
An implementation of various deep learning image segmentation models in [digital pathology field](https://en.wikipedia.org/wiki/Digital_pathology). WSI (Whole slide Image) file is the main file extension we are working on by using [openslide](https://openslide.org/api/python/) python library. We utilize openslide by dividing the pathology slides into smaller section so that we can process each section individually. After that, we can train and use models to recognize abnormal features in particular slides and finally merge the result regions together.

### Specification
We decide to choose non-small cell lung cancer as targeted disease. We further divide the focus to adenocarcinoma which has 5 subtypes and 1 variant including papillary, solid, micropapillary, lepidic, acinar, and mucinous respectively.

![Adenorcarcinoma and it's subtypes and variant](./etc/images/adenocarcinoma_subtypes_variant.png)
[source](https://www.youtube.com/watch?v=-vtFloUyYpE)

# Challenges

- limited computing power, especially with large files like .svs (~2GB+)
- Models' abilities to comprehend features
- Limited amount of focused cancer WSI which implies to dataset shortages
- Abnormal features that lie across multiple grid sections
- How to actually handle large output segmented images?
