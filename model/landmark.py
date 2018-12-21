import tensorflow as tf
from keras.applications.resnet50 import ResNet50
from keras.models import Model,load_model
from keras.layers import Dense,GlobalAveragePooling2D,Input
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import Adadelta
import keras
import math, os, sys
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import coremltools

def get_model():
    input_tensor = Input(shape=(224, 224, 3))  # this assumes K.image_data_format() == 'channels_last'

    # create the base pre-trained model
    base_model = ResNet50(input_tensor=input_tensor, weights='imagenet', include_top=False)

    # base_model = ResNet50(input_tensor=None,weights='imagenet',include_top=False)

    for layer in base_model.layers:
        layer.trainable = False

    x = base_model.output
    x = GlobalAveragePooling2D(data_format='channels_last')(x)
    x = Dense(num_classes, activation='softmax')(x)

    updatedModel = Model(base_model.input, x)

    return updatedModel

def compile_model(compiledModel):

    compiledModel.compile(loss=keras.losses.categorical_crossentropy,
                  optimizer=Adadelta(),
                  metrics=['accuracy'])


def modelFitGenerator(fitModel):
    num_train_samples = sum([len(files) for r, d, files in os.walk(train_data_dir)])
    num_valid_samples = sum([len(files) for r, d, files in os.walk(validation_data_dir)])

    print(num_valid_samples)
    num_train_steps = math.floor(num_train_samples / batch_size)
    num_valid_steps = math.floor(num_valid_samples / batch_size)
    print(num_valid_steps)

    train_datagen = ImageDataGenerator(
        rotation_range=90,
        horizontal_flip=True,
        vertical_flip=True,
        zoom_range=0.4)

    test_datagen = ImageDataGenerator()

    train_generator = train_datagen.flow_from_directory(
        train_data_dir,
        target_size=image_size,
        batch_size=batch_size,
        class_mode='categorical', shuffle=True
    )

    validation_generator = test_datagen.flow_from_directory(
        validation_data_dir,
        target_size=image_size,
        batch_size=batch_size,
        class_mode='categorical', shuffle=True
    )

    print("start history model")

    history = fitModel.fit_generator(
        train_generator,
        steps_per_epoch=num_train_steps,
        epochs=nb_epoch,
        validation_data=validation_generator,
        validation_steps=num_valid_steps)

    printGraph(history)


def printGraph(history):
    fig1 = plt.figure()
    plt.plot(history.history['acc'])
    plt.plot(history.history['val_acc'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    fig1.savefig("1.png")
    # summarize history for loss
    fig2 = plt.figure()
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    fig2.savefig("2.png")


def saveCoreMLModel(kerasModel):
    coreml_model = coremltools.converters.keras.convert(kerasModel,
                                                        input_names=['input'],
                                                        output_names=['probs'],
                                                        image_input_names='input',
                                                        predicted_feature_name='predictedMoney',
                                                        class_labels='labels.txt')
    coreml_model.save('resnet50custom.mlmodel')
    print('CoreML model saved')


def main():
    model = get_model()
    compile_model(model)
    modelFitGenerator(model)
    saveCoreMLModel(model)


if __name__ == '__main__':
    # constants
    image_size = (224, 224)
    train_data_dir = 'train'
    validation_data_dir = 'test'
    nb_epoch = 1
    batch_size = 16
    num_classes = 981
    main()
