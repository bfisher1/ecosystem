
TICKS_PER_DAY = 500 #ticks per day and night
DAYS_PER_SEASON = 30
DAYS_PER_YEAR = DAYS_PER_SEASON * 4
WINTER_SOLSTICE_TICKS_OF_DAYLIGHT = 150
SUMMER_SOLSTICE_TICKS_OF_DAYLIGHT = 350

WINTER_SOLSTICE = 0
SUMMER_SOLSTICE = int(DAYS_PER_YEAR / 2)

# year starts/ends winter solstice, summer solstice is DAYS_PER_YEAR / 2
def getTimeOfDayShouldBeCooling(dayOfYear):
    ticksOfDaylightRange = SUMMER_SOLSTICE_TICKS_OF_DAYLIGHT - WINTER_SOLSTICE_TICKS_OF_DAYLIGHT
    # should be WINTER_SOLSTICE_TICKS_OF_DAYLIGHT if winter solstice, SUMMER_SOLSTICE_TICKS_OF_DAYLIGHT if summer solstice
    timeOfDayTemperatureShouldBeginCooling = -abs((ticksOfDaylightRange / (SUMMER_SOLSTICE)) * dayOfYear - ticksOfDaylightRange) + SUMMER_SOLSTICE_TICKS_OF_DAYLIGHT
    return timeOfDayTemperatureShouldBeginCooling

def shouldHeatUpAtTimeOfDay(dayOfYear, tickOfDay):
    timeOfDayTemperatureShouldBeginCooling = getTimeOfDayShouldBeCooling(dayOfYear)
    return tickOfDay < timeOfDayTemperatureShouldBeginCooling

def timeOfDay(ticks):
    return ticks % TICKS_PER_DAY

def dayOfYear(ticks):
    totalDays = int(ticks / TICKS_PER_DAY)
    return totalDays % DAYS_PER_YEAR
