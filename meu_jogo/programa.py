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
game = True

#Carrega as imagens:
assets = {}
assets['fundo'] = pg.image.load('imagens/plano de fundo.png').convert()
assets['personagem1'] = pg.image.load('imagens/personagem 1 menor.png').convert_alpha()
lsObstaculos = []
for i in range(3):
    filename = 'imagens/obstaculos/ob0{}.png'.format(i)
    img = pg.image.load(filename).convert_alpha()
    img = pg.transform.scale(img, (50,50))
    lsObstaculos.append(img)
assets['obstaculos'] = lsObstaculos

#Carrega os sons:
pg.mixer.music.load('sound/soundtrack.mp3')
pg.mixer.music.set_volume(0.4)
#assets['sons_adicionais'] = 

#Declara classes:
class obstaculo(pg.sprite.Sprite):
    def __init__(self, assets):
        pg.sprite.Sprite.__init__(self)

        self.image = assets['obstaculos'][randint(0,2)] #Alterar randint para quantidade de obstaculos
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
    def __init__(self, groups, assets):
        pg.sprite.Sprite.__init__(self)

        self.image = assets['personagem1']
        self.rect = self.image.get_rect()
        self.rect.centerx = 0.1*largura
        self.rect.bottom = altura/2
        self.speedx = 0
        self.speedy = 0
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
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
groups = {}
groups['all_sprites'] = all_sprites
groups['all_obstaculos'] = all_obstaculos

#Jogador:
jogador = biroliro(groups, assets)
all_sprites.add(jogador)

#Obstaculos:
for i in range(3): #Mudar para quantidade de obstaculos
    obs = obstaculo(assets)
    all_sprites.add(obs)
    all_obstaculos.add(obs)


#Codigo base para o relogio (placar):
font= pg.font.SysFont(None, 30) # nao consegui botar uma fonte do meu pc
lugardotexto= (50,50)
clock = pg.time.Clock()
FPS = 30
minutes = 0
seconds = 0
milliseconds = 0

t0 = pg.time.get_ticks()
#Loop principal:
pg.mixer.music.play(loops=-1)
while game:
    clock.tick(FPS)
    #Checa eventos:
    for event in pg.event.get():
        clock
        if event.type == pg.QUIT:
            game = False
    comandos = pg.key.get_pressed()
    if comandos[pg.K_UP]:
        jogador.speedx = 15
    if comandos[pg.K_DOWN]:
        jogador.speedy = 15
    if comandos[pg.K_RIGHT]:
        jogador.speedx = -15
    if comandos[pg.K_LEFT]:
        jogador.speedy -= -15
    
    #Atualiza posicao dos obstaculos:
    all_sprites.update()
    ai = pg.sprite.spritecollide(jogador, all_obstaculos, True)
    if len(ai) > 0:
        jogador.kill()
        game = False
        
    #Contador: fonte: https://stackoverflow.com/questions/23717803/i-need-to-make-a-stopwatch-with-pygame
    milliseconds = pg.time.get_ticks() - t0
    seconds = (milliseconds//1000)%60
    minutes = milliseconds//60000
    contador = font.render ('Tempo decorrido: {}:{}'.format(minutes, seconds), False,(255, 255, 255), (0,0,0))


    janela.blit(assets['fundo'],(0,0))
    all_sprites.draw(janela)
    janela.blit(contador, lugardotexto)


    pg.display.update()


pg.quit ()





