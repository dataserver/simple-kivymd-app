import sqlite3
import uuid

from kivy.clock import Clock
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivymd.theming import ThemableBehavior
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.list import (IconLeftWidget, ImageLeftWidget, MDList,
                             OneLineIconListItem, TwoLineAvatarListItem)
from kivymd.uix.textfield import MDTextField


class ContentNavigationDrawer(BoxLayout):
    pass

class DrawerList(ThemableBehavior, MDList):
    pass

class FormScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def load_device_info(self, device_id):
        conn = sqlite3.connect("mydb.sqlite3")
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("""
                    SELECT * FROM devices WHERE id=:id LIMIT 1
                    """, {
                        "id" : device_id,
                    })

        data = dict(result=[dict(r) for r in cur.fetchall()])
        conn.close()
        self.ids.action_button.device_id = data['result'][0]['id']
        self.ids.input_name.text = data['result'][0]['name']
        self.ids.input_ip.text = data['result'][0]['ip']

    # SCREEN ACTIONS
    def do_save(self):
        if (self.ids.action_button.device_id != ""):
            self.do_update()
        else:
            self.do_insert()

    def do_insert(self):
        conn = sqlite3.connect("mydb.sqlite3")
        cur = conn.cursor()

        cur.execute("""
                    INSERT INTO devices VALUES (
                        :id, :name, :ip
                    )
                    """, {
                        "id" : str(uuid.uuid4()),
                        "name": self.ids.input_name.text,
                        "ip": self.ids.input_ip.text
                    })
        conn.commit()
        conn.close()
        self.ids.input_name.text = ""
        self.ids.input_ip.text = ""
        self.manager.current = "devices"


    def do_update(self, *args):
        conn = sqlite3.connect("mydb.sqlite3")
        cur = conn.cursor()

        cur.execute("""
                    UPDATE devices SET name=:name, ip=:ip WHERE id=:id
                    """, {
                        "id": self.ids.action_button.device_id,
                        "name": self.ids.input_name.text,
                        "ip": self.ids.input_ip.text
                    })
        conn.commit()
        conn.close()
        self.ids.input_name.text = ""
        self.ids.input_ip.text = ""
        self.ids.action_button.device_id = ""
        self.manager.current = "devices"

    def no_action(self):
        print("no action defined")
