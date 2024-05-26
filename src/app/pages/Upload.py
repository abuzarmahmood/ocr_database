import streamlit as st
import pandas as pd
from io import StringIO
import os
import pandas as pd
from datetime import datetime
from PyPDF2 import PdfWriter, PdfReader

save_path = '/media/bigdata/projects/ocr_database/data'
df_path = os.path.join(save_path, 'doc_df.csv')


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

        # with open(save_path, 'wb') as f:
        #     f.write(uploaded_file.getbuffer())

        input_pdf = PdfReader(uploaded_file)
        st.write("Number of pages in the PDF:", len(input_pdf.pages))

        for i, page in enumerate(input_pdf.pages):
            output = PdfWriter()
            output.add_page(page)

            save_page_path = os.path.join(
                    save_path,
                    uploaded_file.name.split('.')[0] + '_' + str(i) + '.pdf'
                    )
    
            with open(save_page_path, 'wb') as f:
                output.write(f)

            # if os.path.exists(save_path):
            #     st.write("File uploaded successfully, " +\
            #             "File name: " + uploaded_file.name + ", " +\
            #             "File type: " + option + ", " +\
            #             "Notes: " + notes)

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

            if os.path.exists(df_path):
                df = pd.read_csv(df_path)
                df = pd.concat([df, temp_df], ignore_index=True)
                df.to_csv(df_path, index=False)
            else:
                temp_df.to_csv(df_path, index=False)
