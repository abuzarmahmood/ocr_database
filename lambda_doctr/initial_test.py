from doctr.models import ocr_predictor
from doctr.io import DocumentFile
import os
from tqdm import tqdm

def get_bag_of_words(json_output):
  pages = json_output['pages']
  bag_of_words = []
  for this_page in pages:
    for this_block in this_page['blocks']:
      for this_line in this_block['lines']:
        bag_of_words.extend([x['value'] for x in this_line['words']])
  return bag_of_words

model = ocr_predictor(pretrained=True, detect_orientation=True)
file_path = './test.pdf'
pdf_content = open(file_path, 'rb').read()
pdf_doc = DocumentFile.from_pdf(pdf_content)
result = model(pdf_doc)
json_output = result.export()
bag_of_words = get_bag_of_words(json_output)
print(bag_of_words)
