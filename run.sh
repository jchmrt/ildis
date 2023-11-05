#!/bin/bash

source venv/bin/activate
daphne -b 0.0.0.0 -p 8001 ildis.asgi:application