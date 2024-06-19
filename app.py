import boto3
import json
import base64
import os


prompt_data = """
provide me an 4K hd image of a beech, alos use a blue sky rainy season and cinematic display
"""

prompt_template = [{"text":prompt_data, "weight":1}]

bedrock = boto3.client(service_name="bedrock-runtime")

payload= {

    "text_prompts":prompt_template,
    "cfg_scale": 10,
    "seed": 0,
    "steps": 50,
    "width": 1024,
    "height":1024

}

body = json.dumps(payload)
model_id = "stability.stable-diffusion-xl-v1"
response = bedrock.invoke_model(
    body=body,
    modelId=model_id,
    accept='application/json', # can be commented
    contentType='application/json' # can be commented
)

response_body = json.loads(response.get("body").read())
# print(response_body)

artifact = response_body.get("artifacts")[0]
image_encoded = artifact.get("base64").encode("utf-8")
image_bytes = base64.b64decode(image_encoded)


output_dir = "SD_output"
os.makedirs(output_dir, exist_ok=True)
file_name = f"{output_dir}/generated-image.png"
with open(file_name, "wb") as f:
    f.write(image_bytes)
