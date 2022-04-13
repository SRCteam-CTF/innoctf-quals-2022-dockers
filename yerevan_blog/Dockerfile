FROM python:3.9
RUN apt update && apt install -yq qrencode socat curl wget netcat
WORKDIR /app
ADD app/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
ADD app .
RUN useradd -l -M -s /bin/bash -U user && \
    chmod -R o+rx .  && \
    chmod -R o+w uploads  && \
    echo "Ararat{Y3r3v4n_610999}" > /h3r3_15_90ur_f149  && \
    chmod 444 /h3r3_15_90ur_f149
USER user
ENTRYPOINT ["python3", "/app/main.py"]
