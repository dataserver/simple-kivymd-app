import json

from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp, sp
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivymd.theming import ThemableBehavior
from kivymd.uix.label import MDLabel
from kivymd.uix.list import (IconLeftWidget, ImageLeftWidget, MDList,
                             OneLineIconListItem, TwoLineAvatarListItem)
from kivymd.uix.selectioncontrol import MDSwitch
from kivymd.uix.textfield import MDTextField
from sqlitedict import SqliteDict

from configs_env import ENV


class ContentNavigationDrawer(BoxLayout):
    pass

class DrawerList(ThemableBehavior, MDList):
    pass

class ConfigScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_pre_enter(self, *args):
        with SqliteDict(ENV["DB_FILE_NAME"], tablename=ENV["DB_TABLE_CONFIG_NAME"],encode=json.dumps, decode=json.loads) as db:
            c = db["default_config"]
            self.ids.variable_a.active = c["variable_a"]
            self.ids.variable_b.active = c["variable_b"]
            self.ids.variable_c.active = c["variable_c"]
            self.ids.variable_d.text = c["variable_d"]

    def do_switch_click(self, variable_id, switchObject, switchValue):
        pass

    def do_save(self):
        new_cfg = {
            "variable_a": self.ids.variable_a.active,
            "variable_b": self.ids.variable_b.active,
            "variable_c": self.ids.variable_c.active,
            "variable_d" : self.ids.variable_d.text
        }
        with SqliteDict(ENV["DB_FILE_NAME"], tablename=ENV["DB_TABLE_CONFIG_NAME"],encode=json.dumps, decode=json.loads) as db:
            db["default_config"] = new_cfg
            db.commit()
        App.get_running_app().cfg = new_cfg
        self.manager.current = "home"

    def no_action(self):
        print("no action defined")
