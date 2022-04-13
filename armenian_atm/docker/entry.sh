#!/bin/bash

while true; do socat TCP-LISTEN:1337,fork,reuseaddr,bind=0.0.0.0 EXEC:"sudo -u nobody /atm",stderr; done
