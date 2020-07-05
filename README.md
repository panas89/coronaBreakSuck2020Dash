# coronaBreakSuck2020Dash

[! https://img.shields.io/github/license/panas89/coronaBreakSuck2020Dash] [! https://img.shields.io/badge/Made%20at-Starschema-red]
A short description of the project.


## Running locally

Download the data and put it into the app: https://drive.google.com/drive/u/1/folders/1SAjRElTh9Vg0NzhC_Jv9JCuaIEh8UjuB

To run a development instance locally, create a virtualenv, install the 
requirements from `requirements.txt` and launch `app.py` using the 
Python executable from the virtualenv:

```python app.py```

## Deploying on ECS

Use `make image` to create a Docker image. Then, follow [these 
instructions](https://www.chrisvoncsefalvay.com/2019/08/28/deploying-dash-on-amazon-ecs/) 
to deploy the image on ECS.
