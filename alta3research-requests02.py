#!/usr/bin/env python3
from flask import request
from flask import Flask
from pprint import pprint

URL1= "http://127.0.0.1:2224/getdata/alldata"
URL2= "http://127.0.0.1:2224/getdata/11-24-2022"

resp1= request.get(URL1).json()
resp2= request.get(URL2).json()

pprint(resp1)
pprint(resp2)
