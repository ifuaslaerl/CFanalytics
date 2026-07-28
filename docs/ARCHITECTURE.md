# 🏛️ Omni CP Analytics - Arquitetura do Sistema

## 📌 Visão Geral
O sistema é uma ferramenta de Business Intelligence e Upsolving para Programação Competitiva. Ele consolida submissões de múltiplas plataformas (Codeforces, AtCoder, etc.) e cruza dados de múltiplas contas (para ignorar falsos-negativos gerados por contas "smurfs").

## 🧩 Princípios de Design Utilizados
1. **SOLID (Single Responsibility & Open/Closed):** Cada arquivo tem um propósito único. O sistema está aberto para extensão (adicionar novos gráficos ou plataformas) mas fechado para modificação (não é necessário alterar o núcleo para isso).
2. **Adapter Pattern:** Isolamos a comunicação externa através da interface `PlatformAPI`. A camada de negócio não sabe como uma API funciona, apenas que ela retorna uma lista padronizada de objetos `Submission`.
3. **Template Method / Strategy Pattern:** A renderização de gráficos (`BaseChart`) abstrai o Streamlit e o Plotly. Novos gráficos herdam a estrutura base e implementam apenas a lógica de montagem do dado.

## 📂 Estrutura de Diretórios
├── models.py       # Dataclasses universais (User, Problem, Submission). Independentes de plataforma.
├── api.py          # Implementação das APIs usando Adapter Pattern (CodeforcesAPI, AtCoderAPI).
├── analytics.py    # O "Cérebro". Contém a classe `OmniAnalytics`. Agrupa contas e gera métricas.
├── charts.py       # Padrões visuais. Contém a interface `BaseChart` e implementações (ex: VerdictsChart).
├── exporters.py    # Utilitários estáticos para salvar em CSV/JSON.
└── app.py          # Camada de Interface Gráfica (Streamlit). Funciona apenas como um View/Controller.

## 🔄 Fluxo de Dados (Data Flow)
1. O `app.py` recebe handles do usuário (ex: `tourist, tourist_smurf`).
2. O `app.py` injeta as classes de API (`CodeforcesAPI`, `AtCoderAPI`) no `OmniAnalytics`.
3. `OmniAnalytics` faz fetch nos endpoints, converte JSONs caóticos em instâncias limpas de `Submission` e as armazena em memória.
4. O usuário interage na UI, que invoca funções como `get_upsolving_list()`.
5. Se for um gráfico, o `app.py` passa o `OmniAnalytics` para o `BaseChart` respectivo, que consome, formata e desenha na tela.