from io import BytesIO
import time

import boto3
from PIL import Image


s3 = boto3.client('s3')

print("original ojbect from s3 bucket:")
original = s3.get_object(
	#Bucket='testing-s3-lambda-cchicata',
	Bucket='canada-testing',
	Key='Screenshot_20210313_212113.png')
original_data = original.get("Body").read()
original = Image.open(BytesIO(original_data))
original.save('imagedFriends.png')

print('Object processed by S3 object lambda:')
start_time = time.time()
try:
	transformed = s3.get_object(
		Bucket='arn:aws:s3-object-lambda:ca-central-1:575234085143:accesspoint/object-lambda-demo-laws-ep2',
		Key='Screenshot_20210313_212113_683x384_JPEG.png')
	print("--- %s seconds ---" % (time.time() - start_time))
	transformed_data = transformed.get("Body").read()
	transformed = Image.open(BytesIO(transformed_data))
	transformed.save('imagedFriendsV3.JPEG')
except Exception as e:
	print(e)
	print("--- %s seconds ---" % (time.time() - start_time))
