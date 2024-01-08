from src.exception import CustomException
from src.entity.config import PredictConfig
from src.components.predict import Prediction
import os, sys
import cv2
import numpy as np
from from_root import from_root
from src.logger import logging

config = PredictConfig()

def save_uploaded_file(file) -> str:
    """
    Save the uploaded video file and return its path.
    """
    upload_folder = "uploaded_videos"
    os.makedirs(upload_folder, exist_ok=True)
    # Clear the contents of the upload folder
    for filename in os.listdir(upload_folder):
        file_path = os.path.join(upload_folder, filename)
        if os.path.isfile(file_path):
            os.unlink(file_path)

    # Save the new file
    file_path = os.path.join(upload_folder, file.filename)

    try:
        with open(file_path, "wb") as video_file:
            video_file.write(file.file.read())
        return file_path
    except Exception as e:
        raise CustomException(e, sys)

def duplicate_image(img, num_frames):
    logging.info("Duplicate the image into num_frames frames")
    duplicated_frames = [img.copy() for _ in range(num_frames)]
    return duplicated_frames

def create_video(frames, output_video_path):
    logging.info(f"Create image to video...")
    # Get the height and width of the images
    height, width, _ = frames[0].shape

    # Define the video writer
    video_writer = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'mp4v'), 10, (width, height))

    # Write frames to the video
    for frame in frames:
        video_writer.write(frame)

    # Release the video writer
    video_writer.release()
    return True

def process_image(upload_file):
    logging.info("Process the image")
    
    # Read the contents of the UploadFile object
    contents = upload_file.file.read()
    
    # Decode the image
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    return img
# def process_image(file_path):
#     logging.info("Process the image")
#     img = cv2.imread(file_path)
#     if img is None:
#         raise CustomException("Unable to read the image file.", sys)
#     return img

def image_to_video(image_file):
    # Load the image
    img = process_image(image_file)

    # Duplicate the image frames
    num_frames = config.SEQUENCE_LENGTH
    duplicated_frames = duplicate_image(img, num_frames)

    # Specify the output video path
    upload_folder = "uploaded_videos"
    output_video_path = os.path.join(from_root(), upload_folder, "output_video.mp4")
    logging.info(f"Created output path: {output_video_path}")

    # Create the video
    video_created = create_video(duplicated_frames, output_video_path)

    if video_created:
        return output_video_path

if __name__ == "__main__":
    predicted_class = ""
    searchedVideos = []
    image_file = "test.png"  # Change this to the actual image file path
    output_video_file = image_to_video(image_file)

    pred_pipeline = Prediction()
    predicted_class, searchedVideos = pred_pipeline.run_predictions(output_video_file)

    print(predicted_class, searchedVideos)
