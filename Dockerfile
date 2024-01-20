FROM python:3.8.18
COPY . /prediction

# Set the working directory
WORKDIR /prediction

# Install required libraries
RUN apt-get update && apt-get install -y libgl1-mesa-glx
RUN pip3 install --upgrade pip 
RUN pip3 install -r requirements.txt


# Expose the port to 8050
EXPOSE 8050

# Run the application
CMD ["python","app.py"]