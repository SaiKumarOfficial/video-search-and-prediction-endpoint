from tensorflow.keras.model import Sequential   
from tensorflow.keras.layers import TimeDistributed, Flatten, LSTM, Dropout, Dense
from tensorflow.keras.layers import Conv2D, MaxPooling2D
# from tensorflow.keras.optimizers import Adam
# from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from src.logger import logging
from src.entity.config import PredictConfig
from src.exception import CustomException
import sys

class LRCN_model:
    def __init__(self):
        self.config = PredictConfig()

    
    def create_LRCN_model(self):
        try:
        
            labels = self.config.CLASSES_LIST

            logging.info(" Constructing  model architecture...")
            model = Sequential()

            model.add(TimeDistributed(Conv2D(16, (3, 3), padding='same',activation ='relu'),
                                    input_shape = (self.config.SEQUENCE_LENGTH, self.config.IMAGE_HEIGHT, self.config.IMAGE_WIDTH, 3)))
            model.add(TimeDistributed(MaxPooling2D((4, 4))))
            # model.add(TimeDistributed(Dropout(0.25)))

            model.add(TimeDistributed(Conv2D(32, (3, 3), padding='same',activation = 'relu')))

            model.add(TimeDistributed(MaxPooling2D((4, 4))))
            model.add(TimeDistributed(Dropout(0.2)))

            model.add(TimeDistributed(Conv2D(64, (3, 3), padding='same',activation = 'relu')))

            model.add(TimeDistributed(MaxPooling2D((2, 2))))
            model.add(TimeDistributed(Dropout(0.2)))

            model.add(TimeDistributed(Conv2D(64, (3, 3), padding='same',activation = 'relu')))

            model.add(TimeDistributed(MaxPooling2D((2, 2))))
            # model.add(TimeDistributed(Dropout(0.25)))

            model.add(TimeDistributed(Flatten()))

            model.add(LSTM(32))

            model.add(Dense(len(labels), activation = 'softmax'))
    
            # Display the models summary.
            # model.summary()

            # Return the constructed LRCN model.
            return model
    
        except Exception as e:
            raise CustomException(e,sys)