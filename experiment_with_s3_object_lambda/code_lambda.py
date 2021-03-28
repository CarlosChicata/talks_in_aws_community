'''
Purpose:
	Resize and formatting Image based URL params.

Remember:
	- need to create a policy contains "S3 object lambda" and "S3" service.
'''
import io

import boto3
import requests
from PIL import Image


def processing_url(url):
    surl = url.split('/')
    key = surl[-1]
    new_size = tuple([ int(x) for x in key.split("_")[-2].split("x")])
    formating = url.split(".")[-2].split("_")[-1]
    clean_url = "_".join(url.split("/")[-1].split("_")[:-2]) + "." + url.split("/")[-1].split(".")[1]
    return new_size, key, clean_url, formating
    

def lambda_handler(event, context):
    print(event)
    
    object_get_context = event["getObjectContext"]
    request_route = object_get_context["outputRoute"]
    request_token = object_get_context["outputToken"]
    s3_url = object_get_context["inputS3Url"]
    in_mem_file = io.BytesIO()
    # processing s3 URL and get data to processing
    new_size, original_url, clean_url, formatting = processing_url(event["userRequest"]["url"])
    
    # get object from s3
    s3 = boto3.client('s3')
    s3_bucket = event["configuration"]["payload"]
    response = s3.get_object(Bucket=s3_bucket, Key=clean_url)

    # resize and formatting original image
    original_object = Image.open(io.BytesIO(response['Body'].read()))
    transformed_object = original_object.resize(new_size)
    transformed_object.save(in_mem_file, format=formatting)
    
    # Write object back to S3 Object Lambda
    s3.write_get_object_response(
        Body=in_mem_file.getvalue(),
        RequestRoute=request_route,
        RequestToken=request_token)

    return {'status_code': 200}
