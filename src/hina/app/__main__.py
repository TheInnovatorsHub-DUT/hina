from kivy.app import App
from kivy.uix.label import Label


class HinaApp(App):
    def build(self):
        return Label(text="Hello from hina!")
