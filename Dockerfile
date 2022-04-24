FROM pytorch/pytorch:1.8.1-cuda11.1-cudnn8-devel

WORKDIR /app

RUN pip install --upgrade pip

RUN apt-get -y update
# for dlib
RUN apt-get install -y build-essential cmake
# for opencv
RUN apt-get install -y libopencv-dev

# pip install
COPY ./requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

COPY . .



ENTRYPOINT [ "python", "./app.py" ]