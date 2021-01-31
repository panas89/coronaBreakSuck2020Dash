#!/usr/bin/env bash

# Download OpenNRE in app directory
cd app
echo 'Downloading openre package...'
git clone https://github.com/thunlp/OpenNRE.git

# Install OpenNRE
cd OpenNRE
echo 'Installing opennre package...'
python3 setup.py install 

# Download the pretrain model
wget -P bert-base-uncased https://thunlp.oss-cn-qingdao.aliyuncs.com/opennre/pretrain/bert-base-uncased/config.json
wget -P bert-base-uncased https://thunlp.oss-cn-qingdao.aliyuncs.com/opennre/pretrain/bert-base-uncased/pytorch_model.bin
wget -P bert-base-uncased https://thunlp.oss-cn-qingdao.aliyuncs.com/opennre/pretrain/bert-base-uncased/vocab.txt

# Create the neccessary folder for the pretrain model so that we can run the model smoothly
mkdir -p ~/.opennre2/pretrain/bert-base-uncased/

# Move the pretrain model to the corresponding location for the library, i.e., being with HOME/
mv -f bert-base-uncased/* ~/.opennre2/pretrain/bert-base-uncased/

# return to home
cd ..