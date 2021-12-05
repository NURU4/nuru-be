import requests
import boto3


bucket_name = "nuruimages"
client = boto3.client(
				's3', 
                aws_access_key_id='AKIAXGUVCKKK7DWDXFHU', 
                aws_secret_access_key='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',    
)
user_image_key = "test"
myobjects = client.list_objects_v2(Bucket='nuruimages', Prefix="fileuploadtest")
print(myobjects)

