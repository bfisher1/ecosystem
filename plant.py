import random

import pygame
from enum import Enum
import time
import random
from direction import Direction



class PlantType:
    OAK_TREE = 1
    FERN = 2
    GRASS = 3


class Plant:
    def __init__(self, block, offsetX, offsetY):
        self.block = block
        self.type = None
        # offset in the block. should be between -1 and 1
        self.offsetX = offsetX
        self.offsetY = offsetY
        self.z = 1
        self.created = self.block.world.ticks

    def draw(self, x, y, screen, blockSize):
        pass


class OakTree(Plant):
    def __init__(self, block=None, offsetX=.5, offsetY=.5):
        super().__init__(block, offsetX, offsetY)
        self.type = PlantType.OAK_TREE
        # once this hits 1
        self.seedEnergy = 0

    def draw(self, x, y, screen, camera):
        width = min((self.block.world.ticks - self.created) / 100, .85)
        radius = int((camera.scale / 4) * width)
        pygame.draw.circle(screen, (96, 60, 40),
                           ((x + self.offsetX + camera.x) * camera.scale, (y + self.offsetY + camera.y) * camera.scale),
                           radius)

        left = ((x + self.offsetX + camera.x - .5 * width) * camera.scale, (y + self.offsetY + camera.y) * camera.scale)
        top = ((x + self.offsetX + camera.x) * camera.scale, (y + self.offsetY + camera.y - width) * camera.scale)
        right = (
        (x + self.offsetX + camera.x + .5 * width) * camera.scale, (y + self.offsetY + camera.y) * camera.scale)
        pygame.draw.polygon(screen, (0, 255, 0), [left, top, right])
        pygame.draw.polygon(screen, (0, 0, 0), [left, top, right], 2)

    def dropSeed(self):
        direction = random.choice(Direction.all)
        neighbor = self.block.getBlockInDirection(direction)
        if neighbor != None:
            from seed import OakSeed
            neighbor.addSeed(OakSeed(offsetX=random.random(), offsetY=random.random()))

    def grow(self):
        # todo, base off sun and water / temp
        self.seedEnergy += .1
        if self.seedEnergy >= 1:
            self.seedEnergy -= 1
            self.dropSeed()


class Grass(Plant):
    def __init__(self, block=None, offsetX=.5, offsetY=.5):
        super().__init__(block, offsetX, offsetY)
        self.type = PlantType.GRASS
        self.z = 0

    def draw(self, x, y, screen, camera):
        rect = pygame.Rect(((x + camera.x) * camera.scale, (y + camera.y) * camera.scale),
                           ((x + 1 + camera.x) * camera.scale, (y + 1 + camera.y) * camera.scale))
        image = pygame.Surface((camera.scale, camera.scale))
        image.fill((0, 255, 0))
        screen.blit(image, rect)

    def grow(self):
        pass

    """
    Spread to block x,y away if not there
    """

    def spread(self, x, y):
        neighbor = self.block.world.blocks[self.block.x + x][self.block.y + y]
        if not neighbor.containsGrass():
            neighbor.addPlant(Grass())
