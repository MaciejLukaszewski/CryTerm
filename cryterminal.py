import readchar
from threading import Thread
from time import sleep

from screen import Screen

class pTimer():
    def __init__(self, delay, handler_function):
        self.delay = delay
        self.handler_function = handler_function
        self.running = False
        self.ptimer=Thread(target=self.run, daemon=True)

    def start(self):
        self.running=True
        self.ptimer.start()

    def stop(self):
        self.running=False

    def run(self):
        while self.running:
           self.handler_function()
           sleep(self.delay)


screen = Screen()
screen.clear()
screen.hide_cursor()

iter_timer = pTimer(0.06, screen.image_render)
iter_timer.start()

# Wait for user input - if any character is pressed exit program
readchar.readchar()

iter_timer.stop()
screen.clean()
exit()
