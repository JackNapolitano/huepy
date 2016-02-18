#!/usr/bin/python
from phue import Bridge

b = Bridge('10.0.1.15')#keep the quotes when you put the ip
b.connect()
b.get_api()
b.set_light( [1,2,3], 'on', True)

