import random

import worldTime

class BiomeType:
    DESERT = 0
    BEACH = 1
    MOUNTAIN = 2
    FOREST = 3
    PLAINS = 4

BIOME_SIZE = 100
BIOMES = {}

class Biome:
    def __init__(self):
        # total water above all blocks
        self.waterInAir = 0.0
        # change through day
        self.temperature = 0.0
        self.type = None
        # how much the temperature will vary from average on a day
        self.dailyTemperatureOffsetVariation = (-0.1, 0.1)
        # this increments / decrements per day, must stay within tempOffsetVariation range
        # this way, get periods of warmer / colder weather
        self.dailyTemperatureOffset = 0.0
        # daily temperature goes along this range on average
        self.dailyBaseTemperatureRange = (0.0, 1.0)
        # how fast the world gets hot during the day
        self.dailyWarmingRate = 0.1
        # how fast the world gets cool during the day
        self.dailyCoolingRate = 0.1
        self.dailyTemperatureFactorsLastUpdated = 0

    def updateDailyTemperatureFactors(self, ticks):
        # todo, update base range by dayOfYear
        minVar, maxVar = self.dailyTemperatureOffsetVariation
        self.dailyTemperatureOffset = random.uniform(minVar, maxVar)
        pass

    def updateTemperature(self, ticks):
        if ticks - self.dailyTemperatureFactorsLastUpdated:
            self.dailyTemperatureFactorsLastUpdated = ticks
            self.updateDailyTemperatureFactors(ticks)
        timeOfDay = worldTime.timeOfDay(ticks)
        dayOfYear = worldTime.dayOfYear(ticks)
        if worldTime.shouldHeatUpAtTimeOfDay(dayOfYear, timeOfDay):
            #heat up
            maxTemp = self.dailyBaseTemperatureRange[1] + self.dailyTemperatureOffset
            goalTemp = self.temperature + self.dailyWarmingRate
            self.temperature = min(goalTemp, maxTemp)
        else:
            # cool down
            minTemp = self.dailyBaseTemperatureRange[0] + self.dailyTemperatureOffset
            goalTemp = self.temperature - self.dailyCoolingRate
            self.temperature = max(goalTemp, minTemp)

class PlainsBiome(Biome):
    def __init__(self):
        super().__init__()
        self.type = BiomeType.PLAINS
        self.waterInAir = BIOME_SIZE * BIOME_SIZE * 0.3
        self.temperature = 0.65
        self.temperatureOffsetVariation = (-0.05, 0.05)




# todo, return biome based off of perlin
def getBiomeAt(x, y):
    biomeX = int(x / BIOME_SIZE)
    biomeY = int(y / BIOME_SIZE)

    if biomeX not in BIOMES:
        BIOMES[biomeX] = {}
    if biomeY not in BIOMES[biomeX]:
        BIOMES[biomeX][biomeY] = PlainsBiome()
