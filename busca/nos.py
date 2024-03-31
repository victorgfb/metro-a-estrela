from typing import Tuple

import numpy as np
import pandas as pd


class No:
    """
    Representa um nó no algoritmo do A*

    Atributos:
        estado (Tuple[str, str]): O nome da estação e a linha que o nó representa.
        g (int): O tempo que leva para percorrer o caminho até este nó a partir do nó inicial.
        h (int): A estimativa do tempo para percerrer o caminho deste nó até o nó objetivo.
        caminho (list): A lista de nós que formam o caminho do nó inicial até este nó.
        estado_pai (Tuple[str, str]): O estado do nó pai.
    """

    def __init__(
        self,
        estado: Tuple[str, str],
        g: int,
        h: int,
        caminho: list,
        estado_pai: Tuple[str, str],
    ) -> None:
        """
        Inicializa um nó com o estado, g, h, o caminho e o estado do nó pai. Além disso calcula o custo total do nó.
        """

        self.estado = estado
        self.g = round(g, 2)
        self.h = round(h, 2)
        self.custo = round(self.g + self.h, 2)
        self.caminho = caminho
        self.estado_pai = estado_pai

    def __lt__(self, other):
        """
        Define a comparação de menor que entre dois nós com base no custo.
        """

        return self.custo < other.custo

    def __eq__(self, other):
        """
        Define a operação de igualdade entre dois nós.
        """
        return (
            self.estado == other.estado
            and self.g == other.g
            and self.h == other.h
            and self.caminho == other.caminho
            and self.estado_pai == other.estado_pai
        )

    def __hash__(self):
        """
        Define o hash do nó.
        """
        return hash((self.estado, self.g, *self.caminho, self.estado_pai))
