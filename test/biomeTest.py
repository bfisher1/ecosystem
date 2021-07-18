from biome import *
import worldTime

biome = PlainsBiome()
biome.dailyWarmingRate = 0.01
biome.dailyCoolingRate = 0.02

ticksAtSummerSolstice = worldTime.SUMMER_SOLSTICE * worldTime.TICKS_PER_DAY
for tick in range(ticksAtSummerSolstice, ticksAtSummerSolstice + worldTime.TICKS_PER_DAY * 3, 5):
    timeOfDay = worldTime.timeOfDay(tick)
    dayOfYear = worldTime.dayOfYear(tick)
    timeOfDayShouldBeCooling = worldTime.getTimeOfDayShouldBeCooling(dayOfYear)
    biome.updateTemperature(tick)
    print(' '.join([str(dayOfYear), str(timeOfDay), str(round(biome.temperature, 2)), str(timeOfDayShouldBeCooling), str(worldTime.shouldHeatUpAtTimeOfDay(dayOfYear, timeOfDay))]))
