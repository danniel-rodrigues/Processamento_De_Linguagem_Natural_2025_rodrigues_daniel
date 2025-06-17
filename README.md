# **Tutorial de PLN Atividade 1**

## **Integrantes do grupo:**
#### - Allan Cristiano  
#### - Almir Vinícius  
#### - Daniel Santos  
#### - José Clenildo

---

### **Escolha do problema**
Seguindo as instruções do professor, foi feita uma pesquisa no Stack Overflow com a tag de nlp(natural language processing) e analisadas
as perguntas que foram sendo mostradas pela plataforma. Para facilitar o trabalho, o grupo dividiu os temas da Atividade 1 entre os integrantes,
e com isso foi encontrado a pergunta “How to extract numbers (along with comparison adjectives or ranges)” no tema de tokenização. Nesta pergunta
teve apenas 1 resposta aprovada pela plataforma, portanto foi esta a aplicada pelo grupo.

Por não ter código fonte vinculado à pergunta original, foi feito algo que se comportasse de forma parecida com o que seria esperado do código.

### **Processo de desenvolvimento**

A aplicação da resposta inicialmente foi idêntica ao que estava na pergunta no Stack Overflow, porém para tentar tornar ela mais completa o grupo foi
alterando alguns fatores, como a formação das frases de acordo com o nltk e quais tipos de tokens que deveriam ser pegos para a compreensão das frases.
Após os ajustes terem sido realizados, todas as alterações foram disponibilizadas neste repositório do GitHub.

**Link do problema encontrado no Stack Overflow:**
[How to extract numbers (along with comparison adjectives or ranges)](https://stackoverflow.com/questions/45126071/how-to-extract-numbers-along-with-comparison-adjectives-or-ranges)

### **Passo a passo: Criação de ambiente virtual Python**

#### **Pré-requisitos:**

* Python instalado (versão 3.8 ou superior)  
* Terminal / Prompt de comando (Windows, macOS ou Linux)

#### **1 \- Crie uma pasta para o projeto (através do terminal):**  
	mkdir extract_number_with_comparison_adjetives  
	cd extract_number_with_comparison_adjetives

#### **2 \- Crie o ambiente virtual:**  
No terminal, já na pasta do projeto, digite:
	`python3 -m venv venv`

Isso irá criar uma pasta **venv/** com todos os arquivos do ambiente virtual.

#### **3 \- Ative o ambiente virtual:**  
No Windows (cmd ou Powershell):  
  `venv\Scripts\activate`

Você saberá que está ativo se o terminal mostrar algo como:	`(venv)C:\Users\seu_nome\extract_number_with_comparison_adjetives>`

No macOS/Linux:  
	`source venv/bin/activate`

#### **4 \- Instale o NLTK:**  
`pip install nltk`

#### **5 - Rodar o código do python**
Com o terminal localizado no diretório com o código em questão a ser rodado, basta rodar o programa e ver como ele responde.

### **Considerações finais**

No repositório do github se encontram algumas variações do código original que foram feitas, como uma versão que foi necessária
a mudança para rodar no windows, por causa de algum problema na biblioteca, e uma variação que não utilizou e modificação de como
o programa identifica uma frase e suas partes para conseguir englobar os tokens que geram o sentido do texto. Uma versão que conseguiu
concentrar o tratamento dos adjetivos para juntar os adjetivos que se completam em relação ao sentido da frase e consegue identificar a
unidade de medida do valor numérico mais facilmente. Cada variação criada tem seu ponto positivo e negativo, por isso foi interessante
deixar elas separadas para demonstrar como cada uma faz a classificação e identificação dos tokens no processo de tokenização.
