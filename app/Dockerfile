FROM ubuntu:22.04

# Install all required Android build dependencies for ARM/Mac M-series
RUN apt-get update && apt-get install -y \
    python3-pip python3-dev python3-setuptools \
    openjdk-17-jdk-headless zip unzip git curl \
    autoconf libtool pkg-config zlib1g-dev libncurses5-dev \
    libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev \
    && apt-get clean

# Install Buildozer and its dependencies globally
RUN pip3 install --upgrade pip
RUN pip3 install buildozer setuptools cython

# Set up the work directory
WORKDIR /home/user/hostcwd
ENTRYPOINT ["buildozer"]