from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
from PIL import Image

from elementos.chao import Chao
from elementos.player import Player

import threading
import time


class Game:
    def __init__(self):
        self.rotacao_x = -90
        self.rotacao_y = 0
        self.zoom = 1
        self.posicao_camera_x = 0
        self.posicao_camera_y = -2
        self.posicao_camera_z = -10
        
        # self.look_at_x = 0
        # self.look_at_y = 10
        # self.look_at_z = 0
        
        self.posicao_mouse_x = None
        self.posicao_mouse_y = None

        self.frame_rate = 10
        
        self.player = Player(0.5, [-3.5, -1.75, 0], [3, 7])

        self.chao = Chao([10, 15], [0, 0, -7.5], self.player, self)

        self.texturas = []

        self.run()
    
    def run(self):
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(800, 600)
        glutCreateWindow('Game')
        self.texturas += [self.carregar_textura('texturas/grama_clara.jpg')]
        self.texturas += [self.carregar_textura('texturas/grama_escura.jpg')]
        self.texturas += [self.carregar_textura('texturas/agua.jpg')]
        self.texturas += [self.carregar_textura('texturas/asfalto.jpg')]
        self.texturas += [self.carregar_textura('texturas/tronco.jpg')]
        self.texturas += [self.carregar_textura('texturas/folhas.jpg')]
        glutReshapeFunc(self.mudar_tamanho_tela)
        glutKeyboardFunc(self.teclado)
        glutSpecialFunc(self.teclado_especial)
        # glutPassiveMotionFunc(self.mouse)  # para atualizar mouse sem segurar clique
        glutMotionFunc(self.mouse)
        glutDisplayFunc(self.renderizacao_cena)
        self.setup_rc()
        glutMainLoop()

    @staticmethod
    def carregar_textura(caminho_imagem):
        image = Image.open(caminho_imagem)

        dados_imagem = np.array(list(image.getdata()), np.uint8)

        glEnable(GL_TEXTURE_2D)

        textura = glGenTextures(1)

        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

        glBindTexture(GL_TEXTURE_2D, textura)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB,
                    image.size[0], image.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, dados_imagem)

        codigo_erro = glGetError()

        if codigo_erro != GL_NO_ERROR:
            print('Erro para carregar textura')
            return -1

        return textura

    def usar_textura(self, numero_textura):
        if numero_textura > len(self.texturas):
            print('Numero da textura inválido')
            glDisable(GL_TEXTURE_2D)
        elif numero_textura < 0:
            glDisable(GL_TEXTURE_2D)
        else:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texturas[numero_textura])

    @staticmethod
    def colocar_textura(x, y, z, lista_faces_exibidas=[i for i in range(1, 6+1)]):
        x, y, z = x/2, y/2, z/2
        pontos = [
            [x, y, z],
            [x, y, -z],
            [x, -y, z],
            [x, -y, -z],
            [-x, y, z],
            [-x, y, -z],
            [-x, -y, z],
            [-x, -y, -z]
        ]

        glColor3f(255/255, 255/255, 255/255)

        # face 1

        if 1 in lista_faces_exibidas:
            glBegin(GL_QUADS)
            glTexCoord(0, 1)
            glVertex3f(pontos[6][0], pontos[6][1], pontos[6][2])
            glTexCoord(1, 1)
            glVertex3f(pontos[2][0], pontos[2][1], pontos[2][2])
            glTexCoord(1, 0)
            glVertex3f(pontos[0][0], pontos[0][1], pontos[0][2])
            glTexCoord(0, 0)
            glVertex3f(pontos[4][0], pontos[4][1], pontos[4][2])
            glEnd()

        # face 2

        if 2 in lista_faces_exibidas:
            glBegin(GL_QUADS)
            glTexCoord(0, 1)
            glVertex3f(pontos[2][0], pontos[2][1], pontos[2][2])
            glTexCoord(1, 1)
            glVertex3f(pontos[3][0], pontos[3][1], pontos[3][2])
            glTexCoord(1, 0)
            glVertex3f(pontos[1][0], pontos[1][1], pontos[1][2])
            glTexCoord(0, 0)
            glVertex3f(pontos[0][0], pontos[0][1], pontos[0][2])
            glEnd()

        # face 3

        if 3 in lista_faces_exibidas:
            glBegin(GL_QUADS)
            glTexCoord(0, 1)
            glVertex3f(pontos[3][0], pontos[3][1], pontos[3][2])
            glTexCoord(1, 1)
            glVertex3f(pontos[7][0], pontos[7][1], pontos[7][2])
            glTexCoord(1, 0)
            glVertex3f(pontos[5][0], pontos[5][1], pontos[5][2])
            glTexCoord(0, 0)
            glVertex3f(pontos[1][0], pontos[1][1], pontos[1][2])
            glEnd()

        # face 4

        if 4 in lista_faces_exibidas:
            glBegin(GL_QUADS)
            glTexCoord(0, 1)
            glVertex3f(pontos[7][0], pontos[7][1], pontos[7][2])
            glTexCoord(1, 1)
            glVertex3f(pontos[6][0], pontos[6][1], pontos[6][2])
            glTexCoord(1, 0)
            glVertex3f(pontos[4][0], pontos[4][1], pontos[4][2])
            glTexCoord(0, 0)
            glVertex3f(pontos[5][0], pontos[5][1], pontos[5][2])
            glEnd()

        # face 5

        if 5 in lista_faces_exibidas:
            glBegin(GL_QUADS)
            glTexCoord(0, 1)
            glVertex3f(pontos[4][0], pontos[4][1], pontos[4][2])
            glTexCoord(1, 1)
            glVertex3f(pontos[0][0], pontos[0][1], pontos[0][2])
            glTexCoord(1, 0)
            glVertex3f(pontos[1][0], pontos[1][1], pontos[1][2])
            glTexCoord(0, 0)
            glVertex3f(pontos[5][0], pontos[5][1], pontos[5][2])
            glEnd()

        # face 6

        if 6 in lista_faces_exibidas:
            glBegin(GL_QUADS)
            glTexCoord(0, 1)
            glVertex3f(pontos[6][0], pontos[6][1], pontos[6][2])
            glTexCoord(1, 1)
            glVertex3f(pontos[2][0], pontos[2][1], pontos[2][2])
            glTexCoord(1, 0)
            glVertex3f(pontos[3][0], pontos[3][1], pontos[3][2])
            glTexCoord(0, 0)
            glVertex3f(pontos[7][0], pontos[7][1], pontos[7][2])
            glEnd()

    @staticmethod
    def colocar_planos(x, y, z, r, g, b, lista_faces_exibidas=[i for i in range(1, 6+1)]):
        x, y, z = x/2, y/2, z/2
        pontos = [
            [x, y, z],
            [x, y, -z],
            [x, -y, z],
            [x, -y, -z],
            [-x, y, z],
            [-x, y, -z],
            [-x, -y, z],
            [-x, -y, -z]
        ]

        glColor3f(r, g, b)

        # face 1

        if 1 in lista_faces_exibidas:
            glBegin(GL_QUADS)
            glVertex3f(pontos[6][0], pontos[6][1], pontos[6][2])
            glVertex3f(pontos[2][0], pontos[2][1], pontos[2][2])
            glVertex3f(pontos[0][0], pontos[0][1], pontos[0][2])
            glVertex3f(pontos[4][0], pontos[4][1], pontos[4][2])
            glEnd()

        # face 2

        if 2 in lista_faces_exibidas:
            glBegin(GL_QUADS)
            glVertex3f(pontos[2][0], pontos[2][1], pontos[2][2])
            glVertex3f(pontos[3][0], pontos[3][1], pontos[3][2])
            glVertex3f(pontos[1][0], pontos[1][1], pontos[1][2])
            glVertex3f(pontos[0][0], pontos[0][1], pontos[0][2])
            glEnd()

        # face 3

        if 3 in lista_faces_exibidas:
            glBegin(GL_QUADS)
            glVertex3f(pontos[3][0], pontos[3][1], pontos[3][2])
            glVertex3f(pontos[7][0], pontos[7][1], pontos[7][2])
            glVertex3f(pontos[5][0], pontos[5][1], pontos[5][2])
            glVertex3f(pontos[1][0], pontos[1][1], pontos[1][2])
            glEnd()

        # face 4

        if 4 in lista_faces_exibidas:
            glBegin(GL_QUADS)
            glVertex3f(pontos[7][0], pontos[7][1], pontos[7][2])
            glVertex3f(pontos[6][0], pontos[6][1], pontos[6][2])
            glVertex3f(pontos[4][0], pontos[4][1], pontos[4][2])
            glVertex3f(pontos[5][0], pontos[5][1], pontos[5][2])
            glEnd()

        # face 5

        if 5 in lista_faces_exibidas:
            glBegin(GL_QUADS)
            glVertex3f(pontos[4][0], pontos[4][1], pontos[4][2])
            glVertex3f(pontos[0][0], pontos[0][1], pontos[0][2])
            glVertex3f(pontos[1][0], pontos[1][1], pontos[1][2])
            glVertex3f(pontos[5][0], pontos[5][1], pontos[5][2])
            glEnd()

        # face 6

        if 6 in lista_faces_exibidas:
            glBegin(GL_QUADS)
            glVertex3f(pontos[6][0], pontos[6][1], pontos[6][2])
            glVertex3f(pontos[2][0], pontos[2][1], pontos[2][2])
            glVertex3f(pontos[3][0], pontos[3][1], pontos[3][2])
            glVertex3f(pontos[7][0], pontos[7][1], pontos[7][2])
            glEnd()

    def mudar_tamanho_tela(self, largura, altura):
        if altura == 0:
            altura = 1

        glViewport(0, 0, largura, altura)

        f_aspect = largura/altura

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        gluPerspective(35.0, f_aspect, 1.0, 40.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def recomecar_jogo(self):
        self.rotacao_x = -90
        self.rotacao_y = 0
        self.zoom = 1

        self.posicao_camera_x = 0
        self.posicao_camera_y = -2
        self.posicao_camera_z = -10

        self.player.posicao_x, self.player.posicao_y, self.player.posicao_z = [-3.5, -1.75, 0]
        self.player.posicao_chao_x, self.player.posicao_chao_y = [3, 7]

        self.chao.criar_matrizes()

    def teclado(self, tecla, *args):
        glutIgnoreKeyRepeat(True)
        tecla = tecla.decode('utf-8')

        if tecla == '+':
            self.zoom += 0.1
        elif tecla == '-':
            self.zoom -= 0.1
        elif tecla.lower() == 'w':
            resultado = self.chao.mover('frente')
            if resultado == 'mover':
                self.chao.avancar()
                self.posicao_camera_z += 1
                self.player.posicao_x -= 1
                self.player.posicao_chao_x += 1
                self.player.trocar_cor()
            elif resultado == 'fim_de_jogo':
                self.chao.avancar()
                self.posicao_camera_z += 1
                self.player.posicao_x -= 1
                self.player.posicao_chao_x += 1
                self.player.trocar_cor()
                self.recomecar_jogo()
            elif resultado == 'objeto_desconhecido':
                print('objeto_desconhecido')
            
        elif tecla.lower() == 'a':
            resultado = self.chao.mover('esquerda')
            if resultado == 'mover':
                self.player.posicao_z += 1
                self.player.posicao_chao_y += 1
                self.player.trocar_cor()
            elif resultado == 'fim_de_jogo':
                self.player.posicao_z += 1
                self.player.posicao_chao_y += 1
                self.player.trocar_cor()
                self.recomecar_jogo()
            elif resultado == 'objeto_desconhecido':
                print('objeto_desconhecido')
            
        elif tecla.lower() == 's':
            resultado = self.chao.mover('tras')
            if resultado == 'mover':
                self.posicao_camera_z -= 1
                self.player.posicao_x += 1
                self.player.posicao_chao_x -= 1
                self.player.trocar_cor()
            elif resultado == 'fim_de_jogo':
                self.posicao_camera_z -= 1
                self.player.posicao_x += 1
                self.player.posicao_chao_x -= 1
                self.player.trocar_cor()
                self.recomecar_jogo()
            elif resultado == 'objeto_desconhecido':
                print('objeto_desconhecido')

        elif tecla.lower() == 'd':
            resultado = self.chao.mover('direita')
            if resultado == 'mover':
                self.player.posicao_z -= 1
                self.player.posicao_chao_y -= 1
                self.player.trocar_cor()
            elif resultado == 'fim_de_jogo':
                self.player.posicao_z -= 1
                self.player.posicao_chao_y -= 1
                self.player.trocar_cor()
                self.recomecar_jogo()
            elif resultado == 'objeto_desconhecido':
                print('objeto_desconhecido')

        elif tecla.lower() == ' ':
            print("espaço não implementado (copiar 'w')")

        elif tecla.lower() == 'z':
            self.posicao_camera_y += 0.1
        
        elif tecla.lower() == 'x':
            self.posicao_camera_y -= 0.1

        glutPostRedisplay()

    def teclado_especial(self, tecla, *args):
        glutIgnoreKeyRepeat(False)
        if tecla == GLUT_KEY_UP:
            self.posicao_camera_z += 0.1
        elif tecla == GLUT_KEY_DOWN:
            self.posicao_camera_z -= 0.1
        elif tecla == GLUT_KEY_LEFT:
            self.posicao_camera_x += 0.1
        elif tecla == GLUT_KEY_RIGHT:
            self.posicao_camera_x -= 0.1

        print(self.posicao_camera_x)
        print(self.posicao_camera_y)
        print(self.posicao_camera_z)

        glutPostRedisplay()

    def mouse(self, posicao_atual_x, posicao_atual_y):
        if self.posicao_mouse_x is not None:
            if posicao_atual_x > self.posicao_mouse_x:
                self.rotacao_x += 1
            elif posicao_atual_x < self.posicao_mouse_x:
                self.rotacao_x -= 1
        
        if self.posicao_mouse_y is not None:
            if posicao_atual_y > self.posicao_mouse_y:
                self.rotacao_y += 1
            if posicao_atual_y < self.posicao_mouse_y:
                self.rotacao_y -= 1

        self.posicao_mouse_x = posicao_atual_x
        self.posicao_mouse_y = posicao_atual_y

        # fazer: se 360 entao 0, se 0 entao 360, pro angulo sempre ser entre 0 e 360

        glutPostRedisplay()

    def renderizacao_cena(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glPushMatrix()

        glTranslatef(self.posicao_camera_x, self.posicao_camera_y, self.posicao_camera_z)
        glRotatef(self.rotacao_x, 0.0, 1.0, 0.0)
        glRotatef(self.rotacao_y, 1.0, 0.0, 0.0)
        # glRotatef(-10, 0.0, 0.0, 1.0)
        # glRotatef(-90+330, 0.0, 1.0, 0.0)
        # glRotatef(5, 1.0, 0.0, 0.0)

        glScalef(self.zoom, self.zoom, self.zoom)

        glPushMatrix()
        self.chao.exibir()
        glPopMatrix()

        glPushMatrix()
        self.player.exibir()
        glPopMatrix()
        
        glPopMatrix()

        glutSwapBuffers()

    def setup_rc(self):
        whiteLight = [0.05, 0.05, 0.05, 1.0]
        sourceLight = [0.25, 0.25, 0.25, 0.25]
        lightPos = [-1.0, 5.0, 5.0, 1.0]

        glEnable(GL_DEPTH_TEST)
        glFrontFace(GL_CCW)

        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, whiteLight)
        glLightfv(GL_LIGHT1, GL_AMBIENT, sourceLight)

        glLightfv(GL_LIGHT1, GL_POSITION, lightPos)
        glEnable(GL_LIGHT1)

        glEnable(GL_COLOR_MATERIAL)
        glClearDepth(1.0)

        glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)

        glClearColor(0.7, 0.8, 1.0, 0.0)
