# use the python 3.8 image
FROM python:3.8

# set the working directory to /app
WORKDIR /app

# copy all the files from the current directory to the container working directory (e.g. `/app`)
ADD . /app

# initialize the db and install the requirements
RUN python init_db.py
RUN pip install -r requirements.txt


# expose the port 3111
EXPOSE 3111

# start the container by invoking the binary created earlier, which is  `./app_pablo5.py`
CMD ["python", "app_pablo6.py"]
