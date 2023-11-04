from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np


class Musgo:
    def __init__(self, posicao):
        self.posicao_x, self.posicao_y, self.posicao_z = posicao
        self.mostrar = True
    
    def exibir(self):
        if self.mostrar:
            glPushMatrix()

            # cor marrom para o tronco
            glColor3f(34/255, 177/255, 76/255)

            glTranslatef(self.posicao_x, self.posicao_y, self.posicao_z)

            glScalef(0.7, 0.1, 0.7)
            glutSolidCube(1)

            glPopMatrix()
