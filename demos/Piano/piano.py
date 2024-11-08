import os, sys, time

os.chdir(os.path.dirname(os.path.realpath(__file__)))
sys.path.extend(("../..","../../atlastk.zip"))

import atlastk, ucuq

import math

BUZZER_PIN = 2
LOUDSPEAKER_PIN = 6

with open('Body.html', 'r') as file:
  BODY = file.read()

pinNotSet = True

pwm = None
baseFreq = 440.0*math.pow(math.pow(2,1.0/12), -16)
ratio = 0.5

def acConnect(dom):
  ucuq.handleATK(dom)

  dom.inner("", BODY)


def acPlay(dom,id):
  global pwm

  if pinNotSet:
    dom.alert("Please select a pin number!")
  else:
    freq = int(baseFreq*math.pow(math.pow(2,1.0/12), int(id)))
    pwm.setU16(int(ratio*65535))
    pwm.setFreq(freq)
    ucuq.sleep(0.5)
    pwm.setU16(0)
    ucuq.render()


def acSetRatio(dom, id):
  global ratio
  
  ratio = float(dom.getValue(id))

  dom.setValue("RatioSlide" if id == "RatioValue" else "RatioValue", ratio)


def acSetPin(dom, id):
  global pinNotSet, pwm

  rawPin = dom.getValue(id)
  pin = None

  if rawPin in ("Buzzer", "Loudspeaker"):
    pin = BUZZER_PIN if rawPin == "Buzzer" else LOUDSPEAKER_PIN

    dom.disableElement("UserPin")
    dom.setValue("UserPin", pin)
  elif rawPin != "User":
    pin = int(rawPin)
  else:
    dom.enableElement("UserPin")
    
  if pin:
    pinNotSet = False
    pwm = ucuq.PWM(pin)
    ucuq.render()

CALLBACKS = {
  "": acConnect,
  "Play": acPlay,
  "SetRatio": acSetRatio,
  "SetPin": acSetPin
}

HEAD = """
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/beautiful-piano@0.0.6/styles.min.css"></link>
  <script src="https://cdn.jsdelivr.net/npm/beautiful-piano@0.0.6/dist/piano.min.js"></script>
"""

atlastk.launch(CALLBACKS, headContent=HEAD)
