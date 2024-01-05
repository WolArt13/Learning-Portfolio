#Имортируем библиотеку mcpi и связываемся с локальным сервером
from mcpi.minecraft import Minecraft
mc = Minecraft.create()
#Импортируем функцию sleep из библиотеки time
from time import sleep
import keyboard
#Список блоков запрещенных для движения по ним
bannedblocks = [9, 11, 10, 8]
allowedblocks = [6, 31, 32, 37, 38, 39, 40, 59, 51, 81, 104, 105, 106, 115, 141, 175, 142]
#Обьявляем начальные координаты появления блока на позиции игрока
x, y, z = mc.player.getTilePos()
#Обьявляем переменную для проверки высоты после каждого изменения x, y
y = mc.getHeight(x, z)
#Устанавливаем блок на начальную позицию
mc.setBlock(x, y, z, 91, 3)

#Класс с функциями для проверки окружения по разным сторонам
class checkblockaround:
    #Проверка 3 блоков спереди(вверх, вперед, вниз)
    def checkforward(x, y, z):
        """Вывод id блока перед блоком(вперед, вверх, вниз)"""
        forward = mc.getBlock(x + 1, y, z)
        fup = mc.getBlock(x + 1, y + 1, z)
        fdown = mc.getBlock(x + 1, y - 1, z)
        return forward, fup, fdown
    #Проверка 3 блоков справа(вверх, вперед, вниз)
    def checkright(x, y, z):
        """Вывод id блока справа от блока(вперед, вверх, вниз)"""
        right = mc.getBlock(x, y, z + 1)
        rup = mc.getBlock(x, y + 1, z + 1)
        rdown = mc.getBlock(x, y - 1, z + 1)
        return right, rup, rdown
    #Проверка 3 блоков слева(вверх, вперед, вниз)
    def checkleft(x, y, z):
        """Вывод id блока слева от блока(вперед, вверх, вниз)"""
        left = mc.getBlock(x, y, z - 1)
        lup = mc.getBlock(x, y + 1, z - 1)
        ldown = mc.getBlock(x, y - 1, z - 1)
        return left, lup, ldown
    #Проверка 3 блоков сзади(вверх, вперед, вниз)
    def checkbackward(x, y, z):
        """Вывод id блока сзади от блока(вперед, вверх, вниз)"""
        backward = mc.getBlock(x - 1, y, z)
        bup = mc.getBlock(x - 1, y + 1, z)
        bdown = mc.getBlock(x - 1, y - 1, z)
        return backward, bup, bdown
#Проверка разной высоты по разным сторонам
class checkhight:
    def forward(x, y, z):
        """Вывод id блока спереди от блока(вперед, (вверх, вниз) - на 1, 2 блока)"""
        wforw = mc.getBlock(x + 1, y, z)
        wcup = mc.getBlock(x + 1, y + 1, z)
        wcupup = mc.getBlock(x, y + 1, z)
        wcdown = mc.getBlock(x + 1, y - 2, z)
        wcdown2 = mc.getBlock(x + 1, y - 1, z)
        return wforw, wcup, wcupup, wcdown, wcdown2
    def right(x, y, z):
        """Вывод id блока справа от блока(вперед, (вверх, вниз) - на 1, 2 блока)"""
        rforw = mc.getBlock(x, y, z + 1)
        rcup = mc.getBlock(x, y + 1, z + 1)
        rcupup = mc.getBlock(x, y + 1, z)
        rcdown = mc.getBlock(x, y - 2, z + 1)
        rcdown2 = mc.getBlock(x, y - 1, z + 1)
        return rforw, rcup, rcupup, rcdown, rcdown2
    def left(x, y, z):
        """Вывод id блока слева от блока(вперед, (вверх, вниз) - на 1, 2 блока)"""
        lforw = mc.getBlock(x, y, z - 1)
        lcup = mc.getBlock(x, y + 1, z - 1)
        lcupup = mc.getBlock(x, y + 1, z)
        lcdown = mc.getBlock(x, y - 2, z - 1)
        lcdown2 = mc.getBlock(x, y - 1, z - 1)
        return lforw, lcup, lcupup, lcdown, lcdown2
    def backward(x, y, z):
        """Вывод id блока сзади от блока(вперед, (вверх, вниз) - на 1, 2 блока)"""
        bforw = mc.getBlock(x - 1, y, z)
        bcup = mc.getBlock(x - 1, y + 1, z)
        bcupup = mc.getBlock(x, y + 1, z)
        bcdown = mc.getBlock(x - 1, y - 2, z)
        bcdown2 = mc.getBlock(x - 1, y - 1, z)
        return bforw, bcup, bcupup, bcdown, bcdown2
#Движение блока
class movement:
    #Движение вперед
    def forward():
        #Обьявляем координаты x, y, z глобально для доступа к ним в функции
        global x, y, z
        #Обьявляем в переменные результаты проверки высоты спереди
        wforw, wcup, wcupup, wdown, wdown2 = checkhight.forward(x, y, z)
        #Перемещаем вперед если нет жидкости, стены или пропасти
        if not any(block in bannedblocks for block in checkblockaround.checkforward(x, y, z)) and (wcup == 0 or wcup in allowedblocks) and (wdown == 0 and wforw == 0 and wdown2 != 0) or (wdown2 == 0 and wdown != 0) or (wforw != 0 and wdown2 == 0) or (wdown2 != 0 and wforw == 0 and wcup != 0) or (wdown2 != 0 and wforw != 0 and wcup == 0) or wdown != 0:
            #Если впереди 1 блок то забираемся на него
            if wforw != 0 and (not wforw in allowedblocks or wcup in allowedblocks and wcup != 175) and wcupup == 0:
                mc.setBlock(x, y, z, 0)
                mc.setBlock(x + 1, y + 1, z, 91, 3)
                x += 1
                y +=1
            #Если внизу нет 1 блока то спускаемся вниз
            elif wdown2 == 0 or wdown2 in allowedblocks and (not wdown in allowedblocks):
                mc.setBlock(x, y, z, 0)
                mc.setBlock(x + 1, y - 1, z, 91, 3)
                x += 1
                y -= 1
            #Если выше условия не True, просто идем вперед
            else:
                mc.setBlock(x, y, z, 0)
                mc.setBlock(x + 1, y, z, 91, 3)
                x += 1
            return True
        else: 
            return False
    #Движение вправо
    def right():
        #Обьявляем координаты x, y, z глобально для доступа к ним в функции
        global x, y, z 
        #Обьявляем в переменные результаты проверки высоты справа
        rforw, rcup, rcupup, rdown, rdown2 = checkhight.right(x, y, z)
        if not any(block in bannedblocks for block in checkblockaround.checkright(x, y, z)) and (rcup == 0 or rcup in allowedblocks) and (rdown == 0 and rforw == 0 and rdown2 != 0) or (rdown2 == 0 and rdown != 0) or (rforw != 0 and rdown2 == 0) or (rdown2 != 0 and rforw == 0 and rcup != 0) or (rdown2 != 0 and rforw != 0 and rcup == 0) or rdown != 0:
            #Если впереди 1 блок то забираемся на него
            if rforw != 0 and (not rforw in allowedblocks or rcup in allowedblocks and rcup != 175) and rcupup == 0:
                mc.setBlock(x, y, z, 0)
                mc.setBlock(x, y + 1, z + 1, 91, 4)
                z += 1
                y +=1
            #Если внизу нет 1 блока то спускаемся вниз
            elif rdown2 == 0 or rdown2 in allowedblocks and not rdown in allowedblocks and rforw == 0:
                mc.setBlock(x, y, z, 0)
                mc.setBlock(x, y - 1, z + 1, 91, 4)
                z += 1
                y -= 1
            #Если выше условия не True, просто идем вперед
            else:
                mc.setBlock(x, y, z, 0)
                mc.setBlock(x, y, z + 1, 91, 4)
                z += 1
            return True
        else:
            return False
    #Движение влево
    def left():
        #Обьявляем координаты x, y, z глобально для доступа к ним в функции
        global x, y, z
        #Обьявляем в переменные результаты проверки высоты слева
        lforw, lcup, lcupup, ldown, ldown2 = checkhight.left(x, y, z)
        if not any(block in bannedblocks for block in checkblockaround.checkleft(x, y, z)) and (lcup == 0 or lcup in allowedblocks) and (ldown == 0 and lforw == 0 and ldown2 != 0) or (ldown2 == 0 and ldown != 0) or (lforw != 0 and ldown2 == 0) or (ldown2 != 0 and lforw == 0 and lcup != 0) or (ldown2 != 0 and lforw != 0 and lcup == 0) or ldown != 0:
            #Если впереди 1 блок то забираемся на него
            if lforw != 0 and (not lforw in allowedblocks or lcup in allowedblocks and lcup != 175) and lcupup == 0:
                mc.setBlock(x, y, z, 0)
                mc.setBlock(x, y + 1, z - 1, 91, 2)
                z -= 1
                y +=1
            #Если внизу нет 1 блока то спускаемся вниз
            elif ldown2 == 0 or ldown2 in allowedblocks and not ldown in allowedblocks and lforw == 0:
                mc.setBlock(x, y, z, 0)
                mc.setBlock(x, y - 1, z - 1, 91, 2)
                z -= 1
                y -= 1
            #Если выше условия не True, просто идем вперед
            else:
                mc.setBlock(x, y, z, 0)
                mc.setBlock(x, y, z - 1, 91, 2)
                z -= 1
            return True
        else:
            return False
    #Движение назад
    def backward():
        #Обьявляем координаты x, y, z глобально для доступа к ним в функции
        global x, y, z
        #Обьявляем в переменные результаты проверки высоты сзади
        bforw, bcup, bcupup, bdown, bdown2 = checkhight.backward(x, y, z)
        if not any(block in bannedblocks for block in checkblockaround.checkbackward(x, y, z)) and (bcup == 0 or bcup in allowedblocks) and (bdown == 0 and bforw == 0 and bdown2 != 0) or (bdown2 == 0 and bdown != 0) or (bforw != 0 and bdown2 == 0) or (bdown2 != 0 and bforw == 0 and bcup != 0) or (bdown2 != 0 and bforw != 0 and bcup == 0) or bdown != 0:
            #Если впереди 1 блок то забираемся на него
            if bforw != 0 and (not bforw in allowedblocks or bcup in allowedblocks and bcup != 175) and bcupup == 0:
                mc.setBlock(x, y, z, 0)
                mc.setBlock(x - 1, y + 1, z, 91, 1)
                x -= 1
                y +=1
            #Если внизу нет 1 блока то спускаемся вниз
            elif bdown2 == 0 or bdown2 in allowedblocks and not bdown in allowedblocks and bforw == 0:
                mc.setBlock(x, y, z, 0)
                mc.setBlock(x - 1, y - 1, z, 91, 1)
                x -= 1
                y -= 1
            #Если выше условия не True, просто идем вперед
            else:
                mc.setBlock(x, y, z, 0)
                mc.setBlock(x - 1, y, z, 91, 1)
                x -= 1
            return True
        else:
            return False

while True:
    if keyboard.is_pressed('i'):
        movement.forward()
        mc.postToChat(mc.getBlock(x + 1, y, z))
    elif keyboard.is_pressed('j'):
        movement.left()
        mc.postToChat(mc.getBlock(x, y, z - 1))
    elif keyboard.is_pressed('k'):
        movement.backward()
        mc.postToChat(mc.getBlock(x - 1, y, z))
    elif keyboard.is_pressed('l'):
        movement.right()
        mc.postToChat(mc.getBlock(x, y, z + 1))