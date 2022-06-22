__version__ = "1.0.6"

import json
import sqlite3
from os.path import isfile

from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager
from kivy.utils import get_color_from_hex, platform
from kivymd.app import MDApp
from kivymd.font_definitions import fonts
from sqlitedict import SqliteDict

from configs_env import ENV
from screen_config import ConfigScreen
from screen_devices import DevicesScreen
from screen_form import FormScreen
from screen_home import HomeScreen

# add the following just under the imports
if platform == "android":
    from android.permissions import Permission, request_permissions

    request_permissions(
        [
            Permission.INTERNET,
            Permission.READ_EXTERNAL_STORAGE,
            Permission.WRITE_EXTERNAL_STORAGE,
        ]
    )

# Window.size = (300,500)


class WindowManager(ScreenManager):
    pass


class ContentNavigationDrawer(BoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()


class App(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cfg = {}

    def build(self):
        root = Builder.load_file("kv/index.kv")
        return root

    def on_start(self):
        self.theme_cls.primary_palette = "Purple"
        self.theme_cls.accent_palette = "Purple"
        self.theme_cls.primary_hue = "600"  # "500"
        self.create_db_or_connect()

        # from kivymd.icon_definitions import md_icons
        # https://kivy.org/doc/stable/api-kivy.core.text.markup.html #simple text-markup for inline text styling
        # f"""[size=25sp][font={fonts[-1]["fn_regular"]}]{md_icons["home-circle"]}[/size][/font]Title"""

        # home screen
        self.root.get_screen(
            "home"
        ).ids.toolbar.ids.label_title.text = (
            f"""[size=25sp][font={fonts[-1]["fn_regular"]}][/size][/font]Graúna"""
        )
        self.root.get_screen(
            "home"
        ).ids.toolbar.ids.label_title.family_name = "RobotoBlack"
        self.root.get_screen("home").ids.toolbar.ids.label_title.font_size = "25sp"

        # form screen
        self.root.get_screen(
            "form"
        ).ids.toolbar.ids.label_title.text = (
            f"""[size=25sp][font={fonts[-1]["fn_regular"]}][/size][/font]form"""
        )
        self.root.get_screen(
            "form"
        ).ids.toolbar.ids.label_title.family_name = "RobotoBlack"
        self.root.get_screen("form").ids.toolbar.ids.label_title.font_size = "25sp"

        # devices screen
        self.root.get_screen(
            "devices"
        ).ids.toolbar.ids.label_title.text = (
            f"""[size=25sp][font={fonts[-1]["fn_regular"]}][/size][/font]devices"""
        )
        self.root.get_screen(
            "devices"
        ).ids.toolbar.ids.label_title.family_name = "RobotoBlack"
        self.root.get_screen("devices").ids.toolbar.ids.label_title.font_size = "25sp"

        # config screen
        self.root.get_screen(
            "config"
        ).ids.toolbar.ids.label_title.text = (
            f"""[size=25sp][font={fonts[-1]["fn_regular"]}][/size][/font]config"""
        )
        self.root.get_screen(
            "config"
        ).ids.toolbar.ids.label_title.family_name = "RobotoBlack"
        self.root.get_screen("config").ids.toolbar.ids.label_title.font_size = "25sp"

    def go_home(self):
        self.root.current = "home"

    def change_screen_item(self, name):
        self.root.current = name

    def create_db_or_connect(self):
        if isfile(ENV["DB_FILE_NAME"]):
            with SqliteDict(
                ENV["DB_FILE_NAME"],
                tablename=ENV["DB_TABLE_CONFIG_NAME"],
                encode=json.dumps,
                decode=json.loads,
            ) as db:
                cfg = db["default_config"]
            self.cfg = cfg

        else:
            conn = sqlite3.connect(ENV["DB_FILE_NAME"])
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(
                """
                        CREATE TABLE if not exists devices (
                            id TEXT,
                            name TEXT,
                            ip TEXT,
                            PRIMARY KEY (id, name)
                        )
                        """
            )
            cur.execute("""INSERT INTO devices VALUES ('1', 'device A', '172.0.0.1')""")
            cur.execute("""INSERT INTO devices VALUES ('2', 'device B', '172.0.0.2')""")
            cur.execute("""INSERT INTO devices VALUES ('3', 'device C', '172.0.0.3')""")
            cur.execute("""INSERT INTO devices VALUES ('4', 'device D', '172.0.0.4')""")
            cur.execute("""INSERT INTO devices VALUES ('5', 'device E', '172.0.0.5')""")
            cur.execute("""INSERT INTO devices VALUES ('6', 'device F', '172.0.0.6')""")
            cur.execute("""INSERT INTO devices VALUES ('7', 'device G', '172.0.0.7')""")
            cur.execute("""INSERT INTO devices VALUES ('8', 'device H', '172.0.0.8')""")
            cur.execute("""INSERT INTO devices VALUES ('9', 'device I', '172.0.0.9')""")
            cur.execute(
                """INSERT INTO devices VALUES ('10', 'device J', '172.0.0.10')"""
            )
            conn.commit()
            conn.close()

            default_config = {
                "variable_a": False,
                "variable_b": False,
                "variable_c": False,
                "variable_d": "Sample Text",
            }
            with SqliteDict(
                ENV["DB_FILE_NAME"],
                tablename=ENV["DB_TABLE_CONFIG_NAME"],
                encode=json.dumps,
                decode=json.loads,
            ) as db:
                db["default_config"] = default_config
                db.commit()
            self.cfg = default_config

    @staticmethod
    def jsonKeys2int(x):
        # json.loads(jsonDict, object_hook=jsonKeys2int)
        if isinstance(x, dict):
            return {int(k): v for k, v in x.items()}
        return x


if __name__ == "__main__":
    App().run()
