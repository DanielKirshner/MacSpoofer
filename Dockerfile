FROM ubuntu:latest

# Update package list and install necessary packages
RUN apt-get update -qq -y && \
    apt-get install -qq -y python3-pip net-tools iproute2 python3-rich

RUN mkdir -pv /spoofer_workspace

COPY ./* /spoofer_workspace