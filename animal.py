class Animal:
    def __init__(self, x, y, display):
        self.x = x
        self.y = y
        self.display = display

    def move(self, deltaX, deltaY):
        self.x += deltaX
        self.y += deltaY