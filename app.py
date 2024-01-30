from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import File, UploadFile
from src.utils.application import save_uploaded_file, image_to_video
from src.components.predict import Prediction
from fastapi import FastAPI, Request,UploadFile, File, HTTPException, BackgroundTasks
from src.components.storage_helper import StorageConnection
from src.logger import logging
from fastapi.responses import JSONResponse
import uvicorn
import os     
import time 

connection = StorageConnection()
connection.get_package_from_testing()
time.sleep(10)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"))
TEMPLATES = Jinja2Templates(directory='templates')
searchedVideos = []
predicted_class = ""

predict_pipe = Prediction()



    
@app.get("/", status_code=200)
@app.post("/")
async def index(request: Request):
    
    """
    Description : This Route loads the index.html
    """
   
    
    return TEMPLATES.TemplateResponse(name='index.html', context={"request": request})

@app.post('/image')
async def predict_the_image_class(file: UploadFile = File(...)):
    global searchedVideos, predict_pipe, predicted_class

    try:
        if predict_pipe:
            file_extension = file.filename.split('.')[-1].lower()
            logging.info(f"File_extension: {file_extension}")
            logging.info(f"file : {file}")
            logging.info(f"filecontent: {file.file}")


            print(file_extension)
            if file_extension in ['jpeg', 'jpg', 'png']:
                # Process the uploaded image file and get the video file path
                file_path = image_to_video(file)
                
                logging.info(f"file path: {file_path}")
                print(file_path)
            else:
                return {"message": "Unsupported file format. Please upload a valid .mp4, .jpeg, or .png file."}
            # Save the uploaded video file
            # file_path = save_uploaded_file(file)

            # Check if the file path is valid
            if file_path:
                # Run predictions with the video file path
                predicted_class, searchedVideos = predict_pipe.run_predictions(file_path)
                return {"message": "Prediction Completed"}
            else:
                return {"message": "Failed to save the video file."}
        else:
            return {"message": "First load the model in production using the reload_prod_model route"}
    except Exception as e:
        return {"message": f"There was an error processing the video file: {e}"}

@app.post('/video')
async def upload_video_and_predict(file: UploadFile = File(...)):
    """
    Description: This route uploads the video file and runs predictions.
    """
    global searchedVideos, predict_pipe, predicted_class

    try:
        if predict_pipe:
            file_extension = file.filename.split('.')[-1].lower()

            if file_extension == 'mp4':
                # Save and process the uploaded video file
                file_path = save_uploaded_file(file)
            
            else:
                return {"message": "Unsupported file format. Please upload a valid .mp4, .jpeg, or .png file."}
            # Save the uploaded video file
            # file_path = save_uploaded_file(file)

            # Check if the file path is valid
            if file_path:
                # Run predictions with the video file path
                predicted_class, searchedVideos = predict_pipe.run_predictions(file_path)
                return {"message": "Prediction Completed"}
            else:
                return {"message": "Failed to save the video file."}
        else:
            return {"message": "First load the model in production using the reload_prod_model route"}
    except Exception as e:
        return {"message": f"There was an error processing the video file: {e}"}

@app.post('/reload')
def reload():
    """
    Description : This Route resets the predictions in a list for reload.
    """
    global searchedVideos,predicted_class
    searchedVideos = []
    predicted_class = ""
    return


@app.get('/reload_prod_model')
def reload():
    """
    Description : This Route is Event Triggered or owner controlled to update
                  the model in prod with minimal downtime.
    """
    global predict_pipe
    try:
        del predict_pipe
        predict_pipe = Prediction()
        return {"Response": "Successfully Reloaded"}
    except Exception as e:
        return {"Response": e}


@app.get('/gallery')
async def gallery(request: Request):
    """
    Description : This Route lists all the predicted images on the gallery.html listing depends on prediction.
    """
    global searchedVideos
    # return TEMPLATES.TemplateResponse('gallery.html', context={"request": request, "length": len(searchedVideos),

    #                                                    "searchedVideos": searchedVideos, "predicted_class": predicted_class})
    return {"Response": "Successfully Loaded", "searchedVideos": searchedVideos, "predicted_class": predicted_class}

# @app.get('/get_predicted_class', response_model=dict)
# async def get_predicted_class():
#     """
#     Description: This route returns the predicted class in JSON format.
#     """
#     global predicted_class
#     return JSONResponse(content={"predicted_class": predicted_class})


if __name__ == "__main__":
    

    uvicorn.run(app, host="0.0.0.0", port=80)

