"""
Search through words extracted from OCR to find a specific word or phrase.
"""

import os
import pandas as pd
import streamlit as st
from thefuzz import fuzz, process
import numpy as np
from ast import literal_eval
import s3fs
from streamlit_pdf_viewer import pdf_viewer

s3 = s3fs.S3FileSystem(
        anon=False,
        key = st.secrets["S3_KEY"], 
        secret = st.secrets["S3_SECRET"] 
        )
# base_path = 's3://ocr-database-s3'
base_path = f's3://{st.secrets["S3_BUCKET_NAME"]}'
data_path = os.path.join(base_path, 'Data')

df_path = os.path.join(base_path, 'doc_df.csv')

############################################################
# Process 
############################################################
# If any jsons in s3://Processed, load them into the dataframe
# and remove them from the s3 bucket
processed_path = os.path.join(base_path, 'Processed')

if s3.exists(df_path):
  with s3.open(df_path, 'rb') as f:
      df = pd.read_csv(f)

  if s3.exists(processed_path):
    processed_files = s3.ls(processed_path)
    if len(processed_files) > 0:

      p_bar = st.progress(0)
      for file in :
        if file.endswith('.json'):
          with s3.open(file, 'rb') as f:
            entry = pd.read_json(f)
            entry_file_name = entry['file_name']
            entry_file_path = os.path.join(base_path, entry_file_name)
            entry_words = entry['bag_of_words']
            wanted_index = df[df['file_path'] == entry['file_path'].values[0]].index
            df.at[wanted_index, 'words'] = entry_words
            df.at[wanted_index, 'OCR_attempted'] = True
            s3.rm(file)
            p_bar.progress((i+1)/len(processed_files),
                           text=f"Processed {i+1}/{len(processed_files)}"
                           )
      st.write("Processed files loaded successfully.")

with s3.open(df_path, 'wb') as f:
  df.to_csv(f, index=False)
st.write("Document database updated successfully.")

if s3.exists(df_path): 
  with s3.open(df_path, 'rb') as f:
      df = pd.read_csv(f)
  st.write("Document database loaded successfully.")

  ############################################################
  # Search
  ############################################################

  with st.form(key='search_form'):
      st.write("Search for a word or phrase")
      search_term = st.text_input("Search term", "")
      submit_button = st.form_submit_button(label='Submit')

  if submit_button:
    # Iterate through each row in the dataframe
    # and search for the search term in the 'words' column
    search_results = []
    for i, row in df.iterrows():
      words = row['words']
      decoded_words = [word.encode('utf-8').decode('utf-8') for word in words]
      words_str = ''.join(decoded_words)
      match_value = fuzz.partial_token_set_ratio(words_str, search_term)
      search_results.append(match_value)

    # Show top 'n' search results
    n = 5
    top_n_indices = np.argsort(search_results)[-n:][::-1]
    st.write("Top search results:")
    print_list = []
    for idx in top_n_indices:
      word_list = literal_eval(df.iloc[idx]['words'])
      extracted_words = process.extract(
          search_term, word_list, limit=5 
          )
      basename = os.path.basename(df.iloc[idx]['file_path'])
      print_dict = {
          'file_name': basename,
          'file_type': df.iloc[idx]['file_type'],
          'notes': df.iloc[idx]['notes'],
          'words': str(extracted_words)
          }
      print_list.append(print_dict)
      # print_str = pformat(print_dict) 
      # st.write(print_str)
    print_df = pd.DataFrame(print_list)
    print(print_df)
    # st.write(print_list)
    st.write(print_df)

  ############################################################
  # Viewer
  ############################################################

  with st.form(key='view_form'):
      st.write("Enter filename for file to view")
      filename = st.text_input("Filename", "")
      submit_button = st.form_submit_button(label='Submit')


  if submit_button:
    fin_path = os.path.join(data_path, filename)
    if s3.exists(fin_path): 
      pdf_content = s3.open(fin_path, 'rb').read()
      pdf_viewer(pdf_content)
      st.write("File loaded successfully.")
    else:
        st.write("File not found.")

  ############################################################
  # Downloader
  ############################################################

  with st.form(key='Download form'):
      st.write("Enter filename for file to download")
      filename = st.text_input("Filename", "")
      submit_button = st.form_submit_button(label='Submit')


  if submit_button:
    fin_path = os.path.join(data_path, filename)
    if s3.exists(fin_path): 
      pdf_content = s3.open(fin_path, 'rb').read()
      st.download_button(
          label="Download file",
          data=pdf_content,
          file_name=filename,
          # mime='application/pdf'
          )
      st.write("File loaded successfully.")
    else:
        st.write("File not found.")

else:
    st.write("No OCR'd documents found.")

