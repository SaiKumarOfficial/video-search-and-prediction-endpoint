from src.components.custom_ann import CustomAnnoy
from src.entity.config import PredictConfig
from src.logger import logging
import tensorflow as tf
import numpy as np
import cv2
from collections import deque
from from_root import from_root
import os
from collections import Counter

class Prediction(object):
    def __init__(self):
        self.config = PredictConfig()
        self.device = 'cpu'
        self.model_path = self.config.MODEL_PATHS[1][0]
        self.sequence_length = self.config.SEQUENCE_LENGTH
        self.annoy_artifact = self.config.MODEL_PATHS[0][0]
        self.ann = CustomAnnoy(self.config.EMBEDDINGS_LENGTH, 
                               self.config.SEARCH_MATRIX)
        
        self.ann.load(self.annoy_artifact)
        self.estimator = self.load_model()
        self.transforms = self.transformations()

    def load_model(self):
        model = tf.keras.models.load_model(self.model_path)
        return tf.keras.Sequential(model.layers[:-1])
    
    
    def transformations(self):

        def preprocess_video(video_path):
        # Open the video file
            video_reader = cv2.VideoCapture(str(video_path))

            # Get the total number of frames in the video
            video_frames_count = int(video_reader.get(cv2.CAP_PROP_FRAME_COUNT))

            # Calculate the skip frames window based on the sequence length
            skip_frames_window = max(int(video_frames_count / self.sequence_length), 1)

            # Initialize an empty list to store video frames
            frames = []

            # Loop through frames based on the sequence length
            for frame_counter in range(self.sequence_length):
                # Set the current frame position of the video
                video_reader.set(cv2.CAP_PROP_POS_FRAMES, frame_counter * skip_frames_window)

                # Read the frame
                ret, frame = video_reader.read()

                # Check if the frame is successfully read
                if not ret:
                    break

                # Convert the frame to RGB format (assuming BGR format from OpenCV)
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                resized_frame = cv2.resize(frame_rgb, (self.config.IMAGE_HEIGHT, self.config.IMAGE_WIDTH))
                normalized_frame = resized_frame/255.0
                # Add the frame to the list
                frames.append(normalized_frame)
            frames = np.array(frames)
            # Close the video file
            video_reader.release()

            return frames

        return preprocess_video

    def generate_embeddings(self, video_frames):
        
        video_frame = self.estimator.predict(video_frames)
        return video_frame
    
    def generate_links(self, embedding):
        return self.ann.get_nns_by_vector(embedding, self.config.NUMBER_OF_PREDICTIONS)
    
    def predict_on_video(self, model, video_file_path, sequence_length):
        video_reader = cv2.VideoCapture(video_file_path)
        video_frames_count = int(video_reader.get(cv2.CAP_PROP_FRAME_COUNT))
        skip_frames_window = max(int(video_frames_count / sequence_length), 1)

        logging.info(f"skip frames window : {skip_frames_window}")
        print(f"skip frames window : {skip_frames_window}")
        frames_queue = deque(maxlen=sequence_length)
        predicted_labels = []

        frame_counter = 0

        while video_reader.isOpened():
            # Set the current frame position of the video
            video_reader.set(cv2.CAP_PROP_POS_FRAMES, frame_counter * skip_frames_window)

            # Read the frame
            ok, frame = video_reader.read()

            if not ok:
                break

            resized_frame = cv2.resize(frame, (self.config.IMAGE_HEIGHT, self.config.IMAGE_WIDTH))
            normalized_frame = resized_frame / 255.0
            frames_queue.append(normalized_frame)

            if len(frames_queue) == sequence_length:
                # Batch prediction for better performance.
                frames_batch = np.expand_dims(frames_queue, axis=0)
                predicted_labels_probabilities = model.predict(frames_batch)[0]
                predicted_label = np.argmax(predicted_labels_probabilities)
                predicted_class_name = self.config.CLASSES_LIST[predicted_label]
                predicted_labels.append(predicted_class_name)

            frame_counter += 1
        logging.info(f"Frame counter:{frame_counter}")
        print(f"Frame counter:{frame_counter}")

        video_reader.release()

        most_common_label = Counter(predicted_labels).most_common(1)
        return most_common_label[0][0]

    
    def run_predictions(self, video_file_path):
        logging.info(f"Run the predcitions for {video_file_path}")
        video_frames = self.transforms(video_file_path)
        video_frames = video_frames.reshape((1,) + video_frames.shape)
        
        logging.info("Generate the embedding of the given input video")
        embedding = self.generate_embeddings(video_frames)
        # print(embedding)
        logging.info("Return predicted video links ")
        predicted_similar_videos = self.generate_links(embedding[0])

        #===================================================================


        logging.info("Load the model for Class prediction")
        model = tf.keras.models.load_model(self.model_path)
        
        logging.info("Predict the class and return on video at the output file path ")
        predicted_class = self.predict_on_video( model, video_file_path, self.sequence_length )

        return predicted_class, predicted_similar_videos
    
# if __name__=="__main__":
#     pred = Prediction()
#     video_file_path = os.path.join(from_root(), "test_videos", "input.mp4")
#     #output_video_file_path = os.path.join(from_root(), "test_videos", "output.mp4")

#     # started predicrtions
#     predicted_class, resultant_links = pred.run_predictions(video_file_path)

#     logging.info(f"Resultant class: {predicted_class},Resultant links: {resultant_links}")
#     print(predicted_class, resultant_links)


