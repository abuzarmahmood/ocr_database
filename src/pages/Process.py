"""
Given uploaded documents, perform OCR and save the extracted text to a database.
"""
import os
import pandas as pd
import streamlit as st
import s3fs

s3 = s3fs.S3FileSystem(
        anon=False,
        key = st.secrets["S3_KEY"], 
        secret = st.secrets["S3_SECRET"] 
        )
# base_path = 's3://ocr-database-s3'
base_path = f's3://{st.secrets["S3_BUCKET_NAME"]}'

# df_path = 'doc_df.csv'
df_path = os.path.join(base_path, 'doc_df.csv')

# if os.path.exists(df_path):
#   df = pd.read_csv(df_path)
if s3.exists(df_path): 
  with s3.open(df_path, 'rb') as f:
      df = pd.read_csv(f)

  if any(df.OCR_attempted == False):

      OCR_false = df[df.OCR_attempted == False]

      if len(OCR_false) == 0:
          st.write("All documents have been OCR'd.")
      else:
          st.write("Documents that need OCR:")
          st.write(OCR_false)

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

      p_bar = st.progress(0)

      for counter, (i, this_row) in enumerate(OCR_false.iterrows()):
        
        pdf_content = s3.open(this_row['file_path'], 'rb').read()
        pdf_doc = DocumentFile.from_pdf(pdf_content)
        # pdf_doc = DocumentFile.from_pdf(this_row['file_path'])
        file_name = os.path.basename(this_row['file_path']) 
        result = model(pdf_doc)
        json_output = result.export()
        bag_of_words = get_bag_of_words(json_output)
        df.at[i, 'words'] = bag_of_words
        df.at[i, 'OCR_attempted'] = True
        # st.write(f"OCR completed for {file_name}")
        # st.write(f"{i}/{len(OCR_false)} completed")

        # df.to_csv(df_path, index=False)
        with s3.open(df_path, 'wb') as f:
            df.to_csv(f, index=False)

        p_bar.progress((counter+1)/len(OCR_false),
                       text=f"OCR'ing {counter+1}/{len(OCR_false)}"
                       )
      st.write("All documents have been OCR'd.")

  else:
    st.write("All documents have been OCR'd.\n" +\
        "No more documents to process.")
else:
  st.write("No documents uploaded yet.")
