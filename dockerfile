# creates a layer from the python docker image
FROM python:3

# creates and navigates to a directory
WORKDIR /usr/src/app

# adds requirements file and installs dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# adds files from the Docker client’s current directory
COPY ./ ./

# runs the application
CMD [ "python", "./python_chess.py" ]