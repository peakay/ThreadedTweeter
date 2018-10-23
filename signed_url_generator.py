import boto3
import os
import uuid
import requests 

upload_key = uuid.uuid4().hex

session = boto3.session.Session(
      aws_access_key_id='AKIAICD2YSSP6ZTF75FA', 
      aws_secret_access_key='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')

s3 = session.client('s3')
fields = {"acl": "public-read"}

# Ensure that the ACL isn't changed and restrict the user to a length
# between 10 and 100.
conditions = [
    {"acl": "public-read"},
    ["content-length-range", 10, 10000000]
]

# Generate the POST attributes
post = s3.generate_presigned_post(
    Bucket='threadtweeter-media',
    Key=upload_key,
    Fields=fields,
    Conditions=conditions
)
files = {"file": "asdfgasgadfhasdfgadflkjasdfgalskfj"}
print(post)

#response = requests.post(post["url"], data=post["fields"], files=files)
#cd print(response.json)