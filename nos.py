from typing import Tuple

import numpy as np
import pandas as pd


class No:
    def __init__(self, estado: str, g: int, h: int, caminho: list) -> None:
        self.estado = estado
        self.g = g
        self.h = h
        self.custo = self.g + self.h
        self.caminho = caminho

    def incrementa_g(self, valor: int):
        self.g += valor


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
            )
        ]

    def __processa_mapa_linha(self, mapa_caminho) -> pd.DataFrame:
        mapa = pd.read_csv(mapa_caminho, sep=";")
        mapa.columns = [s.lower() for s in mapa.columns]

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

    def imprime_fronteira(self):
        for no in self.fronteira:
            print(f"{no.estado}-{{{no.custo}}}")

    def expande_no() -> None:
        pass

    def calcula_g() -> None:
        pass

    def orderna_fronteira() -> None:
        pass

    def __calcula_h(self, estado_1: str) -> None:
        estacao_1, linha_1 = estado_1
        estacao_2, linha_2 = self.estado_final

        h = self.mapa_distancia_direta.loc[estacao_1, estacao_2]

        if linha_1 != linha_2:
            h += self.tempo_baudeacao

        print(h)

        return h

    def __verifica_objetivo(self, no: No) -> None:
        return self.estado_final == no.estado
