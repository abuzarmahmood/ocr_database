FROM public.ecr.aws/lambda/python:3.11

# Copy evrything from the current directory to the container 
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install the required packages
RUN pip install -r requirements.txt

# Install linux dependencies
# RUN apt-get update && apt-get install -y \
RUN yum update && yum install -y \
    mesa-libGL \
    # libgl1 \
    weasyprint \
    cairo cairo-devel cairomm-devel libjpeg-turbo-devel pango pango-devel pangomm pangomm-devel

# Copy everything else from the current directory to the container 
COPY . ${LAMBDA_TASK_ROOT} 

# Run initial_test.py
RUN python initial_test.py

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "lambda_function.handler" ]
