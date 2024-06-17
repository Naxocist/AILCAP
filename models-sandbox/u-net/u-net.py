import tensorflow as tf
import segmentation_models as sm
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
# import cv2
import os
import keras
from random import randint

from keras.utils import normalize
from keras.metrics import MeanIoU

SIZE_X = 128
SIZE_Y = 128
n_classes = 4

images_path = "128_patches/images_as_128x128_patches.tif"
masked_path = "128_patches/masks_as_128x128_patches.tif"
train_images = []
train_masked = []

with Image.open(images_path) as img:

    for i in range(img.n_frames):
        img.seek(i)

        img_np = np.array(img)
        rgb_image = np.stack((img_np,)*3, axis=-1)
        train_images.append(rgb_image)


with Image.open(masked_path) as img:


    for i in range(img.n_frames):
        img.seek(i)
        
        img_np = np.array(img)
        train_masked.append(img_np)


train_images = np.array(train_images)
train_masked = np.array(train_masked)


from sklearn.preprocessing import LabelEncoder
label_encoder = LabelEncoder()
n, h, w = train_masked.shape
train_masked_reshaped = train_masked.reshape(-1, 1)
train_masked_reshaped_encoded = label_encoder.fit_transform(train_masked_reshaped)
train_masked_encoded_original_shape = train_masked_reshaped_encoded.reshape(n, h, w)

train_masked_input = np.expand_dims(train_masked_encoded_original_shape, axis=3)


from sklearn.model_selection import train_test_split
# split entire dataset to train and testing 
x_train, x_test, y_train, y_test = train_test_split(train_images, train_masked_input, test_size=0.1, random_state=0)

# split training dataset to train and validation
x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size=0.5, random_state=0)

from keras.utils import to_categorical
train_masks_cat = to_categorical(y_train, num_classes=n_classes)
y_train_cat = train_masks_cat.reshape((y_train.shape[0], y_train.shape[1], y_train.shape[2], n_classes))

test_masks_cat = to_categorical(y_test, num_classes=n_classes)
y_test_cat = test_masks_cat.reshape((y_test.shape[0], y_test.shape[1], y_test.shape[2], n_classes))

test_masks_cat = to_categorical(y_val, num_classes=n_classes)
y_val_cat = test_masks_cat.reshape((y_val.shape[0], y_val.shape[1], y_val.shape[2], n_classes))


activation='softmax'
LR = 0.0001
optim = keras.optimizers.Adam(LR)
# Segmentation models losses can be combined together by '+' and scaled by integer or float factor
# set class weights for dice_loss (car: 1.; pedestrian: 2.; background: 0.5;)
dice_loss = sm.losses.DiceLoss(class_weights=np.array([0.25, 0.25, 0.25, 0.25])) 
focal_loss = sm.losses.CategoricalFocalLoss()
total_loss = dice_loss + (1 * focal_loss)
# actulally total_loss can be imported directly from library, above example just show you how to manipulate with losses
# total_loss = sm.losses.binary_focal_dice_loss # or sm.losses.categorical_focal_dice_loss 
metrics = [sm.metrics.IOUScore(threshold=0.5), sm.metrics.FScore(threshold=0.5)]




BACKBONE1 = 'resnet34'
preprocess_input1 = sm.get_preprocessing(BACKBONE1)

# preprocess input
prep_x_train = preprocess_input1(x_train)
prep_x_val = preprocess_input1(x_val)

# define model
model1 = sm.Unet(BACKBONE1, encoder_weights='imagenet', classes=n_classes, activation=activation)

# compile keras model with defined optimozer, loss and metrics
model1.compile(optim, total_loss, metrics=metrics)
# model1.compile(optimizer='adam', loss='categorical_crossentropy', metrics=metrics)

# print(model1.summary())

# history1=model1.fit(prep_x_train, 
#           y_train_cat,
#           batch_size=8, 
#           epochs=50,
#           verbose=1,
#           validation_data=(x_val, y_val_cat))


# model1.save('res34_backbone_50epochs.hdf5')


from keras.models import load_model

model1 = load_model('./res34_backbone_50epochs.hdf5', compile=False)

y_pred=model1.predict(x_test)
print(y_pred)
y_pred_argmax=np.argmax(y_pred, axis=3)
print(y_pred_argmax)
print(y_pred_argmax.shape)

IOU_keras = MeanIoU(num_classes=n_classes)  
IOU_keras.update_state(y_test[:,:,:,0], y_pred_argmax)
print("Mean IoU =", IOU_keras.result().numpy())


for i in range(10) :
    idx = randint(0, 50)

    fig, axs = plt.subplots(1, 3, figsize=(10, 5))

    axs[0].imshow(x_test[idx])
    axs[0].set_title("source")
    axs[0].axis('off')

    axs[1].imshow(y_test[idx])
    axs[1].set_title("ground truth")
    axs[1].axis('off')

    axs[2].imshow(y_pred_argmax[idx])
    axs[2].set_title("predict")
    axs[2].axis('off')

    plt.show()
