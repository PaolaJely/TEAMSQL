#!/bin/bash
pip install gunicorn==23.0.0  # Instala Gunicorn explícitamente
gunicorn --bind 0.0.0.0:$PORT app:app