import random
import pygame
import time
from plant import PlantType

class Seed:
    def __init__(self, block, offsetX, offsetY):
        self.block = block
        self.type = None
        # offset in the block. should be between -1 and 1
        self.offsetX = offsetX
        self.offsetY = offsetY
        self.z = 1
        # once this hits 0, create baby tree
        self.amountGrown = 0.0
        self.dailyWaterConsumed = 0.01
        self.dailySunPercentConsumed = 0.5
        # this can vary by plant
        self.growthFactors = {'water': .5, 'sun': .5}
        # if these fall above amount, start wilting, at 0.0 die
        self.sunNeed = 1.0
        self.waterNeed = 1.0
        self.notBurnedNeed = 1.0
        self.notColdNeed = 1.0
        # how quickly does entire need level match need provided (i.e., if I water plant 50%, how many days until need is at 50%)
        self.needAdjustRate = 0.1
        # percent grown a day if all growth factors are followed
        self.growthRate = 0.1

    def growForDay(self):
        # normalized amounts, percent consumed during the day
        percentWatered = self.block.withdrawWater(self.dailyWaterConsumed) / self.dailyWaterConsumed
        percentSun = self.block.getPercentSunShining(self) / self.dailySunPercentConsumed

        self.waterNeed = percentWatered * self.needAdjustRate - self.needAdjustRate
        self.sunNeed = percentSun * self.needAdjustRate - self.needAdjustRate

        self.amountGrown += (percentWatered * self.growthFactors['water'] + percentSun * self.growthFactors['sun']) * self.growthRate


class OakSeed(Seed):
    def __init__(self, block=None, offsetX=.5, offsetY=.5):
        super().__init__(block, offsetX, offsetY)
        self.type = PlantType.OAK_TREE
        self.created = time.time()

    def draw(self, x, y, screen, camera):
        radius = int(camera.scale / 16)
        pygame.draw.circle(screen, (0, 0, 0), ((x + self.offsetX + camera.x) * camera.scale, (y + self.offsetY + camera.y) * camera.scale), radius)
