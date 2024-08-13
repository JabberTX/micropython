import network
import espnow
import json
import uasyncio as asyncio
from machine import Pin

sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.disconnect()

print('main - set up LED')
led = Pin(2, Pin.OUT)

e = espnow.ESPNow()
e.active(True)

async def led_on(led):
    led.on()

async def led_off(led):
    led.off()

async def blink_led(led, blink_count=5, blink_interval=0.5):
    for _ in range(blink_count):
        led.on()
        await asyncio.sleep(blink_interval)
        led.off()
        await asyncio.sleep(blink_interval)

action_map = {
    "on": led_on,
    "off": led_off,
    "blink": blink_led
}

async def handle_message(msg):
    try:
        msg_json = json.loads(msg)
        action = msg_json.get('led')
        
        if action in action_map:
            if action == "blink":
                await action_map[action](led, blink_count=5, blink_interval=0.5)
            else:
                await action_map[action](led)
        else:
            print(f"Unknown action: {action}")
    except Exception as e:
        print(f"Error processing message: {e}")

async def main():
    while True:
        host, msg = e.recv()
        if msg: 
            mac_address = ':'.join(f'{b:02x}' for b in host)
            
            msg_str = msg.decode('utf-8')
            
            print(f'MAC Address: {mac_address}')
            print(f'Message: {msg_str}')
            
            await handle_message(msg_str)
        
        await asyncio.sleep(0)

asyncio.run(main())
