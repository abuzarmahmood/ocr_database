import s3fs
import os
import streamlit as st
import pandas as pd
import pytest
import time
from pages.Upload import get_unique_filename

s3 = s3fs.S3FileSystem(
        anon=False,
        key = st.secrets["S3_KEY"], 
        secret = st.secrets["S3_SECRET"] 
        )

def test_get_unique_filename():
    # Setup test environment
    test_path = f's3://{st.secrets["S3_BUCKET_NAME"]}/test'
    test_filename = 'test_file.pdf'
    
    # Create a test file
    with s3.open(os.path.join(test_path, test_filename), 'wb') as f:
        f.write(b'test content')
    
    # Test unique filename generation
    unique_name = get_unique_filename(s3, test_path, test_filename)
    assert unique_name != test_filename
    assert unique_name.startswith('test_file_')
    assert unique_name.endswith('.pdf')
    
    # Cleanup
    s3.rm(os.path.join(test_path, test_filename))

def test_file_upload():
    wanted_files = [x for x in os.listdir('.') if x.endswith('.csv')][0]
    
    # Upload file
    s3.put(wanted_files, 's3://ocr-database-s3/' + wanted_files)
    
    # Load csv to dataframe
    df = pd.read_csv(s3.open('s3://ocr-database-s3/' + wanted_files))
    assert not df.empty
