import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.vector import Vector
from kivy.clock import Clock


class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class OnePlayerWindow(Widget):
    easy = ObjectProperty(None)
    normal = ObjectProperty(None)
    hard = ObjectProperty(None)


class TwoPlayersGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    
    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, dt):
        self.ball.move()

        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1
        
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(-4, 0))
        if self.ball.x > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))
        
    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y


class MainWindow(Widget):
    def __init__(self, **kwargs):

        super(MainWindow, self).__init__(**kwargs)
        self.rows = 3

        one_player_btn = ObjectProperty(None)
        two_players_btn = ObjectProperty(None)
        exit_btn = ObjectProperty(None)

        self.MainGrid = GridLayout()
        self.MainGrid.cols = 1

        self.add_widget(self.MainGrid)


class WindowManager(ScreenManager):
    def __init__(self, **kwargs):
        super(WindowManager, self).__init__(**kwargs)

        self.main_window = Screen(name="main_window")
        self.one_player_window = Screen(name="one_player_window")
        self.two_players_window = Screen(name="two_players_window")

        self.add_widget(self.main_window)
        self.add_widget(self.one_player_window)
        self.add_widget(self.two_players_window)

        main_window = MainWindow()
        main_window.one_player_btn.bind(on_press=self.set_one_player_window)
        main_window.two_players_btn.bind(on_press=self.set_two_players_window)

        self.main_window.add_widget(main_window)

    def set_one_player_window(self, *args):
        one_player_window = OnePlayerWindow()
        self.one_player_window.add_widget(one_player_window)
        self.current = "one_player_window"

    def set_two_players_window(self, *args):
        self.game = TwoPlayersGame()
        self.game.serve_ball()
        Clock.schedule_interval(self.game.update, 1.0 / 60.0)
        self.two_players_window.add_widget(self.game)
        self.current = "two_players_window"


class PongApp(App):
    def build(self):
        return WindowManager()


if __name__ == "__main__":
    PongApp().run()
