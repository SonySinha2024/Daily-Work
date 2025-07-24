from google.cloud import aiplatform
from google.collab import auth as google_auth
google_auth.authenticate_user()

import vertexai
PROJECT_ID ="chatbot-45312"
vertexai.init(project=PROJECT_ID)

region="us-central1"
REGION="US-CENTRAL1"
project_id ="chatbot-45312"

# below is part of code
#gcloud config set project {project_id}

## import necessary libs

import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='3'
import warnings
import vertexai
vertexai.init(project =PROJECT_ID, location=REGION)
import kfp
import sys
import uuid
import json
import vertexai
import pandas as pd
from google.auth import default
from datasets import load_dataset
from google.cloud import aiplatform
from vertexai.preview.language_models import TextGenerationModel, EvaluationTextSummarizationSpec


BUCKET_NAME=""
BUCKET_URL=f"gs://my-finetuning-data/TRAIN.jsonl"
REGION="us-central1"

json_url="https://storage.googleapis.com/TRAIN.jsonl"
# or u save in directory of google collab
df =pd.read_json("/content/TRAIN.jsonl",lines=True)
df.head()
df.shape()

## fine tuning codes
model_display_name="bbc-finetuned-model"
tuned_model=TextGenerationModel.from_pretrained("text-bison@002")
tuned_model.tune_model(
    training_data=df,
    train_steps=100,
    tuning_job_location="europe-west4",
    tuned_model_location="europe-west4"
)
## when executing above codes, we get an URL
#like
#https://console.cloud.google.com/vertex-ai/location
# click on the above url with the same gcp account

## response from the fine tuned model
response = tuned_model.predict("Summarize this text to generate a title: \n Ever noticed how plane seats appear to be getting smaller and smaller? With increasing numbers of people taking to the skies, some experts are questioning if having such packed out planes is putting passengers at risk. They say that the shrinking space on aeroplanes is not only uncomfortable it it's putting our health and safety in danger. More than squabbling over the arm rest, shrinking space on planes putting our health and safety in danger? This week, a U.S consumer advisory group set up by the Department of Transportation said at a public hearing that while the government is happy to set standards for animals flying on planes, it doesn't stipulate a minimum amount of space for humans.")
print(response.text)

#To predict with the base model (text-bison@002) for comparison, run the following commands:
base_model = TextGenerationModel.from_pretrained("text-bison@002")
response = base_model.predict("Summarize this text to generate a title: \n Ever noticed how plane seats appear to be getting smaller and smaller? With increasing numbers of people taking to the skies, some experts are questioning if having such packed out planes is putting passengers at risk. They say that the shrinking space on aeroplanes is not only uncomfortable it it's putting our health and safety in danger. More than squabbling over the arm rest, shrinking space on planes putting our health and safety in danger? This week, a U.S consumer advisory group set up by the Department of Transportation said at a public hearing that while the government is happy to set standards for animals flying on planes, it doesn't stipulate a minimum amount of space for humans.")
print(response.text)

## Load the fine tuned model
# It might be easier to load a model that you just fine-tuned. 
# But remember in step 3, it is invoked in the scope of the code itself so it still holds the tuned model in the variable tuned_model. 
# But what if you want to invoke a model that was tuned in the past?
# To do this, you can invoke the get_tuned_model() method on the LLM with the full ENDPOINT URL of the deployed fine tuned model from Vertex AI Model Registry. 
# Note that in this case, you are entering the PROJECT_NUMBER and the MODEL_NUMBER instead of their respective ids.

tuned_model_1 = TextGenerationModel.get_tuned_model("projects/<<PROJECT_NUMBER>>/locations/europe-west4/models/<<MODEL_NUMBER>>")
print(tuned_model_1.predict("YOUR_PROMPT"))

