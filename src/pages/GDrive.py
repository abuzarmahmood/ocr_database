# streamlit_app.py

import streamlit as st
from st_files_connection import FilesConnection

# Create connection object and retrieve file contents.
# Specify input format is a csv and to cache the result for 600 seconds.
conn = st.connection('gcs', type=FilesConnection)
df = conn.read("ocr_database/Pulakat_activated_cage.csv", input_format="csv", ttl=600)

# Print results.
st.write(df)