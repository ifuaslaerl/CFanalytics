import streamlit as st
import pandas as pd
from datetime import date, timedelta
import time
from api import CodeforcesAPI, AtCoderAPI
from analytics import Analytics
from charts import VerdictsChart, LanguagesChart, TagsFrequencyChart

@st.cache_data(ttl=600, show_spinner=False)
def load_analytics_data(handles_str: str) -> Analytics:
    apis = [CodeforcesAPI(), AtCoderAPI()]
    handles_list = handles_str.split(',')
    return Analytics(apis, handles_list)

class CPAnalyticsDashboard:
    def __init__(self):
        self._configure_page()
        self.handles_str = None
        self.analytics = None

    def _configure_page(self):
        st.set_page_config(page_title="CF Analytics", layout="wide")

    def _render_sidebar(self):
        st.sidebar.caption("For multiple accounts, separate with commas.")
        input_handles = st.sidebar.text_input("Handles (CF and/or AtCoder)", value="tourist")
        btn_carregar = st.sidebar.button("Start", type="primary")

        if btn_carregar:
            st.session_state["handles_str"] = input_handles

        self.handles_str = st.session_state.get("handles_str")
        if self.handles_str:
            with st.spinner(f"Processing {self.handles_str}..."):
                self.analytics = load_analytics_data(self.handles_str)

    def _render_upsolving_tab(self):
        st.subheader("Filtrar Questões Pendentes")
        upsolving_list = self.analytics.get_upsolving_list()
        
        c1, c2, c3 = st.columns([2, 1, 1])
        selected_tags = c1.multiselect("Filtrar por Tags", options=self.analytics.get_available_tags())
        
        ratings_validos = [p.rating for p in upsolving_list if isinstance(p.rating, int)]
        min_r, max_r = (min(ratings_validos), max(ratings_validos)) if ratings_validos else (800, 3500)
        rating_range = c2.slider("Faixa de Dificuldade", min_value=800, max_value=3500, value=(min_r, max_r), step=100)
        
        contest_filter = c3.text_input("ID do Contest (Opcional)")

        filtered = self.analytics.filter_unsolved(
            target_tags=selected_tags if selected_tags else None,
            contest_id=contest_filter if contest_filter else None
        )
        
        filtered = [
            p for p in filtered 
            if (isinstance(p.rating, int) and rating_range[0] <= p.rating <= rating_range[1]) or p.rating == "Sem Rating"
        ]

        st.caption(f"Exibindo **{len(filtered)}** de **{len(upsolving_list)}** questões.")

        if filtered:
            df = pd.DataFrame([{
                "Plataforma": p.platform, "Contest": p.contest_id, "Índice": p.index,
                "Nome": p.name, "Rating": p.rating, "Tags": ", ".join(p.tags), "Link": p.url
            } for p in filtered])

            st.dataframe(
                df,
                column_config={"Link": st.column_config.LinkColumn("Link", display_text="Abrir 🔗")},
                width='stretch', hide_index=True
            )
            st.download_button("📥 Baixar CSV", data=df.to_csv(index=False).encode('utf-8'), file_name="upsolving.csv", mime="text/csv")
        else:
            st.info("Nenhuma questão encontrada.")

    def _render_contests_tab(self):
        st.subheader("Contests Incompletos")
        contests = self.analytics.get_incomplete_contests()
        for c_id, problems in list(contests.items())[:15]:
            with st.expander(f"📌 Contest #{c_id} ({problems[0].platform}) — {len(problems)} pendência(s)"):
                for p in problems:
                    st.markdown(f"- **[{p.index} - {p.name}]({p.url})** | Rating: `{p.rating}`")

    def _render_charts_tab(self):
        c1, c2 = st.columns(2)
        
        intervalo = c1.date_input("Epoch", value=(date.today() - timedelta(days=365), date.today()), max_value=date.today())
        start_ts, end_ts = None, None
        if len(intervalo) == 2:
            start_ts = int(time.mktime(intervalo[0].timetuple()))
            end_ts = int(time.mktime(intervalo[1].timetuple())) + 86399 

        classes_graficos = [VerdictsChart, LanguagesChart, TagsFrequencyChart]
        mapa_classes = {cls.name: cls for cls in classes_graficos}
        
        selecionados = c2.multiselect("Charts", options=list(mapa_classes.keys()), default=[VerdictsChart.name, TagsFrequencyChart.name])

        st.divider()
        colunas = st.columns(2)
        for i, nome in enumerate(selecionados):
            container = colunas[i % 2]
            with container:
                st.markdown(f"**{nome}**")
                grafico = mapa_classes[nome](self.analytics, start_ts, end_ts)
                grafico.render(container)

    def run(self):
        self._render_sidebar()
        if not self.analytics:
            st.info("👈 Type the handle(s) in the sidebar to start.")
            return

        st.title(f"Dashboard")
        t1, t2, t3 = st.tabs(["📊 Charts", "🏆 Contests", "🎯 Upsolving"])
        with t1: self._render_charts_tab()
        # with t2: self._render_contests_tab()
        # with t3: self._render_upsolving_tab()

if __name__ == "__main__":
    app = CPAnalyticsDashboard()
    app.run()