FROM alpine:3.14 as builder
RUN apk add --no-cache make g++ binutils

COPY src src/
WORKDIR /src
RUN mkdir build && make

FROM alpine:3.14
RUN apk add --no-cache socat sudo g++ binutils

COPY --from=builder /src/build /
COPY ./docker/entry.sh ./


EXPOSE 1337
ENTRYPOINT /bin/sh /entry.sh
