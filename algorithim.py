from array import *
import math

FAMILIES_NUMBER = 4

def MBTIconverter(MBTI):
    """
    Convert the MBTI into a 2D coordiates

    Args:
        MBTI (4 letter string)

    Returns:
        [float, float]: A 2d coordinates of the MBTI
    """

    if (MBTI[0] == 'I'):
        y = 1
    else:
        y = -1

    if (MBTI[1] == 'N'):
        x = 1
    else:
        x = -1

    if (MBTI[2] == 'T'):
        x *= 2

    if (MBTI[3] == 'J'):
        y *= 2

    return [x, y]

def priority(MBTI, families):
    """
    Determine the priority of which family the member of the provided MBTI should join first

    Args:
        MBTI (4 letter string)
        families (list of [float, float]): A list of families containing a list of its own members' MBTI 2D coordiantes

    Returns:
        String[]: A reordered String list with names of the families
    """

    coordiante = MBTIconverter(MBTI)        # The 2d coordinates of the provided MBTI
    distance = []                           # A empty list to store the distance change
    priority = ['f1', 'f2', 'f3', 'f4']     # A default priority String list 
    
    for i in families:
        # Calculate the distance change between the average coordiantes of the members' MBTI 
        # and the origin (0, 0) before and after adding the new member
        x = 0
        y = 0
        people = 0

        for j in i:
            x += j[0]
            y += j[1]
            people += 1
        before_distance = math.sqrt((x / people) ** 2 + (y / people) ** 2)

        x += coordiante[0]
        y += coordiante[1]
        people += 1
        after_distance = math.sqrt((x / people) ** 2 + (y / people) ** 2)

        distance.append(before_distance-after_distance)

    # Sort the list in descending order with bubble sort and switch the priority
    for i in range(FAMILIES_NUMBER):
        # Last i elements are already in place
        for j in range(0, FAMILIES_NUMBER - i - 1):
            if distance[j] < distance[j+1]:
                # Swap the numbers
                distance[j], distance[j+1] = distance[j+1], distance[j]
                priority[j], priority[j+1] = priority[j+1], priority[j]

    return priority

def selection(MBTI, families, space):
    order = priority(MBTI, families)
    for i in order:
        if (i == 'f1'):
            if (space[0] != 0):
                space[0] -= 1
        elif (i == 'f2'):
            if (space[1] != 0):
                space[1] -= 1
        elif (i == 'f3'):
            if (space[2] != 0):
                space[2] -= 1
        elif (i == 'f4'):
            if (space[3] != 0):
                space[3] -= 1
        return i
    return 'ERROR'