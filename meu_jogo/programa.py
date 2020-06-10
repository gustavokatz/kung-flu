# importando as funções das bibliotecas

from random import randint
import pygame as pg
import os
import sys
import json

pg.init()
pg.mixer.init()
largura = 1000
altura = 600


# Carrega os sons do jogo:
assets = {}
pg.mixer.music.load('sound/soundtrack.mp3')
pg.mixer.music.set_volume(0.2)
assets['talkei'] = pg.mixer.Sound('sound/bolsok.wav')

# Gera tela de jogo:
janela = pg.display.set_mode((largura, altura))
pg.display.set_caption('Kung-flu')
QUIT = 0
GAME = 1
INTRO = 2
SCOREBOARD = 3
# Carrega as imagens (fundo, obstáculos e personagem):
menu = pg.image.load('imagens/menu.png').convert()
menu = pg.transform.scale(menu, (largura,altura))
assets['menu'] = menu
assets['fundo'] = pg.image.load('imagens/plano de fundo.png').convert()
assets['scoreboard'] = pg.image.load('imagens/scoreboard.png').convert()
assets['scoreboard'] = pg.transform.scale(assets['scoreboard'], (largura,altura))
personagem = pg.image.load('imagens/personagem 1 menor.png').convert_alpha()
personagem = pg.transform.rotozoom(personagem, 0, 0.3)
assets['personagem1'] = personagem
nuv = pg.image.load('imagens/nuvem.png').convert_alpha()
nuv = pg.transform.rotozoom(nuv, 0, 0.5)
assets['nuvem'] = nuv
projetil = pg.image.load('imagens/projetil.png').convert_alpha()
projetil = pg.transform.rotozoom(projetil, 0, 0.05)
assets['projetil'] = projetil
lsObstaculos = []
for i in range(3):
    filename = 'imagens/obstaculos/ob02.png'
    img = pg.image.load(filename).convert_alpha()
    img = pg.transform.scale(img, (150, 100))
    lsObstaculos.append(img)
assets['obstaculos'] = lsObstaculos

# Declara classes:

# Classe de obstáculos
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
            self.speedx = randint(-15, -10)
            self.speedy = randint(-3, 3)

# Classe do personagem
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
        self.groups = groups

        # Limite de tiros:
        self.ultimo_tiro = pg.time.get_ticks()
        self.delay_tiro = 1000  # Mudar intervalo de tempo entre tiros.

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

    # Função para o jogador atirar
    def atirar(self):
        t = pg.time.get_ticks()
        passados = t - self.ultimo_tiro
        if passados > self.delay_tiro:
            self.ultimo_tiro = t
            # Criar novo tiro
            novo_projetil = Tiro(
                self.assets, self.rect.centery, self.rect.centerx)
            self.groups['all_sprites'].add(novo_projetil)
            self.groups['all_bullets'].add(novo_projetil)
            self.assets['talkei'].play()

# Classe das nuvens (composição do cenário)
class Nuvem(pg.sprite.Sprite):
    def __init__(self, assets):
        pg.sprite.Sprite.__init__(self)

        self.image = assets['nuvem']
        self.rect = self.image.get_rect()
        self.rect.x = randint(largura, 2000)
        self.rect.y = randint(0, altura/3)
        self.speedx = -2

    def update(self):
        self.rect.x += self.speedx
        # Se passar do canto da tela: novas posições e velocidades
        if self.rect.top > altura or self.rect.right < 0:
            self.rect.x = randint(largura, 2000)
            self.rect.y = randint(0, altura/3)

# Classe dos tiros 
class Tiro(pg.sprite.Sprite):
    def __init__(self, assets, centery, centerx):
        pg.sprite.Sprite.__init__(self)

        self.image = assets['projetil']
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = centerx
        self.rect.centery = centery
        self.speedx = 15

    def update(self):
        self.rect.x += self.speedx
        if self.rect.left > largura:
            self.kill()


# Codigo base para o relógio (placar):
font = pg.font.SysFont("Comic Sans MS", 30)
lugardotexto = (50, 50)
clock = pg.time.Clock()
FPS = 30
minutes = 0
seconds = 0
milliseconds = 0

# Função que salva o tempo para cada tentativa
def salva_tempo(milliseconds):
    with open('highscore.json', 'r') as f:
        dicionario = json.load(f)
        segundos = milliseconds/1000
        dicionario["highscore"].append(segundos)
        dicionario["highscore"].sort(reverse=True)
    with open('highscore.json', 'w') as f:
        a = json.dumps(dicionario)
        f.write(a)

# Função que mostra os melhores tempos ao final de cada tentativa
def mostra_tempo():
    janela.blit(assets['scoreboard'], (0,0))
    with open("highscore.json", 'r') as f:
        dicionario = json.load(f)
    scoreboard = {}
    lugarY = 130
    if len(dicionario["highscore"]) < 8:
        for i in range(len(dicionario["highscore"])):
            scoreboard["{i}"] = font.render(("{}o: {} segundos".format((i+1), dicionario["highscore"][i])), True,(255,255,255))
            janela.blit(scoreboard["{i}"], ((largura*0.35), lugarY))
            lugarY += 50
    else: 
        for i in range(8):
            scoreboard["{i}"] = font.render(("{}o: {} segundos".format((i+1), dicionario["highscore"][i])), True,(255,255,255))
            janela.blit(scoreboard["{i}"], ((largura*0.35), lugarY))
            lugarY += 50
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return QUIT
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    return INTRO
        pg.display.update()
        clock.tick(FPS)

#Loop menu:
def intro_game():
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return QUIT
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    return GAME
        janela.blit(assets['menu'], (0, 0))
        pg.display.update()
        clock.tick(FPS)

# Loop principal:
def game_run():
    t0 = pg.time.get_ticks()

    pg.mixer.music.play(loops=-1)
    all_sprites = pg.sprite.Group()
    all_obstaculos = pg.sprite.Group()
    all_bullets = pg.sprite.Group()
    all_cenary = pg.sprite.Group()
    for i in range(3):  #quantidade de nuvens
        nuvem = Nuvem(assets)
        while pg.sprite.spritecollide(nuvem, all_cenary, False):
            nuvem = Nuvem(assets)
    all_cenary.add(nuvem)
    groups = {}
    groups['all_sprites'] = all_sprites
    groups['all_obstaculos'] = all_obstaculos
    groups['all_bullets'] = all_bullets

    # Jogador:
    jogador = Biroliro(groups, assets)
    all_sprites.add(jogador)

    # Obstaculos:
    for i in range(10):  #quantidade de obstaculos
        obs = Obstaculo(assets)
        all_sprites.add(obs)
        all_obstaculos.add(obs)
    while True:
        clock.tick(FPS)
        # Checa eventos:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return QUIT
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    jogador.speedx -= 15
                if event.key == pg.K_RIGHT:
                    jogador.speedx += 15
                if event.key == pg.K_UP:
                    jogador.speedy -= 15
                if event.key == pg.K_DOWN:
                    jogador.speedy += 15
                if event.key == pg.K_SPACE:
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

        # Contador: fonte: https://stackoverflow.com/questions/23717803/i-need-to-make-a-stopwatch-with-pygame
        milliseconds = pg.time.get_ticks() - t0

        # Atualiza posição dos obstáculos
        all_cenary.update()
        all_sprites.update()
        ai = pg.sprite.spritecollide(
            jogador, all_obstaculos, True, pg.sprite.collide_mask)
        sabao = pg.sprite.groupcollide(
            all_obstaculos, all_bullets, True, True, pg.sprite.collide_mask)
        # Finaliza o jogo quando o personagem colide com o obstáculo
        if len(ai) > 0:
            jogador.kill()
            pg.mixer.music.stop()
            salva_tempo(milliseconds)
            return SCOREBOARD
        # Mata os obstáculos com os tiros
        for obstaculo in sabao:
            obs = Obstaculo(assets)
            all_sprites.add(obs)
            all_obstaculos.add(obs)

        # Conta o tempo jogado
        seconds = (milliseconds//1000) % 60
        minutes = milliseconds//60000
        contador = font.render('Tempo decorrido: {}:{}'.format(
            minutes, seconds), True, (255, 255, 255))
        janela.blit(assets['fundo'], (0, 0))
        all_cenary.draw(janela)
        all_sprites.draw(janela)
        janela.blit(contador, lugardotexto)

        pg.display.update()


state = INTRO
while state != QUIT:
    if state == INTRO:
        state = intro_game()
    elif state == GAME:
        state = game_run()
    elif state == SCOREBOARD:
        state = mostra_tempo()

clock = 10

pg.quit()
