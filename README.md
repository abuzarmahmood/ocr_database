Database to allow search of scanned documents.<br>
Operate on Pareto principle (something better than nothing).

# Accessing


https://github.com/abuzarmahmood/ocr_database/assets/12436309/b6551e7f-1fbb-4c66-bbb4-c4078e98dba2


# Searching


https://github.com/abuzarmahmood/ocr_database/assets/12436309/affa042e-5030-4c96-9bb7-98351f4f1a06





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
