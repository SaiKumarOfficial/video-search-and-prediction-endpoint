# Orbit: Video Search and Classification

## Overview

Orbit is a web application designed to facilitate video search and classification, specifically tailored for content relevant to the Indian Space Research Organisation (ISRO). The application employs a Long-Short Term Memory with Recurrent Convolutional Networks (LRCN) model for video classification. It supports five initial class labels: 'Animation', 'Graphics', 'IndoorControlRoom', 'OutdoorLaunchpad', and 'PersonCloseUp'. Utilizing Annoy for efficient embedding representation, the application provides users with the ten most relevant videos using Approximate Nearest Neighbors (ANN).

## Problem Statement

Organizations like ISRO generate a vast amount of video content that needs to be categorized and made easily accessible. Traditional methods of video classification and search can be time-consuming and inefficient. There's also a concern about the storage space required for deploying such models, leading to increased costs.

## Solution

Orbit addresses these challenges by combining video classification and search functionalities within a single web application. It streamlines the process for users to input videos or images related to ISRO and receive classifications. The use of LRCN ensures accurate video categorization, and Annoy, coupled with ANN, efficiently retrieves the most relevant videos.

## Pipelines

This project is organized into three pipelines, each serving a specific purpose in the development lifecycle.

### 1. Data Collection Pipeline

The Data Collection Pipeline is responsible for gathering, processing, and preparing the data needed for the machine learning model. This pipeline automates the process of data extraction, transformation, and loading (ETL).

- **Repository Link:**
  [Data Collection Pipeline Repository](https://github.com/SaiKumarOfficial/video-search-and-classification-data-collection)

### 2. Training Pipeline

The Training Pipeline focuses on training deep learning models using the prepared data from the Data Collection Pipeline. It includes scripts, configurations, and workflows for model training, evaluation, and validation.

- **Repository Link:**
  [Training Pipeline Repository](https://github.com/SaiKumarOfficial/video-search-and-classification-training-endpoint)

### 3. Production Pipeline

The Production Pipeline handles the deployment and maintenance of the trained deep learning models in a production environment. It includes scripts, configurations, and workflows for model deployment, monitoring, and scaling.

- **Repository Link:**
  [Production Pipeline Repository](https://github.com/SaiKumarOfficial/video-search-and-prediction-endpoint)

## Architecture
![predictionEndpoint](https://github.com/SaiKumarOfficial/video-search-and-prediction-endpoint/assets/95096218/1de8e202-b8a2-4bfa-9ba3-ae0e07efd5e3)

## Tech Stack

- Python
- TensorFlow
- AWS IAM, EKS, S3, VPC
- Docker
- Kubernetes
- Mongodb
- Github Actions


## Cost Optimization

To reduce project costs, the Docker image size was minimized using multi-staged builds, decreasing from 3.79GB to 2.28GB. This optimization enabled deployment on a more cost-effective 8GB volume instance, eliminating the "no space" error encountered with the larger image.
## In local
![dockersizesInlocal](https://github.com/SaiKumarOfficial/video-streaming-data-collection/assets/95096218/a919ce03-ea13-4927-991d-afa64cb1e419)

## Compressed image:
![dokersizesInECR](https://github.com/SaiKumarOfficial/video-streaming-data-collection/assets/95096218/45d0b233-5400-43b7-ac8f-151fb4e266b8)


## Project Setup

### Step 1: Clone the repository

```bash
git clone https://github.com/SaiKumarOfficial/video-streaming-data-collection.git
```

### Step 2: Create a conda environment

```bash
conda create -n <your-env-name> python=3.8.18 -y
conda activate <your-env-name>
```

### Step 3: Install requirements

```bash
pip install -r requirements.txt
```

### Step 4: Set environment variables

```bash
export AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID>
export AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY>
export AWS_DEFAULT_REGION=<AWS_DEFAULT_REGION>
export MONGODB_URL="mongodb+srv://<username>:<password>@cluster0.edjcajk.mongodb.net/?retryWrites=true&w=majority"
```

### Step 5: Run the application server

```bash
python app.py
```

### Step 6:  Access the application:

Visit [http://localhost:8050/](http://localhost:8050/)

![1-page](https://github.com/SaiKumarOfficial/video-streaming-data-collection/assets/95096218/c1140fdd-c897-4c57-bec7-9f2aee87414a)

## Step 7: Provide Image or Video as Input
![2-page](https://github.com/SaiKumarOfficial/video-streaming-data-collection/assets/95096218/bb41ef9f-826e-494c-9431-d0fbaa3e02e0)

### Step 8: Explore similar videos

Visit [http://localhost:8050/gallery](http://localhost:8050/gallery)
![3-page](https://github.com/SaiKumarOfficial/video-streaming-data-collection/assets/95096218/d138be30-480f-49f0-a064-824ca4f83964)

# Blue/Green Deployment on AWS EKS

Deployed application on AWS EKS using Blue/Green strategy with zero downtime and other key achievements.

## Achievements

- **Zero Downtime Deployment:**
  - Successfully deployed the application with no impact on user experience, ensuring continuous service availability.

- **Efficient Blue/Green Strategy:**
  - Implemented a Blue/Green deployment approach, allowing simultaneous operation of the current version (Blue) and the updated version (Green).

- **Smooth Traffic Switch:**
  - Enabled a seamless transition of user traffic from the Blue to the Green environment upon successful validation.

- **Quick Rollback Capability:**
  - Implemented a rollback mechanism for quick and efficient reverting to the stable version in case of issues.

- **Consistent User Experience:**
  - Ensured a consistent user experience throughout the deployment process.


## Deployment Setups

I have provided the step by step procedure on how to setup kubernetes and eks cluster. you can check it from the  directory [k8s/kubernetes_setup.md](https://github.com/SaiKumarOfficial/video-search-and-prediction-endpoint/tree/main/k8s) file.

## Deployment Demo
[![Deployment Demo](https://img.youtube.com/vi/ui-0Svj7i1Q/0.jpg)](https://www.youtube.com/watch?v=ui-0Svj7i1Q)



## Run Locally with Docker

1. Check if the Dockerfile is available in the project directory.

2. Build the Docker image:

```bash
docker build --build-arg AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID>
 --build-arg AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY> 
 --build-arg AWS_REGION=<AWS_REGION> 
 --build-arg  MONGODB_URL=<MONGODB_URL> .
```

3. Run the Docker image:

```bash
docker run -d -p 80:80 <IMAGE_NAME>
```

4. Access the application locally:

```bash
http://localhost:80/
```

To run the project, ensure the MongoDB URL is set, and execute the following command:

```bash
python app.py
```

