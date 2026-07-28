from abc import ABC, abstractmethod
import pandas as pd
import plotly.express as px
from analytics import Analytics

class BaseChart(ABC):
    name: str = "Gráfico Genérico"

    def __init__(self, analytics: Analytics, start_ts: int = None, end_ts: int = None):
        self.analytics = analytics
        self.start_ts = start_ts
        self.end_ts = end_ts

    @abstractmethod
    def build_figure(self):
        pass

    def render(self, container):
        fig = self.build_figure()
        if fig:
            container.plotly_chart(fig, use_container_width=True)
        else:
            container.info(f"Sem dados suficientes para: {self.name}")

class VerdictsChart(BaseChart):
    name = "Distribuição de Veredictos"

    def build_figure(self):
        stats = self.analytics.get_verdict_stats(self.start_ts, self.end_ts)
        if not stats: return None
        df = pd.DataFrame(list(stats.items()), columns=["Veredicto", "Quantidade"])
        color_map = {"OK": "#28a745", "WRONG_ANSWER": "#dc3545", "TIME_LIMIT_EXCEEDED": "#ffc107"}
        return px.pie(df, values="Quantidade", names="Veredicto", hole=0.4, color="Veredicto", color_discrete_map=color_map)

class LanguagesChart(BaseChart):
    name = "Linguagens Utilizadas"

    def build_figure(self):
        stats = self.analytics.get_language_stats(self.start_ts, self.end_ts)
        if not stats: return None
        df = pd.DataFrame(list(stats.items()), columns=["Linguagem", "Submissões"])
        return px.bar(df, x="Linguagem", y="Submissões", color="Submissões", color_continuous_scale="Blues")

class TagsFrequencyChart(BaseChart):
    name = "Frequência de Tags (Estudo)"

    def build_figure(self):
        stats = self.analytics.get_tags_stats(self.start_ts, self.end_ts)
        if not stats: return None
        df = pd.DataFrame(list(stats.items())[:15], columns=["Tag", "Frequência"])
        df = df.sort_values(by="Frequência", ascending=True) 
        return px.bar(df, x="Frequência", y="Tag", orientation='h', color="Frequência", color_continuous_scale="Viridis")