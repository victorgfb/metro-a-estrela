from typing import Tuple

import numpy as np
import pandas as pd

from busca.nos import No


class AEstrela:
    """
    Representa o algoritmo de busca A*

    Atributos:
        velocidade (int): A velocidade média de um trem.
        tempo_baudeacao (int): O tempo gasto para trocar de linha dentro da mesma estação.
        estado_inicial (Tuple[str, str]): O estado inicial.
        estado_final (Tuple[str, str]): O estado final.
        mapa_linhas (pd.DataFrame): O mapa das linhas.
        mapa_tempo_real (pd.DataFrame): O mapa os tempos de deslocamento reais sem incluir baldeação.
        mapa_tempo_estimativa (pd.DataFrame): O mapa com as estimativas do tempo de deslocamento sem incluir baldeação.
        fronteira (list): A fronteira do algoritmo A*.
    """

    velocidade = 40
    tempo_baudeacao = 3

    def __init__(
        self,
        estado_inicial: Tuple[str, str],
        estado_final: Tuple[str, str],
        mapa_linhas_caminho: str,
        mapa_distancia_real_caminho: str,
        mapa_distancia_direta_caminho: str,
    ) -> None:
        """
        Inicializa o algoritmo A* com o estado inicial, o estado final e os mapas.
        """

        print(f"estado inicial->{estado_inicial}")
        print(f"estado final->{estado_final}")

        self.mapa_linhas = self.__processa_mapa_linha(mapa_linhas_caminho)
        self.mapa_tempo_real = self.__processa_mapa_distancia(
            mapa_distancia_real_caminho
        )
        self.mapa_tempo_estimativa = self.__processa_mapa_distancia(
            mapa_distancia_direta_caminho
        )

        print("Verificando se estado inicial é valido...")
        self.__valida_estado(estado_inicial)
        self.estado_inicial = estado_inicial

        print("Verificando se estado final é valido...")
        self.__valida_estado(estado_final)
        self.estado_final = estado_final

        self.fronteira = [
            No(
                estado_inicial,
                g=0,
                h=self.__calcula_h(estado_inicial),
                caminho=[estado_inicial],
                estado_pai=None,
            )
        ]

    def __valida_estado(self, estado: Tuple[str, str]) -> None:
        """
        Verifica se o estado inserido é valido
        """
        estacao, linha = estado

        if estacao not in self.mapa_linhas[linha].values:
            raise Exception("Estado inválido")

        print("Estado válido!")

    def __processa_mapa_linha(self, mapa_caminho) -> pd.DataFrame:
        """
        Processa o mapa de linhas. Lê o arquivo como um pandas DataFrame e coloca todos os campos em minúsculo.
        """
        mapa = pd.read_csv(mapa_caminho, sep=";")
        mapa.columns = [s.lower() for s in mapa.columns]

        for c in mapa.columns:
            mapa[c] = mapa[c].str.lower()

        return mapa

    def __processa_mapa_distancia(self, mapa_caminho: str) -> pd.DataFrame:
        """
        Processa os mapas de distância. Lê o arquivo como um pandas DataFrame, coloca todos os campos em minúsculo
        e transforma as distâncias em tempo de deslocamento. Também é preenchida a diagonal inferior para facilitar
        a consulta.
        """
        mapa = pd.read_csv(mapa_caminho, sep=";")
        mapa.columns = [s.lower() for s in mapa.columns]
        mapa["unnamed: 0"] = mapa["unnamed: 0"].str.lower()

        mapa = mapa.set_index("unnamed: 0")
        mapa.index.name = None

        mapa = mapa.replace("x", None)
        mapa = mapa.replace(r",", ".", regex=True)
        mapa = round((mapa.astype(np.float64) * 60) / self.velocidade, 2)

        upper_tri = np.triu(mapa.values, 1)

        result = upper_tri + upper_tri.T

        mapa = pd.DataFrame(result, columns=mapa.columns, index=mapa.index)

        return mapa

    def __imprime_fronteira(self):
        """
        Imprime a fronteira
        """
        print("Fronteira:")

        for no in self.fronteira:
            print(f"{no.estado}-[custo:{{{no.custo}}} g:{{{no.g}}} h:{{{no.h}}}]")

        print("\n")

    def __retira_no_menor_custo(self) -> No:
        """
        Retira o nó de menor custo da fronteira
        """

        if len(self.fronteira) == 0:
            raise Exception("Fronteira vazia.")

        no_atual = self.fronteira.pop(0)

        return no_atual

    def __expande_no(self, no_atual: No) -> None:
        """
        Expande o nó colocando seus vizinhos de forma ordenada na fronteira
        """
        print("--------------------------------------------")
        print(
            f"Expandindo no {no_atual.estado}-[custo:{{{no_atual.custo}}} g:{{{no_atual.g}}} h:{{{no_atual.h}}}]\n\n"
        )
        estacao_atual, linha_atual = no_atual.estado

        estacao_vizinhas = self.mapa_tempo_real[no_atual.estado[0]].dropna()
        estacao_vizinhas = estacao_vizinhas[estacao_vizinhas != 0]

        for estacao, _ in estacao_vizinhas.items():
            if estacao in self.mapa_linhas[linha_atual].values:
                estado = (estacao, linha_atual)

                if no_atual.estado_pai != estado:
                    self.fronteira.append(
                        No(
                            estado,
                            g=self.__calcula_g(estado, no_atual),
                            h=self.__calcula_h(estado),
                            caminho=[*no_atual.caminho, estado],
                            estado_pai=no_atual.estado,
                        )
                    )
            else:
                # Caso a estação seja de outra linha, primeiro será necessario realizar a baldeação
                # dessa forma é inserido a estação atual em outra linha ao invés da estação vizinha.
                for linha in self.mapa_linhas.columns:
                    if (
                        linha != linha_atual
                        and estacao_atual in self.mapa_linhas[linha].values
                    ):
                        estado = (estacao_atual, linha)

                        if no_atual.estado_pai != estado:
                            self.fronteira.append(
                                No(
                                    estado,
                                    g=self.__calcula_g(estado, no_atual),
                                    h=self.__calcula_h(estado),
                                    caminho=[*no_atual.caminho, estado],
                                    estado_pai=no_atual.estado,
                                )
                            )

        self.fronteira = sorted(set(self.fronteira))

    def __calcula_g(self, estado_1: Tuple[str, str], no_pai: No) -> float:
        """
        Calcula o tempo de deslocamento entre os dois estados.
        """
        estacao_1, linha_1 = estado_1
        estacao_2, linha_2 = no_pai.estado

        g = self.mapa_tempo_real.loc[estacao_1, estacao_2]

        if linha_1 != linha_2:
            g += self.tempo_baudeacao

        g += no_pai.g

        return g

    def __calcula_h(self, estado_1: Tuple[str, str]) -> float:
        """
        Calcula a estimativa de tempo de deslocamento entre o estado e o estado final.
        """
        estacao_1, linha_1 = estado_1
        estacao_2, linha_2 = self.estado_final

        h = self.mapa_tempo_estimativa.loc[estacao_1, estacao_2]

        if linha_1 != linha_2:
            h += self.tempo_baudeacao

        return h

    def __verifica_objetivo(self, no: No) -> bool:
        """
        Verifica se o nó é o estado final
        """
        return self.estado_final == no.estado

    def busca(self) -> Tuple[list, float]:
        """
        Realiza a busca pela solução.
        """
        self.__imprime_fronteira()

        no_atual = self.__retira_no_menor_custo()

        while not self.__verifica_objetivo(no_atual):
            self.__expande_no(no_atual)
            self.__imprime_fronteira()
            no_atual = self.__retira_no_menor_custo()

        return no_atual.caminho, no_atual.custo
