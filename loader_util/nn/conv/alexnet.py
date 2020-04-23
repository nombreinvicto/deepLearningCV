from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import \
    BatchNormalization, \
    Conv2D, \
    MaxPool2D, \
    Activation, \
    Flatten, \
    Dropout, \
    Dense
from tensorflow.keras.regularizers import l2
from tensorflow.keras import backend as K


class AlexNet:
    @staticmethod
    def build(width, height, depth, classes, reg=0.0002):
        # initialise the model
        model = Sequential()
        inputShape = height, width, depth
        chanDim = -1

        # if we are using channel first update input shape
        if K.image_data_format() == "channel_first":
            inputShape = depth, height, width
            chanDim = 1

        # Block1: CONV-RELU-POOL
        model.add(Conv2D(filters=96,
                         kernel_size=(11, 11),
                         strides=(4, 4),
                         input_shape=inputShape,
                         padding='same',
                         kernel_regularizer=l2(reg)))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=chanDim))
        model.add(MaxPool2D(pool_size=(3, 3), strides=(2, 2)))
        model.add(Dropout(0.25))

        # Block2: CONV-RELU-POOL
        model.add(Conv2D(filters=256,
                         kernel_size=(5, 5),
                         padding='same',
                         kernel_regularizer=l2(reg)))
        model.add(Activation('relu'))
        model.add(BatchNormalization(axis=chanDim))
        model.add(MaxPool2D(pool_size=(3, 3), strides=(2, 2)))
        model.add(Dropout(0.25))

        # Block #3: CONV => RELU => CONV => RELU => CONV => RELU
        model.add(Conv2D(384, (3, 3), padding="same",
                         kernel_regularizer=l2(reg)))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=chanDim))
        model.add(Conv2D(384, (3, 3), padding="same",
                         kernel_regularizer=l2(reg)))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=chanDim))
        model.add(Conv2D(256, (3, 3), padding="same",
                         kernel_regularizer=l2(reg)))
        model.add(Activation("relu"))
        model.add(BatchNormalization(axis=chanDim))
        model.add(MaxPool2D(pool_size=(3, 3), strides=(2, 2)))
        model.add(Dropout(0.25))

        # Block #4: first set of FC => RELU layers
        model.add(Flatten())
        model.add(Dense(4096, kernel_regularizer=l2(reg)))
        model.add(Activation("relu"))
        model.add(BatchNormalization())
        model.add(Dropout(0.5))

        # Block #5: second set of FC => RELU layers
        model.add(Dense(4096, kernel_regularizer=l2(reg)))
        model.add(Activation("relu"))
        model.add(BatchNormalization())
        model.add(Dropout(0.5))

        # softmax classifier
        model.add(Dense(classes, kernel_regularizer=l2(reg)))
        model.add(Activation("softmax"))

        # return the constructed network architecture
        return model
