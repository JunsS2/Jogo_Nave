import pygame
import random

# Carregando as imagens
imagemNave = pygame.image.load('nave.png')
imagemAsteroide = pygame.image.load('asteroide.png')
imagemRaio = pygame.image.load('raio.png')
imagemFundo = pygame.image.load('magellanic-clouds.png')

# Configurações da janela e variáveis do jogo
LARGURAJANELA = 600
ALTURAJANELA = 600
CORTEXTO = (255, 255, 255)
QPS = 40
TAMMINIMO = 10
TAMMAXIMO = 40
VELMINIMA = 1
VELMAXIMA = 8
ITERACOES = 6
VELJOGADOR = 5
VELRAIO = (0, -15)
LARGURANAVE = imagemNave.get_width()
ALTURANAVE = imagemNave.get_height()
LARGURARAIO = imagemRaio.get_width()
ALTURARAIO = imagemRaio.get_height()

# Função para mover o jogador
def moverJogador(jogador, teclas, dim_janela):
    borda_esquerda = 0
    borda_superior = 0
    borda_direita = dim_janela[0]
    borda_inferior = dim_janela[1]
   
    if teclas['esquerda'] and jogador['objRect'].left > borda_esquerda:
        jogador['objRect'].x -= jogador['vel']
    if teclas['direita'] and jogador['objRect'].right < borda_direita:
        jogador['objRect'].x += jogador['vel']
    if teclas['cima'] and jogador['objRect'].top > borda_superior:
        jogador['objRect'].y -= jogador['vel']
    if teclas['baixo'] and jogador['objRect'].bottom < borda_inferior:
        jogador['objRect'].y += jogador['vel']

# Função para mover elementos
def moverElemento(elemento):
    elemento['objRect'].x += elemento['vel'][0]
    elemento['objRect'].y += elemento['vel'][1]

# Função para terminar o jogo
def terminar():
    pygame.quit()
    exit()

# Função para aguardar entrada do jogador
def aguardarEntrada():
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                terminar()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    terminar()
                return

# Função para colocar texto na tela
def colocarTexto(texto, fonte, janela, x, y):
    objTexto = fonte.render(texto, True, CORTEXTO)
    rectTexto = objTexto.get_rect()
    rectTexto.topleft = (x, y)
    janela.blit(objTexto, rectTexto)

# Função para verificar colisão entre dois retângulos (retângulos podem ser de nave, asteroide ou raio)
def verificarColisao(rect1, rect2):
    return rect1.colliderect(rect2)

# Inicializando o pygame e configurando a janela
pygame.init()
relogio = pygame.time.Clock()
janela = pygame.display.set_mode((LARGURAJANELA, ALTURAJANELA))
pygame.display.set_caption('Asteroides Troianos')
pygame.mouse.set_visible(False)
imagemFundoRedim = pygame.transform.scale(imagemFundo, (LARGURAJANELA, ALTURAJANELA))

# Configurando a fonte e sons
fonte = pygame.font.Font(None, 48)
somFinal = pygame.mixer.Sound('final_fx.wav')
somRecorde = pygame.mixer.Sound('record.wav')
somTiro = pygame.mixer.Sound('laser.wav')
pygame.mixer.music.load('trilha_nave.wav')

# Tela de início
colocarTexto('Asteroides Troianos', fonte, janela, LARGURAJANELA / 5, ALTURAJANELA / 3)
colocarTexto('Pressione uma tecla para começar.', fonte, janela, LARGURAJANELA / 20, ALTURAJANELA / 2)
pygame.display.update()
aguardarEntrada()

# Iniciando o jogo
recorde = 0
while True:
    asteroides = []
    raios = []
    pontuacao = 0
    deve_continuar = True
   
    teclas = {'esquerda': False, 'direita': False, 'cima': False, 'baixo': False}
    contador = 0
    pygame.mixer.music.play(-1, 0.0)
   
    posX = LARGURAJANELA / 2
    posY = ALTURAJANELA - 50
    jogador = {'objRect': pygame.Rect(posX, posY, LARGURANAVE, ALTURANAVE), 'imagem': imagemNave, 'vel': VELJOGADOR}

    while deve_continuar:
        pontuacao += 1
        if pontuacao > recorde:
            recorde = pontuacao
            somRecorde.play()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                terminar()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    terminar()
                if evento.key == pygame.K_LEFT or evento.key == pygame.K_a:
                    teclas['esquerda'] = True
                if evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
                    teclas['direita'] = True
                if evento.key == pygame.K_UP or evento.key == pygame.K_w:
                    teclas['cima'] = True
                if evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                    teclas['baixo'] = True
                if evento.key == pygame.K_SPACE:
                    raio = {'objRect': pygame.Rect(jogador['objRect'].centerx, jogador['objRect'].top, LARGURARAIO, ALTURARAIO),
                            'imagem': imagemRaio, 'vel': VELRAIO}
                    raios.append(raio)
                    somTiro.play()

            if evento.type == pygame.KEYUP:
                if evento.key == pygame.K_LEFT or evento.key == pygame.K_a:
                    teclas['esquerda'] = False
                if evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
                    teclas['direita'] = False
                if evento.key == pygame.K_UP or evento.key == pygame.K_w:
                    teclas['cima'] = False
                if evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
                    teclas['baixo'] = False

        # Preenchendo o fundo da janela
        janela.blit(imagemFundoRedim, (0, 0))

        # Exibindo pontuação e recorde
        colocarTexto('Pontuação: ' + str(pontuacao), fonte, janela, 10, 0)
        colocarTexto('Recorde: ' + str(recorde), fonte, janela, 10, 40)

        # Adicionando asteroides
        contador += 1
        if contador >= ITERACOES:
            contador = 0
            tamAsteroide = random.randint(TAMMINIMO, TAMMAXIMO)
            posX = random.randint(0, LARGURAJANELA - tamAsteroide)
            posY = -tamAsteroide
            vel_x = random.randint(-1, 1)
            vel_y = random.randint(VELMINIMA, VELMAXIMA)
            asteroide = {'objRect': pygame.Rect(posX, posY, tamAsteroide, tamAsteroide),
                         'imagem': pygame.transform.scale(imagemAsteroide, (tamAsteroide, tamAsteroide)),
                         'vel': (vel_x, vel_y)}
            asteroides.append(asteroide)

        # Movimentando e desenhando os asteroides
        for asteroide in asteroides:
            moverElemento(asteroide)
            janela.blit(asteroide['imagem'], asteroide['objRect'])

        # Eliminando os asteroides que saem da tela
        for asteroide in asteroides[:]:
            if asteroide['objRect'].top > ALTURAJANELA:
                asteroides.remove(asteroide)
            # Verificando colisão com o jogador
            if verificarColisao(jogador['objRect'], asteroide['objRect']):
                somFinal.play()
                deve_continuar = False

        # Movimentando e desenhando os raios
        for raio in raios:
            moverElemento(raio)
            janela.blit(raio['imagem'], raio['objRect'])

        # Eliminando raios que saem da tela
        for raio in raios[:]:
            if raio['objRect'].bottom < 0:
                raios.remove(raio)
            # Verificando colisão com os asteroides
            for asteroide in asteroides[:]:
                if verificarColisao(raio['objRect'], asteroide['objRect']):
                    raios.remove(raio)
                    asteroides.remove(asteroide)
                    pontuacao += 100  # Aumenta a pontuação por destruir o asteroide
                    break

        # Movimentando e desenhando o jogador
        moverJogador(jogador, teclas, (LARGURAJANELA, ALTURAJANELA))
        janela.blit(jogador['imagem'], jogador['objRect'])

        # Atualizando a tela
        pygame.display.update()

        # Controlando o FPS do jogo
        relogio.tick(QPS)

    # Fim de jogo - Exibir a tela final
    colocarTexto('Game Over', fonte, janela, LARGURAJANELA / 3, ALTURAJANELA / 3)
    colocarTexto('Pontuação final: ' + str(pontuacao), fonte, janela, LARGURAJANELA / 3, ALTURAJANELA / 2)
    colocarTexto('Pressione uma tecla para reiniciar', fonte, janela, LARGURAJANELA / 5, ALTURAJANELA / 1.5)
    pygame.display.update()
    aguardarEntrada()
