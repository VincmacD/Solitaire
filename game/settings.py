from gamemode import Gamemode

class Settings:
    def __init__(self):
        self.active_gamemode = Gamemode.KLONDIKE
        self.draw_amount = 1
        self.reset_score = True

    def use_default_settings(self):
        self.active_gamemode = Gamemode.KLONDIKE
        self.draw_amount = 1
        self.reset_score = True

    def update_settings(self, gamemode):
        self.active_gamemode = gamemode
        if self.active_gamemode == Gamemode.KLONDIKE:
            self.use_default_settings()
        else:
            self.active_gamemode = Gamemode.VEGAS
            self.draw_amount = 3
            self.reset_score = False

    def print_current_settings(self):
        print(str.capitalize(self.active_gamemode.name + ' ruled applied.'))
        print('Draw ' + str(self.draw_amount) + ' cards.')
        print('Reset Score: ' + self.reset_score)
