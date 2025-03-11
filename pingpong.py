# Juego de Ping Pong

# Realizado por: Iker Diaz-Maroto, David Garcia y Roberto Carrascoso
# 1ºA CFGM SMR - Fundamentos de la Programación

# Importamos las bibliotecas necesarias para el juego
import pygame  # Biblioteca principal para crear juegos
from pygame.locals import *  # Importa constantes útiles de pygame
import random  # Para generar números aleatorios
import os.path  # Para manejar rutas de archivos

# Definimos el tamaño de la ventana del juego
VENTANA_HORIZONTAL = 1250
VENTANA_VERTICAL = 780
FPS = 144  # Fotogramas por segundo del juego

# Definimos colores que usaremos en el juego
BLANCO = (255,255,255)
NEGRO = (0, 0, 0)
GRIS_TRANSPARENTE = (128, 128, 128, 128)

# Cargamos la imagen de fondo
fondo = pygame.image.load("./assets/fondo.png")

# Configuración de velocidades iniciales y máximas
VELOCIDAD_INICIAL = 8.6  
INCREMENTO_VELOCIDAD = 0.4  
VELOCIDAD_MAXIMA = 25  
VELOCIDAD_PALA_INICIAL = 9.6  
VELOCIDAD_PALA_MAXIMA = 15  
INCREMENTO_VELOCIDAD_PALA = 0.7  

# Obtenemos la carpeta donde está el juego para cargar archivos
carpeta_juego = os.path.dirname(__file__)

# Función para cargar los sonidos del juego
def cargar_sonidos():
    pygame.mixer.init()
    sonidos = {
        'rebote': pygame.mixer.Sound(os.path.join(carpeta_juego, "./assets/rebote.mp3")),
        'error': pygame.mixer.Sound(os.path.join(carpeta_juego, "./assets/error.mp3")),
        'musica': os.path.join(carpeta_juego, "./assets/musica.mp3")
    }
    return sonidos

# Clase para la pelota del juego
class PelotaPong:
    def __init__(self, imagen, sonidos):
        # Inicializamos la pelota con su imagen y posición
        self.imagen = pygame.image.load(imagen).convert_alpha()
        self.ancho, self.alto = self.imagen.get_size()
        self.x = VENTANA_HORIZONTAL / 2 - self.ancho / 2
        self.y = VENTANA_VERTICAL / 2 - self.alto / 2 
        self.velocidad = VELOCIDAD_INICIAL 
        self.dir_x = 1 if random.random() > 0.5 else -1
        self.dir_y = 0.5 if random.random() > 0.5 else -0.5
        self.puntuacion1 = 0 
        self.puntuacion2 = 0 
        self.sonidos = sonidos

    def mover(self):
        # Movemos la pelota según su dirección y velocidad
        self.x += self.dir_x * self.velocidad
        self.y += self.dir_y * self.velocidad
    
    def rebotar(self):
        # Comprobamos si la pelota sale por los laterales o rebota en los bordes superior/inferior
        if self.x <= 0:
            self.reiniciar()
            self.puntuacion2 += 1
            self.sonidos['error'].play()
        elif self.x + self.ancho >= VENTANA_HORIZONTAL:
            self.reiniciar()
            self.puntuacion1 += 1 
            self.sonidos['error'].play()
        elif self.y <= 0 or self.y + self.alto >= VENTANA_VERTICAL:
            self.dir_y = -self.dir_y
            self.aumentar_velocidad()
            self.sonidos['rebote'].play()
    
    def reiniciar(self):
        # Reiniciamos la posición y velocidad de la pelota
        self.x = VENTANA_HORIZONTAL / 2 - self.ancho / 2
        self.y = VENTANA_VERTICAL / 2 - self.alto / 2
        self.velocidad = VELOCIDAD_INICIAL 
        self.dir_x = 1 if random.random() > 0.5 else -1
        self.dir_y = 0.5 if random.random() > 0.5 else -0.5
    
    def aumentar_velocidad(self):
        # Aumentamos la velocidad de la pelota hasta el máximo permitido
        if self.velocidad < VELOCIDAD_MAXIMA:
            self.velocidad += INCREMENTO_VELOCIDAD
        print(f"Velocidad actual de la pelota: {self.velocidad}")

# Clase para las raquetas del juego
class RaquetaPong:
    def __init__(self, sonidos):
        # Inicializamos la raqueta con su imagen y posición
        self.imagen = pygame.image.load(os.path.join(carpeta_juego, "./assets/raqueta.png")).convert_alpha()
        self.ancho, self.alto = self.imagen.get_size()
        self.x = 10
        self.y = VENTANA_VERTICAL / 2 - self.alto / 2 
        self.dir_y = 0
        self.velocidad = VELOCIDAD_PALA_INICIAL
        self.sonidos = sonidos 
    
    def mover1(self):
        # Movemos la raqueta del jugador 1 y evitamos que salga de la pantalla
        self.y += self.dir_y * self.velocidad
        if self.y <= 0:
            self.y = 0
        if self.y + self.alto >= VENTANA_VERTICAL:
            self.y = VENTANA_VERTICAL - self.alto
    
    def mover2(self):
        # Movemos la raqueta del jugador 2 y evitamos que salga de la pantalla
        self.y += self.dir_y * self.velocidad
        if self.y <= 0:
            self.y = 0
        if self.y + self.alto >= VENTANA_VERTICAL:
            self.y = VENTANA_VERTICAL - self.alto
    
    def aumentar_velocidad(self):
        # Aumentamos la velocidad de la raqueta hasta el máximo permitido
        if self.velocidad < VELOCIDAD_PALA_MAXIMA:
            self.velocidad += INCREMENTO_VELOCIDAD_PALA
            print(f"Velocidad actual de la paleta: {self.velocidad}")
    
    def golpear1(self, pelota):
        # Funcion para comprobar si la raqueta 1 golpea la pelota
        if (
            pelota.x < self.x + self.ancho
            and pelota.x > self.x
            and pelota.y + pelota.alto > self.y
            and pelota.y < self.y + self.alto
        ):
            pelota.dir_x = abs(pelota.dir_x)
            pelota.x = self.x + self.ancho
            pelota.aumentar_velocidad()
            self.aumentar_velocidad()
            self.sonidos['rebote'].play()
    # Funcion para comprobar si la raqueta 2 golpea la pelota
    def golpear2(self, pelota):
        if (
            pelota.x + pelota.ancho > self.x
            and pelota.x < self.x + self.ancho
            and pelota.y + pelota.alto > self.y
            and pelota.y < self.y + self.alto
        ):
            pelota.dir_x = -abs(pelota.dir_x)
            pelota.x = self.x - pelota.ancho
            pelota.aumentar_velocidad()
            self.aumentar_velocidad()
            self.sonidos['rebote'].play()

# Función para mostrar el mensaje de ganador
def mostrar_ganador(ventana, fuente, jugador):
    # Creamos una capa semitransparente para oscurecer el fondo
    overlay = pygame.Surface((VENTANA_HORIZONTAL, VENTANA_VERTICAL))
    overlay.fill(NEGRO)
    overlay.set_alpha(128)  # 50% de transparencia
    ventana.blit(overlay, (0, 0))  # Dibujamos la capa
    
    # Preparamos el texto del ganador
    texto = f"¡JUGADOR {jugador} HA GANADO!"
    letrero = fuente.render(texto, True, NEGRO)
    texto_rect = letrero.get_rect(center=(VENTANA_HORIZONTAL/2, VENTANA_VERTICAL/2 - 40))
    
    # Preparamos el texto de partida finalizada
    texto_final = "¡Partida finalizada!"
    letrero_final = fuente.render(texto_final, True, NEGRO)
    texto_final_rect = letrero_final.get_rect(center=(VENTANA_HORIZONTAL/2, VENTANA_VERTICAL/2 + 40))
    
    # Calculamos el tamaño del recuadro blanco
    padding = 40
    total_height = texto_rect.height + texto_final_rect.height + padding * 2
    max_width = max(texto_rect.width, texto_final_rect.width) + padding * 2
    
    # Creamos y posicionamos el recuadro blanco
    fondo_rect = pygame.Rect(0, 0, max_width, total_height)
    fondo_rect.center = (VENTANA_HORIZONTAL/2, VENTANA_VERTICAL/2)
    
    # Dibujamos el recuadro y los textos
    pygame.draw.rect(ventana, BLANCO, fondo_rect, border_radius=15)
    ventana.blit(letrero, texto_rect)
    ventana.blit(letrero_final, texto_final_rect)
    
    # Actualizamos la pantalla y esperamos 3 segundos
    pygame.display.flip()
    pygame.time.wait(3000)

# Función principal del juego
def main():
    pygame.init()  # Iniciamos pygame
    ventana = pygame.display.set_mode((VENTANA_HORIZONTAL, VENTANA_VERTICAL)) # Creamos la ventana
    pygame.display.set_caption("Ping Pong")  # Ponemos título a la ventana
    
    sonidos = cargar_sonidos()  # Cargamos los sonidos
    
    # Configuramos la música de fondo
    pygame.mixer.music.load(sonidos['musica'])
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    
    fuente = pygame.font.Font(None, 60) # Fuente para los textos
    
    # Creamos la pelota
    pelota = PelotaPong(os.path.join(carpeta_juego, "./assets/pelota.png"), sonidos)
    
    # Creamos la raqueta del jugador 1 (izquierda)
    raqueta_1 = RaquetaPong(sonidos)
    raqueta_1.x = 60
    
    # Creamos la raqueta del jugador 2 (derecha)
    raqueta_2 = RaquetaPong(sonidos)
    raqueta_2.x = VENTANA_HORIZONTAL - 60 - raqueta_2.ancho
    
    # Bucle principal del juego donde ejecutamos las funciones
    jugando = True
    while jugando:
        # Añadimos al bucle las funciones 
        pelota.mover()
        pelota.rebotar()
        raqueta_1.mover1()
        raqueta_2.mover2()
        raqueta_1.golpear1(pelota)
        raqueta_2.golpear2(pelota)
        
        # Dibujamos todos los elementos en la pantalla
        ventana.blit(fondo, [0, 0])
        ventana.blit(pelota.imagen, (pelota.x, pelota.y))
        ventana.blit(raqueta_1.imagen, (raqueta_1.x, raqueta_1.y))
        ventana.blit(raqueta_2.imagen, (raqueta_2.x, raqueta_2.y))
        
        # Dibujamos el marcador con borde
        texto = f"{pelota.puntuacion1} : {pelota.puntuacion2}"
        letrero = fuente.render(texto, True, NEGRO)
        texto_rect = letrero.get_rect(center=(VENTANA_HORIZONTAL/2, 60))
        
        # Dibujamos un fondo para el marcador
        fondo_rect = pygame.Rect(0, 0, texto_rect.width + 40, texto_rect.height + 20)
        fondo_rect.center = texto_rect.center
        pygame.draw.rect(ventana, BLANCO, fondo_rect, border_radius=15)
        
        # Dibujamos el texto del marcador
        ventana.blit(letrero, texto_rect)
        
        # Comprobamos si algún jugador ha ganado (llegar a 5 puntos)
        if pelota.puntuacion1 >= 5:
            mostrar_ganador(ventana, fuente, 1)
            jugando = False
        elif pelota.puntuacion2 >= 5:
            mostrar_ganador(ventana, fuente, 2)
            jugando = False
        
        # Actualizamos la pantalla
        pygame.display.flip()
        
        # Gestionamos los eventos (teclas, cierre de ventana, etc.)
        for evento in pygame.event.get():
            if evento.type == QUIT:
                jugando = False
            
            # Control de la raqueta 1 (W y S)
            if evento.type == KEYDOWN:
                if evento.key == K_w:
                    raqueta_1.dir_y = -1
                if evento.key == K_s:
                    raqueta_1.dir_y = 1
                
                # Control de la raqueta 2 (Flecha arriba y abajo)
                if evento.key == K_UP:
                    raqueta_2.dir_y = -1
                if evento.key == K_DOWN:
                    raqueta_2.dir_y = 1
            
            # Detenemos las raquetas al soltar las teclas
            if evento.type == KEYUP:
                if evento.key == K_w or evento.key == K_s:
                    raqueta_1.dir_y = 0
                if evento.key == K_UP or evento.key == K_DOWN:
                    raqueta_2.dir_y = 0
        
        # Controlamos la velocidad del juego
        pygame.time.Clock().tick(FPS)
    
    # Cerramos pygame al terminar
    pygame.quit()

# Ejecutamos la función principal
if __name__ == "__main__":
    main()  