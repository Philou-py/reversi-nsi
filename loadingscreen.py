from asciimatics.effects import Cycle, Print
from asciimatics.renderers import FigletText
from asciimatics.scene import Scene
from asciimatics.screen import Screen

def demo(screen):
    effects = [
            Cycle(
                screen,
                FigletText("REVERSI", font="broadway"),
                int(screen.height / 2 - 8)),
            Print(
                screen,
                FigletText("MADE BY DIEGO", font="Graceful"),
                int(screen.height / 2 +13)
                )
                        ]
    screen.play([Scene(effects, 500)])

Screen.wrapper(demo)

#BannerText(
#                screen,
#                FigletText("made by diego", font="Graceful"),
#                int(screen.height / 2 + 3),
#                3)
