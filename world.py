from os import system
from loc import Loc
from block import *
from plant import *
import random
import pygame
import perlin


class BlockMap:
    def __init__(self):
        self.columns = {}

    def __getitem__(self, x):
        if x not in self.columns:
            self.columns[x] = {}
        return self.columns[x]

    def __setitem__(self, x, value):
        if x not in self.columns:
            self.columns[x] = {}
        self.columns[x] = {}


class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.animals = []
        self.blocks = BlockMap()
        self.ticks = 0
        self.populateBlocks()

    def addAnimal(self, animal):
        self.animals.append(animal)

    def populateBlocks(self):
        # todo, improve with perlin and on the fly loading
        for x in range(self.width):
            for y in range(self.height):
                elevation = perlin.value(x, y, 0.2, 1, 6)
                if elevation < .2:
                    self.blocks[x][y] = HoleBlock(self, x, y)
                elif elevation > .7:
                    self.blocks[x][y] = Fountain(self, x, y)
                else:
                    self.blocks[x][y] = DirtBlock(self, x, y)

                if random.random() > .5:
                    self.blocks[x][y].waterInBlock = 0.0
                else:
                    self.blocks[x][y].waterInBlock = 2.0
                # todo, use perlin to populate block elevations
                self.blocks[x][y].elevation = elevation

        self.blocks[5][5].addPlant(PlantType.OAK_TREE)
        self.blocks[5][5].addPlant(PlantType.GRASS)
        self.blocks[5][6].addPlant(PlantType.GRASS)
        self.blocks[7][6].addPlant(PlantType.GRASS)

        for x in range(self.width):
            for y in range(self.height):
                self.blocks[x][y].initFuture()

    def drawBlock(self, x, y, screen, camera, font):
        self.blocks[x][y].draw(x, y, screen, camera, font)

    def blockAt(self, x, y):
        return y in self.blocks[x]

    def tick(self):
        self.ticks += 1

    def spreadPlant(self, type, spreadOdds=.1):
        blocks = []
        for x in range(self.width):
            for y in range(self.height):
                if self.blocks[x][y].containsGrass():
                    if self.blockAt(x, y + 1) and random.random() < spreadOdds:
                        blocks.append(self.blocks[x][y + 1])
                    if self.blockAt(x + 1, y) and random.random() < spreadOdds:
                        blocks.append(self.blocks[x + 1][y])
                    if self.blockAt(x, y - 1) and random.random() < spreadOdds:
                        blocks.append(self.blocks[x][y - 1])
                    if self.blockAt(x - 1, y) and random.random() < spreadOdds:
                        blocks.append(self.blocks[x - 1][y])
        for block in blocks:
            if block.type == BlockType.DIRT:
                block.spreadPlant(type)

    def update(self):
        if (self.ticks % 5 == 0):
            for x in range(self.width):
                for y in range(self.height):
                    #self.blocks[x][y].evaporate()
                    #self.blocks[x][y].rain()
                    self.blocks[x][y].flowWater()
                    self.blocks[x][y].blowWind()
                    self.blocks[x][y].growPlants()
                    self.blocks[x][y].growSeeds()
                    self.blocks[x][y].runUpdates()





