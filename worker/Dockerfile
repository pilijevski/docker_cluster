FROM python:3.6.8-alpine3.8

COPY ./wait /wait

RUN chmod +x /wait

COPY ["./", "/usr/src/app"]

RUN pip install -r /usr/src/app/requirements.txt

WORKDIR /usr/src/app

## Launch the wait tool and then your application
CMD /wait && python worker.py
