# ---------------------------------------------------------------------------------
#  1. single text sample: spam prediction
# ---------------------------------------------------------------------------------


import boto3
import json
import pandas as pd

# Define the service
client = boto3.client('machinelearning')

# Realtime prediction endpoint url given in the model summary
endpoint_url = "https://realtime.machinelearning.us-east-1.amazonaws.com"

# Model id to be used, replace with your model ID
model_id = "ml-pFfGptQhkPm"

# Actual text samples to be predicted. JSON formatted
# The first one should not be classfified as spam while the second should

# record = {
#         "body": "Hello world, my name is Adarsh"
#     }

record = {
        "body": "Call now to get free contacts for free, no cash no credit card."
    }

# Use the predict() method of the machine learning service
response = client.predict(
    MLModelId       = model_id,
    Record          = record,
    PredictEndpoint = endpoint_url
)

print json.dumps(response, indent=4)





