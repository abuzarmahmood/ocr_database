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

# df_path = 'doc_df.csv'
df_path = os.path.join(base_path, 'doc_df.csv')

# if os.path.exists(df_path):
#     df = pd.read_csv(df_path)
#     st.write("Document database loaded successfully.")
# else:
#     st.write("No documents uploaded yet.")

# Add refresh button at the top
if st.button('🔄 Refresh Document Database'):
    if s3.exists(df_path):
        with s3.open(df_path, 'rb') as f:
            df = pd.read_csv(f)
        st.success("✅ Document database refreshed successfully!")
    else:
        st.error("❌ No documents found in S3 storage.")
        
# Initial load of database
if s3.exists(df_path): 
    with s3.open(df_path, 'rb') as f:
        df = pd.read_csv(f)
    st.info("📚 Document database loaded successfully.")

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

