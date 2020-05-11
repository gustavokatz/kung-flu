#para quem nao tem o python poder jogar

import os, sys
dirpath = os.getcwd()
sys.path.append(dirpath)

if getattr (sys, 'frozen', False): #perguntar oq é isso pq n entedi nada
    os.chdir(sys._MEIPASS) #o cara do video falou q n precisava saber oq era ms sim oq fazia(pessoas sem python podem jogar)
    
#canal Uniday Studio

import pygame
import pygame as pg
from random import randint



pg.init()

fundo =pg.image.load('plano de fundo.png')
personagem1 = pg.image.load('personagem 1 menor.png')
ob1 = pg.image.load('ob1.png')
ob2 = pg.image.load('ob2.png')
ob3 = pg.image.load('ob3.png')

#letra= pg.front.SysFront('' 30) # nao consegui botar uma fonte do meu pc
#texto= front.render ('Tamanho dos chifres:', False,(255, 255, 255), (0,0,0))
#lugardotexto= texto.get_rect()
#lugardotexto= (50,50)



ob1x = 1000
ob1y = 400
ob2x = 1000
ob2y =250
ob3x =1000
ob3y =100
x= 450 #min 0 max 880
y=520 #min 0 max 510
velocidade= 15
velocidade_ob = 10


janela = pg.display.set_mode((1000,600))
pg.display.set_caption('Kung-flu')
janela_aberta = True
while janela_aberta:
    pg.time.delay(15)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            janela_aberta = False


    comandos = pg.key.get_pressed()
    if comandos[pg.K_UP] and y >= 0:
        y-= velocidade
    if comandos[pg.K_DOWN] and y <=510:
        y+= velocidade
    if comandos[pg.K_RIGHT] and x <= 880:
        x+= velocidade
    if comandos[pg.K_LEFT] and x>=0:
        x-= velocidade
    if ob1x <= 0:
        ob1x = randint (1000, 2000 )
    if ob2x <= 0:
        ob2x = randint (1000, 2000 )
    if ob3x <= 0:
        ob3x = randint (1000, 2000 )


    ob1x-=velocidade_ob
    ob2x-=velocidade_ob
    ob3x-=velocidade_ob

    janela.blit(fundo,(0,0) )
    janela.blit(personagem1, (x,y))
    janela.blit(ob1, (ob1x, ob1y))
    janela.blit(ob2, (ob2x, ob2y))
    janela.blit(ob3, (ob3x, ob3y))
    #janela.blit(texto, lugardotexto)
    pg.display.update()


pg.quit ()





