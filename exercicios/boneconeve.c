// gcc snowman_sample.c -lglut -lGL -lGLU -lm -o snowman && ./snowman

# include <GL/glut.h>
# include <stdio.h>
# include <math.h>
  
// Rotation
static GLfloat xRot = 0.0f;
static GLfloat yRot = 0.0f;

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
    GLfloat  sourceLight[] = { 0.25f, 0.25f, 0.25f, 1.0f };  
    GLfloat  lightPos[] = { -10.f, 5.0f, 5.0f, 1.0f };  
  
    glEnable(GL_DEPTH_TEST);    // Hidden surface removal  
    glFrontFace(GL_CCW);        // Counter clock-wise polygons face out  
    glEnable(GL_CULL_FACE);     // Do not calculate inside  
  
    // Enable lighting  
    glEnable(GL_LIGHTING);  
  
    // Setup and enable light 0  
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT,whiteLight);  
    glLightfv(GL_LIGHT0,GL_AMBIENT,sourceLight);  
    glLightfv(GL_LIGHT0,GL_DIFFUSE,sourceLight);  
    glLightfv(GL_LIGHT0,GL_POSITION,lightPos);  
    glEnable(GL_LIGHT0);  
  
    // Enable color tracking  
    glEnable(GL_COLOR_MATERIAL);  
      
    // Set Material properties to follow glColor values  
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE);  
  
    // Black blue background  
    glClearColor(0.25f, 0.25f, 0.50f, 1.0f);  

}  
  
// Respond to arrow keys (rotate snowman)
void SpecialKeys(int key, int x, int y){  

    if(key == GLUT_KEY_DOWN)  
        xRot += 5.0f;  
  
    if(key == GLUT_KEY_UP)  
        xRot -= 5.0f;  
                  
    xRot = (GLfloat)((const int)xRot % 360);

    if(key == GLUT_KEY_LEFT)  
        yRot -= 5.0f;  
  
    if(key == GLUT_KEY_RIGHT)  
        yRot += 5.0f;  
                  
    yRot = (GLfloat)((const int)yRot % 360);
  
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
    glRotatef(xRot, 1.0f, 0.0f, 0.0f);
	glRotatef(yRot, 0.0f, 1.0f, 0.0f);

	// Draw something  
	pObj = gluNewQuadric();  
	gluQuadricNormals(pObj, GLU_SMOOTH);  

    // hat 
	glPushMatrix();
		glColor3f(0.0, 0.0, 0.0);
		glTranslatef(0.0, 1.5, 0.0f);
		glRotatef(90.0f, 5.0f, 0.0f, 0.0f);
		gluCylinder(pObj, 0.2f, 0.2f, 0.5f, 50, 150); 
	glPopMatrix();

    // hat top
    glPushMatrix();
        glColor3f(0.0, 0.0, 0.0);
        glTranslatef(0.0, 1.5, 0.0);
        glRotatef(-90.0f, 5.0f, 0.0f, 0.0f);
        gluDisk(pObj, 0.0, 0.2, 1000, 10);
    glPopMatrix();

    // brim
    glColor3f(0.0, 0.0, 0.0);
    glPushMatrix();
		glTranslatef(0.0, 1.17, 0.0f);
		glRotatef(90.0f, 5.0f, 0.0f, 0.0f);
		gluCylinder(pObj, 0.3f, 0.3f, 0.05f, 50, 150); 
	glPopMatrix();

    // brim top
    glColor3f(0.0, 0.0, 0.0);
    glPushMatrix();
        glTranslatef(0.0, 1.15, 0.0);
        glRotatef(-90.0f, 5.0f, 0.0f, 0.0f);
        gluDisk(pObj, 0.0, 0.3, 1000, 10);
    glPopMatrix();

    // brim down
    glColor3f(0.0, 0.0, 0.0);
    glPushMatrix();
        glTranslatef(0.0, 1.15, 0.0);
        glRotatef(90.0f, 5.0f, 0.0f, 0.0f);
        gluDisk(pObj, 0.0, 0.3, 1000, 10);
    glPopMatrix();

	// Head
    glColor3f(1.0f, 1.0f, 1.0f);  
	glPushMatrix(); // save transform matrix state
		glTranslatef(0.0f, 1.0f, 0.0f);
		gluSphere(pObj, 0.24f, 26, 13);
	glPopMatrix(); // restore transform matrix state

    // eye left
    glColor3f(0.0, 0.0, 0.0);
	glPushMatrix();
		glTranslatef(0.07f, 1.06f, 0.18f);
		gluSphere(pObj, 0.048f, 26, 13);
	glPopMatrix();

    // eye right
       glColor3f(0.0, 0.0, 0.0);
	glPushMatrix();
		glTranslatef(-0.07f, 1.06f, 0.18f);
		gluSphere(pObj, 0.048f, 26, 13);
	glPopMatrix();

	// Nose (orange)
	glColor3f(1.0f, 0.54f, 0.0f);  
	glPushMatrix();
		glTranslatef(0.0f, 1.0f, 0.2f);
		gluCylinder(pObj, 0.04f, 0.0f, 0.3f, 26, 13);  
	glPopMatrix();  

    // scarf
	glPushMatrix();
		glColor3f(1.0, 0.0, 0.0);
		glTranslatef(0.0f, 0.9f, 0.0f);
		glRotatef(90.0f, 5.0f, 0.0f, 0.0f);
		gluCylinder(pObj, 0.21f, 0.21f, 0.08f, 50, 150); 
	glPopMatrix();

    glColor3f(1.0, 0.0, 0.0);
    glPushMatrix();
		glTranslatef(-0.1, 0.8, 0.2f);
		glRotatef(90.0f, 15.0f, 15.0f, 0.0f);
		gluCylinder(pObj, 0.04f, 0.04f, 0.06f, 50, 150); 
	glPopMatrix();

    glColor3f(1.0, 0.0, 0.0);
    glPushMatrix();
		glTranslatef(-0.1, 0.8, 0.2f);
		glRotatef(90.0f, -15.0f, -15.0f, 0.0f);
		gluCylinder(pObj, 0.04f, 0.04f, 0.06f, 50, 150); 
	glPopMatrix();

    // body
    glColor3f(1.0f, 1.0f, 1.0f);  
    glPushMatrix(); // save transform matrix state
		glTranslatef(0.0, 0.6, 0.0); 
		gluSphere(pObj, 0.29f, 26, 13); // obj, raio, qualidade, qualidade2
 	glPopMatrix(); // restore transform matrix state


    // left arm
    glColor3f(0.5, 0.3, 0.2);
	glPushMatrix();
		glTranslatef(0.23, 0.7, 0.0f);
		glRotatef(-150.0f, 5.0f, 0.5f, 5.0f);
		gluCylinder(pObj, 0.02f, 0.01f, 0.5f, 26, 13); 
	glPopMatrix();
    glPushMatrix();
    	glTranslatef(0.65, 0.91, 0.038f);
    	glRotatef(-90.0f, 5.0f, 0.0f, 5.0f);
    	gluCylinder(pObj, 0.01f, 0.005f, 0.2f, 26, 13); 
    glPopMatrix();
    glPushMatrix();
    	glTranslatef(0.65, 0.91, 0.038f);
    	glRotatef(-180.0f, 5.0f, 0.0f, 5.0f);
    	gluCylinder(pObj, 0.01f, 0.005f, 0.2f, 26, 13); 
    glPopMatrix();
	
    // right arm
    glColor3f(0.5, 0.3, 0.2);
	glPushMatrix();
        glTranslatef(-0.72, 0.89f, 0.0f);
		glRotatef(145.0f, 5.0f, 0.5f, 5.0f);
		gluCylinder(pObj, 0.01f, 0.02f, 0.5f, 26, 13); 
	glPopMatrix();
    glPushMatrix();
    	glTranslatef(-0.98+0.15, 1.22-0.22, -0.02f);
    	glRotatef(-240.0f, 5.0f, 0.0f, 5.0f);
    	gluCylinder(pObj, 0.005f, 0.01f, 0.2f, 26, 13); 
    glPopMatrix();
    glPushMatrix();
    	glTranslatef(-1.04+0.15, 1.1-0.22, 0.03f);
    	glRotatef(-240.0f, 10.0f, 10.0f, 10.0f);
    	gluCylinder(pObj, 0.005f, 0.01f, 0.2f, 26, 13); 
    glPopMatrix();

    // button1
    glColor3f(0.0, 0.0, 0.0);
	glPushMatrix();
		glTranslatef(0.0f, 0.7f, 0.23f);
		gluSphere(pObj, 0.048f, 26, 13);
	glPopMatrix();

    // button2
    glColor3f(0.0, 0.0, 0.0);
	glPushMatrix();
		glTranslatef(0.0f, 0.6f, 0.25f);
		gluSphere(pObj, 0.048f, 26, 13);
	glPopMatrix();

    // button3
    glColor3f(0.0, 0.0, 0.0);
	glPushMatrix();
		glTranslatef(0.0f, 0.5f, 0.23f);
		gluSphere(pObj, 0.048f, 26, 13);
	glPopMatrix();

    // feet
    glColor3f(1.0f, 1.0f, 1.0f);  
    glPushMatrix(); // save transform matrix state
		glTranslatef(0.0, 0.17, 0.0); 
		gluSphere(pObj, 0.34f, 26, 13); // obj, raio, qualidade, qualidade2
 	glPopMatrix(); // restore transform matrix state

    // floor
    glColor3f(1.0, 1.0, 1.0);
    glPushMatrix();
        glTranslatef(0.0, -0.2, 0.0);
        glRotatef(-90.0f, 5.0f, 0.0f, 0.0f);
        gluDisk(pObj, 0.0, 1.0, 1000, 10);
    glPopMatrix();

    glColor3f(1.0, 1.0, 1.0);
    glPushMatrix();
        glTranslatef(0.0, -0.2, 0.0);
        glRotatef(90.0f, 5.0f, 0.0f, 0.0f);
        gluDisk(pObj, 0.0, 1.0, 1000, 10);
    glPopMatrix();
	
    // Restore the matrix state  
    glPopMatrix();  
  
    // Buffer swap  
    glutSwapBuffers();  

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
