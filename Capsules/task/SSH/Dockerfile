FROM alpine
RUN apk update && apk add openssh
RUN adduser -s /bin/sh -D -h /home/user user && \
    chmod -R o-rwx /tmp /var/tmp && \
    echo "Ararat{3nC4p5u14710N}" > /flag && \
    chmod -R o+r /flag && \
    chown -R root:root /home/user && \
    ssh-keygen -A && \
    echo 'user:1usual_2http_3traffic!' | chpasswd
CMD /usr/sbin/sshd -D
