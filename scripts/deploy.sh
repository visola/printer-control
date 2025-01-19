#!/bin/bash

ssh $SSH_OPTIONS $HOST -t "rm -Rf server; mkdir -pv server; mkdir -pv server/backend; mkdir -pv server/public"
scp $SSH_OPTIONS main.py $HOST:server/main.py
scp $SSH_OPTIONS -rp backend $HOST:server/
scp $SSH_OPTIONS -rp public $HOST:server/
