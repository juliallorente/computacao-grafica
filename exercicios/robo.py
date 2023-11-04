from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


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

    pObj = gluNewQuadric()
    gluQuadricNormals(pObj, GLU_SMOOTH)

    glScalef(zoom, zoom, zoom)

    antena()

    cabeca()

    distx = 0.1

    olho(distx)

    olho(-distx)

    boca()

    corpo()

    distx, disty = 0.5/2, 0.6/2

    esfera_corpo(distx - 0.05, disty - 0.05)

    esfera_corpo(distx - 0.05, -disty)

    esfera_corpo(-distx + 0.05, disty - 0.05)

    esfera_corpo(-distx + 0.05, -disty)

    distx, ang = 0.5/2, 90

    braco_superior(distx - 0.05, ang, 1)
    braco_superior(-distx + 0.05, -ang, -1)

    distx = 0.5/2 + 0.35 * 1/2

    esfera_braco_superior_inferior(distx)
    esfera_braco_superior_inferior(-distx)

    distx, ang = 0.5/2 + 0.35 * 1/2, 90

    braco_inferior(distx - 0.05, ang, 1)
    braco_inferior(-distx + 0.05, -ang, -1)

    distx = 0.5/2 + 0.35 * 1/2 + 0.35*1/2

    mao(distx)
    mao(-distx)

    distx = 0.5/2 - 0.05

    perna_superior(distx)
    perna_superior(-distx)

    distx = 0.5/2

    esfera_perna_superior_inferior(distx - 0.05)
    esfera_perna_superior_inferior(-distx + 0.05)

    distx = 0.5/2 - 0.05

    perna_inferior(distx)
    perna_inferior(-distx)

    distx = 0.5/2 - 0.05

    pe(distx)
    pe(-distx)

    glPopMatrix()

    glutSwapBuffers()


def antena():
    glPushMatrix()

    glColor3f(122/255, 122/255, 122/255)
    glRotatef(90, 5, 0, 0)
    # (x, z, y)
    glTranslatef(0, 0, - 1 - 0.6/2 - 0.26 + 0.06)
    glutSolidCylinder(0.025, -0.5, 30, 30)

    glTranslatef(0, 0, - 1 - 0.6/2 - 0.26 + 0.06 + 1)
    glutSolidSphere(0.06, 30, 30)

    glPopMatrix()


def cabeca():
    glPushMatrix()

    glColor3f(122/255, 122/255, 122/255)
    glTranslatef(0, 1 + 0.6/2 + 0.3 - 0.06, 0)
    glutSolidSphere(0.26, 30, 30)

    glPopMatrix()


def olho(x):
    glPushMatrix()

    glColor3f(0/255, 0/255, 0/255)
    glTranslatef(x, 1 + 0.6/2 + 0.3 - 0.06 + 0.035, 0.2)
    glutSolidSphere(0.05, 30, 30)

    glPopMatrix()    


def boca():
    glPushMatrix()

    glColor3f(0/255, 0/255, 0/255)
    glTranslatef(0, 1 + 0.6/2 + 0.3 - 0.06 - 0.045, 0.18)
    glScalef(1, 0.5, 1)
    glutSolidSphere(0.1, 30, 30)

    glPopMatrix()    


def corpo():
    glPushMatrix()

    glColor3f(122/255, 122/255, 122/255)
    glTranslatef(0, 1, 0)
    glScalef(0.5, 0.6, 0.2)
    glutSolidCube(1)

    glPopMatrix()


def esfera_corpo(x, y):
    glPushMatrix()

    glColor3f(122/255, 122/255, 122/255)
    glTranslatef(x, 1 + y, 0)
    glutSolidSphere(0.11, 30, 30)

    glPopMatrix()


def braco_superior(x, ang, lado):
    glPushMatrix()

    glColor3f(122/255, 122/255, 122/255)
    # (x, z, y)
    glTranslatef(x, 1 + 0.6/2 - 0.05, 0)
    glRotatef(ang, 5, 0, 0)
    glRotatef(45, 0, 5, 0)
    glutSolidCylinder(0.09, lado*0.35, 30, 30)

    glPopMatrix()


def esfera_braco_superior_inferior(x):
    glPushMatrix()

    glColor3f(122/255, 122/255, 122/255)
    glTranslatef(x, 1 + 0.6/2 - 0.35*1/2 - 0.1, 0)
    glutSolidSphere(0.1, 30, 30)

    glPopMatrix()


def braco_inferior(x, ang, lado):
    glPushMatrix()

    glColor3f(122/255, 122/255, 122/255)
    # (x, z, y)
    glTranslatef(x, 1 + 0.6/2 - 0.35*1/2 - 0.05, 0)
    glRotatef(ang, 5, 0, 0)
    glRotatef(45, 0, 5, 0)
    glutSolidCylinder(0.09, lado*0.35, 30, 30)

    glPopMatrix() 


def perna_superior(x):
    glPushMatrix()

    glColor3f(122/255, 122/255, 122/255)
    glRotatef(90, 5, 0, 0)
    # (x, z, y)
    glTranslatef(x, 0, - 1 + 0.6/2)
    glutSolidCylinder(0.1, 0.5, 30, 30)

    glPopMatrix()


def esfera_perna_superior_inferior(x):
    glPushMatrix()

    glColor3f(122/255, 122/255, 122/255)
    glTranslatef(x, 1 - 0.6/2 - 0.5, 0)
    glutSolidSphere(0.11, 30, 30)

    glPopMatrix()


def mao(x):
    glPushMatrix()

    glColor3f(122/255, 122/255, 122/255)
    glTranslatef(x, 1 + 0.6/2 - 0.35*1/2 - 0.1 - 0.35*1/2, 0)
    glutSolidSphere(0.11, 30, 30)

    glPopMatrix()


def perna_inferior(x):
    glPushMatrix()

    glColor3f(122/255, 122/255, 122/255)
    glRotatef(90, 5, 0, 0)
    # (x, z, y)
    glTranslatef(x, 0, - 1 + 0.6/2 + 0.5)
    glutSolidCylinder(0.1, 0.5, 30, 30)

    glPopMatrix()


def pe(x):
    glPushMatrix()

    glColor3f(122/255, 122/255, 122/255)
    glTranslatef(x, 1 - 0.6/2 - 0.5 - 0.5, 0.03)
    glScalef(0.2, 0.1, 0.3)
    glutSolidCube(1)

    glPopMatrix()


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
    global texturas
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow('Robo')
    glutReshapeFunc(mudar_tamanho_tela)
    glutSpecialFunc(teclas_especiais)
    glutDisplayFunc(renderizacao_cena)
    setup_rc()
    glutMainLoop()


if __name__ == '__main__':
    main()