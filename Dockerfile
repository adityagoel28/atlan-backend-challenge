# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.11

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# create root directory for our project in the container
RUN mkdir /data_collection

# Set the working directory to /data_collection
WORKDIR /data_collection

COPY requirements.txt /data_collection/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /data_collection
COPY . /data_collection/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]