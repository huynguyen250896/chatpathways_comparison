FROM python:3.9

# copy source into container
WORKDIR /workspace
COPY . /workspace

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install Python libraries
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# Install bash
RUN apt-get update && apt-get install -y bash