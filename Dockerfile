# use an official Python runtime as a parent image
FROM python:3.7.2-slim

# set the working directory to /app
WORKDIR /app

# copy the requirements into the container at /app
ADD ./requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

ADD . /app
