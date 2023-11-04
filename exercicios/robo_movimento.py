from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time


# zoom e rotacionar campo de visão

yRot = 0.0
xRot = 0.0
zoom = 1

# variaveis de rotacao globais

zoom_braco_esquerdo_superior = 0
zoom_braco_esquerdo_inferior = 0
zoom_braco_direito_superior = 0
zoom_braco_direito_inferior = 0
zoom_perna_esquerda_superior = 0
zoom_perna_esquerda_inferior = 0
zoom_perna_direita_superior = 0
zoom_perna_direita_inferior = 0


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

    # pObj = gluNewQuadric()
    # gluQuadricNormals(pObj, GLU_SMOOTH)

    glScalef(zoom, zoom, zoom)

    corpo()

    # distx = 0.5/2 + 0.35 * 1/2 + 0.35*1/2

    # mao(distx)
    # mao(-distx)

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

    # verificar

    # distx = 0.5/2 + 0.35 * 1/2

    # esfera_braco_superior_inferior(distx)

    # esfera_braco_superior_inferior(-distx)

    antena()

    cabeca()

    distx = 0.1

    olho(distx)

    olho(-distx)

    boca()

    # distx, disty = 0.5/2, 0.6/2

    # esfera_corpo(distx - 0.05, disty - 0.05)

    # esfera_corpo(-distx + 0.05, disty - 0.05)

    distx = 0.5/2 - 0.05

    glColor3f(122/255, 122/255, 122/255)
    glTranslatef(0, 1, 0)
    glScalef(0.5, 0.6, 0.2)
    glutSolidCube(1)
    glScalef(1/0.5, 1/0.6, 1/0.2) # resetar escala

    distx, ang = 0.5/2, 90

    braco_superior(tipo='esquerda')

    braco_superior(tipo='direita')

    perna_superior(distx, 'esquerda')

    perna_superior(distx, 'direita')

    glPopMatrix()


def esfera_corpo(x, y):
    glPushMatrix()

    glColor3f(122/255, 122/255, 122/255)
    glTranslatef(x, 1 + y, 0)
    glutSolidSphere(0.11, 30, 30)

    glPopMatrix()


def braco_superior(tipo):
    global zoom_braco_esquerdo_superior, zoom_braco_direito_superior

    glPushMatrix()

    glColor3f(122/255, 122/255, 122/255)
    # (x, z, y)
    if tipo == 'esquerda':
        glTranslatef(0.5/2, 0.6/2 - 0.05, 0)
        glRotatef(90, 5, 0, 0)
        glRotatef(45+zoom_braco_esquerdo_superior, 0, 5, 0)
        glutSolidSphere(0.11, 30, 30)
        glutSolidCylinder(0.09, 0.35, 30, 30)
        glTranslatef(0, 0, 0.35)
        glutSolidSphere(0.11, 30, 30)
        braco_inferior('esquerda')
    elif tipo == 'direita':
        glTranslatef(-0.5/2, 0.6/2 - 0.05, 0)
        glRotatef(-90, 5, 0, 0)
        glRotatef(45+zoom_braco_direito_superior, 0, 5, 0)
        glutSolidSphere(0.11, 30, 30)
        glutSolidCylinder(0.09, -0.35, 30, 30)
        glTranslatef(0, 0, -0.35)
        glutSolidSphere(0.11, 30, 30)
        braco_inferior('direita')


    glPopMatrix()


def braco_inferior(tipo):
    global zoom_braco_esquerdo_inferior, zoom_braco_direito_inferior

    glPushMatrix()

    glColor3f(122/255, 122/255, 122/255)
    if tipo == 'esquerda':
        glRotatef(zoom_braco_esquerdo_inferior, 0, 5, 0)
        glutSolidCylinder(0.09, 0.35, 30, 30)
        glTranslatef(0, 0, 0.35)
        glutSolidSphere(0.11, 30, 30)
    elif tipo == 'direita':
        glRotatef(zoom_braco_direito_inferior, 0, 5, 0)
        glutSolidCylinder(0.09, -0.35, 30, 30)
        glTranslatef(0, 0, -0.35)
        glutSolidSphere(0.11, 30, 30)

    glPopMatrix() 


def perna_superior(x, tipo):
    global zoom_perna_esquerda_superior, zoom_perna_direita_superior

    glPushMatrix()

    glColor3f(122/255, 122/255, 122/255)
    glRotatef(90, 5, 0, 0)

    if tipo == 'esquerda':
        glRotatef(zoom_perna_esquerda_superior, 5, 0, 0)
        # (x, z, y)
        glTranslatef(-x, 0, 0.6/2)
        glutSolidSphere(0.11, 30, 30)
        glutSolidCylinder(0.1, 0.5, 30, 30)
        esfera_perna_superior_inferior()
        perna_inferior('esquerda')
    elif tipo == 'direita':
        glRotatef(zoom_perna_direita_superior, 5, 0, 0)
        # (x, z, y)
        glTranslatef(x, 0, 0.6/2)
        glutSolidSphere(0.11, 30, 30)
        glutSolidCylinder(0.1, 0.5, 30, 30)
        esfera_perna_superior_inferior()
        perna_inferior('direita')

    glPopMatrix()


def esfera_perna_superior_inferior():
    glPushMatrix()

    glColor3f(122/255, 122/255, 122/255)
    glTranslatef(0, 0, 0.5)
    glutSolidSphere(0.11, 30, 30)

    glPopMatrix()


def perna_inferior(tipo):
    global zoom_perna_esquerda_inferior, zoom_perna_direita_inferior

    glPushMatrix()

    glColor3f(122/255, 122/255, 122/255)

    if tipo == 'esquerda':
        glRotatef(zoom_perna_esquerda_inferior, 5, 0, 0)
         # (x, z, y)
        glTranslatef(0, 0, 0.5)
        glutSolidCylinder(0.1, 0.5, 30, 30)
        pe()
    elif tipo == 'direita':
        glRotatef(zoom_perna_direita_inferior, 5, 0, 0)
         # (x, z, y)
        glTranslatef(0, 0, 0.5)
        glutSolidCylinder(0.1, 0.5, 30, 30)
        pe()

    glPopMatrix()


def pe():
    glPushMatrix()

    glColor3f(122/255, 122/255, 122/255)
    glTranslatef(0, 0, 0.5)
    glScalef(0.2, 0.3, 0.1)
    glutSolidCube(1)
    glScalef(1/0.2, 1/0.1, 1/0.3)

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


orientacao_bes = True # add == True and sub == False
orientacao_bei = True # add == True and sub == False

def movimento_nao_ciclico_abanar_braco_esquerdo(min, max):
    global zoom_braco_esquerdo_superior
    global zoom_braco_esquerdo_inferior
    global orientacao_bes
    global orientacao_bei

    angulo_minimo_braco_esquerdo_superior = min
    angulo_maximo_braco_esquerdo_superior = max

    # braco superior
    if orientacao_bes: # aumentar o angulo
        zoom_braco_esquerdo_superior += 2
        if zoom_braco_esquerdo_superior >= angulo_maximo_braco_esquerdo_superior:
            orientacao_bes = False
    else: # diminuir o angulo
        zoom_braco_esquerdo_superior -= 2
        if zoom_braco_esquerdo_superior <= angulo_minimo_braco_esquerdo_superior:
            orientacao_bes = True

    angulo_minimo_braco_esquerdo_inferior = min
    angulo_maximo_braco_esquerdo_inferior = max

    # braco inferior
    if orientacao_bei: # aumentar o angulo
        zoom_braco_esquerdo_inferior += 2
        if zoom_braco_esquerdo_inferior >= angulo_maximo_braco_esquerdo_inferior:
            orientacao_bei = False
    else: # diminuir o angulo
        zoom_braco_esquerdo_inferior -= 2
        if zoom_braco_esquerdo_inferior <= angulo_minimo_braco_esquerdo_inferior:
            orientacao_bei = True


orientacao_bds = True # add == True and sub == False
orientacao_bdi = True # add == True and sub == False

def movimento_nao_ciclico_abanar_braco_direito(min, max):
    global zoom_braco_direito_superior
    global zoom_braco_direito_inferior
    global orientacao_bds
    global orientacao_bdi

    angulo_minimo_braco_direito_superior = min
    angulo_maximo_braco_direito_superior = max

    # braco superior
    if orientacao_bds: # aumentar o angulo
        zoom_braco_direito_superior += 2
        if zoom_braco_direito_superior >= angulo_maximo_braco_direito_superior:
            orientacao_bds = False
    else: # diminuir o angulo
        zoom_braco_direito_superior -= 2
        if zoom_braco_direito_superior <= angulo_minimo_braco_direito_superior:
            orientacao_bds = True

    angulo_minimo_braco_direito_inferior = min
    angulo_maximo_braco_direito_inferior = max

    # braco inferior
    if orientacao_bdi: # aumentar o angulo
        zoom_braco_direito_inferior += 2
        if zoom_braco_direito_inferior >= angulo_maximo_braco_direito_inferior:
            orientacao_bdi = False
    else: # diminuir o angulo
        zoom_braco_direito_inferior -= 2
        if zoom_braco_direito_inferior <= angulo_minimo_braco_direito_inferior:
            orientacao_bdi = True


orientacao_pes = True # add == True and sub == False
orientacao_pei = True # add == True and sub == False
orientacao_pds = False # add == True and sub == False
orientacao_pdi = False # add == True and sub == False

def movimento_ciclico_correr():
    global zoom_perna_esquerda_superior
    global zoom_perna_esquerda_inferior
    global zoom_perna_direita_superior
    global zoom_perna_direita_inferior

    global orientacao_pes
    global orientacao_pei
    global orientacao_pds
    global orientacao_pdi

    angulo_minimo_perna_superior = -10
    angulo_maximo_perna_superior = 10

    # perna superior
    if orientacao_pes: # diminuir o angulo
        zoom_perna_esquerda_superior -= 2
        if zoom_perna_esquerda_superior <= angulo_minimo_perna_superior:
            orientacao_pes = False
    else: # aumentar o angulo
        zoom_perna_esquerda_superior += 2
        if zoom_perna_esquerda_superior >= angulo_maximo_perna_superior:
            orientacao_pes = True

    # perna superior
    if orientacao_pds: # diminuir o angulo
        zoom_perna_direita_superior -= 2
        if zoom_perna_direita_superior <= angulo_minimo_perna_superior:
            orientacao_pds = False
    else: # aumentar o angulo
        zoom_perna_direita_superior += 2
        if zoom_perna_direita_superior >= angulo_maximo_perna_superior:
            orientacao_pds = True

    angulo_minimo_perna_inferior = -10
    angulo_maximo_perna_inferior = 10

    # perna inferior
    if orientacao_pei: # diminuir o angulo
        zoom_perna_esquerda_inferior -= 2
        if zoom_perna_esquerda_inferior <= angulo_minimo_perna_inferior:
            orientacao_pei = False
    else: # aumentar o angulo
        zoom_perna_esquerda_inferior += 2
        if zoom_perna_esquerda_inferior >= angulo_maximo_perna_inferior:
            orientacao_pei = True

    # perna superior
    if orientacao_pdi: # diminuir o angulo
        zoom_perna_direita_inferior -= 2
        if zoom_perna_direita_inferior <= angulo_minimo_perna_inferior:
            orientacao_pdi = False
    else: # aumentar o angulo
        zoom_perna_direita_inferior += 2
        if zoom_perna_direita_inferior >= angulo_maximo_perna_inferior:
            orientacao_pdi = True


def teclado(tecla, x, y):
    global zoom_braco_esquerdo_superior
    global zoom_braco_esquerdo_inferior
    global zoom_braco_direito_superior
    global zoom_braco_direito_inferior
    global zoom_perna_esquerda_superior
    global zoom_perna_esquerda_inferior
    global zoom_perna_direita_superior
    global zoom_perna_direita_inferior
    
    tecla = tecla.decode('utf-8')

    if tecla == 'z':
        movimento_nao_ciclico_abanar_braco_esquerdo(-10, 80)
        movimento_nao_ciclico_abanar_braco_direito(-10, 80)
    if tecla == 'x':
        movimento_nao_ciclico_abanar_braco_esquerdo(-10, 0)
        movimento_nao_ciclico_abanar_braco_direito(-10, 0)
        movimento_ciclico_correr()
    if tecla == 'q':
        zoom_braco_esquerdo_superior -= 2
    if tecla == 'w':
        zoom_braco_esquerdo_inferior -= 2
    if tecla == 'e':
        zoom_braco_direito_superior -= 2
    if tecla == 'r':
        zoom_braco_direito_inferior -= 2
    if tecla == 't':
        zoom_perna_esquerda_superior -= 2
        print(zoom_perna_esquerda_superior)
    if tecla == 'y':
        zoom_perna_esquerda_inferior -= 2
    if tecla == 'u':
        zoom_perna_direita_superior -= 2
    if tecla == 'i':
        zoom_perna_direita_inferior -= 2
    if tecla == 'a':
        zoom_braco_esquerdo_superior += 2
    if tecla == 's':
        zoom_braco_esquerdo_inferior += 2
    if tecla == 'd':
        zoom_braco_direito_superior += 2
    if tecla == 'f':
        zoom_braco_direito_inferior += 2
    if tecla == 'g':
        zoom_perna_esquerda_superior += 2
        print(zoom_perna_esquerda_superior)
    if tecla == 'h':
        zoom_perna_esquerda_inferior += 2
    if tecla == 'j':
        zoom_perna_direita_superior += 2
    if tecla == 'k':
        zoom_perna_direita_inferior += 2

    glutPostRedisplay()


def main():
    global texturas
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow('Robo')
    glutReshapeFunc(mudar_tamanho_tela)
    glutSpecialFunc(teclas_especiais)
    glutDisplayFunc(renderizacao_cena)
    glutKeyboardFunc(teclado)
    setup_rc()
    glutMainLoop()


if __name__ == '__main__':
    main()