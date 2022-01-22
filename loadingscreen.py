from asciimatics.effects import Cycle, Print, BannerText
from asciimatics.renderers import FigletText
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.screen import ManagedScreen
from time import sleep


def loadingScreen(screen):
    effects = [
            Cycle(
                screen,
                FigletText("REVERSI", font="broadway"),
                int(screen.height / 2 - 8)),
            Print(
                screen,
                FigletText("MADE BY DIEGO", font="Graceful"),
                int(screen.height / 2 +5)
                ),
            BannerText(
                screen,
                FigletText("Press [q] to start", font="Mini"),
                int(screen.height / 2 + 13),
                1
                )]
    screen.play([Scene(effects, 500, True)])
    return

def launch():
    Screen.wrapper(loadingScreen)

