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
pg.mixer.music.set_volume(0.1)
assets['talkei'] = pg.mixer.Sound('sound/bolsok.wav')
assets['shield_on'] = pg.mixer.Sound('sound/definicoes.wav')
assets['shield_off'] = pg.mixer.Sound('sound/sneeze.wav')
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
assets['mascara'] = pg.image.load('imagens/bolsonaro_mask.png').convert_alpha()
assets['mascara'] = pg.transform.rotozoom(assets['mascara'], 0, 0.8)
nuv = pg.image.load('imagens/nuvem.png').convert_alpha()
nuv = pg.transform.rotozoom(nuv, 0, 0.5)
assets['nuvem'] = nuv
projetil = pg.image.load('imagens/projetil.png').convert_alpha()
projetil = pg.transform.rotozoom(projetil, 0, 0.05)
assets['projetil'] = projetil
assets['shield'] = pg.image.load('imagens/antiVirus.png').convert_alpha()
assets['shield'] = pg.transform.rotozoom(assets['shield'], 0, 0.2)
assets['obstaculos'] = pg.image.load('imagens/obstaculos/ob02.png').convert_alpha()
assets['obstaculos'] = pg.transform.scale(assets['obstaculos'], (150, 100))
    


# Declara classes:

# Classe de obstáculos
class Obstaculo(pg.sprite.Sprite):
    def __init__(self, assets):
        pg.sprite.Sprite.__init__(self)

        self.image = assets['obstaculos']
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = randint(largura, 2000)
        self.rect.y = randint(0, altura)
        self.speedx = randint(-15, -10)
        self.speedy = randint(-3, 3)

    # Atualiza as posições ao longo do jogo
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # Se passar do canto da tela: novas posições e velocidades
        if self.rect.top > altura or self.rect.right < 0 or self.rect.left > largura:
            self.rect.x = randint(largura, 2000)
            self.rect.y = randint(0, altura)
            self.speedx = randint(-15, -10)
            self.speedy = randint(-3, 3)

#Classe do power-up shield (antivirus):
class Shield(pg.sprite.Sprite):
    def __init__(self, assets):
        pg.sprite.Sprite.__init__(self)

        self.image = assets["shield"]
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = randint(largura*2, largura*3)
        self.rect.y = randint(altura*0.2, altura*0.8)
        self.speedx = randint(-7, -5) #Velocidade horizontal do shield
        self.speedy = 0
        self.assets = assets
    
    # Atualiza posições quando aparece um novo shield
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right < 0:
            self.rect.x = randint(largura*2, largura*3)
            self.rect.y = randint(altura*0.1, altura*0.9)
            self.speedx = randint(-7, -5) #Velocidade horizontal do shield
            self.speedy = 0
            
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

    # Implementa a movimentação do jogador 
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

    # Jogador passa a ter uma proteção para a próxima colisão com obstáculo:
    def mascara(self,assets):
        self.assets = assets
        self.image = assets['mascara']
        self.mask = pg.mask.from_surface(self.image)
    
    #Tira mascara ao colidir com obstaculo:
    def tira_mascara(self,assets):
        self.assets =  assets
        self.image = assets['personagem1']
        self.mask = pg.mask.from_surface(self.image)

# Classe das nuvens (composição do cenário)
class Nuvem(pg.sprite.Sprite):
    def __init__(self, assets):
        pg.sprite.Sprite.__init__(self)

        self.image = assets['nuvem']
        self.rect = self.image.get_rect()
        self.rect.x = randint(largura, 2000)
        self.rect.y = randint(0, altura/3)
        self.speedx = -2

    # Atualiza as posições das nuvens ao passarem da tela
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

# Função que mostra os melhores tempos no scoreboard ao final de cada tentativa
def mostra_tempo():
    janela.blit(assets['scoreboard'], (0,0))
    with open("highscore.json", 'r') as f:
        dicionario = json.load(f)
    scoreboard = {}
    lugarY = 130
    if len(dicionario["highscore"]) < 8:
        for i in range(len(dicionario["highscore"])):
            scoreboard["{i}"] = font.render(("{}o: {:.2f} segundos".format((i+1), dicionario["highscore"][i])), True,(255,255,255))
            janela.blit(scoreboard["{i}"], ((largura*0.35), lugarY))
            lugarY += 50
    else: 
        for i in range(8):
            scoreboard["{i}"] = font.render(("{}o: {:.2f} segundos".format((i+1), dicionario["highscore"][i])), True,(255,255,255))
            janela.blit(scoreboard["{i}"], ((largura*0.35), lugarY))
            lugarY += 50
    
    # Ao chegar no scoreboard, pode-se fechar a tela ou pressionar return para voltar ao menu do jogo
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
    all_shields = pg.sprite.Group()
    for i in range(3):  #quantidade de nuvens
        nuvem = Nuvem(assets)
        while pg.sprite.spritecollide(nuvem, all_cenary, False):
            nuvem = Nuvem(assets)
    all_cenary.add(nuvem)
    groups = {}
    groups['all_sprites'] = all_sprites
    groups['all_obstaculos'] = all_obstaculos
    groups['all_bullets'] = all_bullets
    groups['shield'] = all_shields

    # Jogador:
    jogador = Biroliro(groups, assets)
    all_sprites.add(jogador)
    comMascara = 0
    # Obstáculos:
    for i in range(8):  #quantidade de obstáculos
        obs = Obstaculo(assets)
        all_sprites.add(obs)
        all_obstaculos.add(obs)
        
    #Cria power-up (shield):
    shield = Shield(assets)
    all_shields.add(shield)
    all_sprites.add(shield)
    
    while True:
        clock.tick(FPS)
        # Checa eventos:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return QUIT
            # Movimentação do jogador ao pressionar as setas e atirar com espaço
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
        # Implementa colisões
        #Colisão entre jogador e obstaculos:
        ai = pg.sprite.spritecollide(
            jogador, all_obstaculos, True, pg.sprite.collide_mask)
        
        #Colisão entre obstáculos e bolhas:
        sabao = pg.sprite.groupcollide(
            all_obstaculos, all_bullets, True, True, pg.sprite.collide_mask)
        #Colisão entre jogador e shield:
        protecao = pg.sprite.spritecollide(jogador, all_shields, True, pg.sprite.collide_mask)
        #Retira mascara quando ha colisao:
        if len(ai) > 0 and comMascara == 1:
            assets['shield_off'].play()
            jogador.tira_mascara(assets)
            comMascara = 0
            shield = Shield(assets)
            all_shields.add(shield)
            all_sprites.add(shield)
        #Se nao tem mascara, mata jogador:
        elif len(ai) > 0:
            jogador.kill()
            pg.mixer.music.stop()
            salva_tempo(milliseconds)
            return SCOREBOARD
        #Mata os obstáculos com os tiros
        for obstaculo in sabao:
            obs = Obstaculo(assets)
            all_sprites.add(obs)
            all_obstaculos.add(obs)
        #Equipa shield:
        if len(protecao) > 0:
            jogador.mascara(assets)
            assets['shield_on'].play()
            comMascara = 1
            shield.kill()

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
