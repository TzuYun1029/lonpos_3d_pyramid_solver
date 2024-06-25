import sys
import pygame
from pygame.locals import *
import pygame_gui
from pygame_gui.core import ObjectID

import find_ans

brick_name_color_dict = {
    'F': [255, 255, 255],
    'K': [83, 255, 31],
    'A': [255, 91, 3],
    'J': [150, 0, 224],
    'L': [145, 145, 145],
    'G': [43, 220, 255],
    'H': [255, 105, 212],
    'C': [0, 28, 189],
    'E': [0, 94, 31],
    'I': [255, 244, 41],
    'D': [255, 215, 196],
    'B': [237, 12, 12],
    '.': [173, 173, 173, 50],
}

# Initialize GUI interface

pygame.init()
window_size = (1000, 700)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('Lonpos Pyramid Answer Generator')
manager = pygame_gui.UIManager(window_size, 'theme.json')
text_font = pygame.font.SysFont("Arial", 30)

background = pygame.Surface(window_size)
background.fill(pygame.Color('#FFFFFF'))
screen.blit(background, (0, 0))

quesButton = []
pickColorButton = []

targetQues = 0

pickedColor = ""

Dots = []

# Initial buttons
for i in range(len(find_ans.ques_list)):
    quesButton.append(pygame_gui.elements.UIButton(relative_rect=pygame.Rect((150 + (i % 4) * 50 + (i//4)*25, 275 + (i//4)*50), (40, 40)),
                                                   text=str(i+1),
                                                   manager=manager))
count = 0
for c in brick_name_color_dict.keys():
    if c != '.':
        b = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((500 + 60 * (count//6), 20 + 60 * (count % 6)), (50, 50)),
                                         text=c,
                                         manager=manager,
                                         object_id=ObjectID(object_id='#'+c))

        pickColorButton.append(b)
        count += 1

create_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((150, 440), (200, 50)),
                                             text='Input Question',
                                             manager=manager)

hint_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((150, 520), (200, 50)),
                                           text='Hint',
                                           manager=manager)

ans_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((150, 600), (200, 50)),
                                          text='Answer',
                                          manager=manager)

prev_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((510, 625), (100, 50)),
                                           text='< prev',
                                           manager=manager)
next_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((865, 625), (100, 50)),
                                           text='next >',
                                           manager=manager)


def drawText(text, font, textColor, x, y):
    global screen

    img = font.render(text, True, textColor)
    screen.blit(img, img.get_rect(center=(x, y)))


def drawLayer(layer, add, brickArr):
    global screen, text_font, brick_name_color_dict, Dots

    idx = layer**2
    offset = (layer-1)/2

    for ctr in range(idx):
        r = 15 * (1+(ctr//layer)*0.1) + 2
        x = 740 + (ctr % layer - offset) * (2*r-1)
        y = (150 * layer - 247) + (1 + (ctr//layer - offset)
                                   * 0.75) * (r+10) + ((5 - layer) ** 2) * 10

        if brickArr[ctr+add] != '.':
            dot0 = pygame.draw.circle(screen, (0, 0, 0), (x, y), r+1)
            dot = pygame.draw.circle(
                screen, brick_name_color_dict[brickArr[ctr+add]], (x, y), 15 * (1+(ctr//layer)*0.1))
            drawText(brickArr[ctr+add], text_font, (0, 0, 0), x, y)

        else:
            dot0 = pygame.draw.circle(
                screen, brick_name_color_dict[brickArr[ctr+add]], (x, y), r+1, 2)

        Dots.append(dot0)  # record all Dots pos


def drawAns(brickArr):
    global Dots
    add = 0
    Dots = []
    for layer in range(5, 0, -1):
        drawLayer(layer, add, brickArr)
        add += (layer**2)


def setUpLayout(brickArr, hintText):
    global screen, manager, background, curStatus, foundAns, notFinal, notFirst, pickedColor

    screen.blit(background, (0, 0))
    manager.draw_ui(screen)
    pygame.draw.rect(screen, (73, 73, 73), [490, 10, 495, 680], 5)
    titleFont = pygame.font.SysFont('microsoftjhengheiui', 50)
    drawText('Lonpos Pyramid', titleFont, (0, 0, 0), 250, 75)
    titleFont = pygame.font.SysFont('microsoftjhengheiui', 30)
    drawText('Answer Generator', titleFont, (0, 0, 0), 250, 150)
    titleFont = pygame.font.SysFont('microsoftjhengheiui', 20)
    drawText(hintText, titleFont, (0, 0, 0), 250, 220)

    drawAns(brickArr)

    # check buttons visibility
    prev_button.visible = (curStatus == 'hint' and foundAns and notFirst)
    next_button.visible = (curStatus == 'hint' and foundAns and notFinal)

    for b in pickColorButton:
        b.visible = (curStatus == 'create')

    if curStatus == 'create':
        titleFont = pygame.font.SysFont('microsoftjhengheiui', 15)
        img = titleFont.render('Picked color: ', True, (0, 0, 0))
        screen.blit(img, (500, 400))

        if pickedColor != "":
            pygame.draw.rect(screen, brick_name_color_dict[pickedColor], [
                             590, 400, 30, 30])
            pygame.draw.rect(screen, [0, 0, 0], [590, 400, 30, 30], 2)

    manager.draw_ui(screen)


def printResult(att, che, elap):
    titleFont = pygame.font.SysFont('microsoftjhengheiui', 20)
    img = titleFont.render('Total attempts: ' + str(att), True, (0, 0, 0))
    screen.blit(img, (510, 30))
    img = titleFont.render('Total checks: '+str(che), True, (0, 0, 0))
    screen.blit(img, (510, 60))
    img = titleFont.render('Elapsed time: ' + f"{elap:.4f}s", True, (0, 0, 0))
    screen.blit(img, (510, 90))


def findStackOrder(ansArray):
    bricks = list(brick_name_color_dict.keys())
    bricks.remove('.')
    order = []
    add = 0
    for layer in range(5, 0, -1):
        for idx in range(layer**2):
            if ansArray[idx+add] in bricks:
                order.append(ansArray[idx+add])
                bricks.remove(ansArray[idx+add])
        add += layer**2

    return order


def fixOrder(queOrder, ansOrder):
    # print(queOrder)
    # print(ansOrder)

    for i in queOrder:
        for j in ansOrder:
            if i == j and i != '.':
                ansOrder.remove(j)
    # print(queOrder + ansOrder)
    return queOrder + ansOrder


def generateHintSteps(quesArray, ansArray, orderArray):
    global emptyGrid
    maps = []
    e = emptyGrid.copy()
    for i in orderArray:
        for j in range(len(ansArray)):
            if i == ansArray[j]:
                e[j] = i

        maps.append(e.copy())

    # print(maps)
    colorExist = []
    for p in quesArray:
        if p != '.' and (p not in colorExist):
            colorExist.append(p)

    # print(colorExist)

    for i in range(len(colorExist) - 1):
        maps.pop(0)

    if maps[0] == quesArray:
        maps.pop(0)

    # print(maps)
    return maps


def findDrawCircle(pos):
    add = 0
    for layer in range(5, 0, -1):
        for idx in range(layer**2):
            if Dots[idx+add].collidepoint(pos):
                return idx+add
        add += layer**2
    return -1


if __name__ == '__main__':
    global curStatus, foundAns, emptyGrid, notFinal, notFirst

    count = 0
    for i in range(6):
        count += i**2
    emptyGrid = []
    for j in range(count):
        emptyGrid.append('.')

    clock = pygame.time.Clock()
    running = True
    foundAns = False
    curStack = emptyGrid.copy()
    finalStack = []
    prevStatus = 'start'
    curStatus = 'start'
    hintText = 'Please choose a question or input by yourself.'
    attempts = -1
    check_count = 0
    elapsed_time = 0

    stepMaps = []
    hintIdx = -1
    notFinal = True
    notFirst = False

    while running:
        time_delta = clock.tick(60)/1000.0

        setUpLayout(curStack, hintText)
        if attempts != -1 and curStatus != 'create':
            printResult(attempts, check_count, elapsed_time)

        pygame.display.update()

        # Answer mode
        if curStatus == 'ans' and prevStatus != 'ans':
            attempts = -1
            

            if prevStatus == 'create':
                find_ans.setCustomQues(curStack)
                # print(curStack)

            setUpLayout(curStack, hintText)

            if attempts != -1 and curStatus != 'create':
                printResult(attempts, check_count, elapsed_time)
            pygame.display.update()
            manager.update(time_delta)
            # print(find_ans.ques)
            print('find ans')
            ansStack, attempts, check_count, elapsed_time = find_ans.find_ans()
            if ansStack != 'Fail':
                curStack = ansStack
                hintText = 'Complete! Please choose the next question.'
            else:
                attempts = -1
                curStack = emptyGrid.copy()
                hintText= 'No solution! Please check the input question again.'

            foundAns = True
            curStatus = 'choose'

        # Hint mode
        if curStatus == 'hint' and prevStatus != 'hint':
            foundAns = False
            attempts = -1
            if prevStatus == 'create':
                find_ans.setCustomQues(curStack)

            print('find ans for hint')

            setUpLayout(curStack, hintText)
            if attempts != -1 and curStatus != 'create':
                printResult(attempts, check_count, elapsed_time)
            pygame.display.update()
            manager.update(time_delta)

            finalStack, attempts, check_count, elapsed_time = find_ans.find_ans()
            if finalStack != 'Fail':
                foundAns = True

                ansOrder = findStackOrder(finalStack)
                queOrder = findStackOrder(curStack)
                ansOrder = fixOrder(queOrder, ansOrder)

                stepMaps = generateHintSteps(curStack, finalStack, ansOrder)
                stepMaps.insert(0, curStack)
                # print(stepMaps)
                hintIdx = 0

                notFinal = (hintIdx != len(stepMaps) - 1)
                notFirst = (hintIdx != 0)

                hintText = '                   Complete! \nPress "next >" to show the next step.'
            else:
                attempts = -1
                curStack = emptyGrid.copy()
                hintText= 'No solution! Please check the input question again.'

        if curStatus == 'hint' and foundAns:
            curStack = stepMaps[hintIdx]

        manager.update(time_delta)

        prevStatus = curStatus
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            manager.process_events(event)

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                for i in range(len(quesButton)):
                    if event.ui_element == quesButton[i]:
                        curStatus = 'choose'
                        hintText = 'Your choice: question '+str(i+1)
                        targetQues = i
                        curStack = find_ans.setQuestion(targetQues)
                        attempts = -1
                        foundAns = False
                        # print (curStack)

                for i in range(len(pickColorButton)):
                    if event.ui_element == pickColorButton[i]:
                        pickedColor = list(brick_name_color_dict.keys())[i]

                if event.ui_element == create_button:
                    print('create mode')
                    hintText = '   Please input question from the right panel\nand click the below button to generate the answer.'
                    curStatus = 'create'
                    curStack = emptyGrid.copy()

                if event.ui_element == hint_button:
                    hintText = 'Generating the steps...'
                    print('change to hint')

                    curStatus = 'hint'

                if event.ui_element == ans_button:
                    hintText = 'Generating the answer...'
                    curStatus = 'ans'

                if event.ui_element == next_button:
                    # print('next step')
                    if hintIdx + 1 < len(stepMaps):
                        hintIdx += 1

                    notFinal = (hintIdx != len(stepMaps) - 1)
                    notFirst = (hintIdx != 0)

                if event.ui_element == prev_button:
                    # print('prev step')
                    if hintIdx - 1 >= 0:
                        hintIdx -= 1

                    notFinal = (hintIdx != len(stepMaps) - 1)
                    notFirst = (hintIdx != 0)

            elif event.type == MOUSEBUTTONDOWN:
                if curStatus == 'create':
                    # event.pos => the position of clicked event happened
                    if pickedColor != "":
                        dotIdx = findDrawCircle(event.pos)
                        if dotIdx != -1:
                            if curStack[dotIdx] == pickedColor:
                                curStack[dotIdx] = '.'
                                print('clear '+pickedColor + ' at pos', dotIdx)
                            else: 
                                print('fill '+pickedColor + ' at pos', dotIdx)
                                curStack[dotIdx] = pickedColor
                        
