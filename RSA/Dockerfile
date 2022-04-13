FROM python:3.7-alpine
RUN apk update && apk add socat gcc libc-dev gmp-dev mpfr-dev mpc1-dev
RUN pip3 install gmpy2
WORKDIR /task
COPY task/ .
CMD socat tcp-listen:40001,reuseaddr,fork exec:"python3 server.py"
