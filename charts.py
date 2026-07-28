from abc import ABC, abstractmethod
import pandas as pd
import plotly.express as px
from analytics import Analytics

class BaseChart(ABC):
    name: str = "Chart"

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
            container.plotly_chart(fig, width='stretch')
        else:
            container.info(f"Not enough data on: {self.name}")

class VerdictsChart(BaseChart):
    name = "Veredicts"

    def build_figure(self):
        stats = self.analytics.get_verdict_stats(self.start_ts, self.end_ts)
        if not stats: return None
        df = pd.DataFrame(list(stats.items()), columns=["Veredict", "Amount"])
        color_map = {"OK": "#28a745",
                    "WRONG_ANSWER": "#dc3545",
                    "TIME_LIMIT_EXCEEDED": "#fbff00",
                    "RUNTIME_ERROR": "#ff6a07",
                    "COMPILATION_ERROR": "#828180",
                    "SKIPPED": "#ffffff"}
        return px.pie(df, values="Amount", names="Veredict", hole=0.4, color="Veredict", color_discrete_map=color_map)

class LanguagesChart(BaseChart):
    name = "Linguagens Utilizadas"

    def build_figure(self):
        stats = self.analytics.get_language_stats(self.start_ts, self.end_ts)
        if not stats: return None
        df = pd.DataFrame(list(stats.items()), columns=["Linguagem", "Submissões"])
        return px.bar(df, x="Linguagem", y="Submissões", color="Submissões", color_continuous_scale="Blues")

class TagsFrequencyChart(BaseChart):
    name = "Tags"

    def build_figure(self):
        stats = self.analytics.get_tags_stats(self.start_ts, self.end_ts)
        if not stats: return None
        df = pd.DataFrame(list(stats.items())[:15], columns=["Tag", "Frequency"])
        df = df.sort_values(by="Frequency", ascending=True) 
        fig = px.bar(df, x="Frequency", y="Tag", orientation='h', color="Frequency", color_continuous_scale="Viridis")
        fig.update_layout(yaxis_title=None, xaxis_title=None)
        return fig