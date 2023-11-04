// gcc generate_city_final.c -lglut -lGL -lGLU -lm -o generate_city_final && ./generate_city_final

#include <GL/glut.h>
#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define PI 3.14

// ***** DEFINIR ESTA SEÇÃO PARA O USO DO SOFTWARE *****
//  ***  PARÂMETROS DA CIDADE  ***

#define TAM_TERRENO 100

#define NUM_CASAS 20

#define NUM_LAGOS 10

#define NUM_PREDIOS 3

#define NUM_ARVORES 60
// *****   *****   *****   *****   *****   *****   *****

// tamanho_casa, escala_x, escala_z -> da geracao de cada casa
double array_pontos_casas[NUM_CASAS*3];

// tamanho_casa, escala_x, escala_z -> da geracao de cada predio
double array_pontos_predios[NUM_PREDIOS*3];

// total de coordenadas (x,y,z) sem colisão que o software gera -- obs: y eh constante
double array_posicoes_a_usar[NUM_CASAS+NUM_LAGOS+NUM_PREDIOS+NUM_ARVORES];

// rotações
static GLfloat yRot = 0.0f;
static GLfloat zRot = -15.0f;

// viewport e redimensionar janela  
void ChangeSize(int w, int h) {  
    GLfloat fAspect;  
 
    if(h == 0)  
        h = 1;  
 
    glViewport(0, 80, w, h);
 
    fAspect = (GLfloat)w/(GLfloat)h;  
 
    glMatrixMode(GL_PROJECTION);  
    glLoadIdentity();  
 
    gluPerspective(35.0f, fAspect, 1.0, 300.0);  
 
    glMatrixMode(GL_MODELVIEW);  
    glLoadIdentity();  
    }  
 
// inicializacoes  
void SetupRC(){  

    GLfloat  whiteLight[] = { 0.05f, 0.05f, 0.05f, 1.0f };  
    GLfloat  sourceLight[] = { 0.25f, 0.25f, 0.25f, 1.0f };  
    GLfloat  lightPos[] = { -10.f, 5.0f, 5.0f, 1.0f };  
 
    glEnable(GL_DEPTH_TEST);   
    glFrontFace(GL_CCW);     
 
    glEnable(GL_LIGHTING);
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT,whiteLight);  
    glLightfv(GL_LIGHT0,GL_AMBIENT,sourceLight);  
    glLightfv(GL_LIGHT0,GL_DIFFUSE,sourceLight);  
    glLightfv(GL_LIGHT0,GL_POSITION,lightPos);  
    glEnable(GL_LIGHT0);  
 
    glEnable(GL_COLOR_MATERIAL);  
     
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE);  
 
    glClearColor(0.5f, 0.7f, 0.8f, 1.0f);  
}  

void SpecialKeys(int key, int x, int y){  

    if(key == GLUT_KEY_LEFT)  
        yRot -= 5.0f;  
 
    if(key == GLUT_KEY_RIGHT)
        yRot += 5.0f;  
       
    if(key == GLUT_KEY_UP){ 
        zRot += 5.0f; 
    } 
    
    if(key == GLUT_KEY_DOWN){
        zRot -= 5.0f;  
    }
                 
    yRot = (GLfloat)((const int)yRot % 360);
 
    glutPostRedisplay();  
}

// funcões:
double gera_numero_aleatorio(double inicio_intervalo, double final_intervalo){
	
	// le de /dev/random um numero aleatorio para a seed
	unsigned int randval;
	FILE *f;	
	
	f = fopen("/dev/urandom", "r");	
	fread(&randval, sizeof(randval), 1, f);	
	fclose(f);
	
	srand(randval);
	
	double num = ( (double)rand() * (final_intervalo - inicio_intervalo)) / (double)RAND_MAX + inicio_intervalo;
	
	return num;
}

int calcula_distancia(double nova_posicao_x, double nova_posicao_z, int numero_posicoes_ja_calculadas, int indice_posicao1_da_vez, int indice_posicao2_da_vez){
		
	int primeiro_indice= 0; // pos indice x	
	int segundo_indice = 1; // pos indice z
	int contadora=0;	
	int flag = 0;	
	
	while(contadora != numero_posicoes_ja_calculadas){		
		// x e z gerados ja estao presentes na lista
			
		if(primeiro_indice == indice_posicao1_da_vez && segundo_indice == indice_posicao2_da_vez){
			primeiro_indice+= 2;
			segundo_indice += 2;	
		}
		//  x_lista - x_gerado 						    z_lista - z_gerado
		if( fabs(array_posicoes_a_usar[primeiro_indice] - nova_posicao_x) <= 10 && fabs(array_posicoes_a_usar[segundo_indice] - nova_posicao_z) <= 10 ){
			flag = 1;
			break;		
		}
		primeiro_indice+= 2;
		segundo_indice += 2;	

		contadora++;		
	}
	// ponto gerado da conflito
	if(flag == 1){
		return 1;
	}	
	
	// ponto gerado nao da conflito
	return -1;
}

/* SEQUÊNCIA DO USO DOS PONTOS: 
	casas: 		0 - NUM_CASAS * 2
	lagos: 		NUM_CASAS * 2 + 1
	predios:	NUM_LAGOS * 2 + 1
	arvores:	NUM_PREDIOS * 2 + 1
*/
void gera_posicoes_a_usar(){

	int i;
	int posicao_1 = 0;
	int posicao_2 = 1;

	double coordenada_x;
	double coordenada_z;

	// comeca neutro
	int retorno = 0;

	// NUM_CASAS + NUM_LAGOS + NUM_PREDIOS + NUM_ARVORES
	for(i=0;i<NUM_CASAS + NUM_LAGOS + NUM_PREDIOS + NUM_ARVORES; i++){
		// ponto (x,z)	
		while(retorno != -1){
			coordenada_x = gera_numero_aleatorio(-TAM_TERRENO+10, TAM_TERRENO-10);
			coordenada_z = gera_numero_aleatorio(-TAM_TERRENO+10, TAM_TERRENO-10);
			
			array_posicoes_a_usar[posicao_1]=coordenada_x;
			array_posicoes_a_usar[posicao_2]=coordenada_z;
						
			retorno = calcula_distancia(coordenada_x, coordenada_z, i, posicao_1, posicao_2);
		}
		retorno = 0;

		posicao_1+=2;
		posicao_2+=2;		
	}

	// printa os pontos gerados
	posicao_1=0;
	posicao_2=1;

	printf("\nPONTOS GERADOS:\n");
	for(i=0;i<NUM_CASAS + NUM_LAGOS + NUM_PREDIOS + NUM_ARVORES; i++){
		printf("\n(%d)   (%lf,%lf)", i, array_posicoes_a_usar[posicao_1], array_posicoes_a_usar[posicao_2]);		
		posicao_1+=2;
		posicao_2+=2;
	}
}

// calcula o tamanho_casa, escala_x, escala_z
void calcula_pontos_casas(){

	int prim_indice = 0;
	int segu_indice = 1;
	int terc_indice = 2;
	int num_casas = 0;	
	
	while(num_casas != NUM_CASAS){
	
		if(num_casas != NUM_CASAS && num_casas != 0){
			
			prim_indice += 3;
			segu_indice += 3;
			terc_indice += 3;
			
			// tamanho_casa
			array_pontos_casas[prim_indice] = gera_numero_aleatorio(1.0, 2.0);
			// escala_x
			array_pontos_casas[segu_indice] = gera_numero_aleatorio(1.0, 2.0);
			// escala_z
			array_pontos_casas[terc_indice] = gera_numero_aleatorio(1.0, 2.0);
			
			num_casas++;
		}		
		if(num_casas == 0){
			// tamanho_casa
			array_pontos_casas[prim_indice] = gera_numero_aleatorio(1.0, 2.0);
			// escala_x
			array_pontos_casas[segu_indice] = gera_numero_aleatorio(1.0, 2.0);
			// escala_z
			array_pontos_casas[terc_indice] = gera_numero_aleatorio(1.0, 2.0);
			
			num_casas++;		
		}
	}
}

// calcula o tamanho_predio, escala_y
void calcula_pontos_predios(){

	int prim_indice = 0;
	int segu_indice = 1;
	int num_predios = 0;	
	
	while(num_predios != NUM_PREDIOS){
	
		if(num_predios != NUM_PREDIOS && num_predios != 0){
			
			prim_indice += 2;
			segu_indice += 2;
			
			// tamanho_predio
			array_pontos_predios[prim_indice] = gera_numero_aleatorio(1.5, 2.0);
			// escala_y
			array_pontos_predios[segu_indice] = gera_numero_aleatorio(1.0, 7.0);
			
			num_predios++;
		}		
		if(num_predios == 0){
			// tamanho_predio
			array_pontos_predios[prim_indice] = gera_numero_aleatorio(1.5, 2.0);
			// escala_y
			array_pontos_predios[segu_indice] = gera_numero_aleatorio(1.0, 7.0);
			
			num_predios++;		
		}
	}
}

void gera_terreno(void){

	glPushMatrix();
	   	glTranslatef(0.0f, -2.0f, 0.0f);
		glBegin(GL_QUADS);
			glColor3f(0.45f, 0.8f, 0.2f);
			glVertex3f(TAM_TERRENO, 0.0f, TAM_TERRENO);
			glVertex3f(TAM_TERRENO, 0.0f, -TAM_TERRENO);
			glVertex3f(-TAM_TERRENO, 0.0f, -TAM_TERRENO);
			glVertex3f(-TAM_TERRENO, 0.0f, TAM_TERRENO);
		glEnd();
	glPopMatrix();
}

void gera_predio(double tamanho_predio, double escala_y){

	glPushMatrix();
		glColor3f(0.9f, 0.9f, 0.8f);
		glScalef(1,escala_y,1);
		glutSolidCube(tamanho_predio);	
	glPopMatrix();
}

void gera_telhado(double tamanho_casa, double escala_x, double escala_z){

		double valor1 = tamanho_casa/2.0;
		double valor2 = 0.0;
	glPushMatrix();
		glColor3f(1.0f, 0.4f, 0.0f);	
		glBegin(GL_TRIANGLES);
			// Frente
			glVertex3f( valor2, valor1, valor2);
			glVertex3f(-valor1, -valor1, valor1);
			glVertex3f(valor1, -valor1, valor1); 
			// Direita
			glVertex3f(valor2, valor1, valor2);
			glVertex3f(valor1, -valor1, valor1);
			glVertex3f(valor1, -valor1, -valor1); 
			// Trás
			glVertex3f(valor2, valor1, valor2);
			glVertex3f(valor1, -valor1, -valor1);
			glVertex3f(-valor1, -valor1, -valor1); 
			// Esquerda
			glVertex3f( valor2, valor1, valor2);
			glVertex3f(-valor1,-valor1,-valor1);
			glVertex3f(-valor1,-valor1, valor1);
		glEnd();
	glPopMatrix();
}

void gera_cubo(double tamanho_casa, double escala_x, double escala_z){

	glPushMatrix();
		glColor3f(1.0f, 1.0f, 0.0f);
		glScalef(escala_x,1.0,escala_z);
		glutSolidCube(tamanho_casa);	
	glPopMatrix();
}

void gera_casas(int indice_tamanho_casa, int indicie_escala_x, int indice_escala_z){

	double tamanho_casa = array_pontos_casas[indice_tamanho_casa];
	double escala_x = array_pontos_casas[indicie_escala_x];
	double escala_z = array_pontos_casas[indice_escala_z];
	
	glPushMatrix(); 
		// tamanho, escala_x, escala_z
		gera_cubo(tamanho_casa, escala_x, escala_z);
	glPopMatrix();
	glPushMatrix();
		// escala_x, escala_z
		glTranslatef(0.0f, tamanho_casa - (0.3 * tamanho_casa), 0.0f);
		glScalef(escala_x,0.4,escala_z);
		gera_telhado(tamanho_casa, escala_x, escala_z);			
	glPopMatrix();	
}

void gera_predios(int indice_tamanho_predio, int indicie_escala_y){

	double tamanho_predio = array_pontos_predios[indice_tamanho_predio];
	double escala_y = array_pontos_predios[indicie_escala_y];
	
	glPushMatrix();
		gera_predio(tamanho_predio, escala_y);
	glPopMatrix();
}

void gera_lago(void){	

		glColor3f(0.43f, 0.54f, 1.0f); 
	glPushMatrix();	
		glRotatef(90.0f, 1.0f, 0.0f, 0.0f); 
		glTranslatef(0.0f, 0.0f, 1.99f); 
		glBegin(GL_TRIANGLE_FAN);		
			glVertex2d(1.0,0.0);
			for (int i=0;i<=100;++i)
				glVertex2d(cos(2*i*PI/100),sin(2*i*PI/100));	
		glEnd();
	glPopMatrix();	
}

void gera_arvore(){
	// folhas
	glPushMatrix();
		glColor3f(0.2f, 0.4f, 0.35f);	
		glRotatef(-90.0f, 1.0f, 0.0f, 0.0f); 
		glutSolidCone(0.5, 1.0, 100, 100);
	glPopMatrix();
	glPushMatrix();
	   	glTranslatef(0.0f, 0.5f, 0.0f);
	   	glRotatef(-90.0f, 1.0f, 0.0f, 0.0f);   
		glutSolidCone(0.5, 1.0, 100, 100);
	glPopMatrix();
	// tronco
	glPushMatrix();
		glTranslatef(0.0f, -0.9f, 0.0f);
		GLUquadricObj *tronco;

		glColor3f(1.0f, 1.0f, 1.0f);	
		
		tronco = gluNewQuadric();  
		gluQuadricNormals(tronco, GLU_SMOOTH);
		glRotatef(-90.0f, 1.0f, 0.0f, 0.0f); 
		glColor3f(0.4f, 0.3f, 0.15f);	
		gluCylinder(tronco, 0.1, 0.1, 1.0, 100, 100);		
	glPopMatrix();
}

// inserções:
void insere_arvores(){
	// indices para controle das posicoes das arvores
	int prim_indice_das_posicoes_arvores = NUM_PREDIOS * 2 + 1;
	int segu_indice_das_posicoes_arvores = NUM_PREDIOS * 2 + 2;
	int i = 0;
	
	glTranslatef(0.0f, -1.5f, 0.0f);
	glScalef(0.7,0.7,0.7);
	
	// arvore 0
	glPushMatrix();
glTranslatef(array_posicoes_a_usar[prim_indice_das_posicoes_arvores], 0.0f, array_posicoes_a_usar[segu_indice_das_posicoes_arvores]); 
	    	gera_arvore();
	glPopMatrix();
	
	// gera arvores ate o limite de NUM_ARVORES
	for(i = 0; i < NUM_ARVORES; i++){		
		glPushMatrix();
		prim_indice_das_posicoes_arvores += 2;
		segu_indice_das_posicoes_arvores += 2;
		
		glTranslatef(array_posicoes_a_usar[prim_indice_das_posicoes_arvores], 0.0f, array_posicoes_a_usar[segu_indice_das_posicoes_arvores]); 
		    	gera_arvore();
		glPopMatrix();   
	}	
}

void insere_lagos(){
	// indices para controle das posicoes dos lagos
	int prim_indice_das_posicoes_lagos = NUM_CASAS * 2 + 1;
	int segu_indice_das_posicoes_lagos = NUM_CASAS * 2 + 2;
	int i;
	
	// lago 0
	glPushMatrix();
		glTranslatef(array_posicoes_a_usar[prim_indice_das_posicoes_lagos], 0.0f, array_posicoes_a_usar[segu_indice_das_posicoes_lagos]); 
	    	gera_lago();
	glPopMatrix();
	
	// gera lagos ate o limite de NUM_LAGOS
	for(i = 1; i < NUM_LAGOS; i++){
	glPushMatrix();			
		prim_indice_das_posicoes_lagos+=2;
		segu_indice_das_posicoes_lagos+=2;

		glTranslatef(array_posicoes_a_usar[prim_indice_das_posicoes_lagos], 0.0f, array_posicoes_a_usar[segu_indice_das_posicoes_lagos]); 
	    	gera_lago();
	glPopMatrix(); 
	}		
}

void insere_casas(){
	// indices para controle das casas
	int prim_indice_das_casas = 0;
	int segu_indice_das_casas = 1;
	int terc_indice_das_casas = 2;
	int i = 0;
	
	// indices para controle das posicoes das casas
	int prim_indice_das_posicoes_casas = 0;
	int segu_indice_das_posicoes_casas = 1;
	
	// casa 0
	glPushMatrix();			
		glTranslatef(array_posicoes_a_usar[prim_indice_das_posicoes_casas], -2.0f, array_posicoes_a_usar[segu_indice_das_posicoes_casas]);  		
		gera_casas(prim_indice_das_casas, segu_indice_das_casas, terc_indice_das_casas);
	glPopMatrix();
	
	// gera casas ate o limite de NUM_CASAS
	for(i = 1; i < NUM_CASAS; i++){
		glPushMatrix();			
		prim_indice_das_casas += 3;
		segu_indice_das_casas += 3;
		terc_indice_das_casas += 3;
				
		prim_indice_das_posicoes_casas += 2;
		segu_indice_das_posicoes_casas += 2;
		
		glTranslatef(array_posicoes_a_usar[prim_indice_das_posicoes_casas], -2.0f, array_posicoes_a_usar[segu_indice_das_posicoes_casas]);  		
		gera_casas(prim_indice_das_casas, segu_indice_das_casas, terc_indice_das_casas); 
	glPopMatrix(); 
	}
}

void insere_predios(){

	// indices para controle dos predios
	int prim_indice_dos_predios = 0;
	int segu_indice_dos_predios = 1;
	int i;
	
	// indices para controle das posicoes dos predios
	int prim_indice_das_posicoes_predios = NUM_LAGOS * 2 + 1;
	int segu_indice_das_posicoes_predios = NUM_LAGOS * 2 + 2;
	
	// predio 0
	glPushMatrix();		
		glTranslatef(array_posicoes_a_usar[prim_indice_das_posicoes_predios], -2.0f, array_posicoes_a_usar[segu_indice_das_posicoes_predios]);  		
		gera_predios(prim_indice_dos_predios, segu_indice_dos_predios);
	glPopMatrix();
	
	// gera predios ate o limite de NUM_PREDIOS
		for(i = 1; i < NUM_PREDIOS; i++){
			glPushMatrix();	
				prim_indice_dos_predios += 2;
				segu_indice_dos_predios	+= 2;	
				prim_indice_das_posicoes_predios += 2;
				segu_indice_das_posicoes_predios += 2;
				
				glTranslatef(array_posicoes_a_usar[prim_indice_das_posicoes_predios], -2.0f, array_posicoes_a_usar[segu_indice_das_posicoes_predios]);  		
				gera_predios(prim_indice_dos_predios, segu_indice_dos_predios);
			glPopMatrix();
		}
}

// funcao renderiza
void RenderScene(void){	

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

glPushMatrix();

	glTranslatef(0.0f, -2.0f, zRot);        
    	glRotatef(yRot, 0.0f, 1.0f, 0.0f);

// *** Gera o terreno plano da cidade ***
	glPushMatrix();		
	    	gera_terreno();
	glPopMatrix();	
	
// *** Gerando NUM_CASAS casas ***
	glPushMatrix();		
	 	insere_casas();
	glPopMatrix(); 	

// *** Gerando NUM_LAGOS lagos ***
	glPushMatrix();
		insere_lagos();	
	glPopMatrix();   

// *** Gerando NUM_PREDIOS predios ***
	glPushMatrix();
		insere_predios();
	glPopMatrix();

// *** Gerando NUM_ARVORES arvores ***
	glPushMatrix();		
		insere_arvores();
    	glPopMatrix(); 
    	
glPopMatrix();

// Buffer swap  
glutSwapBuffers();  

}    

int main(int argc, char *argv[]){

    glutInit(&argc, argv);  
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH);  
    glutInitWindowSize(1920, 1080);  
    glutCreateWindow("Random City Generator");  
    glutReshapeFunc(ChangeSize);  
    glutSpecialFunc(SpecialKeys);  
    glutDisplayFunc(RenderScene); 
     
    SetupRC();
    calcula_pontos_casas();
    calcula_pontos_predios(); 
    gera_posicoes_a_usar();
   
    glutMainLoop();  
     
    return 0;
}
