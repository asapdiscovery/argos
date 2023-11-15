# Use the conda-forge base image with Python
FROM mambaorg/micromamba:jammy

# set environment variables
ENV PYTHONUNBUFFERED 1

# set work directory
WORKDIR /argos
# copy project
COPY . /argos

RUN micromamba config append channels conda-forge 
RUN  micromamba config append channels openeye

COPY --chown=$MAMBA_USER:$MAMBA_USER devtools/conda-envs/argos-ubuntu-latest.yml /tmp/env.yaml

RUN micromamba install -y -n base git -f /tmp/env.yaml && \
    micromamba clean --all --yes

ARG MAMBA_DOCKERFILE_ACTIVATE=1

