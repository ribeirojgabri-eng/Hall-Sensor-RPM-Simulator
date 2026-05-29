import pygame
import math
import time
import sys

# Inicialização global
pygame.init()

LARGURA, ALTURA = 640, 480
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Concept S - Protótipo Sensor Hall Corrigido")

# Cores
COR_FUNDO = (15, 15, 15)
COR_EIXO = (100, 100, 100)
COR_IMA = (255, 50, 50)
COR_SENSOR_ATIVO = (0, 255, 100)
COR_SENSOR_INATIVO = (240, 240, 240)
COR_TEXTO = (240, 240, 240)
COR_REVCUT = (255, 0, 0)
COR_ALERTA = (255, 180, 0)

# Física e lógica
RPM_MAX = 6500.0
ACELERACAO_RPM_POR_SEGUNDO = 2500.0
DESACELERACAO_RPM_POR_SEGUNDO = 1800.0

velocidade_rpm = 0.0
angulo_total = 0.0          # Ângulo acumulado, não limitado a 360
rotacoes_contadas = 0       # Total de passagens pelo sensor
ultima_rotacao_inteira = 0  # Usado para detectar quantas voltas ocorreram entre frames

# Medição de RPM por contagem em janela de tempo
janela_medicao = 1.0
inicio_janela = time.perf_counter()
rotacoes_inicio_janela = 0
rpm_medido = 0.0

# Efeito visual do sensor
flash_sensor_ate = 0.0
DURACAO_FLASH_SENSOR = 0.05

fonte = pygame.font.SysFont("Arial", 24)
fonte_pequena = pygame.font.SysFont("Arial", 18)
clock = pygame.time.Clock()
ultimo_tempo = time.perf_counter()

print("Simulador inicializado. Segure ESPAÇO para acelerar. Feche a janela para sair.")

while True:
    agora = time.perf_counter()
    dt = agora - ultimo_tempo
    ultimo_tempo = agora

    # Evita saltos enormes se a janela travar ou for arrastada.
    dt = min(dt, 0.1)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_SPACE]:
        velocidade_rpm = min(
            velocidade_rpm + ACELERACAO_RPM_POR_SEGUNDO * dt,
            RPM_MAX
        )
    else:
        velocidade_rpm = max(
            velocidade_rpm - DESACELERACAO_RPM_POR_SEGUNDO * dt,
            0.0
        )

    # Conversão correta: RPM -> graus por segundo.
    # 1 rotação = 360 graus; RPM / 60 = rotações por segundo.
    graus_por_segundo = velocidade_rpm * 360.0 / 60.0
    angulo_total += graus_por_segundo * dt
    angulo_visual = angulo_total % 360.0

    # Contagem correta de rotações/passagens pelo sensor.
    # Em alta rotação, podem ocorrer mais de 1 passagem entre dois frames.
    rotacao_inteira_atual = int(angulo_total // 360.0)
    novas_rotacoes = rotacao_inteira_atual - ultima_rotacao_inteira

    if novas_rotacoes > 0:
        rotacoes_contadas += novas_rotacoes
        ultima_rotacao_inteira = rotacao_inteira_atual
        flash_sensor_ate = agora + DURACAO_FLASH_SENSOR

    # Mede o RPM real contado em uma janela de 1 segundo.
    if agora - inicio_janela >= janela_medicao:
        rotacoes_na_janela = rotacoes_contadas - rotacoes_inicio_janela
        rpm_medido = rotacoes_na_janela * 60.0 / (agora - inicio_janela)
        inicio_janela = agora
        rotacoes_inicio_janela = rotacoes_contadas

    # O sensor fica verde quando acabou de detectar passagem ou quando a marca está próxima.
    sensor_perto_do_zero = angulo_visual < 15.0 or angulo_visual > 345.0
    sensor_detectou_agora = agora < flash_sensor_ate
    cor_atual_sensor = COR_SENSOR_ATIVO if (sensor_perto_do_zero or sensor_detectou_agora) else COR_SENSOR_INATIVO

    # Desenho
    tela.fill(COR_FUNDO)
    centro = (LARGURA // 2, ALTURA // 2)

    pygame.draw.circle(tela, COR_EIXO, centro, 80, 2)

    rad = math.radians(angulo_visual)
    px = int(centro[0] + 80 * math.cos(rad))
    py = int(centro[1] + 80 * math.sin(rad))
    pygame.draw.line(tela, COR_IMA, centro, (px, py), 5)

    pygame.draw.rect(tela, cor_atual_sensor, (centro[0] + 90, centro[1] - 40, 10, 80))

    cor_hud = COR_REVCUT if velocidade_rpm >= 6400 else COR_SENSOR_ATIVO
    if abs(rpm_medido - velocidade_rpm) > 300 and velocidade_rpm > 1000:
        cor_rpm_medido = COR_ALERTA
    else:
        cor_rpm_medido = COR_SENSOR_ATIVO

    txt_rpm_alvo = fonte.render(f"RPM comandado: {int(velocidade_rpm)} / {int(RPM_MAX)}", True, cor_hud)
    txt_rpm_medido = fonte.render(f"RPM contado pelo sensor: {int(rpm_medido)}", True, cor_rpm_medido)
    txt_contagem = fonte.render(f"Passagens/rotações contadas: {rotacoes_contadas}", True, COR_TEXTO)
    txt_dica = fonte.render("SEGURE [ESPAÇO] PARA ACELERAR", True, COR_TEXTO)
    txt_obs = fonte_pequena.render("A 6500 RPM são ~108,33 passagens por segundo; a simulação conta matematicamente entre frames.", True, (160, 160, 160))

    tela.blit(txt_rpm_alvo, (30, 30))
    tela.blit(txt_rpm_medido, (30, 65))
    tela.blit(txt_contagem, (30, 100))
    tela.blit(txt_dica, (30, ALTURA - 70))
    tela.blit(txt_obs, (30, ALTURA - 35))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
