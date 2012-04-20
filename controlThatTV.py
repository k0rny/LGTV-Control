#!/usr/bin/env python
# -*- coding: utf-8 -*-

#script to control a LG 32LD450, 37LD450 or 42LD450 via RS232, you may need to change tv.port

import serial
import sys
from time import sleep

POWER_ON_DELAY  = 6 #seconds to wait after power on before sending other commands

CMD_POWER_ON    = u"6B 61 20 30 31 20 30 31 0D".replace(' ','').decode("hex")
CMD_POWER_OFF   = u"6B 61 20 30 31 20 30 30 0D".replace(' ','').decode("hex")

CMD_INPUT_D_TV  = u"78 62 20 30 31 20 30 30 0D".replace(' ','').decode("hex")
CMD_INPUT_A_TV  = u"78 62 20 30 31 20 31 30 0D".replace(' ','').decode("hex")
CMD_INPUT_AV_1  = u"78 62 20 30 31 20 32 30 0D".replace(' ','').decode("hex")
CMD_INPUT_AV_2  = u"78 62 20 30 31 20 32 31 0D".replace(' ','').decode("hex")
CMD_INPUT_COMP  = u"78 62 20 30 31 20 34 30 0D".replace(' ','').decode("hex")
CMD_INPUT_RGB   = u"78 62 20 30 31 20 36 30 0D".replace(' ','').decode("hex")
CMD_INPUT_HDMI1 = u"78 62 20 30 31 20 37 30 0D".replace(' ','').decode("hex")
CMD_INPUT_HDMI2 = u"78 62 20 30 31 20 39 31 0D".replace(' ','').decode("hex")

#translates command-line arguments to RS232-codes
cmdDict = { "off"  : CMD_POWER_OFF,
            "on"   : CMD_POWER_ON,
            "dtv"  : CMD_INPUT_D_TV,
            "atv"  : CMD_INPUT_A_TV,
            "av1"  : CMD_INPUT_AV_1,
            "av2"  : CMD_INPUT_AV_2,
            "comp" : CMD_INPUT_COMP,
            "rgb"  : CMD_INPUT_RGB,
            "hdmi1": CMD_INPUT_HDMI1,
            "hdmi2": CMD_INPUT_HDMI2 }

#seperate power-commands from input-commands
CMD_NAMES = cmdDict.keys()
POWER_NAMES  = tuple(("off", "on"))
INPUT_NAMES  = tuple(set(CMD_NAMES)-set(POWER_NAMES ))

#quick and dirty
def abort(msg):
    print msg
    sys.exit(1)

#check for multiple, missing or wrong arguments
def checkArgs():
    if len(sys.argv) == 1:
        print "usage: {0} <on|off> <dtv|atv|av1|av2|comp|rgb|hdmi1|hdmi2>".format(sys.argv[0])
    else:
        args = sys.argv[1:]
        for arg in args:
            if arg not in CMD_NAMES: abort("unknown commands")
        sumcount = 0
        for cmd in INPUT_NAMES :
            count = args.count(cmd)
            if count > 1: abort("multiple commands")
            sumcount = sumcount + count
        if sumcount > 1: abort("multiple commands")
        if POWER_NAMES [0] in args and POWER_NAMES [1] in args:
            abort("multiple commands")

if __name__ == '__main__':
        checkArgs()
        tv = serial.Serial()
        tv.port = "/dev/ttyUSB0"
        tv.timeout = 1
        tv.writeTimeout = 1
        tv.open()
        if tv.isOpen():
            args = sys.argv[1:]
            if POWER_NAMES [1] in args:             #power-on action
                tv.write(CMD_POWER_ON)
                tv.flush()
                sleep(POWER_ON_DELAY)
            elif POWER_NAMES [0] in args:           #power-off action
                tv.write(CMD_POWER_OFF)
                tv.flush()
            for cmd in POWER_NAMES :                #remove power-commands from argument-list
                if cmd in args: args.remove(cmd)
            if args:                                #input-action
                cmd = args[0]
                tv.write(cmdDict[cmd])
                tv.flush()
            tv.close()
        else:
            abort("opening TV failed")
