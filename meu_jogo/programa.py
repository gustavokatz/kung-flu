#para quem nao tem o python poder jogar

import os, sys
dirpath = os.getcwd()
sys.path.append(dirpath)

if getattr (sys, 'frozen', False): #perguntar oq é isso pq n entedi nada
    os.chdir(sys._MEIPASS) #o cara do video falou q n precisava saber oq era ms sim oq fazia(pessoas sem python podem jogar)
    
#canal Uniday Studio

import pygame as pg
from random import randint



pg.init()
pg.mixer.init()
largura = 1000
altura = 600

#Gera tela:
janela = pg.display.set_mode((largura, altura))
pg.display.set_caption('Kung-flu')
janela_aberta = True

#Carrega as imagens:
assets = {}
assets['fundo'] = pg.image.load('imagens/plano de fundo.png').convert()
assets['personagem1'] = pg.image.load('imagens/personagem 1 menor.png').convert_alpha()
lsObstaculos = []
for i in range(3):
    filename = 'imagens/obstaculos/ob0{}.png'.format(i)
    img = pg.image.load(filename).convert.aplha()
    img = pg.transform.scale(img, (50,50))
assets['obstaculos'] = lsObstaculos

#Carrega os sons:
pg.mixer.music.load('sound/soundtrack.mp3')
pg.mixer.music.set_volume(0.4)
#assets['sons_adicionais'] = 

#Declara classes:
class obstaculo(pg.sprite.Sprite):
    def __init__(self, assets):
        pg.sprite.Sprite.__init__(self)

        self.image = assets['obstaculos'][randint(0,3)] #Alterar randint para quantidade de obstaculos
        self.rect = self.image.get_rect()
        self.rect.x = randint(largura, 2000)
        self.rect.y = randint(0, altura)
        self.speedx = randint(-3, 3)
        self.speedy = randint(2, 9)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # Se passar do canto da tela: novas posições e velocidades
        if self.rect.top > altura or self.rect.right < 0 or self.rect.left > largura:
            self.rect.x = randint(largura, 2000)
            self.rect.y = randint(0, altura)
            self.speedx = randint(-3, 3)
            self.speedy = randint(2, 9)

class biroliro(pg.sprite.Sprite):
    def __init__(self, assets):
        pg.sprite.Sprite.__init__(self)

        self.image = assets['persongem1']
        self.rect = self.image.get_rect()
        self.rect.centerx = 0.1*largura
        self.rect.bottom = height/2
        self.velocidade = 15
    def update(self):
        self.rect.x += self.velocidade
        if self.rect.right > largura:
                self.rect.right = largura
        if self.rect.left < 0:
            self.rect.right = 0
        if self.rect.bottom > altura:
            self.rect.bottom = altura
        if self.rect.bottom < 0:
            self.rect.bottom = 0
        


#Criando grupo de obstaculos:
all_sprites = pg.sprite.Group()
all_obstaculos = pg.sprite.Group()
#Codigo base para o relogio (placar):
font= pg.font.SysFont(None, 30) # nao consegui botar uma fonte do meu pc
lugardotexto= (50,50)
clock = pygame.time.Clock()
FPS = 30
minutes = 0
seconds = 0
milliseconds = 0

#Loop principal:
pygame.mixer.music.play(loops=-1)
while janela_aberta:
    clock.tick(FPS)

    #Checa eventos:
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
    
    #Atualiza posicao dos obstaculos:

    #Contador: fonte: https://stackoverflow.com/questions/23717803/i-need-to-make-a-stopwatch-with-pygame
    if milliseconds > 1000:
        seconds += 1
        milliseconds -= 1000

    if seconds > 60:
        minutes += 1
        seconds -= 60
    milliseconds += clock.tick_busy_loop(60)
    contador = font.render ('Tempo decorrido: {}:{}'.format(minutes, seconds), False,(255, 255, 255), (0,0,0))


    janela.blit(fundo,(0,0))
    janela.blit(personagem1, (x,y))
    janela.blit(ob1, (ob1x, ob1y))
    #janela.blit(ob2, (ob2x, ob2y))
    #janela.blit(ob3, (ob3x, ob3y))
    janela.blit(contador, lugardotexto)


    pg.display.update()


pg.quit ()





