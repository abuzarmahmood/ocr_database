import streamlit as st
import pandas as pd
from io import StringIO
import os
import pandas as pd
from datetime import datetime
from PyPDF2 import PdfWriter, PdfReader
import s3fs
import time

def get_unique_filename(s3, path, filename):
    """Generate a unique filename if a conflict is detected"""
    base, ext = os.path.splitext(filename)
    counter = 1
    new_filename = filename
    while s3.exists(os.path.join(path, new_filename)):
        new_filename = f"{base}_{int(time.time())}_{counter}{ext}"
        counter += 1
    return new_filename

s3 = s3fs.S3FileSystem(
        anon=False,
        key = st.secrets["S3_KEY"], 
        secret = st.secrets["S3_SECRET"] 
        )
# base_path = 's3://ocr-database-s3'
base_path = f's3://{st.secrets["S3_BUCKET_NAME"]}'

save_path = os.path.join(base_path, 'Data')
if not s3.exists(save_path):
    s3.makedirs(save_path)

df_path = os.path.join(base_path, 'doc_df.csv')

with st.form(key='my_form'):
    st.write("Upload a file")
    uploaded_file = st.file_uploader("Choose a file")

    option = st.selectbox(
            'What kind of file is this?',
            (
                'Shipping',
                'Experiment Metadata',
                'Other'
            )
        )

    notes = st.text_area("Notes", "")

    submit_button = st.form_submit_button(label='Submit')

if submit_button:
    if uploaded_file is not None:

        input_pdf = PdfReader(uploaded_file)
        st.write("Number of pages in the PDF:", len(input_pdf.pages))

        p_bar = st.progress(0)
        for i, page in enumerate(input_pdf.pages):
            
            p_bar.progress((i+1)/len(input_pdf.pages),
                           text=f"Uploading page {i+1}/{len(input_pdf.pages)}"
                           )

            output = PdfWriter()
            output.add_page(page)

            base_filename = get_unique_filename(s3, save_path, uploaded_file.name)
            save_page_path = os.path.join(
                    save_path,
                    base_filename.split('.')[0] + '_' + str(i) + '.pdf'
                    )
    
            # with open(save_page_path, 'wb') as f:
            #     output.write(f)
            with s3.open(save_page_path, 'wb') as f:
                output.write(f)

            time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            time_now = pd.to_datetime(time_now)

            temp_df = pd.DataFrame(
                    {
                        'file_name': [uploaded_file.name], 
                        'page_number': [i],
                        'file_path': [save_page_path],
                        'file_type': [option], 
                        'notes': [notes],
                        'upload_time': [time_now],
                        'words': [[]],
                        'OCR_attempted': [False],
                        }
                    )

            if s3.exists(df_path): 
                with s3.open(df_path, 'rb') as f:
                    df = pd.read_csv(f)
                    # Drop any rows with duplicate file_path
                    df = df.drop_duplicates(subset='file_path', keep='first')
                    df = pd.concat([df, temp_df], ignore_index=True)
                with s3.open(df_path, 'wb') as f:
                    df.to_csv(f, index=False)
            else:
                with s3.open(df_path, 'wb') as f:
                    temp_df.to_csv(f, index=False)

st.write("Upload Completed")
