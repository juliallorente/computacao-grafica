from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np


class Cubo:
    def __init__(self, tamanho, posicao, cor, tipo, game, escala=[1, 1, 1]):
        self.tamanho = tamanho
        self.posicao_x, self.posicao_y, self.posicao_z = posicao
        self.cor_r, self.cor_g, self.cor_b = cor
        self.tipo = tipo
        self.game = game
        self.escala_x, self.escala_y, self.escala_z = escala
        self.mostrar = True
    
    def exibir(self):
        if self.mostrar:
            if self.tipo == 'grama_clara':
                glPushMatrix()
                glColor3f(1, 1, 1)
                glTranslatef(self.posicao_x, self.posicao_y, self.posicao_z)
                self.game.usar_textura(0)
                self.game.colocar_textura(1, 1, 1, [5])
                self.game.usar_textura(-1)
                self.game.colocar_planos(1, 1, 1, 137/255, 85/255, 56/255, [1, 2, 3, 4, 6])
                glPopMatrix()

            elif self.tipo == 'grama_escura':
                glPushMatrix()
                glColor3f(1, 1, 1)
                glTranslatef(self.posicao_x, self.posicao_y, self.posicao_z)
                self.game.usar_textura(1)
                self.game.colocar_textura(1, 1, 1, [5])
                self.game.usar_textura(-1)
                self.game.colocar_planos(1, 1, 1, 137/255, 85/255, 56/255, [1, 2, 3, 4, 6])
                glPopMatrix()

            elif self.tipo == 'agua':
                glPushMatrix()
                glColor3f(1, 1, 1)
                glTranslatef(self.posicao_x, self.posicao_y, self.posicao_z)
                self.game.usar_textura(2)
                self.game.colocar_textura(1, 1, 1, [5])
                self.game.usar_textura(-1)
                self.game.colocar_planos(1, 1, 1, 0/255, 162/255, 232/255, [1, 2, 3, 4, 6])
                glPopMatrix()

            elif self.tipo == 'asfalto':
                glPushMatrix()
                glColor3f(1, 1, 1)
                glTranslatef(self.posicao_x, self.posicao_y, self.posicao_z)
                self.game.usar_textura(3)
                self.game.colocar_textura(1, 1, 1, [5])
                self.game.usar_textura(-1)
                self.game.colocar_planos(1, 1, 1, 123/255, 123/255, 123/255, [1, 2, 3, 4, 6])
                glPopMatrix()
