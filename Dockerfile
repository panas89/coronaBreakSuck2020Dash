FROM ubuntu:latest

RUN apt-get update -y && apt-get install -y \
    python3-pip \
    python3-dev \
    git \
    wget

COPY ./requirements.txt /requirements.txt

WORKDIR /

RUN pip3 install -r requirements.txt

RUN python3 -m spacy download en_core_web_sm

COPY . /

RUN bash ./install_opennre.sh

# UNCOMMENT when running locally, to expose app on a port
EXPOSE 5000

ENTRYPOINT [ "python3" ]

CMD [ "app/dash/index.py" ]
