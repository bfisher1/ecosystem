def minList(list, eval):
    minVal = None
    minElement = None
    for element in list:
        val = eval(element)
        if minVal == None or minVal < val:
            minVal = val
            minElement = element
    return minElement
