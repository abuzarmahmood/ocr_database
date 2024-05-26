from fastapi import FastAPI
from fastapi import File, UploadFile

app = FastAPI()
@app.get("/")
async def root():
 return {"greeting":"Hello world"}


# @app.post("/upload")
# def upload(file: UploadFile = File(...)):
#     try:
#         contents = file.file.read()
#         with open(file.filename, 'wb') as f:
#             f.write(contents)
#     except Exception:
#         return {"message": "There was an error uploading the file"}
#     finally:
#         file.file.close()
# 
#     return {"message": f"Successfully uploaded {file.filename}"}


@app.post("default_file_upload")
def default_file_upload_example(file: UploadFile = File(...)):
    return {}

# @app.post('/files')
# def get_file(file: bytes = File(...)):
#     content = file.decode('utf-8')
#     lines = content.split('\n')
#     return {"content": lines}

@app.post('/upload')
def upload_file(uploaded_file: UploadFile = File(...)):
    path = f"files/{uploaded_file.filename}"
    with open(path, 'w+b') as file:
        shutil.copyfileobj(uploaded_file.file, file)

    return {
        'file': uploaded_file.filename,
        'content': uploaded_file.content_type,
        'path': path,
    }
