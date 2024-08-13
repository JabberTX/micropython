import network
import espnow
import json

class Telemetry:
    def __init__(self):
        # Initialize WLAN interface
        print('Startup')
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.wlan.disconnect()   # Disconnect from any Access Point

        # Initialize ESP-NOW
        print('Init ESPNow')
        self.esp_now = espnow.ESPNow()
        self.esp_now.active(True)
        self.esp_now.irq(self.receive_callback)  # Set the receive callback

        self.telemetry_callback = None
        self.return_mac = None
        print('Startup complete')

    def register_telemetry_callback(self, callback):
        print('Telemetry callback')
        self.telemetry_callback = callback

    def receive_callback(self, espnow_event):
        mac, msg = espnow_event.ireq()
        print(f'Received message from {mac}: {msg}')
        self.process_packet(msg)

    def process_packet(self, packet_bytes):
        print('Process Packet Start')
        try:
            packet = json.loads(packet_bytes)
            if self.telemetry_callback is not None:
                print('telemetry_callback start')
                self.telemetry_callback(packet)
                print('telemetry_callback complete')
        except json.JSONDecodeError as e:
            print(f'Error decoding JSON: {e}')

# Example of telemetry.py content
