import nltk
import re


# Mapeamento de palavras para relações padronizadas
# 'gt' -> Greater Than, 'lt' -> Less Than, 'ge' -> Greater or Equal, 'le' -> Less or Equal, 'eq' -> Equal
RELATION_MAP = {
    'more': 'gt', 'greater': 'gt', 'over': 'gt', 'faster': 'gt',
    'less': 'lt', 'under': 'lt', 'slower': 'lt',
    ('at', 'least'): 'ge', ('not', 'less'): 'ge',
    ('at', 'most'): 'le', ('not', 'more'): 'le',
}

def get_numerical_phrases(sentence):
    """
    Extrai frases numéricas de uma sentença, retornando uma lista de dicionários.
    """
    # --- Pré-processamento ---
    # 1. Garante que símbolos monetários sejam tokens separados.
    sentence = sentence.replace('$', '$ ').replace('£', '£ ').replace('€', '€ ')
    
    # 2. Separa números de unidades coladas (ex: "200lbs" -> "200 lbs")
    sentence = re.sub(r'(\d+)([a-zA-Z]+)', r'\1 \2', sentence)

    # --- Pipeline NLTK ---
    tokens = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokens)

    # Gramática para identificar frases numéricas
    grammar = r"""
        NumericalPhrase:
            {<RB|JJR|JJS|IN>*<\$>?<CD><NN|NNS>?}
            {<\$>?<CD><NN|NNS>?}
    """

    parser = nltk.RegexpParser(grammar)
    tree = parser.parse(tagged)
    
    results = []
    
    for subtree in tree.subtrees():
        if subtree.label() == 'NumericalPhrase':
            # Inicializa o dicionário de resultado para cada frase encontrada
            phrase_data = {
                'value': None, 'unit': None, 'relation': 'eq', 'position': None
            }
            
            leaves = subtree.leaves()
            
            # --- Extração da Posição ---
            try:
                first_word = leaves[0][0]
                phrase_data['position'] = tokens.index(first_word)
            except (ValueError, IndexError):
                phrase_data['position'] = -1

            # --- Extração da Relação ---
            chunk_words = [word.lower() for word, tag in leaves]
            # Procura por frases de duas palavras primeiro
            for i in range(len(chunk_words) - 1):
                pair = (chunk_words[i], chunk_words[i+1])
                if pair in RELATION_MAP:
                    phrase_data['relation'] = RELATION_MAP[pair]
                    break
            # Se não encontrou, procura por uma de palavra única
            if phrase_data['relation'] == 'eq':
                for word in chunk_words:
                    if word in RELATION_MAP:
                        phrase_data['relation'] = RELATION_MAP[word]
                        break

            # --- Extração de Valor e Unidade ---
            for i, (token, tag) in enumerate(leaves):
                if tag == 'CD':
                    phrase_data['value'] = int(token)
                elif tag in ('NN', 'NNS'):
                    phrase_data['unit'] = token.lower()
                elif token == '$':
                    phrase_data['unit'] = 'dollar'

            # Adiciona o dicionário à lista de resultados apenas se um valor foi encontrado
            if phrase_data['value'] is not None:
                results.append(phrase_data)
                
    return results

# --- Bloco de Execução Principal ---
if __name__ == "__main__":
    # Lista de exemplos para testar a função
    sentences = [
        "I want something greater than $10.",
        "The weight must be not more than 200lbs.",
        "Show me products with a height in 5-7 feets.",
        "He runs faster than 30 seconds.",
        "She has at least 3 apples.",
        "I have 2 cats and 3 dogs."
    ]

    # Itera sobre as sentenças, chama a função e imprime o resultado
    for s in sentences:
        print(f"Sentença: {s}")
        extraction_result = get_numerical_phrases(s)
        print(f"Extração: {extraction_result}\n")