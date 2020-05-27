# para quem nao tem o python poder jogar

from random import randint
import pygame as pg
import os
import sys
import pickle #https://stackoverflow.com/questions/16726354/saving-the-highscore-for-a-python-game
try:
    with open('clock.dat', 'rb') as file:
        clock = pickle.load(file)
except:
    clock = 0
print("High clock: %d" % clock)
#dirpath = os.getcwd()
#sys.path.append(dirpath)

if getattr(sys, 'frozen', False):  # perguntar oq é isso pq n entedi nada
    # o cara do video falou q n precisava saber oq era ms sim oq fazia(pessoas sem python podem jogar)
    os.chdir(sys._MEIPASS)

# canal Uniday Studio


pg.init()
# pg.mixer.init()
largura = 1000
altura = 600

# Carrega os sons:
# pg.mixer.music.load('sound/soundtrack.mp3')
# pg.mixer.music.set_volume(0.4)
# assets['sons_adicionais'] =

# Gera tela:
janela = pg.display.set_mode((largura, altura))
pg.display.set_caption('Kung-flu')
game = True

# Carrega as imagens:
assets = {}
assets['fundo'] = pg.image.load('imagens/plano de fundo.png').convert()
assets['personagem1'] = pg.image.load('imagens/personagem 1 menor.png').convert_alpha()
nuv = pg.image.load('imagens/nuvem.png').convert_alpha()
nuv = pg.transform.rotozoom(nuv, 0, 0.5)
assets['nuvem'] = nuv
assets['projetil'] = pg.image.load('imagens/projetil.png').convert_alpha()
lsObstaculos = []
for i in range(3):
    filename = 'imagens/obstaculos/ob0{}.png'.format(i)
    img = pg.image.load(filename).convert_alpha()
    img = pg.transform.scale(img, (150, 100))
    lsObstaculos.append(img)
assets['obstaculos'] = lsObstaculos

# Declara classes:


class Obstaculo(pg.sprite.Sprite):
    def __init__(self, assets):
        pg.sprite.Sprite.__init__(self)

        # Alterar randint para quantidade de obstaculos
        self.image = assets['obstaculos'][randint(0, 2)]
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = randint(largura, 2000)
        self.rect.y = randint(0, altura)
        self.speedx = randint(-15, -10)
        self.speedy = randint(-3, 3)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # Se passar do canto da tela: novas posições e velocidades
        if self.rect.top > altura or self.rect.right < 0 or self.rect.left > largura:
            self.rect.x = randint(largura, 2000)
            self.rect.y = randint(0, altura)
            self.speedx = randint(-15,-10)
            self.speedy = randint(-3, 3)


class Biroliro(pg.sprite.Sprite):
    def __init__(self, groups, assets):
        pg.sprite.Sprite.__init__(self)

        self.image = assets['personagem1']
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = 0.1*largura
        self.rect.bottom = altura/2
        self.speedx = 0
        self.speedy = 0
        self.assets = assets 

        #Limite de tiros:
        self.ultimo_tiro = pg.time.get_ticks()
        self.delay_tiro = 1000 #Mudar intervalo de tempo entre tiros.

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > largura:
            self.rect.right = largura
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > altura:
            self.rect.bottom = altura
        if self.rect.top < 0:
            self.rect.top = 0
    def atirar(self ):
        t = pg.time.get_ticks()
        passados = t - self.ultimo_tiro
        if passados > self.delay_tiro:
            self.ultimo_tiro = t
            #Criar novo projetil
            novo_projetil = Tiro(self.assets, self.rect.top, self.rect.centerx)
            self.groups['all_sprites'].add(novo_projetil)
            self.groups['all_bullets'].add(novo_projetil)


class Nuvem(pg.sprite.Sprite):
    def __init__(self, assets):
        pg.sprite.Sprite.__init__(self)

        # Alterar randint para quantidade de obstaculos
        self.image = assets['nuvem']
        self.rect = self.image.get_rect()
        self.rect.x = randint(largura, 2000)
        self.rect.y = randint(0, altura)
        self.speedx = -2

    def update(self):
        self.rect.x += self.speedx
        # Se passar do canto da tela: novas posições e velocidades
        if self.rect.top > altura or self.rect.right < 0 or self.rect.left > largura:
            self.rect.x = randint(largura, 2000)
            self.rect.y = randint(altura/5, altura/3)

class Tiro(pg.sprite.Sprite):
    def __init__(self, assets, bottom, centerx):
        pg.sprite.Sprite.__init__(self)

        self.image = assets['projetil']
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.bottom = bottom
        self.speedx = 20 

    def update(self):
        self.rect.x += self.speedx
        if self.rect.left > largura:
            self.kill()

# Criando grupos de assets:
all_sprites = pg.sprite.Group()
all_obstaculos = pg.sprite.Group()
all_cenary = pg.sprite.Group()
all_bullets = pg.sprite.Group()
groups = {}
groups['all_sprites'] = all_sprites
groups['all_obstaculos'] = all_obstaculos
groups['all_bullets'] = all_bullets

# Cenario:
for i in range(2):
    nuvem = Nuvem(assets)
    all_cenary.add(nuvem)
# Jogador:
jogador = Biroliro(groups, assets)
all_sprites.add(jogador)

# Obstaculos:
for i in range(3):  # Mudar para quantidade de obstaculos
    obs = Obstaculo(assets)
    all_sprites.add(obs)
    all_obstaculos.add(obs)


# Codigo base para o relogio (placar):
font = pg.font.SysFont(None, 30)
lugardotexto = (50, 50)
clock = pg.time.Clock()
FPS = 30
minutes = 0
seconds = 0
milliseconds = 0


t0 = pg.time.get_ticks()
# Loop principal:
# pg.mixer.music.play(loops=-1)
while game:
    clock.tick(FPS)
    # Checa eventos:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                jogador.speedx -= 15
            if event.key == pg.K_RIGHT:
                jogador.speedx += 15
            if event.key == pg.K_UP:
                jogador.speedy -= 15
            if event.key == pg.K_DOWN:
                jogador.speedy += 15
            if event.key ==pg.K_SPACE:
                jogador.atirar()

        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT:
                jogador.speedx += 15
            if event.key == pg.K_RIGHT:
                jogador.speedx -= 15
            if event.key == pg.K_UP:
                jogador.speedy += 15
            if event.key == pg.K_DOWN:
                jogador.speedy -= 15

    # Atualiza posicao dos obstaculos:
    all_cenary.update()
    all_sprites.update()
    ai = pg.sprite.spritecollide(jogador, all_obstaculos, True)
    if len(ai) > 0:
        jogador.kill()
        game = False

    # Contador: fonte: https://stackoverflow.com/questions/23717803/i-need-to-make-a-stopwatch-with-pygame
    milliseconds = pg.time.get_ticks() - t0
    seconds = (milliseconds//1000) % 60
    minutes = milliseconds//60000
    contador = font.render('Tempo decorrido: {}:{}'.format(
        minutes, seconds), False, (255, 255, 255), (0, 0, 0))
    janela.blit(assets['fundo'], (0, 0))
    all_cenary.draw(janela)
    all_sprites.draw(janela)
    janela.blit(contador, lugardotexto)

    pg.display.update()

    

                

    # Atualiza posicao dos obstaculos:
    all_cenary.update()
    all_sprites.update()
    ai = pg.sprite.spritecollide(jogador, all_obstaculos, True)
    if len(ai) > 0:
        jogador.kill()
        game = False

    # Contador: fonte: https://stackoverflow.com/questions/23717803/i-need-to-make-a-stopwatch-with-pygame
    milliseconds = pg.time.get_ticks() - t0
    seconds = (milliseconds//1000) % 60
    minutes = milliseconds//60000
    contador = font.render('Tempo decorrido: {}:{}'.format(
        minutes, seconds), False, (255, 255, 255), (0, 0, 0))
    janela.blit(assets['fundo'], (0, 0))
    all_cenary.draw(janela)
    all_sprites.draw(janela)
    janela.blit(contador, lugardotexto)

    pg.display.update()

    
clock = 10

# save the score
with open('score.dat', 'wb') as file:
    pickle.dump(clock, file)

pg.quit()