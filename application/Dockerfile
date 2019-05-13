FROM python:3.6-onbuild
COPY ./wait /wait

RUN chmod +x /wait

COPY ["./", "/usr/src/app"]

WORKDIR /usr/src/app

## Launch the wait tool and then your application
CMD /wait && /bin/bash
