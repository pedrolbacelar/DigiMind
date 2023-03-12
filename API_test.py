from interface_API import interface_API
from time import sleep
api = interface_API()


while True:
    api.indicator(logic = 1.0, input = 0.8)
    sleep(15)
    