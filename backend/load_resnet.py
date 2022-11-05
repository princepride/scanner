from __future__ import division, print_function
from werkzeug.utils import secure_filename

import tensorflow as tf
from tensorflow.keras.callbacks import ModelCheckpoint,CSVLogger
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Flatten,Input,add
from tensorflow.keras.layers import Conv2D,Add,ZeroPadding2D,AveragePooling2D
from tensorflow.keras.layers import MaxPooling2D,GlobalAveragePooling2D
from tensorflow.keras.layers import BatchNormalization
from tensorflow.keras.layers import Activation
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.utils import plot_model
from tensorflow.keras import optimizers
from tensorflow.keras import regularizers
from keras.losses import categorical_crossentropy
import os

def read_image(path):
    file_bytes = tf.io.read_file(path)
    img = tf.image.decode_png(file_bytes, channels=3)
    img = tf.cast(img, tf.float32) / 255.0
    img = tf.image.resize(img, [200,200], method="nearest")
    return img

def resIdentity_blk(x, filter):
    x_skip = x
    
    #Layer 1
    x = Conv2D(filter, (3,3), padding='same')(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)

    #Layer 2
    x = Conv2D(filter, (3,3), padding='same')(x)
    x = BatchNormalization()(x)

    #Add Layer
    x = Add()([x, x_skip])
    x = Activation('relu')(x)

    return x

def resConv_blp(x, filter):
    x_skip = x

    #Layer 1
    x = Conv2D(filter, (3,3), padding='same', strides = (2,2))(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)

    #Layer 2
    x = Conv2D(filter, (3,3), padding='same')(x)
    x = BatchNormalization()(x)

    #Skip Layer
    x_skip = Conv2D(filter, (1,1), strides = (2,2))(x_skip)
    #x_skip = BatchNormalization()(x_skip)

    #Add Layer
    x = Add()([x, x_skip])
    x = Activation('relu')(x)

    return x

def build_residualCNN(num_classes=3):
  input = tf.keras.Input(shape=(200, 200, 3), name='img')
  #x = ZeroPadding2D((3,3))(inputs)

  #Beginning Conv Layer with MaxPool
  x = Conv2D(16, (3,3), padding='valid', strides=(2,2))(input)
  x = BatchNormalization()(x)
  x = Activation('relu')(x)
  #x = MaxPooling2D(pool_size=(3,3), strides=(2,2))(x)

  x = resConv_blp(x,16)
  x = resIdentity_blk(x,16)
  x = resIdentity_blk(x,16)

  x = resConv_blp(x,32)
  x = resIdentity_blk(x,32)
  x = resIdentity_blk(x,32) 

  x= AveragePooling2D(pool_size=(8,8))(x)
  x= Flatten()(x)

  output = Dense(num_classes, activation='softmax',kernel_initializer='he_normal')(x)
  model = Model(inputs = input,outputs = output)
  return model

class prediction():
    
    def __init__(self,classify_model_weights,num_classes=3):
    
        self.final_classify_model = build_residualCNN()
    
        self.final_classify_model.load_weights(classify_model_weights)
        self.final_classify_model.compile(loss='categorical_crossentropy', optimizer=optimizers.Adam(learning_rate=0.001), metrics=['acc'])
        print('Residual CNN Model Loaded....')
    
    def Predict(self,image_path):
        """
        This function predicts the classfication output.
        ------------------------------------------------------------------
        final_classify_model      : saved classification model instance
        image_path                : image path
        ------------------------------------------------------------------
        """

         # read the original image
        image_orig = read_image(image_path)

        #get the classification output
        classify_output = self.final_classify_model.predict(tf.expand_dims(image_orig, axis=0))
        return classify_output
        #print(classify_output)

def resnetPredict(classify_weights_path, image_path):
    pred = prediction(classify_weights_path)
    classify_output = pred.Predict(image_path)
    return classify_output


if __name__ == '__main__':
    resnetPredict(r"./models/resnetModel17.h5","dirty_crumpled_pet_bottle_6.jpeg")