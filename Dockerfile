# Set Base Image
FROM python:3.9

# Set Working Dir
WORKDIR /repo

# Copy Requirements txt
COPY ./requirements.txt /repo/requirements.txt

# Install Dependencies
RUN pip install -r requirements.txt

# Copy Files
COPY ./app /repo/app
COPY ./run.py /repo/run.py

# CMD
CMD ["python", "run.py"]