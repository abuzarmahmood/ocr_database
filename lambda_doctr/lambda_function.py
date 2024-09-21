import json
import boto3
from doctr.models import ocr_predictor
from doctr.io import DocumentFile
import os

def get_bag_of_words(json_output):
  pages = json_output['pages']
  bag_of_words = []
  for this_page in pages:
    for this_block in this_page['blocks']:
      for this_line in this_block['lines']:
        bag_of_words.extend([x['value'] for x in this_line['words']])
  return bag_of_words

s3Client = boto3.client("s3")

def lambda_handler(event, context):
    # TODO implement
    bucket = event['Records'][0]['s3']['bucket']['name']
    file_name = event['Records'][0]['s3']['object']['key']
    
    print(bucket)
    print(file_name)
    file_basename = os.path.basename(file_name)
    file_basename = file_basename.split('.')[0]
    
    dump_str = f'bucket = {bucket}, key = {file_name}'
    
    response = s3Client.get_object(Bucket = bucket, Key = file_name)
    pdf_content = response['Body'].read()
    print('Data read')

    model = ocr_predictor(pretrained=True, detect_orientation=True)
    pdf_doc = DocumentFile.from_pdf(pdf_content)
    result = model(pdf_doc)
    json_output = result.export()
    bag_of_words = get_bag_of_words(json_output)
    print('OCR processed')

    out_dict = dict(
        file_name = file_name,
        bag_of_words = bag_of_words
    )
    # Write to "Processed" directory
    s3Client.put_object(
            Bucket = bucket, Key = f'Processed/{file_basename}.json', 
            Body = json.dumps(out_dict))
    print('Data written to S3')
    
    return {
        'statusCode': 200,
        'body': json.dumps(dump_str)
    }
