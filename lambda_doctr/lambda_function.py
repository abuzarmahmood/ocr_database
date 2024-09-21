import json
import boto3

s3Client = boto3.client("s3")

def lambda_handler(event, context):
    # TODO implement
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    print(bucket)
    print(key)
    
    dump_str = f'bucket = {bucket}, key = {key}'
    
    response = s3Client.get_object(Bucket = bucket, Key = key)
    data = response['Body'].read()
    print('Data read')
    
    return {
        'statusCode': 200,
        'body': json.dumps(dump_str)
    }
