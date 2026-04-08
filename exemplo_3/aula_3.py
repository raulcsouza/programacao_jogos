import pygame  # importa a biblioteca pygame
import sys  # importa a biblioteca sys
import random  # importa a biblioteca random

# -----------------------------  
# Inicialização  
# -----------------------------  
pygame.init()  # inicializa o pygame

LARGURA = 800  # define a largura da janela
ALTURA = 600  # define a altura da janela

tela = pygame.display.set_mode((LARGURA, ALTURA))  # cria a janela do jogo
pygame.display.set_caption("Aula 3 - Tiros e Pontuação")  # define o título da janela

clock = pygame.time.Clock()  # cria um relógio para controlar os FPS

# -----------------------------  
# Cores  
# -----------------------------  
BRANCO = (255, 255, 255)  # define a cor branca
AZUL = (50, 100, 255)  # define a cor azul
VERMELHO = (200, 50, 50)  # define a cor vermelha
AMARELO = (255, 220, 0)  # define a cor amarela
PRETO = (0, 0, 0)  # define a cor preta

# -----------------------------  
# Fonte e função auxiliar  
# -----------------------------  
fonte = pygame.font.SysFont(None, 36)  # cria a fonte padrão

def desenhar_texto(texto, x, y, cor=PRETO):  # função para desenhar texto
    img = fonte.render(texto, True, cor)  # renderiza o texto
    tela.blit(img, (x, y))  # desenha o texto na tela

# -----------------------------  
# Jogador e status  
# -----------------------------  
jogador_largura = 60  # define a largura do jogador
jogador_altura = 60  # define a altura do jogador
jogador_x = LARGURA // 2 - jogador_largura // 2  # centraliza o jogador no eixo X
jogador_y = ALTURA - 100  # posiciona o jogador no eixo Y
velocidade_jogador = 6  # define a velocidade do jogador

vidas = 10  # define a quantidade inicial de vidas
pontos = 0  # define a pontuação inicial

# -----------------------------  
# Classe Inimigo  
# -----------------------------  
class Inimigo:  # classe que representa o inimigo
    def __init__(self):  # construtor da classe
        self.largura = 50  # largura do inimigo
        self.altura = 50  # altura do inimigo
        self.resetar()  # chama a função de reposicionamento

    def resetar(self):  # função para reposicionar o inimigo
        self.x = random.randint(0, LARGURA - self.largura)  # sorteia a posição X
        self.y = random.randint(-300, -50)  # sorteia a posição Y acima da tela
        self.vel = random.randint(8, 10)  # sorteia a velocidade do inimigo

    def mover(self):  # função que move o inimigo
        self.y += self.vel  # move o inimigo para baixo

    def desenhar(self):  # função que desenha o inimigo
        pygame.draw.rect(tela, VERMELHO, (self.x, self.y, self.largura, self.altura))  # desenha o inimigo

    def get_rect(self):  # função que retorna o retângulo do inimigo
        return pygame.Rect(self.x, self.y, self.largura, self.altura)  # devolve a área do inimigo

# -----------------------------  
# Classe Tiro  
# -----------------------------  
class Tiro:  # classe que representa o tiro
    def __init__(self, x, y):  # construtor da classe
        self.x = x  # guarda a posição X do tiro
        self.y = y  # guarda a posição Y do tiro
        self.largura = 6  # define a largura do tiro
        self.altura = 18  # define a altura do tiro
        self.vel = 15  # define a velocidade do tiro

    def mover(self):  # função que move o tiro
        self.y -= self.vel  # move o tiro para cima

    def desenhar(self):  # função que desenha o tiro
        pygame.draw.rect(tela, AMARELO, (self.x, self.y, self.largura, self.altura))  # desenha o tiro amarelo

    def get_rect(self):  # função que retorna o retângulo do tiro
        return pygame.Rect(self.x, self.y, self.largura, self.altura)  # devolve a área do tiro

inimigos = [Inimigo() for _ in range(5)]  # cria 5 inimigos
tiros = []  # cria uma lista vazia para armazenar os tiros

tempo_entre_tiros = 100  # define o intervalo mínimo entre tiros em milissegundos
ultimo_tiro = 0  # armazena o instante do último tiro

# -----------------------------  
# Loop principal  
# -----------------------------  
while True:  # inicia o loop principal do jogo
    for evento in pygame.event.get():  # percorre os eventos da janela
        if evento.type == pygame.QUIT:  # verifica se o usuário fechou a janela
            pygame.quit()  # encerra o pygame
            sys.exit()  # encerra o programa

        if evento.type == pygame.KEYDOWN:  # verifica se uma tecla foi pressionada
            if evento.key == pygame.K_SPACE:  # verifica se a tecla foi espaço
                agora = pygame.time.get_ticks()  # pega o tempo atual em milissegundos
                if agora - ultimo_tiro >= tempo_entre_tiros:  # verifica se já pode atirar de novo
                    tiro_x = jogador_x + jogador_largura // 2 - 3  # centraliza o tiro no jogador
                    tiro_y = jogador_y  # define a altura inicial do tiro
                    tiros.append(Tiro(tiro_x, tiro_y))  # cria o tiro e adiciona na lista
                    ultimo_tiro = agora  # atualiza o tempo do último tiro

    teclas = pygame.key.get_pressed()  # lê o teclado

    if teclas[pygame.K_LEFT] and jogador_x > 0:  # verifica movimento para a esquerda
        jogador_x -= velocidade_jogador  # move o jogador para a esquerda

    if teclas[pygame.K_RIGHT] and jogador_x < LARGURA - jogador_largura:  # verifica movimento para a direita
        jogador_x += velocidade_jogador  # move o jogador para a direita

    jogador_rect = pygame.Rect(jogador_x, jogador_y, jogador_largura, jogador_altura)  # cria o retângulo do jogador

    # -----------------------------  
    # Atualização dos tiros  
    # -----------------------------  
    for tiro in tiros[:]:  # percorre uma cópia da lista de tiros
        tiro.mover()  # move o tiro
        if tiro.y < 0:  # verifica se o tiro saiu da tela
            tiros.remove(tiro)  # remove o tiro da lista

    # -----------------------------  
    # Atualização dos inimigos e colisões  
    # -----------------------------  
    for inimigo in inimigos:  # percorre os inimigos
        inimigo.mover()  # move o inimigo

        if jogador_rect.colliderect(inimigo.get_rect()):  # verifica colisão entre jogador e inimigo
            vidas += 1  # diminui uma vida
            inimigo.resetar()  # reposiciona o inimigo

        elif inimigo.y > ALTURA:  # verifica se o inimigo passou da tela
            vidas -= 1  # diminui uma vida
            inimigo.resetar()  # reposiciona o inimigo

        for tiro in tiros[:]:  # percorre uma cópia da lista de tiros
            if tiro.get_rect().colliderect(inimigo.get_rect()):  # verifica colisão entre tiro e inimigo
                pontos += 10  # soma pontos
                inimigo.resetar()  # reposiciona o inimigo
                tiros.remove(tiro)  # remove o tiro que acertou
                break  # sai do laço interno

    if vidas <= 0:  # verifica se as vidas acabaram
        pygame.quit()  # encerra o pygame
        sys.exit()  # encerra o programa

    # -----------------------------  
    # Desenho na tela  
    # -----------------------------  
    tela.fill(BRANCO)  # preenche a tela com branco
    pygame.draw.rect(tela, AZUL, (jogador_x, jogador_y, jogador_largura, jogador_altura))  # desenha o jogador

    for tiro in tiros:  # percorre os tiros
        tiro.desenhar()  # desenha cada tiro

    for inimigo in inimigos:  # percorre os inimigos
        inimigo.desenhar()  # desenha cada inimigo

    desenhar_texto(f"Pontos: {pontos}", 20, 20)  # mostra a pontuação
    desenhar_texto(f"Vidas: {vidas}", 20, 60)  # mostra as vidas
    desenhar_texto(f"Tiros na tela: {len(tiros)}", 20, 100)  # mostra quantos tiros estão ativos

    pygame.display.flip()  # atualiza a tela
    clock.tick(60)  # mantém 60 quadros por segundo