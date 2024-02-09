# Use the conda-forge base image with Python
FROM mambaorg/micromamba:jammy


ARG USER_ID
ARG GROUP_ID

USER root

RUN addgroup --gid $GROUP_ID user
RUN adduser --disabled-password --gecos '' --uid $USER_ID --gid $GROUP_ID user
USER user


# set environment variables
ENV PYTHONUNBUFFERED 1

# set work directory
WORKDIR /argos
# copy project
COPY . /argos


RUN micromamba config append channels conda-forge 
RUN  micromamba config append channels openeye

COPY --chown=user:user devtools/conda-envs/argos-ubuntu-latest.yml /tmp/env.yaml

RUN micromamba install -y -n base git -f /tmp/env.yaml && \
    micromamba clean --all --yes

USER root
RUN mkdir /openeye
RUN chown -R user:user /openeye
RUN mkdir /argos/pdb_data
RUN chown -R user:user /argos/pdb_data
USER user
ENV OE_LICENSE=/openeye/oe_license.txt


ARG MAMBA_DOCKERFILE_ACTIVATE=1

