#!/bin/bash

ssh $SSH_OPTIONS $HOST -t "rm -Rf server; mkdir -pv server; mkdir -pv server/backend; mkdir -pv server/public"
scp $SSH_OPTIONS scripts/printer_control.service $HOST:server/printer_control.service
scp $SSH_OPTIONS scripts/start.sh $HOST:server/start.sh
scp $SSH_OPTIONS main.py $HOST:server/main.py
scp $SSH_OPTIONS -rp backend $HOST:server/
scp $SSH_OPTIONS -rp public $HOST:server/
