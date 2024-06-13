import s3fs
import os
import streamlit as st
import pandas as pd

s3 = s3fs.S3FileSystem(
        anon=False,
        key = st.secrets["S3_KEY"], 
        secret = st.secrets["S3_SECRET"] 
        )
s3.ls('s3://ocr-database-s3')

wanted_files = [x for x in os.listdir('.') if x.endswith('.csv')][0]

# Upload file
s3.put(wanted_files, 's3://ocr-database-s3/' + wanted_files)

# Load cvs to dataframe
df = pd.read_csv(s3.open('s3://ocr-database-s3/' + wanted_files))
