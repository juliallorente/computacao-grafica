from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
from PIL import Image


texturas = []
yRot = 0.0
xRot = 0.0
zoom = 1


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


def usar_textura(numero_textura):
    global texturas

    if numero_textura > len(texturas):
        print('Numero da textura inválido')
        glDisable(GL_TEXTURE_2D)
    elif numero_textura < 0:
        glDisable(GL_TEXTURE_2D)
    else:
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, texturas[numero_textura])


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

    agua()

    chao()

    cubo_tijolo()

    translate_tower = 1-0.15
    criar_torre(pObj, translate_tower, 0.0, translate_tower)
    criar_torre(pObj, -translate_tower, 0.0, translate_tower)
    criar_torre(pObj, translate_tower, 0.0, -translate_tower)
    criar_torre(pObj, -translate_tower, 0.0, -translate_tower)

    torre_central(pObj)

    criar_janela(90, 90)  # direita
    criar_janela(270, 270)  # esquerda
    criar_janela(180, 180)  # trás

    criar_porta()

    criar_arvore(pObj, 1.5, 1.5)
    criar_arvore(pObj, 1.5, -1.5)
    criar_arvore(pObj, -1.5, 1.5)
    criar_arvore(pObj, -1.5, -1.5)

    glPopMatrix()

    glutSwapBuffers()


def agua():
    glPushMatrix()
    glColor3f(1, 1, 1)
    glTranslatef(0, -0.1, 0)
    usar_textura(4)
    colocar_textura(8, 0.15, 8, [5])
    usar_textura(-1)
    colocar_planos(8, 0.15, 8, 0/255, 162/255, 232/255, [1, 2, 3, 4, 6])
    glPopMatrix()


def chao():
    glPushMatrix()
    glColor3f(1, 1, 1)
    glTranslatef(0, 0, 0)
    usar_textura(1)
    colocar_textura(6, 0.1, 6, [5])
    usar_textura(-1)
    colocar_planos(6, 0.1, 6, 100/255, 65/255, 33/255, [1, 2, 3, 4])
    glPopMatrix()


def cubo_tijolo():
    glPushMatrix()
    glColor3f(1, 1, 1)
    glTranslatef(0, 0.8, 0)
    usar_textura(0)
    colocar_textura(1.6, 1.6, 1.6)
    glPopMatrix()


def criar_torre(pObj, posx, posy, posz):
    glColor3f(221/255, 100/255, 173/255)
    glPushMatrix()
    glTranslatef(posx, posy, posz)
    glRotatef(-90.0, 5.0, 0.0, 0.0)
    gluCylinder(pObj, 0.3, 0.3, 1.8, 26, 13)
    glPopMatrix()

    glColor3f(0/255, 0/255, 0/255)
    glPushMatrix()
    glTranslatef(posx, posy+1.8-0.2, posz)
    glRotatef(-90.0, 5.0, 0.0, 0.0)
    gluCylinder(pObj, 0.5, 0, 1.8, 26, 13)
    glPopMatrix()


def torre_central(pObj):
    glColor3f(0/255, 0/255, 0/255)
    glPushMatrix()
    glTranslatef(0, 1.6, 0)
    glRotatef(-90.0, 5.0, 0.0, 0.0)
    gluCylinder(pObj, 1, 0, 1, 26, 13)
    glPopMatrix()


def criar_janela(rotate_x, rotate_z):
    glPushMatrix()
    glRotatef(rotate_x, 0, rotate_z, 0)
    glTranslatef(0, 1.6/2, 1.6/2-0.2)
    usar_textura(2)
    colocar_textura(1.6/2, 1.6/2, 0.5, [1])
    usar_textura(-1)
    colocar_planos(1.6/2, 1.6/2, 0.5, 0, 0, 0, [2, 4, 5, 6])
    glPopMatrix()


def criar_porta():
    glPushMatrix()
    glTranslatef(0, 0.6, 1.6/2-0.2)
    usar_textura(3)
    colocar_textura(1.6/2, 1.6*2.1/3, 0.5, [1])
    usar_textura(-1)
    colocar_planos(1.6/2, 1.6*2.1/3, 0.5, 0, 0, 0, [2, 4, 5, 6])
    glPopMatrix()


def criar_arvore(pObj, posx, posz):
    glPushMatrix()
    glColor3f(100/255, 65/255, 33/255)
    glTranslatef(posx, 1, posz)
    glRotatef(90, 5, 0, 0)
    gluCylinder(pObj, 0.1, 0.1, 1, 26, 13)
    glPopMatrix()

    glPushMatrix()
    glColor3f(0, 1, 0)
    glTranslatef(posx, 0.15+1, posz)
    glRotatef(90, 5, 0, 0)
    gluCylinder(pObj, 0, 0.4, 0.5, 26, 13); 
    glPopMatrix()
	
    glPushMatrix()
    glColor3f(0, 1, 0)
    glTranslatef(posx, 0.7+1, posz)
    glRotatef(90, 5, 0, 0)
    gluCylinder(pObj, 0, 0.3, 0.7, 26, 13); 
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
    glutCreateWindow('Castelo')
    texturas += [carregar_textura('textura/tijolo.jpg')]
    texturas += [carregar_textura('textura/grama.jpg')]
    texturas += [carregar_textura('textura/janela.jpg')]
    texturas += [carregar_textura('textura/porta.jpg')]
    texturas += [carregar_textura('textura/agua.jpg')]
    glutReshapeFunc(mudar_tamanho_tela)
    glutSpecialFunc(teclas_especiais)
    glutDisplayFunc(renderizacao_cena)
    setup_rc()
    glutMainLoop()


if __name__ == '__main__':
    main()
