"""
Search through words extracted from OCR to find a specific word or phrase.
"""

import os
import pandas as pd
import streamlit as st
from thefuzz import fuzz, process
import numpy as np
from ast import literal_eval

df_path = 'doc_df.csv'

if os.path.exists(df_path):
    df = pd.read_csv(df_path)
    st.write("Document database loaded successfully.")
else:
    st.write("No documents uploaded yet.")

with st.form(key='my_form'):
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
