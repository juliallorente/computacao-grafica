from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import random

from elementos.cubo import Cubo
from elementos.arvore import Arvore
from elementos.musgo import Musgo
from elementos.tronco import Tronco


class Chao:
    def __init__(self, tamanho, posicao, player, game):
        self.tamanho_x, self.tamanho_y = tamanho
        self.posicao_x, self.posicao_y, self.posicao_z = posicao

        self.player = player

        self.game = game

        self.dicionario_pecas = {
            0: 'grama_clara',
            1: 'grama_clara_com_arvore',
            2: 'grama_escura',
            3: 'grama_escura_com_arvore',
            4: 'agua',
            5: 'agua_com_musgo',
            6: 'agua_com_tronco',
            7: 'asfalto'
        }

        self.matriz_informacao = []

        self.matriz_cubos = None

        self.count = 0

        self.criar_matrizes()

    def criar_matrizes(self):
        self.matriz_informacao = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]

        for _ in range(30):
            for linha in self.gerar_linhas_aleatorias():
                self.matriz_informacao.append(linha)

        self.criar_cubos()

    @staticmethod
    def gerar_linhas_aleatorias():
        return random.choice([
            [
                [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
                [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7]
            ],
            [
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7]
            ],
            [
                [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                random.choices(population=[4, 5, 6], weights=[0.6, 0.2, 0.2], k=15),
                random.choices(population=[4, 5, 6], weights=[0.6, 0.2, 0.2], k=15)
            ],
            [
                [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                random.choices(population=[4, 5, 6], weights=[0.6, 0.2, 0.2], k=15)
            ]
        ])

    def verificar_movimento(self, posicao_futura_x, posicao_futura_y):
        if posicao_futura_x < 0 or not (0 <= posicao_futura_y <= len(self.matriz_informacao[0])-1):
            return 'nao_mover'
        elif self.dicionario_pecas[self.matriz_informacao[posicao_futura_x][posicao_futura_y]] in \
            ['grama_clara_com_arvore', 'grama_escura_com_arvore']:
            return 'nao_mover'
        elif self.dicionario_pecas[self.matriz_informacao[posicao_futura_x][posicao_futura_y]] in \
            ['grama_clara', 'grama_escura', 'agua_com_musgo', 'agua_com_tronco', 'asfalto']:
            return 'mover'
        elif self.dicionario_pecas[self.matriz_informacao[posicao_futura_x][posicao_futura_y]] in \
            ['agua']:
            return 'fim_de_jogo'
        return 'objeto_desconhecido'

    def mover(self, direcao):
        if direcao == 'frente':
            return self.verificar_movimento(self.player.posicao_chao_x + 1, self.player.posicao_chao_y)
        elif direcao == 'tras':
            return self.verificar_movimento(self.player.posicao_chao_x - 1, self.player.posicao_chao_y)
        elif direcao == 'esquerda':
            return self.verificar_movimento(self.player.posicao_chao_x, self.player.posicao_chao_y + 1)
        elif direcao == 'direita':
            return self.verificar_movimento(self.player.posicao_chao_x, self.player.posicao_chao_y - 1)

    def avancar(self):
        if self.count == 2:
            for linha in self.gerar_linhas_aleatorias():
                self.matriz_informacao.append(linha)
            self.criar_cubos()
            self.count = 0
        else:
            self.count += 1

    def criar_cubos(self):
        self.matriz_cubos = [[None for _ in range(len(self.matriz_informacao[0]))] for _ in range(len(self.matriz_informacao))]

        for i in range(len(self.matriz_cubos)):
            for j in range(len(self.matriz_cubos[0])):
                if self.dicionario_pecas[self.matriz_informacao[i][j]] == 'grama_clara':
                    tamanho_cubo = 1

                    self.matriz_cubos[i][j] = [
                        Cubo(
                            tamanho_cubo,
                            [-1*(i*tamanho_cubo+tamanho_cubo/2), -2-tamanho_cubo/2, (j*tamanho_cubo+tamanho_cubo/2)],
                            [0, 1, 0],
                            'grama_clara',
                            self.game
                        )
                    ]

                elif self.dicionario_pecas[self.matriz_informacao[i][j]] == 'grama_clara_com_arvore':
                    tamanho_cubo = 1

                    self.matriz_cubos[i][j] = [
                        Cubo(
                            tamanho_cubo,
                            [-1*(i*tamanho_cubo+tamanho_cubo/2), -2-tamanho_cubo/2, (j*tamanho_cubo+tamanho_cubo/2)],
                            [0, 1, 0],
                            'grama_clara',
                            self.game
                        ),
                        
                        Arvore(
                            [-1*(i*tamanho_cubo+tamanho_cubo/2), -1.5, (j*tamanho_cubo+tamanho_cubo/2)]
                        )
                    ]

                elif self.dicionario_pecas[self.matriz_informacao[i][j]] == 'grama_escura':
                    tamanho_cubo = 1

                    self.matriz_cubos[i][j] = [
                        Cubo(
                            tamanho_cubo,
                            [-1*(i*tamanho_cubo+tamanho_cubo/2), -2-tamanho_cubo/2, (j*tamanho_cubo+tamanho_cubo/2)],
                            [0, 1, 0.3],
                            'grama_escura',
                            self.game
                        )
                    ]

                elif self.dicionario_pecas[self.matriz_informacao[i][j]] == 'grama_escura_com_arvore':
                    tamanho_cubo = 1

                    self.matriz_cubos[i][j] = [
                        Cubo(
                            tamanho_cubo,
                            [-1*(i*tamanho_cubo+tamanho_cubo/2), -2-tamanho_cubo/2, (j*tamanho_cubo+tamanho_cubo/2)],
                            [0, 1, 0.3],
                            'grama_escura',
                            self.game
                        ),
                        
                        Arvore(
                            [-1*(i*tamanho_cubo+tamanho_cubo/2), -1.5, (j*tamanho_cubo+tamanho_cubo/2)]
                        )
                    ]

                elif self.dicionario_pecas[self.matriz_informacao[i][j]] == 'agua':
                    tamanho_cubo = 1

                    self.matriz_cubos[i][j] = [
                        Cubo(
                            tamanho_cubo,
                            [-1*(i*tamanho_cubo+tamanho_cubo/2), -2-tamanho_cubo/2-0.1, (j*tamanho_cubo+tamanho_cubo/2)],
                            [0, 0, 1],
                            'agua',
                            self.game
                        )
                    ]

                elif self.dicionario_pecas[self.matriz_informacao[i][j]] == 'agua_com_musgo':
                    tamanho_cubo = 1

                    self.matriz_cubos[i][j] = [
                        Cubo(
                            tamanho_cubo,
                            [-1*(i*tamanho_cubo+tamanho_cubo/2), -2-tamanho_cubo/2-0.1, (j*tamanho_cubo+tamanho_cubo/2)],
                            [0, 0, 1],
                            'agua',
                            self.game
                        ),

                        Musgo(
                            [-1*(i*tamanho_cubo+tamanho_cubo/2), -2, (j*tamanho_cubo+tamanho_cubo/2)]
                        )
                    ]

                elif self.dicionario_pecas[self.matriz_informacao[i][j]] == 'agua_com_tronco':
                    tamanho_cubo = 1

                    self.matriz_cubos[i][j] = [
                        Cubo(
                            tamanho_cubo,
                            [-1*(i*tamanho_cubo+tamanho_cubo/2), -2-tamanho_cubo/2-0.1, (j*tamanho_cubo+tamanho_cubo/2)],
                            [0, 0, 1],
                            'agua',
                            self.game
                        ),

                        Tronco(
                            [-1*(i*tamanho_cubo+tamanho_cubo/2), -2, (j*tamanho_cubo+tamanho_cubo/2)]
                        )
                    ]

                elif self.dicionario_pecas[self.matriz_informacao[i][j]] == 'asfalto':
                    tamanho_cubo = 1

                    self.matriz_cubos[i][j] = [
                        Cubo(
                            tamanho_cubo,
                            [-1*(i*tamanho_cubo+tamanho_cubo/2), -2-tamanho_cubo/2-0.1, (j*tamanho_cubo+tamanho_cubo/2)],
                            [0.7, 0.7, 0.7],
                            'asfalto',
                            self.game
                        )
                    ]




                # if self.dicionario_pecas[self.matriz_informacao[i][j]] == 'borda':
                #     tamanho_cubo = 1
                #     z = -1
                #     self.matriz_cubos[i][j] = Cubo(
                #         tamanho_cubo,
                #         [-1*(i*tamanho_cubo+tamanho_cubo/2), -2-tamanho_cubo/2, (j*tamanho_cubo+tamanho_cubo/2)],
                #         [1, 0, 0])
                # elif self.dicionario_pecas[self.matriz_informacao[i][j]] == 'grama_clara':
                #     tamanho_cubo = 1
                #     z = -2
                #     self.matriz_cubos[i][j] = Cubo(
                #         tamanho_cubo,
                #         [-1*(i*tamanho_cubo+tamanho_cubo/2), -2-tamanho_cubo/2, (j*tamanho_cubo+tamanho_cubo/2)],
                #         [0, 0.8, 0])
                # elif self.dicionario_pecas[self.matriz_informacao[i][j]] == 'grama_escura':
                #     tamanho_cubo = 1
                #     z = -2
                #     self.matriz_cubos[i][j] = Cubo(
                #         tamanho_cubo,
                #         [-1*(i*tamanho_cubo+tamanho_cubo/2), -2-tamanho_cubo/2, (j*tamanho_cubo+tamanho_cubo/2)],
                #         [0, 1, 0.5])
                # elif self.dicionario_pecas[self.matriz_informacao[i][j]] == 'agua':
                #     tamanho_cubo = 1
                #     z = -2
                #     self.matriz_cubos[i][j] = Cubo(
                #         tamanho_cubo,
                #         [-1*(i*tamanho_cubo+tamanho_cubo/2), -2-tamanho_cubo/2-0.1, (j*tamanho_cubo+tamanho_cubo/2)],
                #         [0, 0, 1])
                # elif self.dicionario_pecas[self.matriz_informacao[i][j]] == 'asfalto':
                #     tamanho_cubo = 1
                #     z = -2
                #     self.matriz_cubos[i][j] = Cubo(
                #         tamanho_cubo,
                #         [-1*(i*tamanho_cubo+tamanho_cubo/2), -2-tamanho_cubo/2, (j*tamanho_cubo+tamanho_cubo/2)],
                #         [0, 0, 0])

    def exibir(self):
        glPushMatrix()
        glTranslatef(self.posicao_x, self.posicao_y, self.posicao_z)
        for i in range(len(self.matriz_cubos)):
            for j in range(len(self.matriz_cubos[0])):
                if self.matriz_cubos[i][j] is not None:
                    for elemento in self.matriz_cubos[i][j]:
                        elemento.exibir()
        glPopMatrix()

