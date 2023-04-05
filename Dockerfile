# latch base image + dependencies for latch SDK --- removing these will break the workflow
FROM 812206152185.dkr.ecr.us-west-2.amazonaws.com/latch-base:9c8f-main
RUN pip install latch==2.14.2
RUN mkdir /opt/latch

RUN apt-get install -y curl unzip

# Get miniconda
# RUN curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
#     --output miniconda.sh &&\
#     bash miniconda.sh -b -p /opt/conda
# ENV CONDA_DIR /opt/conda
# ENV PATH=$CONDA_DIR/bin:$PATH

# Get Mamba
# RUN conda install -y mamba -n base -c conda-forge

# copy all code from package (use .dockerignore to skip files)
COPY . /root/

# latch internal tagging system + expected root directory --- changing these lines will break the workflow
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag
WORKDIR /root
