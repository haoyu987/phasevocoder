from PVgui import Label,Button,Scroller
from phaseV4 import pitchshift
from realtimePV2 import realtimePitchshift
import pygame
import struct
from Tkinter import Tk
from tkFileDialog import askopenfilename

pygame.init()
def main():
    screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("pitch shifter demo")
    
    background = pygame.Surface(screen.get_size())
    background.fill((0xCC, 0xFF, 0xCC))
    screen.blit(background, (0, 0))

    label = Label()
    label.text = "Pitch shifter"
    label.size = (150, 20)
    label.bgColor = ((0xCC, 0xFF, 0xCC))
    label.center = (200, 50)

    label2 = Label()
    label2.text = "File:"
    label2.font = pygame.font.SysFont(None, 20)
    label2.bgColor = ((0xE6, 0xFF, 0xCC))
    label2.size = (40, 20)
    label2.center = (30, 100)

    label3 = Label()
    label3.text = ""
    label3.font = pygame.font.SysFont(None, 20)
    label3.bgColor = ((0xE6, 0xFF, 0xCC))
    label3.size = (350, 20)
    label3.center = (220, 100)

    button0 = Button()
    button0.text = "real time"
    button0.bgColor = ((0xCC, 0xCD, 0xFF))
    button0.center = (300, 150)
    
    button1 = Button()
    button1.text = "load file"
    button1.bgColor = ((0xCC, 0xE6, 0xFF))
    button1.center = (100, 150)

    button2 = Button()
    button2.text = "shift"
    button2.bgColor = ((0xFF, 0xCC, 0xCD))
    button2.center = (300, 200)

    button3 = Button()
    button3.text = "stretch"
    button3.bgColor = ((0xFF, 0xFE, 0xCC))
    button3.center = (100, 200)

    scroller = Scroller()
    scroller.value = 1.0
    scroller.increment = .01
    scroller.maxValue = 2.0
    scroller.minValue = 0.5
    scroller.center = (200, 250)
    scroller.bgColor = ((0xCC, 0xFF, 0xFF))
    
    allSprites = pygame.sprite.Group(label, label2, label3, button0, button1, button2, button3, scroller)
    
    clock = pygame.time.Clock()
    keepGoing = True
    filename = ''
    while keepGoing:
        clock.tick(50)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button0.pressed(pygame.mouse.get_pos()):
                    realtimePitchshift(scroller.value)
                if button1.pressed(pygame.mouse.get_pos()):
                    Tk().withdraw()
                    filename = askopenfilename()
                    label3.text = filename
                if button2.pressed(pygame.mouse.get_pos()):
                    if filename == '':
                        pass
                    else:
                        pitchshift(filename,scroller.value,"tune")
                if button3.pressed(pygame.mouse.get_pos()):
                    if filename == '':
                        pass
                    else:
                        pitchshift(filename,scroller.value,"stretch")

        # if record_flag == True:
        #     print "start."
        #     mic_input = mic_input + sound_record()
        
        screen.blit(background, (0, 0))
        
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
        
        pygame.display.flip()

if __name__ == "__main__":
    main()
