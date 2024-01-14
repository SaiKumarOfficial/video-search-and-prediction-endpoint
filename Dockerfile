FROM python:3.8.18
COPY . /prediction

WORKDIR /prediction

RUN apt-get update && apt-get install -y libgl1-mesa-glx
RUN pip3 install --upgrade pip 
RUN pip3 install -r requirements.txt

EXPOSE 8000

CMD ["python","app.py"]
