import nltk

# Baixa os recursos necessários, caso ainda não estejam disponíveis.
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('averaged_perceptron_tagger_eng')

def get_numerical_phrases(sentence):
    """
    Extrai frases numéricas de uma sentença.
    Para cada expressão encontrada, extrai o valor numérico e, se disponível,
    a unidade (por exemplo, "cats" ou "books").
    Expressões monetárias (ex.: "$10") são transformadas em "10 (dólar)".
    
    Argumentos:
        sentence: A sentença de entrada.
    
    Retorna:
        Uma lista de elementos extraídos no formato "valor (unidade)" ou apenas
        o valor numérico, de acordo com o padrão.
    """
    # Pré-processamento: garante que símbolos monetários sejam tokens separados.
    sentence = sentence.replace('$', ' $').replace('£', ' £').replace('€', ' €')

    # Tokenização
    tokens = nltk.word_tokenize(sentence)
    # Etiquetagem de partes do discurso
    tagged = nltk.pos_tag(tokens)

    # Definição da gramática:
    # 1) CurrencyPhrase: pega expressões monetárias (e.g., "$10")
    # 2) NumericalPhrase: expressões numéricas complexas e simples (e.g., "5 books", "more than 5 books")
    grammar = r"""
        CurrencyPhrase: {<\$><CD>}
        NumericalPhrase: {<NN|NNS>?<RB>?<JJR><IN><CD><NN|NNS>?}
        NumericalPhrase: {<CD><NN|NNS>?}
    """

    # Criação do parser com a gramática
    parser = nltk.RegexpParser(grammar)
    tree = parser.parse(tagged)

    phrases = []
    # Percorre as subárvores capturando os padrões definidos.
    for subtree in tree.subtrees():
        label = subtree.label()
        leaves = list(subtree.leaves())
        # Caso seja expressão monetária
        if label == 'CurrencyPhrase':
            currency, value = None, None
            for token, tag in leaves:
                if token == '$':
                    currency = "dólar"
                elif tag == "CD":
                    value = token
            if value and currency:
                phrases.append(f"{value} ({currency})")
            else:
                phrases.append(" ".join(token for token, tag in leaves))
        # Caso seja uma expressão numérica geral
        elif label == 'NumericalPhrase':
            numeric_value, unit = None, None
            for i, (token, tag) in enumerate(leaves):
                if tag == "CD":
                    numeric_value = token
                    # Se houver um próximo token e for um substantivo, define-o como unidade
                    if i + 1 < len(leaves):
                        next_token, next_tag = leaves[i + 1]
                        if next_tag in ("NN", "NNS"):
                            unit = next_token
                    break  # Usa o primeiro valor numérico encontrado
            if numeric_value is not None:
                if unit:
                    phrases.append(f"{numeric_value}, unit: ({unit})")
                else:
                    phrases.append(numeric_value)
            else:
                # Se não identificar o número, retorna a expressão completa
                phrases.append(" ".join(token for token, tag in leaves))
    return phrases

# Exemplos de uso
sentences = [
    "I have more than 5 books.",
    "The price is less than $10.",
    "The temperature is exactly 25 degrees.",
    "He has at least 3 apples.",
    "She has 2 cats and 3 dogs."
]

for s in sentences:
    print(f"Sentença: {s}")
    print(f"Extração: {get_numerical_phrases(s)}\n")