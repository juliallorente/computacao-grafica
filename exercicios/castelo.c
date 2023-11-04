// gcc castle.c -lglut -lGL -lGLU -lm -o castle && ./castle

# include <GL/glut.h>
# include <stdio.h>

// header

void criar_torre(GLUquadricObj *pObj, GLfloat posx, GLfloat posy, GLfloat posz);
void criar_parede();
void criar_paredes(GLfloat angulox, GLfloat anguloz, GLfloat translatex, GLfloat translatey, GLfloat translatez);
void criar_arvores(GLUquadricObj *pObj, GLfloat posx, GLfloat posy, GLfloat posz);

// Rotation
static GLfloat yRot = 0.0f;
static GLfloat xRot = 0.0f;

// Change viewing volume and viewport.  Called when window is resized  
void ChangeSize(int w, int h)  
    {  
    GLfloat fAspect;  
  
    // Prevent a divide by zero  
    if(h == 0)  
        h = 1;  
  
    // Set Viewport to window dimensions  
    glViewport(0, 0, w, h);  
  
    fAspect = (GLfloat)w/(GLfloat)h;  
  
    // Reset coordinate system  
    glMatrixMode(GL_PROJECTION);  
    glLoadIdentity();  
  
    // Produce the perspective projection  
    gluPerspective(35.0f, fAspect, 1.0, 40.0);  
  
    glMatrixMode(GL_MODELVIEW);  
    glLoadIdentity();  
    }  
  
  
// This function does any needed initialization on the rendering context.  Here it sets up and initializes the lighting for the scene.  
void SetupRC(){  

    // Light values and coordinates  
    GLfloat  whiteLight[] = { 0.05f, 0.05f, 0.05f, 1.0f };  
    GLfloat  sourceLight[] = { 0.25f, 0.25f, 0.25f, 0.25f };  
    GLfloat  lightPos[] = { -1.0f, 5.0f, 5.0f, 1.0f };  
  
    glEnable(GL_DEPTH_TEST);    // Hidden surface removal  
    glFrontFace(GL_CCW);        // Counter clock-wise polygons face out  
    glEnable(GL_CULL_FACE);     // Do not calculate inside  
  
    // Enable lighting  
    // glEnable(GL_LIGHTING);  
  
    // Setup and enable light 1
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT,whiteLight);  
    glLightfv(GL_LIGHT1,GL_AMBIENT,sourceLight);  
    // glLightfv(GL_LIGHT1,GL_DIFFUSE,sourceLight);  
    glLightfv(GL_LIGHT1,GL_POSITION,lightPos);  
    glEnable(GL_LIGHT1);  
  
    // Enable color tracking  
    glEnable(GL_COLOR_MATERIAL);  
      
    // Set Material properties to follow glColor values  
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE);  
  
    // Black blue background  
    glClearColor(0.7f, 0.8f, 1.0f, 0.0f);  

}  
  
// Respond to arrow keys (rotate castle)
void SpecialKeys(int key, int x, int y){  

    if(key == GLUT_KEY_LEFT)  
        yRot -= 5.0f;  
  
    if(key == GLUT_KEY_RIGHT)  
        yRot += 5.0f;  
        
    if(key == GLUT_KEY_UP)  
        xRot -= 5.0f;  
  
    if(key == GLUT_KEY_DOWN)  
        xRot += 5.0f; 
                  
    yRot = (GLfloat)((const int)yRot % 360);
    xRot = (GLfloat)((const int)xRot % 360);  
  
    // Refresh the Window  
    glutPostRedisplay();  
}
  
// Called to draw scene  
void RenderScene(void){  

    GLUquadricObj *pObj;    // Quadric Object  
      
    // Clear the window with current clearing color  
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);  
  
    // Save the matrix state and do the rotations  
    glPushMatrix();

	// Move object back and do in place rotation  
	glTranslatef(0.0f, -1.0f, -5.0f);  
	glRotatef(yRot, 0.0f, 1.0f, 0.0f);
	glRotatef(xRot, 1.0f, 0.0f, 0.0f);  

	// Draw something  
	pObj = gluNewQuadric();  
	gluQuadricNormals(pObj, GLU_SMOOTH);  

	// floor
    glPushMatrix();
		glColor3f(0.1f, 1.0f, 0.1f); 
		glTranslatef(0.0, 0.0, 0.0f);
		glRotatef(-90.0f, 90.0f, 0.0f, 0.0f);
		glScalef(15.0f, 15.0f, 0.1f);
		glutSolidCube(0.5);
	glPopMatrix();

    // castle floor
    glPushMatrix();
		glColor3f(0.5f, 0.5f, 0.5f); // vermelho, verde, azul
		glTranslatef(0.0, 0.01, 0.0f);
		glRotatef(-90.0f, 90.0f, 0.0f, 0.0f);
		glScalef(7.5f, 7.5f, 0.1f);
		glutSolidCube(0.5);
	glPopMatrix();
	

    // create tower
    float translate_tower = 1.35;
    criar_torre(pObj, translate_tower, 0.0, translate_tower);
    criar_torre(pObj, -translate_tower, 0.0, translate_tower);
    criar_torre(pObj, translate_tower, 0.0, -translate_tower);
    criar_torre(pObj, -translate_tower, 0.0, -translate_tower);

    // create wall
    criar_parede();
    
    // crate walls
    criar_paredes(90.0,90.0, 0, 0.0, 1.35);
    criar_paredes(90.0,90.0, 0, 0.0, -1.35);
    criar_paredes(0.0,0.0, 0, 0.0, -1.35);

    // create trees
    for(int i=0; i < 10; i++){
        criar_arvores(pObj, 0, 0.15, i+2);
    }

    // Restore the matrix state  
    glPopMatrix();  
  
    // Buffer swap  
    glutSwapBuffers();  

}    

void criar_torre(GLUquadricObj *pObj, GLfloat posx, GLfloat posy, GLfloat posz) {
    glColor3f(0.35f, 0.35f, 0.35f);  
	glPushMatrix();
		glTranslatef(posx, posy, posz);
		glRotatef(-90.0f, 5.0f, 0.0f, 0.0f);
		gluCylinder(pObj, 0.2f, 0.2f, 1.5/2.0f, 26, 13);  
	glPopMatrix();
}

void criar_parede() {
    glRotatef(0, 0, 0, 0);
    glColor3f(0.55f, 0.55f, 0.55f);
	glPushMatrix();
        float x=0.77,y=2.7/2.2,z=0.3, translatex=-1.15, translatez=1.35;
		glTranslatef(translatex, y/4, translatez);
        // x = largura da parede
        // y = altura da parede
        // z = espessura
		glScalef(x, y, z);
		glutSolidCube(0.5);
	glPopMatrix();

	glPushMatrix();
		glTranslatef(translatex+x*0.5, 0.15, translatez);
		glScalef(x, y*1.32/3, z);
		glutSolidCube(0.5);
	glPopMatrix();

	glPushMatrix();
		glTranslatef(translatex+x*0.5, 0.25+y*0.325, translatez);
		glScalef(x, y/3, z);
		glutSolidCube(0.5);
	glPopMatrix();

    glPushMatrix();
		glTranslatef(translatex+x, y/4, translatez);
		glScalef(x, y, z);
		glutSolidCube(0.5);
	glPopMatrix();
    
    glPushMatrix();
		glTranslatef(translatex+x*1.5, 0.25+y*0.325, translatez);
		glScalef(x, y/3, z);
		glutSolidCube(0.5);
	glPopMatrix();

    glPushMatrix();
		glTranslatef(translatex+x*2, y/4, translatez);
		glScalef(x, y, z);
		glutSolidCube(0.5);
	glPopMatrix();

    glPushMatrix();
		glTranslatef(translatex+x*2.5, 0.15, translatez);
		glScalef(x, y*1.32/3, z);
		glutSolidCube(0.5);
	glPopMatrix();

	glPushMatrix();
		glTranslatef(translatex+x*2.5, 0.25+y*0.325, translatez);
		glScalef(x, y/3, z);
		glutSolidCube(0.5);
	glPopMatrix();

    glPushMatrix();
		glTranslatef(translatex+x*3, y/4, translatez);
		glScalef(x, y, z);
		glutSolidCube(0.5);
	glPopMatrix();
}

void criar_paredes(GLfloat angulox, GLfloat anguloz, GLfloat translatex, GLfloat translatey, GLfloat translatez) {
    glColor3f(0.6f, 0.6f, 0.6f);
	glPushMatrix();
        float x=5.4,y=2.7/2.2,z=0.3;
        glRotatef(angulox, 0, anguloz, 0);
        glTranslatef(translatex, translatey+y/4, translatez);
		// glTranslatef(translatex, y/4, translatez);
        // x = largura da parede
        // y = altura da parede
        // z = espessura
		glScalef(x, y, z);
		glutSolidCube(0.5);
	glPopMatrix();

    x=0.77;
    y=2.7/2.2;
    z=0.3;
    
    glPushMatrix();
        glRotatef(angulox, 0, anguloz, 0);
		glTranslatef(translatex+0.7, 0.25+y*0.325, translatez);
		glScalef(x, y/3, z);
		glutSolidCube(0.5);
	glPopMatrix();

    glPushMatrix();
        glRotatef(angulox, 0, anguloz, 0);
		glTranslatef(translatex, 0.25+y*0.325, translatez);
		glScalef(x, y/3, z);
		glutSolidCube(0.5);
	glPopMatrix();

    glPushMatrix();
        glRotatef(angulox, 0, anguloz, 0);
		glTranslatef(translatex-0.7, 0.25+y*0.325, translatez);
		glScalef(x, y/3, z);
		glutSolidCube(0.5);
	glPopMatrix();
}

void criar_arvores(GLUquadricObj *pObj, GLfloat posx, GLfloat posy, GLfloat posz) {
    glColor3f(0.7, 0.35, 0.25);
	glPushMatrix();
		glTranslatef(posx, posy, posz);
		glRotatef(90.0f, 5.0f, 0.0f, 0.0f);
		gluCylinder(pObj, 0.05/2.0f, 0.05/2.0f, 0.3/2.0f, 26, 13);  
	glPopMatrix();
	glColor3f(0.0, 1.0, 0.0);
	glPushMatrix();
		glTranslatef(posx, posy+0.3, posz);
		glRotatef(90.0f, 5.0f, 0.0f, 0.0f);
		gluCylinder(pObj, 0.0/2.0f, 0.13/2.0f, 0.38/2.0f, 26, 13);  
	glPopMatrix();
		glPushMatrix();
		glTranslatef(posx, posy+0.4, posz);
		glRotatef(90.0f, 5.0f, 0.0f, 0.0f);
		gluCylinder(pObj, 0.0/2.0f, 0.09/2.0f, 0.3/2.0f, 26, 13);  
	glPopMatrix();
}

int main(int argc, char *argv[]){

    glutInit(&argc, argv);  
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH);  
    glutInitWindowSize(800, 600);  
    glutCreateWindow("Modeling with Quadrics");  
    glutReshapeFunc(ChangeSize);  
    glutSpecialFunc(SpecialKeys);  
    glutDisplayFunc(RenderScene);  
    SetupRC();  
    glutMainLoop();  
      
    return 0; 
}
