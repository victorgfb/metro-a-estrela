from typing import Tuple

import numpy as np
import pandas as pd


class No:
    def __init__(
        self, estado: str, g: int, h: int, caminho: list, estado_pai: Tuple[str, str]
    ) -> None:
        self.estado = estado
        self.g = round(g, 2)
        self.h = round(h, 2)
        self.custo = round(self.g + self.h, 2)
        self.caminho = caminho
        self.estado_pai = estado_pai

    def __lt__(self, other):
        return self.custo < other.custo

    def __eq__(self, other):
        return (
            self.estado == other.estado
            and self.g == other.g
            and self.h == other.h
            and self.caminho == other.caminho
            and self.estado_pai == other.estado_pai
        )

    def __hash__(self):
        return hash((self.estado, self.g, *self.caminho, self.estado_pai))


class AEstrela:
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
        print(f"estado inicial->{estado_inicial}")
        print(f"estado final->{estado_final}")

        self.estado_final = estado_final

        self.mapa_linhas = self.__processa_mapa_linha(mapa_linhas_caminho)
        self.mapa_distancia_real = self.__processa_mapa_distancia(
            mapa_distancia_real_caminho
        )
        self.mapa_distancia_direta = self.__processa_mapa_distancia(
            mapa_distancia_direta_caminho
        )

        self.estado_inicial = estado_inicial
        self.fronteira = [
            No(
                estado_inicial,
                g=0,
                h=self.__calcula_h(estado_inicial),
                caminho=[estado_inicial],
                estado_pai=None,
            )
        ]

    def __processa_mapa_linha(self, mapa_caminho) -> pd.DataFrame:
        mapa = pd.read_csv(mapa_caminho, sep=";")
        mapa.columns = [s.lower() for s in mapa.columns]

        for c in mapa.columns:
            mapa[c] = mapa[c].str.lower()

        return mapa

    def __processa_mapa_distancia(self, mapa_caminho: str) -> pd.DataFrame:
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
        print("Fronteira:")

        for no in self.fronteira:
            print(f"{no.estado}-{{{no.custo}}}-g:{{{no.g}}}-h:{{{no.h}}}")

    def __retira_no_menor_custo(self) -> None:
        no_atual = self.fronteira.pop(0)

        return no_atual

    def __expande_no(self, no_atual: No) -> None:
        print("--------------------------------------------")
        print(
            f"Expandindo no {no_atual.estado}-{{{no_atual.custo}}}-g:{{{no_atual.g}}}-h:{{{no_atual.h}}}\n\n"
        )
        estacao_atual, linha_atual = no_atual.estado

        estacao_vizinhas = self.mapa_distancia_real[no_atual.estado[0]].dropna()
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

    def __calcula_g(self, estado_1: Tuple[str, str], no_pai: No) -> None:
        estacao_1, linha_1 = estado_1
        estacao_2, linha_2 = no_pai.estado

        g = self.mapa_distancia_real.loc[estacao_1, estacao_2]

        if linha_1 != linha_2:
            g += self.tempo_baudeacao

        g += no_pai.g

        return g

    def __calcula_h(self, estado_1: Tuple[str, str]) -> None:
        estacao_1, linha_1 = estado_1
        estacao_2, linha_2 = self.estado_final

        h = self.mapa_distancia_direta.loc[estacao_1, estacao_2]

        if linha_1 != linha_2:
            h += self.tempo_baudeacao

        return h

    def __verifica_objetivo(self, no: No) -> None:
        return self.estado_final == no.estado

    def busca(self) -> None:
        self.__imprime_fronteira()

        no_atual = self.__retira_no_menor_custo()

        while not self.__verifica_objetivo(no_atual):
            self.__expande_no(no_atual)
            self.__imprime_fronteira()
            no_atual = self.__retira_no_menor_custo()

        return no_atual.caminho, no_atual.custo
