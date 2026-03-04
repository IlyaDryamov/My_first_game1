from utils import randbool
from utils import randcell
from utils import randcell2
from clouds import Clouds




# 0 поле
# 1 дерево
# 2 река
# 3 госпитль
# 4 апгрейт шоп
# 5 огонь


CELL_TYPES = "🟩🌲🌊🏩🏰🔥"
TREE_BONUS = 100
UPGRADE_COST = 5000
LIFE_COST = 10000

class Map:

    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.cells = [[0 for i in range(w)] for j in range(h)]
        self.generate_forest(5,10)
        self.generate_river(15)
        self.generate_river(29)
        self.generate_upgrade_shop()
        self.generate_hospital()
        self.clouds = Clouds(w, h)

    def print_map(self, airp, clouds):
        print("⬛" * (self.w + 2))
        for ri in range(self.h):
            print("⬛", end="")
            for ci in range(self.w):
                cell = self.cells[ri][ci]
                if (clouds.cells[ri][ci] == 1):
                    print("💭", end="")
                elif (clouds.cells[ri][ci] == 2):
                    print("🌀", end="")
                elif (airp.x == ri and airp.y == ci):
                    print("🚁", end="")
                elif (cell >= 0 and cell < len(CELL_TYPES)):
                    print(CELL_TYPES[cell], end="")
            print("⬛")
        print("⬛" * (self.w + 2))

    def chek_bounds(self, x, y):
        if(x < 0 or y < 0 or x >= self.h or y >= self.w):
            return False
        return True
    
    def generate_forest(self, r, mxr):
        for ri in range(self.h):
            for ci in range(self.w):
                if randbool(r, mxr):
                    self.cells[ri][ci] = 1

    def generate_river(self, l):
        rc = randcell(self.w, self.h)
        rx, ry = rc[0], rc[1]
        self.cells[rx][ry] = 2
        while l > 0:
            rc2 = randcell2(rx, ry)
            rx2, ry2 = rc2[0], rc2[1]
            if (self.chek_bounds(rx2, ry2)):
                self.cells[rx2][ry2] = 2
                rx, ry = rx2, ry2
                l -= 1

    def generate_tree(self):
        c = randcell(self.w, self.h)
        cx, cy = c[0], c[1]
        if (self.cells[cx][cy] == 0):
            self.cells[cx][cy] = 1

    def generate_upgrade_shop(self):
        c = randcell(self.w, self.h)
        cx, cy = c[0], c[1]
        self.cells[cx][cy] = 4

    def generate_hospital(self):
        c = randcell(self.w, self.h)
        cx, cy = c[0], c[1]
        if self.cells[cx][cy] != 4:
            self.cells[cx][cy] = 3
        else:
            self.generate_hospital()

    def add_fire(self):
        c = randcell(self.w, self.h)
        cx, cy = c[0], c[1]
        if self.cells[cx][cy] == 1:
            self.cells[cx][cy] = 5
    
    def update_fires(self):
        for ri in range(self.h):
            for ci in range(self.w):
                cell = self.cells[ri][ci]
                if cell == 5:
                    self.cells[ri][ci] = 0
        for i in range(5):
            self.add_fire()

    def process_airplane(self, airp, clouds):
        c = self.cells[airp.x][airp.y]
        d = clouds.cells[airp.x][airp.y]
        if (c == 2):
            airp.tank = airp.mxtank
        if(c == 5 and airp.tank > 0):
            airp.tank -= 1
            airp.score += TREE_BONUS
            self.cells[airp.x][airp.y] = 1
        if(c == 4 and airp.score >= UPGRADE_COST):
            airp.mxtank += 1
            airp.score -= UPGRADE_COST
        if(c == 3 and airp.score >= LIFE_COST):
            airp.lives += 10
            airp.score -= LIFE_COST
        if (d == 2):
            airp.lives -= 1
            if airp.lives == 0:
                airp.game_over()
        
    def export_data(self):
        return {"cells": self.cells}
    
    def import_data(self, data):
        self.cells = data["cells"] or [[0 for i in range(self.w)] for j in range(self.h)]