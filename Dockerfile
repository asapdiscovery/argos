# Use the conda-forge base image with Python
FROM continuumio/miniconda3:latest


# set environment variables
ENV PYTHONUNBUFFERED 1

# set work directory
WORKDIR /argos
# copy project
COPY . /argos



# COPY --chown=$MAMBA_USER:$MAMBA_USER devtools/conda-envs/argos-ubuntu-latest.yml /tmp/env.yaml

RUN conda env create --file devtools/conda-envs/argos-ubuntu-latest.yml  && \
    conda clean --all --yes

ARG MAMBA_DOCKERFILE_ACTIVATE=1

