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
pg.mixer.init()
largura = 1000
altura = 600
#Carrega as imagens:
fundo =pg.image.load('imagens/plano de fundo.png')
personagem1 = pg.image.load('imagens/personagem 1 menor.png')
#ob1 = pg.image.load('imagens/ob1.png')
#ob2 = pg.image.load('imagens/ob2.png')
ob1 = pg.image.load('imagens/globo.png')
ob1 = pygame.image.load('imagens/globo.png').convert_alpha()

class obstaculo(pygame.sprite.Sprite):
    def __init__(self, img):
        pygame.sprite.Sprite.__init__(self)

        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = randint(largura, 2000)
        self.rect.y = randint(0, altura)
        self.speedx = randint(-3, 3)
        self.speedy = randint(2, 9)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # novas posições e velocidades
        if self.rect.right < 0:
            self.rect.x = randint(largura, 2000)
            self.rect.y = randint(0, 600)
            self.speedx = randint(-3, 3)
            self.speedy = randint(2, 9)


#Carrega os sons:
pg.mixer.music.load('sound/soundtrack.mp3')
pg.mixer.music.set_volume(0.4)

font= pg.font.SysFont(None, 30) # nao consegui botar uma fonte do meu pc
lugardotexto= (50,50)

clock = pygame.time.Clock()
minutes = 0
seconds = 0
milliseconds = 0



#ob1x = 1000
#ob1y = 400
#ob2x = 1000
#ob2y =250
#ob3x =1000
#ob3y =100
x= 450 #min 0 max 880
y=520 #min 0 max 510
velocidade= 15
#elocidade_ob = 10


janela = pg.display.set_mode((largura, altura))
pg.display.set_caption('Kung-flu')
janela_aberta = True

#Loop principal:
pygame.mixer.music.play(loops=-1)
while janela_aberta:
    pg.time.delay(15)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            janela_aberta = False


    comandos = pg.key.get_pressed()
    if comandos[pg.K_UP] and y >= 0:
        y-= velocidade
    if comandos[pg.K_DOWN] and y <= 510:
        y+= velocidade
    if comandos[pg.K_RIGHT] and x <= 880:
        x+= velocidade
    if comandos[pg.K_LEFT] and x >= 0:
        x-= velocidade
    #if ob1x <= 0:
        #ob1x = randint (1000, 2000)
    #if ob2x <= 0:
        #ob2x = randint (1000, 2000)
    #if ob3x <= 0:
        #ob3x = randint (1000, 2000)

    #Contador: fonte: https://stackoverflow.com/questions/23717803/i-need-to-make-a-stopwatch-with-pygame
    if milliseconds > 1000:
        seconds += 1
        milliseconds -= 1000

    if seconds > 60:
        minutes += 1
        seconds -= 60
    milliseconds += clock.tick_busy_loop(60)
    contador = font.render ('Tempo decorrido: {}:{}'.format(minutes, seconds), False,(255, 255, 255), (0,0,0))

    #ob1x-=velocidade_ob
    #ob2x-=velocidade_ob
    #ob3x-=velocidade_ob

    janela.blit(fundo,(0,0))
    janela.blit(personagem1, (x,y))
    janela.blit(ob1, (ob1x, ob1y))
    #janela.blit(ob2, (ob2x, ob2y))
    #janela.blit(ob3, (ob3x, ob3y))
    janela.blit(contador, lugardotexto)


    pg.display.update()


pg.quit ()





