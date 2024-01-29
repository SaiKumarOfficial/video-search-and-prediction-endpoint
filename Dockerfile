######################
# Stage -1
######################
FROM python:3.8.18 AS build
COPY . /prediction
WORKDIR /prediction

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

######################
# Stage -2
######################
FROM python:3.8.18-slim

# Install required libraries
RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0

# Copy the application files
COPY --from=build /prediction /prediction
COPY --from=build /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages


# Set the working directory
WORKDIR /prediction

# Set environment variables
ENV PYTHONPATH=/usr/local/lib/python3.8/site-packages
ENV LD_LIBRARY_PATH=/usr/local/lib:${LD_LIBRARY_PATH}

# Fetch the artifacts
RUN python src/components/storage_helper.py
# Expose the port
EXPOSE 80

# Run the application
CMD ["python", "app.py"]