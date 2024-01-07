from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import File, UploadFile
from src.components.predict import Prediction
from fastapi import FastAPI, Request,UploadFile, File, HTTPException
import uvicorn
import os      


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"))
TEMPLATES = Jinja2Templates(directory='templates')
searchedVideos = []
predicted_class = ""

predict_pipe = Prediction()


def save_uploaded_file(file: UploadFile) -> str:
    """
    Save the uploaded video file and return its path.
    """
    upload_folder = "uploaded_videos"
    os.makedirs(upload_folder, exist_ok=True)
    # Clear the contents of the upload folder
    for filename in os.listdir(upload_folder):
        file_path = os.path.join(upload_folder, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to clear the upload folder: {e}")

    # save the new file
    file_path = os.path.join(upload_folder, file.filename)

    try:
        with open(file_path, "wb") as video_file:
            video_file.write(file.file.read())
        return file_path
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save the video file: {e}")
    
@app.get("/", status_code=200)
@app.post("/")
async def index(request: Request):
    """
    Description : This Route loads the index.html
    """
    return TEMPLATES.TemplateResponse(name='index.html', context={"request": request})


@app.post('/video')
async def upload_video_and_predict(file: UploadFile = File(...)):
    """
    Description: This route uploads the video file and runs predictions.
    """
    global searchedVideos, predict_pipe, predicted_class

    try:
        if predict_pipe:
            # Save the uploaded video file
            file_path = save_uploaded_file(file)

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
    return TEMPLATES.TemplateResponse('gallery.html', context={"request": request, "length": len(searchedVideos),
                                                               "searchedVideos": searchedVideos, "predicted_class": predicted_class})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3001)

