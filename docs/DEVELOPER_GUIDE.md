# 🛠️ Guia do Desenvolvedor (Manutenção e Expansão)

#Este guia define os protocolos rígidos para adicionar novas funcionalidades ao sistema. **Nunca quebre o encapsulamento das camadas.**

## 1️⃣ Como adicionar suporte a um NOVO SITE (ex: Vjudge, CSES)
A camada lógica (`analytics.py`) **NÃO DEVE** ser tocada. Tudo acontece em `api.py`.
#
1. Abra `api.py`.
2. Crie uma nova classe herdando de `PlatformAPI` (ex: `class CSESApi(PlatformAPI):`).
3. Implemente obrigatoriamente o método `get_user_submissions(self, handle)`.
4. Faça a requisição HTTP/Scraping necessária dentro desse método.
5. Traduza a resposta para a Dataclass universal `Submission` (e instancie o `Problem` interno nela).
6. Vá no arquivo principal (backend ou `app.py`) e adicione sua nova classe na injeção de dependências do `OmniAnalytics`:
   ```python
   apis = [CodeforcesAPI(), AtCoderAPI(), CSESApi()]
   analytics = OmniAnalytics(apis, ["handle1"])
   ```

## 2️⃣ Como adicionar um NOVO GRÁFICO (ex: Heatmap de Submissões)
A camada principal do Streamlit (`app.py`) **NÃO DEVE** conter lógica de Plotly/Dataframes. Tudo acontece em `charts.py`.

1. Abra `charts.py`.
2. Crie uma nova classe herdando de `BaseChart` (ex: `class ActivityHeatmapChart(BaseChart):`).
3. Defina o atributo estático `name` (ex: `name = "Heatmap de Atividade"`).
4. Implemente o método abstrato `build_figure(self)`.
   * Acesse os dados via `self.analytics`.
   * Retorne um objeto Figure do Plotly (ou `None` se não houver dados).
5. Exemplo:
   ```python
   class HeatmapChart(BaseChart):
       name = "Dias mais ativos"
       def build_figure(self):
           dados = self.analytics.get_alguma_coisa()
           if not dados: return None
           fig = px.density_heatmap(...)
           return fig
   ```
6. Vá no `app.py`, importe sua nova classe e adicione-a na lista de `classes_de_graficos`:
   ```python
   classes_de_graficos = [VerdictsChart, LanguagesChart, HeatmapChart]
   ```
   *Magia:* O gráfico aparecerá automaticamente no select box da interface e será renderizado corretamente no grid.

## 3️⃣ Regra de Ouro (State Management)
#O Streamlit executa o script proceduralmente a cada interação. **Toda e qualquer chamada pesada de API deve ser encapsulada em uma função decorada com `@st.cache_data`.** Nunca inicialize `OmniAnalytics` diretamente no escopo global sem caching, senão o sistema tomará Rate Limit das APIs.