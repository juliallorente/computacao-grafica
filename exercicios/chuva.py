from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time
import random


particulas = [{'x': None, 'y': None} for _ in range(10000)]

gravidade = 3/10000

active_particles = 0


def mudar_tamanho_tela(width, height):
    if (height == 0):
        height = 1

    glViewport(0, 0, width, height)

    fAspect = width/height

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(35.0, fAspect, 1.0, 40.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def inicia_particulas():

  for value, i in enumerate(range(1, len(particulas), 2)):

    particulas[i-1]['x'] = -0.001*(value+1)
    particulas[i-1]['y'] = GLUT_WINDOW_WIDTH/GLUT_WINDOW_HEIGHT*2 - random.random()*10

    particulas[i]['x'] = 0.001*(value+1)
    particulas[i]['y'] = GLUT_WINDOW_WIDTH/GLUT_WINDOW_HEIGHT*2 - random.random()*10


def renderizacao_cena():
    global particulas, gravidade, active_particles

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glTranslatef(0, 0, -6)

    glBegin(GL_POINTS)

    glColor3f(63/255, 72/255, 204/255)

    if not active_particles:
        active_particles = 1
        inicia_particulas()
    
    for i in range(len(particulas)):
        particulas[i]['y'] -= gravidade*500

    time.sleep(1/pow(2,4))

    for i in range(len(particulas)):
        glVertex3f(particulas[i]['x'], particulas[i]['y'], 0)

    for i in range(len(particulas)):
        if particulas[i]['y'] <= -GLUT_WINDOW_WIDTH/GLUT_WINDOW_HEIGHT*2:
            particulas[i]['y'] = GLUT_WINDOW_WIDTH/GLUT_WINDOW_HEIGHT*2- random.random()*10

    glEnd()

    glutSwapBuffers()


def setup_rc():
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

    glClearColor(0/255, 0/255, 0/255, 0.0)


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH | GLUT_ALPHA)
    glutInitWindowSize(800, 300)
    glutInitWindowPosition(0, 0)
    glutCreateWindow('Chuva')
    glutReshapeFunc(mudar_tamanho_tela)
    glutDisplayFunc(renderizacao_cena)
    glutIdleFunc(renderizacao_cena)
    setup_rc()
    glutMainLoop()


if __name__ == '__main__':
    main()
