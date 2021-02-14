#!/usr/bin/env bash
# The script is obtained from https://github.com/gannochenko/poc_docker-heroku/blob/master/deploy.sh

# Login into heroku (for mac add an underscore after=: --username=_ --)
# docker login --username=_ --password=`heroku auth:token 2> stdout` registry.heroku.com
docker login --username= --password=`heroku auth:token 2> stdout` registry.heroku.com

# Build image
docker build -t registry.heroku.com/covidinsights/web -f ./Dockerfile .

# Push to Heroku
docker push registry.heroku.com/covidinsights/web

# Publish the app
heroku container:release web -a covidinsights