FROM  python:alpine

COPY . /app

WORKDIR /app

RUN pip3 install -r requirements.txt --user

ENTRYPOINT [ "python3", "ipgeolocation.py" ]
