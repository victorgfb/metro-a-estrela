from nos import AEstrela

if __name__ == "__main__":
    estado_inicial = ("e5", "amarelo")
    estado_final = ("e1", "vermelho")
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

    print(f"Custo da solução: {custo_solucao}")
    print(f"Solução: {solucao}")
