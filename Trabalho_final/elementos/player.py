from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np


class Player:
    def __init__(self, tamanho, posicao, posicao_chao, atualizar_cor=False):
        self.tamanho = tamanho
        self.posicao_x, self.posicao_y, self.posicao_z = posicao
        self.posicao_chao_x, self.posicao_chao_y = posicao_chao
        self.mostrar = True
        self.count = 0
        self.atualizar_cor = atualizar_cor
    
    def trocar_cor(self):
        if self.atualizar_cor:
            if self.count == 0:
                self.count = 1
            else:
                self.count = 0

    def exibir(self):
        if self.mostrar:
            glPushMatrix()
            
            if self.count == 0:
                glColor3f(0/255, 0/255, 0/255)
            else:
                glColor3f(255/255, 255/255, 255/255)

            glTranslatef(self.posicao_x, self.posicao_y, self.posicao_z)
            glutSolidCube(self.tamanho)

            glPushMatrix()

            glTranslatef(0, 0.5, 0)
            
            if self.count == 0:
                glColor3f(255/255, 255/255, 255/255)
            else:
                glColor3f(0/255, 0/255, 0/255)

            glutSolidCube(self.tamanho)

            glPopMatrix()

            glPopMatrix()
