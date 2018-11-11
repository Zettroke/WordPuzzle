__author__ = 'Olleggerr'
import math
import random
from os.path import join
listletters = []
listcoord = []
abc = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']

base_dir = '.'


def serch(obj, array):
    for val in array:
        if val.x == obj.x and val.y == obj.y:
            return True
    return False


class Letter:
    x = -1
    y = -1
    char = ""

    def __init__(self, x, y, char=None):
        self.x = x
        self.y = y
        self.char = char


def start(words, hard):
    listletters.clear()
    listcoord.clear()
    freeletters = []
    amountS = 0
    for val in words:
        amountS += len(val)
    sqside = int(math.sqrt(amountS*hard))*50

    def generate():
        sides = ["up", "down", "left", "right"]
        for i in range(len(words)):
            count = 0
            bl = True
            while bl:
                xcurr = int(random.randint(0, sqside/50)*50)
                ycurr = int(random.randint(0, sqside/50)*50)
                if xcurr < sqside and ycurr < sqside:
                    bl = serch(Letter(xcurr, ycurr), listletters)
            listletters.append(Letter(xcurr, ycurr, words[i][0]))
            xrnd = xcurr
            yrnd = ycurr

            for val in words[i][1:len(words[i])]:

                while True:
                    move = sides[random.randint(0, 3)]
                    tempxrnd = xrnd
                    tempyrnd = yrnd
                    if move == "up":
                        yrnd += 50
                    elif move == "down":
                        yrnd -= 50
                    elif move == "left":
                        xrnd -= 50
                    elif move == "right":
                        xrnd += 50
                    templetter = Letter(xrnd, yrnd, val)
                    if not serch(templetter, listletters) and xrnd >= 0 and yrnd >= 0 and yrnd < sqside and xrnd < sqside:
                        listletters.append(templetter)
                        break
                    elif count <= 50:
                        xrnd = tempxrnd
                        yrnd = tempyrnd
                        count += 1
                    else:
                        listletters.clear()
                        return False
        return True
    bl = False
    count_try = 0
    while not bl:

        bl = generate()
        count_try += 1
    for x in range(0, sqside, 50):
        for y in range(0, sqside, 50):
            temp = Letter(x, y)
            if not serch(temp, listletters):
                freeletters.append(temp)


    max = math.ceil(len(freeletters)/3)
    min = math.ceil(len(freeletters)/12)
    num = random.randint(min, max//2)
    lenght = math.ceil(len(freeletters)/num)
    l = []
    for i in range(num):
        l.append(lenght)
    while sum(l) != len(freeletters):
        if sum(l) > len(freeletters):
            i = random.randint(0,len(l)-1)
            if l[i] <= 3:
                continue
            else:
                l[i] -= 1
        else:
            i = random.randint(0,len(l)-1)
            if l[i] >= 12:
                continue
            else:
                l[i] += 1
    for i in range(10):
        i1 = random.randint(0, len(l)-1)
        i2 = random.randint(0, len(l)-1)
        if 3 < l[i1] < 12 and 3 < l[i2] < 12:
            l[i1] += 1
            l[i2] -= 1
        else:
            continue
    words = open(join(base_dir, 'datasorted.dat'), 'r', encoding="utf-8").read().split()
    ranges = []
    nums = []
    z = 0
    for i in range(len(words)):
        if len(words[i]) > z:
            z = len(words[i])
            nums.append(z)
            ranges.append(i)
    ranges.append(len(words)-1)
    bonuswords = []
    for i in l:
        bonuswords.append(words[random.randint(ranges[i-3], ranges[i-2])])
    lenwords = 0
    for i in bonuswords:
        lenwords += len(i)
    for i in bonuswords:
        for val in i:
            i1 = random.randint(0, len(freeletters)-1)
            freeletters[i1].char = val
            listletters.append(freeletters[i1])
            freeletters.remove(freeletters[i1])
            '''freeletters[counter].char = val
            listletters.append(freeletters[counter])
            counter += 1'''

    return (listletters, bonuswords)


def getborder(words, hard):
    amountS = 0
    for val in words:
        amountS += len(val)
    sqside = int(math.sqrt(amountS*hard))
    return sqside

