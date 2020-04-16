#!/bin/bash
set -x

docker image rm h42/auth

docker build -t h42/auth .
