#!/usr/bin/env python3
from flask import request
from flask import Flask
from pprint import pprint

URL= "http://127.0.0.1:2224/"

resp= request.get(URL).json()

pprint(resp)
