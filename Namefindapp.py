from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.anchorlayout import AnchorLayout
from kivy.core.window import Window
import webbrowser

Window.clearcolor = (0, 0, 0, 1)

questions = [
    "Q1: Solve 3x - 4 = 53",
    "Q2: Let f(x)=2x+3. Find the value of f(6)?",
    "Q3: Solve for x: 4x - 2 = 22",
    "Q4: Solve the quadratic equation: x² - 18x + 81 = 0",
    "Q5: Solve: (2³ + 2) − 3 × 3 ÷ (√81 − 8)"
]

class IntroScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = AnchorLayout(anchor_x='center', anchor_y='center')
        box = BoxLayout(orientation='vertical', size_hint=(0.8, 0.3), padding=20, spacing=10)
        box.add_widget(Label(text='Mayank Joshi Studios', font_size=50, color=(1, 1, 1, 1)))
        layout.add_widget(box)
        self.add_widget(layout)

    def on_enter(self):
        Clock.schedule_once(self.switch_to_lock, 10)

    def switch_to_lock(self, dt):
        self.manager.current = 'lock'

class LockScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.entered_pin = ""
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        top_bar = AnchorLayout(anchor_x='right', anchor_y='top')
        yt_btn = Button(text='Powered By Astral Valiant', size_hint=(None, None), size=(240, 40),
                        background_color=(0, 0, 0, 0), color=(1, 0, 0, 1), bold=True)
        yt_btn.bind(on_release=self.open_channel)
        top_bar.add_widget(yt_btn)
        layout.add_widget(top_bar)

        self.display = Label(text='Enter Key', font_size=30)
        layout.add_widget(self.display)

        keypad = GridLayout(cols=3, spacing=10, size_hint=(1, 0.6))
        for i in range(1, 10):
            btn = Button(text=str(i), on_release=self.key_pressed)
            keypad.add_widget(btn)
        keypad.add_widget(Button(text='⌫', on_release=self.backspace))
        keypad.add_widget(Button(text='0', on_release=self.key_pressed))
        keypad.add_widget(Button(text='✔', on_release=self.check_key))
        layout.add_widget(keypad)

        self.add_widget(layout)

    def key_pressed(self, instance):
        if len(self.entered_pin) < 4:
            self.entered_pin += instance.text
            self.display.text = '*' * len(self.entered_pin)

    def backspace(self, instance):
        self.entered_pin = self.entered_pin[:-1]
        self.display.text = '*' * len(self.entered_pin)

    def check_key(self, instance):
        if self.entered_pin == "2011":
            self.manager.current = 'start'
        else:
            popup = Popup(title='Incorrect Key', content=Label(text='Wrong key! Try again.'),
                          size_hint=(None, None), size=(300, 200))
            popup.open()
            self.entered_pin = ""
            self.display.text = 'Enter Key'

    def open_channel(self, instance):
        webbrowser.open("https://youtube.com/@astralvaliant?si=i6iLrgISASpAEXK8")

class StartScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        title = Label(text='[b]Find Name[/b]', markup=True, font_size=32, size_hint=(1, 0.2))
        message = Label(
            text='Namaste!\nAgar aap naam janna chahte hain to aapko questions ke answer dene honge.\nAre you ready?',
            font_size=20, halign='center', valign='middle'
        )

        btn_layout = BoxLayout(size_hint=(1, 0.3), spacing=20)
        yes_btn = Button(text='Yes', on_press=self.go_to_questions)
        no_btn = Button(text='No', on_press=self.quit_app)
        btn_layout.add_widget(yes_btn)
        btn_layout.add_widget(no_btn)

        layout.add_widget(title)
        layout.add_widget(message)
        layout.add_widget(btn_layout)
        self.add_widget(layout)

    def go_to_questions(self, instance):
        self.manager.current = 'question'

    def quit_app(self, instance):
        App.get_running_app().stop()

class QuestionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_index = 0
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        self.title = Label(text='[b]Find Name[/b]', markup=True, font_size=32, size_hint=(1, 0.2))
        self.question_label = Label(
            text=questions[self.current_index], font_size=24,
            halign='center', valign='middle'
        )

        self.next_btn = Button(text='➡️ Next', size_hint=(1, 0.2))
        self.next_btn.bind(on_press=self.next_question)

        self.layout.add_widget(self.title)
        self.layout.add_widget(self.question_label)
        self.layout.add_widget(self.next_btn)
        self.add_widget(self.layout)

    def next_question(self, instance):
        self.current_index += 1
        if self.current_index < len(questions):
            self.question_label.text = questions[self.current_index]
        else:
            self.question_label.text = (
                "🎉 Congratulations! You finished all questions.\n\n"
                "Hint: A B C D E F G H I J K L M N O P Q R S T U V W X Y Z"
            )
            self.next_btn.disabled = True
            Clock.schedule_once(self.close_app, 5)

    def close_app(self, dt):
        App.get_running_app().stop()

class QuizApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(IntroScreen(name='intro'))
        sm.add_widget(LockScreen(name='lock'))
        sm.add_widget(StartScreen(name='start'))
        sm.add_widget(QuestionScreen(name='question'))
        return sm

if __name__ == '__main__':
    QuizApp().run()