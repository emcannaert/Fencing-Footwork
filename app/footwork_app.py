from kivy.config import Config
from kivy.clock import Clock
import threading
from plyer import tts
import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
import time 

# Set the window size for desktop testing
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '800')
Config.set('graphics', 'resizable', True)

class LabeledSlider(BoxLayout):
    def __init__(self, title, min_val, max_val, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = "110dp"
        self.add_widget(Label(text=title, size_hint_y=None, height="30dp", font_size='18sp'))
        slider_padding = 30 
        self.slider = Slider(min=min_val, max=max_val, value=int((min_val+max_val)/2), step=1, padding=slider_padding)
        self.add_widget(self.slider)
        tick_container = FloatLayout(size_hint_y=None, height="20dp")
        num_steps = max_val - min_val
        for i in range(min_val, max_val + 1):
            pos_x = (i - min_val) / num_steps
            lbl = Label(text=str(i), font_size='12sp', color=(0.7, 0.7, 0.7, 1),
                        size_hint=(None, None), size=("40dp", "20dp"),
                        pos_hint={'center_x': pos_x, 'top': 1})
            tick_container.add_widget(lbl)
        padded_ticks = BoxLayout(padding=(slider_padding, 0))
        padded_ticks.add_widget(tick_container)
        self.add_widget(padded_ticks)

class StringLabeledSlider(BoxLayout):
    def __init__(self, title, options, callback, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = "120dp"
        self.options = options
        self.add_widget(Label(text=title, size_hint_y=None, height="30dp", font_size='18sp'))
        slider_padding = 40
        self.slider = Slider(min=0, max=len(options) - 1, value=1, step=1, padding=slider_padding)
        self.slider.bind(value=callback)
        self.add_widget(self.slider)
        tick_container = FloatLayout(size_hint_y=None, height="30dp")
        num_steps = len(options) - 1
        for i, text in enumerate(options):
            pos_x = i / num_steps if num_steps > 0 else 0.5
            lbl = Label(text=text, font_size='12sp', color=(0.7, 0.7, 0.7, 1),
                        size_hint=(None, None), size=("60dp", "30dp"),
                        pos_hint={'center_x': pos_x, 'top': 1})
            tick_container.add_widget(lbl)
        padded_ticks = BoxLayout(padding=(slider_padding, 0))
        padded_ticks.add_widget(tick_container)
        self.add_widget(padded_ticks)

class FencingManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_running = False
        self.profiles = ["Child", "Normal", "Athletic", "Custom"]
        self.piste_length = 42 
        self.pos_ = self.piste_length/2.0
        self.end_margin = 8.0

        # --- SETTINGS SCREEN ---
        settings_screen = Screen(name='settings')
        scroll = ScrollView(do_scroll_x=False, do_scroll_y=True)
        self.settings_layout = BoxLayout(orientation='vertical', padding=20, spacing=15, size_hint_y=None)
        self.settings_layout.bind(minimum_height=self.settings_layout.setter('height'))

        # Header Row
        top_row = BoxLayout(orientation='horizontal', size_hint_y=None, height="90dp", spacing=20)
        duration_col = BoxLayout(orientation='vertical', spacing=5)
        duration_col.add_widget(Label(text="Duration (s)", font_size='16sp'))
        self.time_input = TextInput(text='90', multiline=False, input_filter='int', halign='center')
        duration_col.add_widget(self.time_input)
        piste_col = BoxLayout(orientation='vertical', spacing=5)
        piste_col.add_widget(Label(text="Piste (ft)", font_size='16sp'))
        self.piste_l_input = TextInput(text='42', multiline=False, input_filter='int', halign='center')
        piste_col.add_widget(self.piste_l_input)
        top_row.add_widget(duration_col); top_row.add_widget(piste_col)
        self.settings_layout.add_widget(top_row)

        # Standard Sliders
        self.s1 = LabeledSlider("Pace", 1, 5)
        self.s1.slider.bind(value=self.update_all_ui)
        self.s2 = LabeledSlider("Complexity", 1, 3)
        self.s2.slider.bind(value=self.update_all_ui) 
        self.settings_layout.add_widget(self.s1)
        self.settings_layout.add_widget(self.s2)
        
        # Fencer Type
        self.s_fencer_type = StringLabeledSlider("Fencer Type", self.profiles, self.on_profile_change)
        self.settings_layout.add_widget(self.s_fencer_type)

        # PRE-DEFINE Custom Container (But don't add to layout yet)
        self.custom_container = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None, height="100dp")
        row1 = BoxLayout(spacing=10, size_hint_y=None, height="40dp")
        self.adv_input = TextInput(hint_text="Adv (ft)", multiline=False, input_filter='float')
        self.lng_input = TextInput(hint_text="Lng (ft)", multiline=False, input_filter='float')
        row1.add_widget(self.adv_input); row1.add_widget(self.lng_input)
        row2 = BoxLayout(spacing=10, size_hint_y=None, height="40dp")
        self.ret_input = TextInput(hint_text="Ret (ft)", multiline=False, input_filter='float')
        self.long_ret_input = TextInput(hint_text="Long Ret", multiline=False, input_filter='float')
        row2.add_widget(self.ret_input); row2.add_widget(self.long_ret_input)
        self.custom_container.add_widget(row1); self.custom_container.add_widget(row2)

        self.fleche_row = BoxLayout(spacing=10, size_hint_y=None, height="40dp")
        self.fleche_input = TextInput(hint_text="Fleche (ft)", multiline=False, input_filter='float')
        self.fleche_row.add_widget(self.fleche_input)

        # Start Button
        self.start_btn = Button(text="START LESSON", size_hint_y=None, height="60dp", background_color=(0.2, 0.8, 0.2, 1), bold=True)
        self.start_btn.bind(on_release=self.start_lesson)
        self.settings_layout.add_widget(self.start_btn)

        scroll.add_widget(self.settings_layout)
        settings_screen.add_widget(scroll)

        # --- RUNNING SCREEN ---
        self.run_screen = Screen(name='running')
        run_layout = BoxLayout(orientation='vertical', padding=40, spacing=30)
        self.timer_display = Label(text="Time Left: 90s", font_size='40sp', bold=True)
        self.action_display = Label(text="READY...", font_size='35sp', color=(0.3, 0.7, 0.9, 1))
        stop_btn = Button(text="STOP", size_hint=(None, None), size=("200dp", "60dp"), pos_hint={'center_x': 0.5}, background_color=(0.8, 0.2, 0.2, 1), bold=True)
        stop_btn.bind(on_release=self.stop_lesson)
        run_layout.add_widget(self.timer_display); run_layout.add_widget(self.action_display); run_layout.add_widget(stop_btn)
        self.run_screen.add_widget(run_layout)

        self.add_widget(settings_screen)
        self.add_widget(self.run_screen)

    def on_profile_change(self, instance, value):
        self.update_all_ui()

    def update_all_ui(self, *args):
        if not hasattr(self, 's_fencer_type'): return
        
        idx = int(self.s_fencer_type.slider.value)
        is_custom = (self.profiles[idx] == "Custom")
        is_complex = (int(self.s2.slider.value) >= 3)

        # Remove everything first to reset order
        if self.custom_container in self.settings_layout.children:
            self.settings_layout.remove_widget(self.custom_container)
        if self.start_btn in self.settings_layout.children:
            self.settings_layout.remove_widget(self.start_btn)

        if is_custom:
            # Handle Fleche field
            if is_complex and self.fleche_row not in self.custom_container.children:
                self.custom_container.add_widget(self.fleche_row)
                self.custom_container.height = "150dp"
            elif not is_complex and self.fleche_row in self.custom_container.children:
                self.custom_container.remove_widget(self.fleche_row)
                self.custom_container.height = "100dp"
            
            self.settings_layout.add_widget(self.custom_container)

        # Always put Start Button at the bottom
        self.settings_layout.add_widget(self.start_btn)

    def start_lesson(self, instance):
        self.is_running = True
        self.time_remaining = float(self.time_input.text or 90)
        self.current = 'running'
        self.visual_event = Clock.schedule_interval(self.update_timer, 1.0)
        self.next_action_event = Clock.schedule_once(self.execute_next_step, 1.5)

    def update_timer(self, dt):
        if self.time_remaining > 0:
            self.time_remaining -= 1
            self.timer_display.text = f"Time Left: {int(self.time_remaining)}s"
        else:
            self.stop_lesson()

    def get_user_settings(self):
        settings = { "adv": 1.5, "lng": 3.5, "ret": 1.5, "lret": 3.0, "fleche": 5.0 }
        val = int(self.s_fencer_type.slider.value)
        settings["fencerType"] = self.profiles[val]
        
        if settings["fencerType"] == "Custom":
            def safe_f(ui, d):
                try: return float(ui.text) if ui.text.strip() else d
                except: return d
            settings["adv"] = safe_f(self.adv_input, 1.5)
            settings["lng"] = safe_f(self.lng_input, 3.5)
            settings["ret"] = safe_f(self.ret_input, 1.5)
            settings["lret"] = safe_f(self.long_ret_input, 3.0)
            settings["fleche"] = safe_f(self.fleche_input, 5.0)
        return settings

    def get_fencer_pars(self, fType, s):
             # adv.  ret.  long-ret. lunge  double-adv. double-ret.  adv-lunge  retr-lunge   long-lunge   fleche  redouble  duck
        if fType == "Child": return [0.7, -0.7, -1.3, 0.0, 1.5, -1.5, 0.85, -0.75, 2.0, 4, 3.0, 0.0]
        if fType == "Normal": return [1.0, -1.0, -1.6, 0.0, 2.0, -2.0, 1.4, -1.1, 2.5, 7.0, 5.0, 0.0]
        if fType == "Athletic": return [1.2, -1.2, -1.9, 0.0, 2.4, -2.4, 1.5, -1.3, 3.0, 8.0, 6.0, 0.0]
        if fType == "Custom": return [s['adv'], -s['ret'], -s['lret'], 0.0, 2*s['adv'], -2*s['ret'], s['adv'], -s['ret'], 1.5*s['adv'], s['fleche'], 2*s['adv'], 0.0]
        return [1, -1, -2, 0, 2, -2, 1, -1, 2, 7, 5, 0]

    def get_action_tempi(self, pace):
        tempi = {

         # adv.  ret.  long-ret. lunge  double-adv. double-ret.  adv-lunge  retr-lunge   long-lunge   fleche  redouble  duck
            1: [3.0, 3.0, 3.0, 5.0, 4.0, 4.0, 6.0, 6.0, 5.0, 8.0, 6.0, 4.0],
            2: [2.2, 2.2, 2.2, 3.0, 3.0, 3.0, 3.5, 3.5, 3.5, 6.0, 4.4, 3.2],
            3: [1.8, 1.8, 1.8, 2.2, 2.5, 2.5, 2.7, 2.7, 3.0, 5.5, 4.0, 2.7],
            4: [1.25, 1.25, 1.25, 2.1, 2.2, 2.2, 2.5, 2.4, 2.3, 5.5, 3.3, 2.3],
            5: [1.0, 1.0, 1.2, 1.9, 1.8, 1.8, 2.3, 2.15, 2.1, 5.0, 3.0, 2.0]
        }
        return tempi.get(pace, tempi[3])

    def get_rand_action(self, complexity):
        rand = random.random()
         # adv.  ret.  long-ret. lunge  double-adv. double-ret.  adv-lunge  retr-lunge   long-lunge   fleche  redouble  duck
        if complexity == 1: fs = [0.4, 0.35, 0.10, 0.15]
        elif complexity == 2: fs = [0.20, 0.20, 0.05, 0.10, 0.10, 0.10, 0.10, 0.05, 0.10]
        else: fs = [0.15, 0.225, 0.05, 0.10, 0.075, 0.15, 0.075, 0.05, 0.05, 0.025, 0.025, 0.025]
        
        acc = 0
        for i, f in enumerate(fs):
            acc += f
            if rand <= acc: return i
        return 0

    def isValidAction(self, action_len):
        new_pos = self.pos_ + action_len
        return self.end_margin < new_pos < (self.piste_length - self.end_margin)

    def execute_next_step(self, dt):
        if not self.is_running: return
        actions = ["advance", "retreat", "long-retreat", "lunge", "double-advance", "double-retreat", "advance-lunge", "retreat-lunge", "long-lunge", "fleche", "redouble", "duck"]
        comp = int(self.s2.slider.value)
        pace = int(self.s1.slider.value)
        s = self.get_user_settings()
        lens = self.get_fencer_pars(s['fencerType'], s)
        ts = self.get_action_tempi(pace)

        valid = False
        action = 0
        while not valid:
            action = self.get_rand_action(comp)
            valid = self.isValidAction(lens[action])

        self.pos_ += lens[action]
        action_text = actions[action]
        self.action_display.text = action_text.upper()
        self.announce(action_text)
        self.next_action_event = Clock.schedule_once(self.execute_next_step, ts[action])

    def announce(self, text):
        threading.Thread(target=self._speak, args=(text,), daemon=True).start()

    def _speak(self, text):
        if not self.is_running: 
            return
        try:
            clean_text = text.lower().strip() + "  ."
            tts.speak(clean_text)
            time.sleep(0.1) 
            
        except Exception as e:
            print(f"TTS Error: {e}")

    def stop_lesson(self, *args):
        self.is_running = False
        self.pos_ = self.piste_length / 2.0 # Reset fencer to middle
        Clock.unschedule(self.visual_event)
        Clock.unschedule(self.next_action_event)
        self.current = 'settings'

class FootworkApp(App):
    def build(self):
        return FencingManager()

if __name__ == '__main__':
    FootworkApp().run()