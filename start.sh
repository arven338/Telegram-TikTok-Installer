#!/bin/bash
gunicorn launch:app --bind 0.0.0.0:$PORT
