
import network
import espnow
import json

class Telemetry:
    def __init__(self, peer_mac):
        self.peer_mac = peer_mac
        # A WLAN interface must be active to send()/recv()
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        self.wlan.disconnect()   # Because ESP8266 auto-connects to last Access Point

        self.esp_now = espnow.ESPNow()
        self.esp_now.active(True)
        self.esp_now.irq(self.receive_callback)
        self.esp_now.add_peer(self.peer_mac)

        self.telemetry_callback = None

    def register_telemetry_callback(self, callback):
        self.telemetry_callback = callback

    def receive_callback(self, interface):
        while True:
            mac, msg = interface.recv(0)  # 0 timeout == no waiting
            if mac is None:
                return
            self.process_callback(msg)

    # Packets are JSON strings
    def process_callback(self, packet):
        print('process_callback')
        response = json.loads(packet)
        if self.telemetry_callback is not None:
            print('callback received')
            self.telemetry_callback(response)

    def send_packet(self, packet):
        self.esp_now.send(self.peer_mac, packet, True)

    def shutdown(self):
        self.esp_now.active(False)
        self.wlan.active(False)
