import sqlite3

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivymd.theming import ThemableBehavior
from kivymd.uix.label import MDLabel
from kivymd.uix.list import (
    IconLeftWidget,
    ImageLeftWidget,
    MDList,
    OneLineIconListItem,
    OneLineListItem,
    TwoLineAvatarListItem,
    TwoLineIconListItem,
    TwoLineListItem,
)
from kivymd.uix.textfield import MDTextField
from sqlitedict import SqliteDict

from configs_env import ENV


class ContentNavigationDrawer(BoxLayout):
    pass


class DrawerList(ThemableBehavior, MDList):
    pass


class MyDevicesListItem(TwoLineListItem):
    """need object prop for extra data"""

    device_id = ObjectProperty()


class DevicesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_pre_enter(self, *args):

        self.ids.box_layout.clear_widgets()

        conn = sqlite3.connect(ENV["DB_FILE_NAME"])
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        scroll = ScrollView()
        list_view = MDList()

        header = OneLineListItem(
            text="Devices",
            secondary_text="List of devices",
        )
        list_view.add_widget(header)

        cur.execute("""SELECT * FROM devices""")
        results = [dict(row) for row in cur.fetchall()]
        # things = con.execute(select_query).fetchall()
        # unpacked = [{k: item[k] for k in item.keys()} for item in things]
        if len(results) > 0:
            for row in results:
                device_id = {row["id"]}
                item = MyDevicesListItem(
                    device_id=row["id"],
                    text=row["name"],
                    secondary_text=row["ip"],
                    on_release=(
                        lambda x, value_for_pass=device_id: self.do_edit_device(
                            value_for_pass
                        )
                    ),
                )
                list_view.add_widget(item)
        else:
            pass

        scroll.add_widget(list_view)
        self.ids.box_layout.add_widget(scroll)

        conn.close()

    def show_menu(self, device_id):
        print("device id", device_id)

    def do_edit_device(self, device_id):
        self.parent.current = "form"
        self.parent.get_screen("form").load_device_info(device_id)

    def do_delete_device(self):
        conn = sqlite3.connect(ENV["DB_FILE_NAME"])
        cur = conn.cursor()

        screen_content = self.root.ids.screen_manager.get_screen("scr_devices")
        cur.execute(
            """
            DELETE FROM devices WHERE id=:id
            """,
            {"id": self.db_id.text},
        )
        conn.commit()
        conn.close()

    def no_action(self):
        print("no action defined")
