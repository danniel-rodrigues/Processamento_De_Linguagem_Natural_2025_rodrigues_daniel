import nltk
import re
import os


# Caminho onde você quer salvar os dados NLTK (por exemplo, dentro do seu projeto)
nltk_data_path = os.path.join(os.path.dirname(__file__), 'venv', 'nltk_data')

# Cria o diretório, se não existir
os.makedirs(nltk_data_path, exist_ok=True)

# Adiciona esse caminho à lista de onde o NLTK procura os dados
nltk.data.path.append(nltk_data_path)

# Baixa os pacotes necessários para esse caminho
nltk.download('punkt_tab', download_dir=nltk_data_path)
nltk.download('averaged_perceptron_tagger', download_dir=nltk_data_path)


# Dicionário de símbolos e nomes de unidades/moedas
unit_map = {
    '$': 'dollar', 'dollars': 'dollar', 'usd': 'dollar',
    '¥': 'yene',
    'lbs': 'pound', 'pounds': 'pound',
    'kg': 'kilogram', 'kilograms': 'kilogram',
    'seconds': 'second', 'second': 'second', 's': 'second',
    'feet': 'foot', 'feets': 'foot', 'ft': 'foot',
    'meters': 'meter', 'meter': 'meter',
}

# Relações completas como aparecem no texto
relation_keywords = {
    ('not', 'more'): 'not more than',
    ('not', 'greater'): 'not greater than',
    ('not', 'less'): 'not less than',
    ('at', 'least'): 'at least',
    ('at', 'most'): 'at most',
    ('greater',): 'greater than',
    ('more',): 'more than',
    ('less',): 'less than',
    ('under',): 'less than',
    ('over',): 'greater than',
    ('between',): 'between',
    ('in',): 'between',
    ('within',): 'between',
    ('faster',): 'greater than',
    ('slower',): 'less than',
}

# Duas regras de chunk
grammar = r"""
    NumericalPhrase: 
        {<NN|NNS>?<RB>?<JJR|RBR><IN><\$>?<CD><CD>?<NN|NNS>?}  # e.g., greater than $100
    RangePhrase:
        {<NN|NNS>?<IN>?<JJ>?<NN|NNS>?}     # e.g., 5-7 feet
"""


def space_currency_amounts(text, currencies_dict):
    # busca qualquer um dos símbolos da lista de moedas seguido por um número
    # opcionalmente seguido de parte decimal
    pattern = r'((?:' + '|'.join(re.escape(sym) for sym in currencies_dict.keys()) + r')\d+(?:[\.,]\d+)?)'
    
    # recebe o trecho encontrado, verifica a moeda, e devolve com um espaço no meio: "$ 100"
    def replacer(match):
        s = match.group(0)
        for symbol in currencies_dict:
            if s.startswith(symbol):
                return s.replace(symbol, f"{symbol} ")
        return s

    # percorre todo o texto e modifica todas as ocorrências coladas da moeda + número
    return re.sub(pattern, replacer, text)


def extract_chunks(text):
    tokens = nltk.word_tokenize(text)
    # tokens = [re.sub(r'–|−|—', '-', t) for t in tokens]  # normaliza hífens
    pos_tags = nltk.pos_tag(tokens)

    parser = nltk.RegexpParser(grammar)
    tree = parser.parse(pos_tags)

    results = []

    for subtree in tree.subtrees():
        label = subtree.label()
        # chunk_words = [w for w, t in subtree.leaves()]
        chunk_pos = [i for i, (w, _) in enumerate(pos_tags) if w == subtree.leaves()[0][0]][0]

        if label == 'NumericalPhrase':
            relation = None
            unit = None
            value = None

            # verifica relação pela combinação de palavras
            words_lower = [w.lower() for w, _ in subtree.leaves()]
            for length in range(3, 0, -1):  # tenta bigramas e trigramas primeiro
                for i in range(len(words_lower) - length + 1):
                    key = tuple(words_lower[i:i+length])
                    if key in relation_keywords:
                        relation = relation_keywords[key]
                        break
                if relation:
                    break

            for word, tag in subtree.leaves():
                lw = word.lower()

                match = re.match(r'(\d+(?:\.\d+)?)([a-zA-Z¥$€]*)', lw)  # número + unidade colada
                if match:
                    num = match.group(1)
                    unit_suffix = match.group(2)
                    value = float(num) if '.' in num else int(num)
                    if unit_suffix in unit_map:
                        unit = unit_map[unit_suffix]
                elif lw in unit_map:
                    unit = unit_map[lw]
                elif word in unit_map:  # <-- adiciona esta verificação extra para símbolos como '¥'
                    unit = unit_map[word]


            if value:
                results.append({
                    'value': value,
                    'unit': unit,
                    'relation': relation,
                    'position': chunk_pos
                })

        elif label == 'RangePhrase':
            nums = []
            unit = None

            for word, tag in subtree.leaves():
                lw = word.lower()
                if tag == 'CD':
                    nums.append(float(word) if '.' in word else int(word))
                elif lw in unit_map:
                    unit = unit_map[lw]

            if len(nums) == 2:
                results.append({
                    'from': nums[0],
                    'to': nums[1],
                    'unit': unit,
                    'relation': 'between',
                    'position': chunk_pos
                })

    return results

sentence = "send me a table with a price greater than $100"
# sentence = "weight not more than 200lbs"
# sentence = "height in 5-7 feets"
preparedSentence = space_currency_amounts(sentence, unit_map)
print(extract_chunks(preparedSentence))
