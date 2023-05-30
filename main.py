import tm1637
from machine import Pin
from utime import sleep
import time

mydisplay = tm1637.TM1637(clk=Pin(21), dio=Pin(22))
brightness = 1

minute_btn_pin = Pin(13, Pin.IN, Pin.PULL_DOWN)
minute_prv_state = minute_btn_pin.value()

hour_btn_pin = Pin(12, Pin.IN, Pin.PULL_DOWN)
hour_prv_state =hour_btn_pin.value()

edit_btn_pin = Pin(11, Pin.IN, Pin.PULL_DOWN)
edit_mode = Pin(18, Pin.OUT)

led_pin = Pin(25, Pin.OUT, Pin.PULL_DOWN)

debounce_delay = 50  # Debounce delay in milliseconds

def minute_btn_clicked(pin):
    global minute_prv_state,h,m
    minute_cur_state = pin.value()

    # Check if the button state has changed
    if edit_mode.value() == 1:
        if minute_cur_state != minute_prv_state:
            minute_prv_state = minute_cur_state
            if minute_prv_state == 1:
                m += 1
                if m>59:
                    m = 0
                mydisplay.numbers(h, m)
    else:
        if minute_cur_state != minute_prv_state:
            minute_prv_state = minute_cur_state
            if minute_prv_state == 1:
                global brightness
                brightness = brightness + 1 if brightness < 7 else 1 
                mydisplay.brightness(brightness)


    sleep(debounce_delay / 1000)  # Debounce delay

def hour_btn_clicked(pin):
    global hour_prv_state,h,m
    hour_cur_state = pin.value()

    # Check if the button state has changed
    if edit_mode.value() == 1:
        if hour_cur_state != hour_prv_state:
            hour_prv_state = hour_cur_state
            if hour_prv_state == 1:
                h += 1
                if h>23: 
                    h=0
            mydisplay.numbers(h, m)
    else:
        if hour_cur_state != hour_prv_state:
            hour_prv_state = hour_cur_state
            if hour_prv_state == 1:
                global brightness
                brightness = brightness + 1 if brightness < 7 else 1 
                mydisplay.brightness(brightness)


    sleep(debounce_delay / 1000)  # Debounce delay

edit_btn_state = edit_btn_pin.value()
def edit_btn_clicked(pin):
    global edit_btn_state
    new_state = pin.value()
    if new_state != edit_btn_state:
        edit_btn_state = new_state
        if edit_btn_state == 1:
            blink_colon()
            edit_mode.toggle()
    sleep(debounce_delay / 1000)

colon_visible= True
def blink_colon():
    global colon_visible
    if edit_mode.value() == 0:
        colon_visible = not colon_visible
        mydisplay.numbers(h, m, colon=colon_visible)
    else:
        mydisplay.numbers(h, m, colon=True)    



# Attach interrupt handler to button pin
minute_btn_pin.irq(trigger=Pin.IRQ_RISING, handler=minute_btn_clicked)
hour_btn_pin.irq(trigger=Pin.IRQ_RISING, handler=hour_btn_clicked)
edit_btn_pin.irq(trigger=machine.Pin.IRQ_RISING, handler=edit_btn_clicked)
 
# Show a word
h = 16
m = 34

previous_time = time.ticks_ms()
while True:
    led_pin.value(1)
    blink_colon()
    current_time = time.ticks_ms()

    if edit_mode.value() == 1:
        previous_time = time.ticks_ms()
        current_time = time.ticks_ms()

    elapsed_time = time.ticks_diff(current_time, previous_time)
    if elapsed_time >= 60000:  # 60,000 milliseconds = 60 seconds
        m += 1
        if m>59:
            m = 0 
            h = h+1
        if h>23: 
            h=0
        previous_time = current_time

    time.sleep_ms(250) 
    
