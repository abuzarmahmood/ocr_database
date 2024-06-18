Database to allow search of scanned documents.<br>
Operate on Pareto principle (something better than nothing).

# Accessing


https://github.com/abuzarmahmood/ocr_database/assets/12436309/b6551e7f-1fbb-4c66-bbb4-c4078e98dba2



# Searching


https://github.com/abuzarmahmood/ocr_database/assets/12436309/13c44802-c8b8-485b-9b30-070aec4e734f




# Structure
- ## Frontend:
	- Submit scans
	- Upload scans
	- Provide metadata
		- Document Types
	- Search scans
		- By metadata
	- By content (OCR)
	- View scans
		- Path to saved scan

- ## Backend:
    - Accept scans
	- Store scans
	- Extract metadata
	- Extract text from scans
	- Search scans
	    - By metadata
	    - By content
	- Return path to saved scan

Notes:
    - To fix opencv issue, https://docs.streamlit.io/knowledge-base/dependencies/libgl
