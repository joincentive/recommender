# Define Base Image. We'll use Python 3
FROM python:3

# Copy your Python file to the image
COPY *.py /

# Install any dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt

RUN python -m spacy download en_core_web_md

# Tell Docker how to start your script
ENTRYPOINT [ "python", "./api.py" ]

