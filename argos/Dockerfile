# Use the conda-forge base image with Python
FROM mambaorg/micromamba:1.4.1

# set environment variables
ENV PYTHONUNBUFFERED 1

# set work directory
WORKDIR /argos
# copy project
COPY . /argos

# RUN micromamba list

RUN micromamba install -y -n base git -f /devtools/conda_envs/argos-ubuntu-latest.yml && \
    micromamba clean --all --yes

ARG MAMBA_DOCKERFILE_ACTIVATE=1

