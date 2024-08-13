from util import *
from window import *
import NotoSans_15 as font_15
import NotoSans_20 as font_20
import NotoSans_25 as font_25
import NotoSans_32 as font_32
from machine import Pin, Timer, ADC


class WelcomeWindow:

    BATTERY_DEFICIT_VOL = 1750
    BATTERY_FULL_VOL = 2100

    def __init__(self, window_manager, display, robot_chain):
        self.window_manager = window_manager
        self.display = display
        self.robot_chain = robot_chain
        self.window = Window(self.display, "Welcome")
        self.window.register_activate(self.window_activated)
        self.window.register_about_to_close(self.window_closing)
        self.theme_callback = None

        main_view = View("Top", Point(40, 0), Point(160, 240))
        self.window.add_view(main_view)

        label = VisualLabel(Point(0, 20), "FIFteen", font_15, True, Color.TITLE)
        main_view.add_component(label)
        label = VisualLabel(Point(0, 35), "TWEnty", font_20, True, Color.TITLE)
        main_view.add_component(label)
        label = VisualLabel(Point(0, 55), "TWENTY five", font_25, True, Color.TITLE)
        main_view.add_component(label)
        label = VisualLabel(Point(0, 70), "THIRTY two", font_32, True, Color.TITLE)
        main_view.add_component(label)

        # label = VisualLabel(Point(0, 60), "UNIVERSAL", font_25, True, Color.TITLE)
        # main_view.add_component(label)
        # label = VisualLabel(Point(0, 88), "ROBOT", font_25, True, Color.TITLE)
        # main_view.add_component(label)
        # label = VisualLabel(Point(0, 116), "CONFIGURER", font_25, True, Color.TITLE)
        # main_view.add_component(label)

        battery_y = 170
        label = VisualLabel(Point(10, battery_y), "Batt:", font_25, False, Color.LABEL)
        main_view.add_component(label)

        label_box = Rectangle(Point(75, battery_y - 2), Point(70, 30))
        self.battery_label = VisualLabel(label_box, "", font_25, False, Color.GOOD_LABEL)
        main_view.add_component(self.battery_label)

        self.charging_label = VisualLabel(Point(0, battery_y + 35), '', font_15, Color.ALERT_LABEL)
        main_view.add_component(self.charging_label)

        self.battery = ADC(Pin(1))
        self.battery.atten(ADC.ATTN_11DB)  # get the full range 0 - 3.3v

        # Make an invisible button
        button = VisualButton(Rectangle(Point(0, 78), Point(160, 80)), '', font_15, Color.BUTTON, False)
        main_view.add_component(button)
        button.register_click_handler(self.enter_urc)
        self.build_theme_window()

    def register_theme_callback(self, callback):
        self.theme_callback = callback

    def build_theme_window(self):
        self.theme_window = Window(self.display, "Theme")

        main_view = View("Top", Point(40, 0), Point(160, 240))
        self.theme_window.add_view(main_view)

        label = VisualLabel(Point(0, 30), "THEMES", font_25, True, Color.TITLE)
        main_view.add_component(label)

        self.themes = Theme.available_themes()
        box = Rectangle(Point(0, 70), Point(160, 104))
        items = [theme.name for theme in self.themes]
        self.vlist = VisualList(box, items, font_20, Color.LIST)
        main_view.add_component(self.vlist)
        self.vlist.register_click_handler(self.choose_button_click)

        button = VisualButton(Rectangle(Point(20, 190), Point(120, 35)), "CHOOSE", font_25, Color.BUTTON)
        main_view.add_component(button)
        button.register_click_handler(self.choose_button_click)

    def choose_button_click(self, item=None):
        if item is None:
            item = self.vlist.selected_item()
        theme = next((x for x in self.themes if x.name == item))
        theme.apply()
        if self.theme_callback is not None:
            self.theme_callback()

    def enter_urc(self):
        print('Entering Main Menu from Welcome Screen')
        self.window_manager.push_window_chain(self.robot_chain)

    def update_battery(self, timer):
        voltage = get_battery_level(self.battery)
        if voltage >= 3.7:
            color = Color.GOOD_LABEL
        elif voltage >= 3.4:
            color = Color.WARNING_LABEL
        else:
            color = Color.ALERT_LABEL
        self.battery_label.set_text('{:.2f}v'.format(voltage))
        self.battery_label.set_color(color)
        if voltage > 4.3:
            self.charging_label.set_text('charging')
            self.charging_label.set_color(Color.ALERT_LABEL)
        else:
            self.charging_label.set_text('                  ')
            self.charging_label.set_color(Color.BACKGROUND)

    def cancel_battery_timer(self, window):
        self.battery_timer.deinit()

    def setup_battery_timer(self, window):
        self.battery_timer = Timer(2, mode=Timer.PERIODIC, freq=1, callback=self.update_battery)

    def window_activated(self, window):
        print(f'{window.name} activated')
        self.setup_battery_timer(None)
        self.window.register_screensaver_activate(self.cancel_battery_timer)
        self.window.register_screensaver_deactivate(self.setup_battery_timer)

    def window_closing(self, window):
        print(f'{window.name} closing')
        self.cancel_battery_timer(window)
