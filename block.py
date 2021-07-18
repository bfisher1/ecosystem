from enum import Enum
import pygame
from plant import *
import random
from seed import *
from wind import Wind
from direction import *
from color import Color
from math import sqrt
import util

class BlockType(Enum):
    DIRT = 1
    WATER = 2
    SAND = 3
    HOLE = 4
    FOUNTAIN = 5

EVAPORATION_RATE = .1 #.01
# start raining once water in air hits this amount
CONDENSATION_AMOUNT = .7
PRECIPITATION_RATE = .2 #.05
WATER_FLOW_RATE = .2
SEED_IN_WATER_SPEED = .1

class FutureBlock:
    def __init__(self, block):
        self.waterInBlock = block.waterInBlock
        self.waterFloatingInAir = block.waterFloatingInAir
        self.waterFallingInAir = block.waterFallingInAir
        self.waterDirections = block.waterDirections

class Block:
    def __init__(self, world, x, y):
        self.world = world
        self.type = None
        self.color = None
        self.plants = []
        self.seeds = []
        self.x = x
        self.y = y
        # water level of 1 means block is fully saturated, 2 means that it is a full puddle
        self.waterInBlock = 0.0
        # how much water in air is floating from evaporation
        self.waterFloatingInAir = 0.0
        # how much water in air is raining
        self.waterFallingInAir = 0.0
        # 0 = freezing, 1.0 = burning, .6 = balmy
        self.temperatureInAir = 0.6
        # how much water will be blown into neighbor block at a time
        self.wind = Wind(0.01, Direction.RIGHT)
        self.elevation = 0.0
        self.waterDirections = []

    # call once block is fully constructed to create future block because now all values are set
    def initFuture(self):
        self.next = FutureBlock(self)

    def addPlant(self, plantType):
        plant = None
        if plantType == PlantType.OAK_TREE:
            plant = OakTree(block=self)
        elif plantType == PlantType.GRASS:
            plant = Grass(block=self)
        self.plants.append(plant)
        self.plants.sort(key=lambda plant: plant.z, reverse=False)

    def draw(self, x, y, screen, camera, font):
        # rect = pygame.Rect(self.getScreenLoc(camera), self.getScreenLoc(camera, offsetX=1, offsetY=1))
        # image = pygame.Surface((camera.scale, camera.scale))
        # image.fill(self.color)
        # screen.blit(image, rect)
        if self.waterInBlock > 0 and len(self.waterDirections) < 4:# and abs(self.next.waterInBlock - self.waterInBlock) > .1:
            # image.fill((0, 0, 255))
            waterWidth = camera.scale #min(camera.scale, camera.scale * self.waterInBlock)
            waterWidthNormalized = 0 * min(1.0, self.waterInBlock)
            #self.drawRect(self.getScreenLoc(camera, offsetX=waterWidthNormalized/4, offsetY=waterWidthNormalized/4), waterWidth, waterWidth, screen, Color.BLUE)
            if Direction.DOWN in self.waterDirections:
                self.drawRect(self.getScreenLoc(camera, offsetY=1), camera.scale, 2, screen, Color.NAVY)
            if Direction.UP in self.waterDirections:
                self.drawRect(self.getScreenLoc(camera), camera.scale, 2, screen, Color.NAVY)
            if Direction.LEFT in self.waterDirections:
                self.drawRect(self.getScreenLoc(camera), 2, camera.scale, screen, Color.NAVY)
            if Direction.RIGHT in self.waterDirections:
                self.drawRect(self.getScreenLoc(camera, offsetX=1), 2, camera.scale, screen, Color.NAVY)

        for plant in self.plants:
            plant.draw(x, y, screen, camera)

        for seed in self.seeds:
            seed.draw(x, y, screen, camera)

        if self.isRaining():
            self.drawRain(x, y, screen, camera)

        self.drawElevation(screen, camera, font)

    # todo move to graphics
    def createRect(self, loc, width, length, screen, color):
        x, y = loc
        rect = pygame.Rect((x, y), (x + width, y + length))
        image = pygame.Surface((width, length))
        image.fill(color)
        return image, rect

    def drawRect(self, loc, width, length, screen, color):
        image, rect = self.createRect(loc, width, length, screen, color)
        screen.blit(image, rect)

    def drawElevation(self, screen, camera, font):
        textsurface = font.render(str(round(self.waterInBlock, 1)), False, (255, 255, 255))
        screen.blit(textsurface, self.getScreenLoc(camera))

    def getScreenLoc(self, camera, offsetX=0, offsetY=0):
        return ((self.x + camera.x + offsetX) * camera.scale, (self.y + camera.y + offsetY) * camera.scale)

    def drawRain(self, x, y, screen, camera):
        radius = camera.scale / 16
        cerulean = (42, 82, 190)
        drift = ((self.world.ticks % 100) / 100) * .2
        pygame.draw.circle(screen, cerulean, ((x + 0.2 + camera.x) * camera.scale, (y + 0.2 + camera.y + drift) * camera.scale), radius)
        pygame.draw.circle(screen, cerulean, ((x + 0.2 + camera.x) * camera.scale, (y + 0.8 + camera.y + drift) * camera.scale), radius)
        pygame.draw.circle(screen, cerulean, ((x + 0.2 + camera.x) * camera.scale, (y + 0.8 + camera.y + drift) * camera.scale), radius)
        pygame.draw.circle(screen, cerulean, ((x + 0.8 + camera.x) * camera.scale, (y + 0.2 + camera.y + drift) * camera.scale), radius)
        pygame.draw.circle(screen, cerulean, ((x + 0.8 + camera.x) * camera.scale, (y + 0.8 + camera.y + drift) * camera.scale), radius)


    def containsGrass(self):
        for plant in self.plants:
            if plant.type == PlantType.GRASS:
                return True
        return False

    def addPlantIfNotHere(self, plant):
        for existingPlant in self.plants:
            if existingPlant.type == plant.type:
                return
        self.addPlant(plant)

    def spreadPlant(self, type):
        if type == PlantType.GRASS:
            self.addPlantIfNotHere(Grass())
        if type == PlantType.OAK_TREE:
            self.addSeed(OakSeed())

    def addSeed(self, seed):
        self.seeds.append(seed)

    def evaporate(self):
        waterEvaporated = min(self.temperatureInAir * EVAPORATION_RATE, self.waterInBlock)
        self.next.waterInBlock -= waterEvaporated
        self.next.waterFloatingInAir += waterEvaporated

    def rain(self):
        # todo, randomize this, maybe based on temp, day
        if self.waterFloatingInAir >= CONDENSATION_AMOUNT:
            self.next.waterFloatingInAir -= CONDENSATION_AMOUNT
            self.next.waterFallingInAir += CONDENSATION_AMOUNT

        if self.waterFallingInAir > 0:
            waterFallen = min(self.waterFallingInAir, PRECIPITATION_RATE)
            self.next.waterFallingInAir -= waterFallen
            self.next.waterInBlock += waterFallen

            if waterFallen <= 0.00001:
                self.next.waterFallingInAir = 0

    def isRaining(self):
        return self.waterFallingInAir > 0.1

    def blowWind(self):
        # make list of wind vectors external to blocks
        # over time, make these vectors move each other
        # eventually, randomly show up / fizzle out
        blockBlowingInto = self.getBlockInDirection(self.wind.direction)
        if blockBlowingInto != None:
            waterMovedFromFloating = min(self.wind.waterVelocity, self.waterFloatingInAir)
            waterMovedFromFalling = min(self.wind.waterVelocity, self.waterFallingInAir)
            blockBlowingInto.next.waterFloatingInAir += waterMovedFromFloating
            blockBlowingInto.next.waterFallingInAir += waterMovedFromFalling
            self.next.waterFloatingInAir -= waterMovedFromFloating
            self.next.waterFallingInAir -= waterMovedFromFalling

    def flowWater(self):
        blocksUnderElevation = []
        underElevationDirs = []
        blocksAtElevation = []
        atElevationDirs = []
        #todo, get directions better
        for direction in [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]:
            neighbor = self.getBlockInDirection(direction)
            if neighbor != None:
                if neighbor.elevation < self.elevation and neighbor.waterInBlock < 1:
                    blocksUnderElevation.append(neighbor)
                    underElevationDirs.append(direction)
                elif neighbor.elevation == self.elevation and neighbor.waterInBlock < 1:
                    blocksAtElevation.append(neighbor)
                    atElevationDirs.append(direction)
        blocksFlowingInto = []
        if len(blocksUnderElevation) == 0 and len(blocksAtElevation) > 0:
            blocksFlowingInto = blocksAtElevation
            self.waterDirections = atElevationDirs
        elif len(blocksUnderElevation) > 0:
            blocksFlowingInto = blocksUnderElevation
            self.waterDirections = underElevationDirs
        if len(blocksFlowingInto):
            waterFlowingFromSelf = min(WATER_FLOW_RATE, self.waterInBlock)
            waterPerBlock = waterFlowingFromSelf / len(blocksFlowingInto)
            for block in blocksFlowingInto:
                block.next.waterInBlock += waterPerBlock
            self.next.waterInBlock -= waterFlowingFromSelf

            for seed in self.seeds:
                dist = lambda b: sqrt((self.x + seed.offsetX - b.x) ** 2 + (self.y + seed.offsetY - b.y) ** 2)

                # move the seed towards the block it is closest to
                closestBlock = util.minList(blocksFlowingInto, dist)
                xDiff = ((closestBlock.x - self.x))
                yDiff = ((closestBlock.y - self.y))

                if xDiff != 0:
                    seed.offsetX += (xDiff / abs(xDiff)) * SEED_IN_WATER_SPEED
                if yDiff != 0:
                    seed.offsetY += (yDiff / abs(yDiff)) * SEED_IN_WATER_SPEED

    def runUpdates(self):
        self.waterInBlock = self.next.waterInBlock
        self.waterFloatingInAir = self.next.waterFloatingInAir
        self.waterFallingInAir = self.next.waterFallingInAir
        self.next = FutureBlock(self)


    def getBlockInDirection(self, direction):
        x, y = None, None
        if direction == Direction.UP:
            x, y = self.x, self.y - 1
        if direction == Direction.DOWN:
            x, y = self.x, self.y + 1
        if direction == Direction.LEFT:
            x, y = self.x - 1, self.y
        if direction == Direction.RIGHT:
            x, y = self.x + 1, self.y

        if 0 <= x and x < self.world.width and 0 <= y and y < self.world.height:
            return self.world.blocks[x][y]

        return None

    def growPlants(self):
        for plant in self.plants:
            plant.grow()

    def growSeeds(self):
        pass


class DirtBlock(Block):
    def __init__(self, world, x, y):
        super().__init__(world, x, y)
        self.type = BlockType.DIRT
        self.color = (96, 60, 40)
        self.waterSaturation = 1.0

    def withdrawWater(self, targetPercent):
        percentReturned = targetPercent * self.waterSaturation
        self.waterSaturation -= percentReturned
        return percentReturned

    # todo, base this off weather and off of plant height
    def getPercentSunShining(self, plant):
        return .5

class HoleBlock(Block):
    def __init__(self, world, x, y):
        super().__init__(world, x, y)
        self.type = BlockType.HOLE
        self.color = (0, 0, 0)
        self.waterSaturation = 0.0

    def flowWater(self):
        self.next.waterInBlock = 0.0

class Fountain(Block):
    def __init__(self, world, x, y):
        super().__init__(world, x, y)
        self.type = BlockType.FOUNTAIN
        self.color = (255, 255, 255)
        self.waterSaturation = 1.0

    def flowWater(self):
        self.next.waterInBlock += .1
        super().flowWater()

class SandBlock(Block):
    def __init__(self, world, x, y):
        super().__init__(world, x, y)
        self.type = BlockType.SAND
        self.color = (239, 228, 176)
