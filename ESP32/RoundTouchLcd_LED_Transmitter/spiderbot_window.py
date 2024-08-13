from util import *
from window import *
from telemetry import *
from macs import *
import NotoSans_15 as font_15
import NotoSans_20 as font_20
import NotoSans_25 as font_25
import NotoSans_32 as font_32


class SpiderBot:
    def __init__(self, window_manager, display):
        self.window_manager = window_manager
        self.display = display
        self.build_root_window()

    def build_root_window(self):
        self.root_window = Window(self.display, "SpiderBot")

        box = Rectangle(Point(0, 0), Point(240, 240))
        main_view = View("Top", box.origin, box.extent)
        self.root_window.add_view(main_view)

        button = VisualButton(Rectangle(Point(0, 78), Point(160, 80)), '', font_15, Color.LABEL, False)
        main_view.add_component(button)
        button.register_click_handler(self.open_spiderbot_window)

    def open_spiderbot_window(self):
        SpiderBotWindow(self.window_manager, self.display)


class SpiderBotWindow:
    def __init__(self, window_manager, display):
        self.window_manager = window_manager
        self.display = display
        self.build_spiderbot_choose_window()
        self.window_manager.push_window(self.choose_window)
        self.window_manager.disable_screensaver()

        self.telemetry = Telemetry(SPIDERBOT_MAC_ADDRESS)
        self.telemetry.register_telemetry_callback(self.get_telemetry_packet)

    def build_spiderbot_choose_window(self):
        self.choose_window = Window(self.display, 'SpiderBot')

        top_view = View("Top", Point(0, 0), Point(240, 58))
        middle_view = View("Middle", Point(40,58), Point(160, 124))
        bottom_view = View("Bottom", Point(0, 182), Point(240, 58))

        self.choose_window.add_view(top_view)
        self.choose_window.add_view(middle_view)
        self.choose_window.add_view(bottom_view)

        label = VisualLabel(Point(0, 20), 'LED Test', font_32, True, Color.TITLE)
        top_view.add_component(label)

        button_y = 20
        button = VisualButton(Rectangle(Point(0, button_y), Point(160, 35)), "ON", font_25, Color.BUTTON)
        middle_view.add_component(button)
        button.register_click_handler(self.clicked_led_on)

        button_y += 40
        button = VisualButton(Rectangle(Point(0, button_y), Point(160, 35)), "OFF", font_25, Color.BUTTON)
        middle_view.add_component(button)
        button.register_click_handler(self.clicked_led_off)

        button_y += 40
        button = VisualButton(Rectangle(Point(0, button_y), Point(160, 35)), "BLINK", font_25, Color.BUTTON)
        middle_view.add_component(button)
        button.register_click_handler(self.clicked_led_blink)
        self.choose_window.register_about_to_close(self.about_to_close)

    def about_to_close(self, window):
        print('Finished: {}'.format(window.name))
        self.window_manager.enable_screensaver()
        self.telemetry.shutdown()

    def clicked_led_on(self):
        print('SpiderBot LED on')
        self.telemetry.send_packet(self.led_on_packet())

    def clicked_led_off(self):
        print('SpiderBot LED off')
        self.telemetry.send_packet(self.led_off_packet())

    def clicked_led_blink(self):
        print('SpiderBot LED blink')
        self.telemetry.send_packet(self.led_blink_packet())

    def led_on_packet(self):
        return json.dumps({'led': 'on'})
    def led_off_packet(self):
        return json.dumps({'led': 'off'})
    def led_blink_packet(self):
        return json.dumps({'led': 'blink'})
    
    def get_telemetry_packet(self, packet):
        print('get_telemetry_packet')
        self.process_telemetry_packet(packet)

    def process_telemetry_packet(self, packet):
        print('Processing callback')
        if 'on' in packet:
            print('on returned')
            # self.robot_voltage = packet['rv']
        if 'off' in packet:
            print('off returned')
            # self.heading = packet['heading'] 
        if 'blink' in packet:
            print('blink returned')
            # self.heading = packet['heading'] 



