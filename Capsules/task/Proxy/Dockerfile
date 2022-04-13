FROM python:3.7-alpine
COPY proxy.py /task/proxy.py
CMD python3 /task/proxy.py --up_ip ssh --up_port 22 --low_port 40002 --decapsulator
