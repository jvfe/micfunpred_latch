# latch base image + dependencies for latch SDK --- removing these will break the workflow
from 812206152185.dkr.ecr.us-west-2.amazonaws.com/latch-base:9c8f-main
run pip install latch==2.17.0
run mkdir /opt/latch

# install system requirements
copy system-requirements.txt /opt/latch/system-requirements.txt
run apt-get update --yes && xargs apt-get install --yes </opt/latch/system-requirements.txt

# install MicFunPred
run curl -L \
    https://github.com/microDM/MicFunPred/archive/refs/heads/master.zip \
    -o MicFunPred.zip &&\
    unzip MicFunPred.zip &&\
    cd MicFunPred-master &&\
    pip install .

# copy all code from package (use .dockerignore to skip files)
copy . /root/

# latch internal tagging system + expected root directory --- changing these lines will break the workflow
arg tag
env FLYTE_INTERNAL_IMAGE $tag
workdir /root
