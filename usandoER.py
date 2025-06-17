import re

# Textos de exemplo
textos = [
    "o valor é more than 50",
    "a temperatura está less than 10 graus",
    "procuro algo que custe between 100 and 200 reais",
    "a capacidade é de at least 25 litros",
    "o preço pode ser AT MOST 99"
]

# Regex da resposta aceita no Stack Overflow
regex_solucao = r"(?i)(?:\b(between|from)\s+(\d+)\s+and\s+(\d+)\b|\b(more|greater)\s+than\s+(\d+)\b|\b(less)\s+than\s+(\d+)\b|\b(at\s+least)\s+(\d+)\b|\b(at\s+most)\s+(\d+)\b)"

print("\n--- Aplicação da Solução ---")
for texto in textos:
    # re.search encontra a primeira ocorrência do padrão no texto
    encontrado = re.search(regex_solucao, texto)
    if encontrado:
        # .group(0) retorna todo o texto que casou com a expressão
        print(f"Texto: '{texto}' -> Padrão completo encontrado: '{encontrado.group(0)}'")
    else:
        print(f"Texto: '{texto}' -> Nenhum padrão encontrado.")