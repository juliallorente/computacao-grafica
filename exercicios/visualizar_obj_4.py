from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from objloader import OBJ
import time


# zoom e rotacionar campo de visão

yRot = 0.0
xRot = 0.0
zoom = 1

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


def teclas_especiais(key, x, y):
    global xRot, yRot, zoom
    if key == GLUT_KEY_LEFT:
        yRot -= 5.0

    if key == GLUT_KEY_RIGHT:
        yRot += 5.0

    if key == GLUT_KEY_UP:
        xRot -= 5.0

    if key == GLUT_KEY_DOWN:
        xRot += 5.0

    if key == GLUT_KEY_F1:
        zoom += 0.1

    if key == GLUT_KEY_F2:
        zoom -= 0.1

    yRot = int(yRot % 360)
    xRot = int(xRot % 360)

    glutPostRedisplay()


def renderizacao_cena():
    global zoom

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glPushMatrix()

    glTranslatef(0.0, -1.0, -5.0)
    glRotatef(yRot, 0.0, 1.0, 0.0)
    glRotatef(xRot, 1.0, 0.0, 0.0)

    glScalef(zoom, zoom, zoom)

    glTranslatef(0, 1, 0)

    obj = OBJ('livro.obj')

    glCallList(obj.gl_list)

    glPopMatrix()

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

    glClearColor(0.7, 0.8, 1.0, 0.0)

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow('Visualizar OBJ')
    glutReshapeFunc(mudar_tamanho_tela)
    glutSpecialFunc(teclas_especiais)
    glutDisplayFunc(renderizacao_cena)
    setup_rc()
    glutMainLoop()


if __name__ == '__main__':
    main()
