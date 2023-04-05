from .tower import Tower


class Player:
    def __init__(self, tower: Tower):
        self.money = 100
        self.tower = tower

    def get_money(self, m):
        self.money += m

    def take_money(self, m):
        self.money -= m

    def set_tower(self, new):
        self.tower = new

    def show_info(self):
        return self.tower.show_info()