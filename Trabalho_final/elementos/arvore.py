from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np


class Arvore:
    def __init__(self, posicao):
        self.posicao_x, self.posicao_y, self.posicao_z = posicao
        self.mostrar = True
    
    def exibir(self):
        if self.mostrar:
            glPushMatrix()

            # cor marrom para o tronco
            glColor3f(137/255, 85/255, 56/255)

            glTranslatef(self.posicao_x, self.posicao_y, self.posicao_z)

            glScalef(0.8, 1.5, 0.8)
            glutSolidCube(1)
            
            glPushMatrix()

            # cor verde para as folhas
            glColor3f(34/255, 177/255, 76/255)

            glTranslatef(0, 0.75, 0)

            glScalef(1/0.8, 1/1.5, 1/0.8)
            glutSolidCube(1)

            glPopMatrix()

            glPopMatrix()
