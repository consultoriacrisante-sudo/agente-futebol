from buscar_escalacoes import buscar_escalacoes
from estruturar_escalacoes import estruturar_escalacao


print()
print("=" * 60)
print("TESTE DA ESTRUTURAÇÃO COM DADOS REAIS")
print("=" * 60)


time_casa = "Marseille"
time_fora = "Strasbourg"
campeonato = "Ligue 1"
data = "21/08/2026"


print()
print(f"Buscando: {time_casa} x {time_fora}")
print()


resultados = buscar_escalacoes(
    time_casa,
    time_fora,
    campeonato,
    data
)


print(f"Total de fontes encontradas: {len(resultados)}")
print()


for numero, resultado in enumerate(resultados, start=1):

    dados = estruturar_escalacao(resultado)

    print("=" * 60)
    print(f"FONTE {numero}")
    print("=" * 60)

    print()
    print("Título:")
    print(dados["titulo"])

    print()
    print("Escalação confirmada:")
    print(dados["confirmada"])

    print()
    print("Formação encontrada:")
    print(dados["formacao"])

    print()
    print("URL:")
    print(dados["url"])

    print()
