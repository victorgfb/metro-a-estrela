from nos import AEstrela

if __name__ == "__main__":
    estado_inicial = ("e7", "azul")
    estado_final = ("e10", "verde")
    mapa_linhas_caminho = "linhas.csv"
    mapa_distancia_real_caminho = "distancia_real.csv"
    mapa_distancia_direta_caminho = "distancia_direta.csv"

    a = AEstrela(
        estado_inicial,
        estado_final,
        mapa_linhas_caminho,
        mapa_distancia_real_caminho,
        mapa_distancia_direta_caminho,
    )

    a.imprime_fronteira()
