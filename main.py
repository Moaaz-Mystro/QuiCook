# Imports
import json
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import AsyncImage
from kivy.uix.scrollview import ScrollView
import os
from kivy.graphics import Color, Rectangle
import pyperclip

# Main Vars
Lang = "Ar"

file_path = os.path.join(os.path.dirname(__file__), f"recipies{Lang}.json")
with open(file_path, "r", encoding="utf-8") as f:
    recipies_file = json.load(f)


class MainApp(App):
    def build(self):
        self.title = "Recipies App"
        self.icon = os.path.join(os.path.dirname(__file__), f"icon.png")
        return MainManager()


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        self.add_widget(layout)

        scroll_view = ScrollView()
        box = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10, padding=10)
        box.bind(minimum_height=box.setter('height'))
        scroll_view.add_widget(box)

        
        

        for item in recipies_file:
            recipe_widget = RootWidget(item, self)
            box.add_widget(recipe_widget)

        layout.add_widget(scroll_view)

    def show_details(self, item):
        detail_screen = DetailScreen(item)
        self.manager.add_widget(detail_screen)
        self.manager.current = detail_screen.name


class MainManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.main_screen = MainScreen(name='main')
        self.add_widget(self.main_screen)
        self.current = 'main'


class RootWidget(BoxLayout):
    def __init__(self, item, main_screen, **kwargs):
        super().__init__(orientation="vertical", size_hint_y=None, height=350, spacing=10, **kwargs)
        self.item = item
        self.main_screen = main_screen

        # الصورة
        self.add_widget(AsyncImage(source=item["img"], size_hint_y=None, height=200))

        # الاسم + زرار في النص
        inner_box = BoxLayout(orientation="vertical", size_hint_y=None, height=100, spacing=10)
        inner_box.add_widget(Label(text=item["title"], font_size='20sp', halign="center", valign="middle"))
        see_more_btn = Button(
            text="See More",
            size_hint=(None, None),
            size=(200, 40),
            background_color=(0.3, 0.3, 0, 1),
            pos_hint={"center_x": 0.5}
        )
        see_more_btn.bind(on_release=self.view_details)
        inner_box.add_widget(see_more_btn)

        self.add_widget(inner_box)

        # border بين الوصفات
        border = BoxLayout(size_hint_y=None, height=2)
        border.bind(size=self._update_border, pos=self._update_border)
        self.add_widget(border)

    def _update_border(self, instance, value):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(0.3, 0.3, 0, 1)
            Rectangle(size=instance.size, pos=instance.pos)

    def view_details(self, instance):
        self.main_screen.show_details(self.item)


class DetailScreen(Screen):
    def __init__(self, item, **kwargs):
        super().__init__(**kwargs)
        self.name = f"detail_{item['id']}"
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.add_widget(layout)

        layout.add_widget(AsyncImage(source=item["img"], size_hint_y=None, height=250))
        layout.add_widget(Label(text=item["title"], font_size='24sp', size_hint_y=None, height=50))

        # Ingredients Section
        layout.add_widget(Label(text="Ingredients:", font_size='20sp', size_hint_y=None, height=40))
        for ingredient in item["ingredients"]:
            layout.add_widget(Label(text=ingredient, size_hint_y=None, height=30))

        # Border
        border1 = BoxLayout(size_hint_y=None, height=2)
        border1.bind(size=self._update_border, pos=self._update_border)
        layout.add_widget(border1)

        # Instructions Section
        layout.add_widget(Label(text="Instructions:", font_size='20sp', size_hint_y=None, height=40))

        if isinstance(item["instructions"], str):
            layout.add_widget(Label(text=item["instructions"], size_hint_y=None, height=60))
        else:
            for step in item["instructions"]:
                layout.add_widget(Label(text=step, size_hint_y=None, height=30))

        # زرار Back في النص
        back_btn = Button(
            text="Back",
            size_hint=(None, None),
            size=(200, 40),
            pos_hint={"center_x": 0.5},
            background_color=(0.3, 0.3, 0, 1)
        )
        back_btn.bind(on_release=self.go_back)
        layout.add_widget(back_btn)
        layout.add_widget(Label(text="If there is an error, please mail me at mystro2012730@gmail.com", font_size='17sp', size_hint_y=None, height=50, color=(1, 1, 1, 1), bold=True))
        layout.add_widget(Label(text="Made by Moaaz", font_size='15sp', size_hint_y=None, height=30, color=(1, 1, 1, 1), italic=True))
        layout.add_widget(Button(text="Copy Email Address", size_hint=(None, None), size=(200, 40), pos_hint={"center_x": 0.5}, background_color=(0.3, 0.3, 0, 1), on_release=lambda x: pyperclip.copy("mystro2012730@gmail.com")))


    def _update_border(self, instance, value):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(0.3, 0.3, 0, 1)
            Rectangle(size=instance.size, pos=instance.pos)

    def go_back(self, instance):
        self.manager.current = 'main'
        self.manager.remove_widget(self)


MainApp().run()
