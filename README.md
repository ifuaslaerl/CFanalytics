# CF Analytics

Um dashboard interativo e inteligente para acompanhamento e **Upsolving** em Programação Competitiva. Construído em Python, o sistema reúne dados de múltiplas plataformas e múltiplas contas para auxiliar os seus estudos.

## Funcionalidades

- **Upsolving Inteligente:** Cruzamento de dados de múltiplas contas. Se você tomou *Wrong Answer* na conta secundária e *Accepted* na principal, a questão é considerada resolvida.
- **Múltiplas Plataformas:** Suporte nativo à API do **Codeforces** e à API do **AtCoder** (via Kenkoooo).
- **Análise Gráfica (BI):** Gráficos interativos para veredictos, linguagens utilizadas e mapeamento das tags que você mais estuda, com filtros de data precisos.
- **Filtros Avançados:** Filtre as suas questões pendentes por dificuldade (rating), contest específico ou tags (ex: `dp`, `graphs`).
- **Exportação:** Baixe as suas listas de questões filtradas em CSV para estudar offline ou importar no Notion/Excel.

## 🛠️ Como Instalar e Rodar

### Pré-requisitos
Certifique-se de ter o [Python 3.9+](https://www.python.org/downloads/) instalado na sua máquina.

### Passo 1: Instalar dependências
Abra o seu terminal na pasta do projeto (`cf_analytics`) e execute o comando abaixo para instalar as bibliotecas necessárias:

```bash
pip install -r requirements.txt
```

*(Dica: É recomendado usar um ambiente virtual (`venv`) para não misturar as bibliotecas do projeto com as do seu sistema operacional).*

### Passo 2: Rodar a aplicação
Ainda no terminal, inicie o servidor do Streamlit:

```bash
streamlit run app.py
```

O seu navegador abrirá automaticamente no endereço `http://localhost:8501`.

## 🎯 Como Usar
1. Na barra lateral esquerda, digite o seu handle (nome de usuário).
2. Se você possuir contas secundárias (smurfs) no Codeforces ou no AtCoder, digite todas elas separadas por vírgula. Exemplo: `tourist, tourist_smurf`.
3. Clique em **Analisar Contas**.
4. Navegue pelas abas superiores para acessar o seu Banco de Upsolving, Contests Pendentes e a Análise Gráfica.

## 🤝 Como Contribuir
Este projeto foi feito para ser expandido! Se você quiser adicionar suporte ao Vjudge, CSES ou criar novos gráficos de desempenho:
1. Leia o arquivo `DEVELOPER_GUIDE.md` para entender como o Padrão *Adapter* e o Padrão *Strategy* estão implementados.
2. Adicione sua classe no módulo correspondente (`api.py` ou `charts.py`).
3. O sistema reconhecerá automaticamente a sua modificação sem quebrar o código antigo.