from busca.a_estrela import AEstrela

if __name__ == "__main__":
    estado_inicial = tuple(
        input('Insira o estado inicial (no formato "estação,linha"): ').split(",")
    )

    estado_final = tuple(
        input('Insira o estado final (no formato "estação,linha"): ').split(",")
    )

    # estado_inicial = ("e14", "vermelho")
    # estado_final = ("e6", "azul")

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

    solucao, custo_solucao = a.busca()

    print("###################################")
    print(f"Custo da solução: {custo_solucao}")
    print(f"Solução: {solucao}")
