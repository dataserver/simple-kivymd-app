
from kivy.clock import Clock
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivymd.theming import ThemableBehavior
from kivymd.uix.label import MDLabel
from kivymd.uix.list import (IconLeftWidget, ImageLeftWidget, MDList,
                             OneLineIconListItem, TwoLineAvatarListItem)
from kivymd.uix.textfield import MDTextField


class ContentNavigationDrawer(BoxLayout):
    pass

class DrawerList(ThemableBehavior, MDList):
    pass

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_pre_enter(self, *args):
        Clock.schedule_once(self.on_change_screen)
        pass

    def on_enter(self, *args):
        # Clock.schedule_once(self.on_change_screen)
        pass

    def on_change_screen(self, *args):
        self.ids.box_layout.clear_widgets()

        scroll = ScrollView()
        list_view = MDList()
        my_label = MDLabel(text="Hello World!", pos_hint={"center_x": 0.5, "center_y": 0.5}, size_hint_x=None, width=200)
        scroll.add_widget(list_view)
        self.ids.box_layout.add_widget(my_label)
        self.ids.box_layout.add_widget(scroll)

    # SCREEN ACTIONS
    def no_action(self):
        print("no action defined")
