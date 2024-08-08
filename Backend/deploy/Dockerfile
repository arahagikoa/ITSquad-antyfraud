# Use the official Python 3.9 image based on Debian Bullseye
FROM python:3.8-bullseye


RUN mkdir /APP
RUN mkdir /APP/Backend
COPY . /APP/Backend
COPY ../CNN_MODEL/ /APP/Backend/CNN_MODEL
COPY ../../NLP/training_model/saved_model/ /APP/Backend/saved_model

WORKDIR /APP

RUN apt-get update && \
    apt-get install -y \
    libc6 libgcc-s1 libgssapi-krb5-2 libssl1.1 libstdc++6 zlib1g libgdiplus \
    libpq-dev libxml2-dev libxslt1-dev libldap2-dev libsasl2-dev build-essential libgdiplus \
    curl software-properties-common


RUN wget https://packages.microsoft.com/config/debian/11/packages-microsoft-prod.deb -O packages-microsoft-prod.deb && \
    dpkg -i packages-microsoft-prod.deb && \
    rm packages-microsoft-prod.deb && \
    apt-get update && \
    apt-get install -y dotnet-sdk-6.0
RUN apt-get install -y libopenmpt0


WORKDIR /APP/Backend

# Copy the shell script into the container
COPY dependencies.sh /APP/Backend/dependencies.sh
# Copy requirements.txt file to app
COPY requirements.txt /APP/Backend/requirements.txt
# Make the script executable
RUN chmod +x /APP/Backend/dependencies.sh

# In this shell file are all dependenies necessary to run app
RUN /APP/Backend/dependencies.sh


RUN pip install gunicorn

EXPOSE 80
ENV DOTNET_SYSTEM_GLOBALIZATION_INVARIANT=1
CMD gunicorn --bind=0.0.0.0:80 --timeout 600 main:app
