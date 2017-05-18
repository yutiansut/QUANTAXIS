# coding:utf-8
# 实现一些zeromq的基本功能

import zmq
from random import randint

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5556")


headlines = [
"Rohit's 150 goes in vain as India lose to SA",
"1st phase of polling for 49 Bihar seats today",
"Pele sends football-crazy Kolkata into a tizzy",
"K P Sharma Oli elected new Nepal PM"
]
politics = [
"Advani rubs Modi on wrong side",
"1st phase of polling for 49 Bihar seats today",
"Shiv sena stays away from Modi's functions",
"K P Sharma Oli elected new Nepal PM"
]
sports= [
"Rohit's 150 goes in vain as India lose to SA",
"Hamilton triumphs in Sochi",
"Kolkata to give Pele a grand second coming",
"Karnataka denied home advantage"
]
i=-1
while True:
    i=i+1
    
    if(i==4):
    	i=0
    sports_news = sports[i]
    socket.send_string("%s %s" %('SP',sports_news))

    politics_news = politics[i]
    socket.send_string("%s %s" %('PO',politics_news))

    headlines_news = headlines[i]
    socket.send_string("%s %s" %('HL',headlines_news))