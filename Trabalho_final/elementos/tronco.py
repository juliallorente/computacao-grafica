from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np


class Tronco:
    def __init__(self, posicao):
        self.posicao_x, self.posicao_y, self.posicao_z = posicao
        self.mostrar = True
    
    def exibir(self):
        if self.mostrar:
            glPushMatrix()

            # cor marrom para o tronco
            glColor3f(137/255, 85/255, 56/255)

            glTranslatef(self.posicao_x, self.posicao_y, self.posicao_z)

            glScalef(0.55, 0.2, 1)
            glutSolidCube(1)

            glPopMatrix()
