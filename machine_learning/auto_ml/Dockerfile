#FROM tensorflow/tensorflow:latest
#
#COPY requirements.txt ./
#RUN pip install --no-cache-dir -r requirements.txt
#
#COPY . /
#
## Run deep_learning.py when the container launches
##CMD ["python", "./deep_learning_test.py"]


FROM --platform=linux/arm64 python:3.10
#from --platform=linux/arm64 python:3.8
ARG TENSORFLOW_VERSION=v2.9.1
ARG DEBIAN_FRONTEND=noninteractive
RUN apt update && apt install -y build-essential python3-dev pkg-config zip zlib1g-dev unzip curl wget git htop openjdk-11-jdk liblapack3 libblas3 libhdf5-dev npm
RUN npm install -g @bazel/bazelisk
RUN pip install six numpy grpcio h5py packaging opt_einsum wheel requests
RUN git clone https://github.com/tensorflow/tensorflow.git && mkdir -p /wheels/tensorflow
WORKDIR tensorflow
RUN git checkout $TENSORFLOW_VERSION
RUN bazel build -c opt --verbose_failures //tensorflow/tools/pip_package:build_pip_package
RUN /bazel-bin/tensorflow/tools/pip_package/build_pip_package /wheels/tensorflow
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . /
CMD ["pip", "install", "--extra-index-url", "/wheels", "tensorflow"]