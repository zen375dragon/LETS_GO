# Plays LET'S GO! by Bongo Cat using the onboard piezo buzzer on the Maker Pi Pico board.

import machine
import utime
from pitches import *
import _thread

led = machine.Pin(25, machine.Pin.OUT)
button = machine.Pin(22, machine.Pin.IN, machine.Pin.PULL_UP)
buzzer = machine.PWM(machine.Pin(18))

import array, time
from machine import Pin
import rp2
from rp2 import PIO, StateMachine, asm_pio

NUM_LEDS = 1

@asm_pio(sideset_init=PIO.OUT_LOW, out_shiftdir=PIO.SHIFT_LEFT,
autopull=True, pull_thresh=24)
def ws2812():
    T1 = 2
    T2 = 5
    T3 = 3
    label("bitloop")
    out(x, 1) .side(0) [T3 - 1]
    jmp(not_x, "do_zero") .side(1) [T1 - 1]
    jmp("bitloop") .side(1) [T2 - 1]
    label("do_zero")
    nop() .side(0) [T2 - 1]

sm = StateMachine(0, ws2812, freq=8000000, sideset_base=Pin(28))

sm.active(1)

ar = array.array("I", [0 for _ in range(NUM_LEDS)])

B0  = 31
C1  = 33
CS1 = 35
D1  = 37
DS1 = 39
E1  = 41
F1  = 44
FS1 = 46
G1  = 49
GS1 = 52
A1  = 55
AS1 = 58
B1  = 62
C2  = 65
CS2 = 69
D2  = 73
DS2 = 78
E2  = 82
F2  = 87
FS2 = 93
G2  = 98
GS2 = 104
A2  = 110
AS2 = 117
B2  = 123
C3  = 131
CS3 = 139
D3  = 147
DS3 = 156
E3  = 165
F3  = 175
FS3 = 185
G3  = 196
GS3 = 208
A3  = 220
AS3 = 233
B3  = 247
C4  = 262
CS4 = 277
D4  = 294
DS4 = 311
E4  = 330
F4  = 349
FS4 = 370
G4  = 392
GS4 = 415
A4  = 440
AS4 = 466
B4  = 494
C5  = 523
CS5 = 554
D5  = 587
DS5 = 622
E5  = 659
F5  = 698
FS5 = 740
G5  = 784
GS5 = 831
A5  = 880
AS5 = 932
B5  = 988
C6  = 1047
CS6 = 1109
D6  = 1175
DS6 = 1245
E6  = 1319
F6  = 1397
FS6 = 1480
G6  = 1568
GS6 = 1661
A6  = 1760
AS6 = 1865
B6  = 1976
C7  = 2093
CS7 = 2217
D7  = 2349
DS7 = 2489
E7  = 2637
F7  = 2794
FS7 = 2960
G7  = 3136
GS7 = 3322
A7  = 3520
AS7 = 3729
B7  = 3951
C8  = 4186
CS8 = 4435
D8  = 4699
DS8 = 4978

cat = [E7, 0.9, FS7, 0.25, GS7, 1.3, AS7, 0.8, B7, 2.47, GS7, GS7, 0.17, B7, 0.7, GS7, GS7, 0.1, B7, 0.1, B7, 0.9, FS7, FS7, 0.8, E7, 1.6, GS7, GS7, 0.08, B7, 0.07, GS7, 0.07, B7, 0.07, B7, 0.07, GS7, GS7, 0.14, FS7, FS7, 0.15, AS7, 0.1, FS7, 0.08, E7, 0.04, GS7, 0.05, GS7, 0.25, GS7, GS7, 0.08, B7, 0.07, GS7, 0.07, B7, 0.07, B7, 0.07, GS7, GS7, 0.14, FS7, FS7, 0.15, AS7, 0.1, FS7, 0.08, E7, E7, 0.45, GS7, GS7, 0.12, B7, 0.07, GS7, 0.07, B7, 0.07, B7, 0.07, GS7, GS7, 0.14, FS7, FS7, 0.15, AS7, 0.1, FS7, 0.08, E7, E7, 0 ]
cat2 = [1.5, GS7, GS7, 0.08, B7, 0.07, GS7, 0.07, B7, 0.07, B7, 0.07, GS7, GS7, 0.14, FS7, FS7, 0.15, AS7, 0.1, FS7, 0.08, E7, 0.1, GS7, GS7, 0.12, B7, 0.07, GS7, 0.07, B7, 0.07, B7, 0.07, GS7, GS7, 0.14, FS7, FS7, 0.15, AS7, 0.1, FS7, 0.08, E7, 0]

def button_thread():
    while True:
        if button.value() == 0:
            for i in cat:
                if i < 31:
                    buzzer.duty_u16(0)
                    utime.sleep(i)
                else:
                    buzzer.freq(i)
                    buzzer.duty_u16(19660)
                    utime.sleep(0.15)
_thread.start_new_thread(button_thread, ())

while True:
    if button.value() == 0:
        utime.sleep(15.75)
        for i in range(2):
            print("blue")
            for i in range(NUM_LEDS):
                ar[i] = 255
            sm.put(ar,8)
            time.sleep_ms(820)
                    
            print("red")
            for i in range(NUM_LEDS):
                ar[i] = 255<<8
            sm.put(ar,8)
            time.sleep_ms(820)

            print("green")
            for i in range(NUM_LEDS):
                ar[i] = 255<<16
            sm.put(ar,8)
            time.sleep_ms(820)

            print("white")
            for i in range(NUM_LEDS):
                ar[i] = 0xFFFFFF
            sm.put(ar,8)
            time.sleep_ms(820)
                
            utime.sleep(0.17)
