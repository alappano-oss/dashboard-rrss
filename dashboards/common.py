from __future__ import annotations
import pandas as pd
import streamlit as st
from src.metrics import kpis
from src.comparisons import compare_kpis, equivalent_previous_period
from src.content_analysis import top_contents, format_summary, weekday_summary, add_relative_performance
from src.charts import time_series, bar_summary
from src.insights import generate_insights
from src.utils import fmt_number, fmt_pct


def render_dashboard(df: pd.DataFrame, brand_config: dict):
    st.title(f"Dashboard de Analytics — {brand_config['display_name']}")
    if df.empty:
        st.info('No hay datos procesados para esta marca. Cargá uno o más CSV desde “Actualizar datos”.')
        return
    df=df.copy(); df['date']=pd.to_datetime(df['date'], errors='coerce')
    min_date,max_date=df['date'].min(),df['date'].max()
    st.caption(f'Período disponible: {min_date:%d/%m/%Y} — {max_date:%d/%m/%Y}')

    with st.sidebar:
        st.header('Filtros')
        platforms=sorted(df['platform'].dropna().unique().tolist())
        formats=sorted(df['format'].dropna().unique().tolist())
        contents=sorted(df['content_type'].dropna().unique().tolist())
        selected_platform=st.multiselect('Plataforma',platforms)
        selected_format=st.multiselect('Formato',formats)
        selected_content=st.multiselect('Tipo de contenido',contents)
        dates=st.date_input('Fecha desde / hasta',(min_date.date(),max_date.date()))
        if st.button('Limpiar filtros',use_container_width=True): st.rerun()
    filtered=df.copy()
    if selected_platform: filtered=filtered[filtered.platform.isin(selected_platform)]
    if selected_format: filtered=filtered[filtered.format.isin(selected_format)]
    if selected_content: filtered=filtered[filtered.content_type.isin(selected_content)]
    if isinstance(dates,tuple) and len(dates)==2:
        filtered=filtered[(filtered.date.dt.date>=dates[0])&(filtered.date.dt.date<=dates[1])]

    cur=kpis(filtered)
    start,end=filtered.date.min(),filtered.date.max()
    previous=pd.DataFrame()
    if pd.notna(start) and pd.notna(end):
        ps,pe=equivalent_previous_period(start,end); previous=df[(df.date>=ps)&(df.date<=pe)]
    prev=kpis(previous) if not previous.empty else {}

    st.subheader('Resumen ejecutivo')
    cards=[('Alcance','reach_total'),('Impresiones','impressions_total'),('Interacciones','interactions_total'),('Engagement Rate','er_reach'),('Seguidores netos','followers_net'),('Publicaciones','posts')]
    cols=st.columns(6)
    for col,(label,key) in zip(cols,cards):
        val=cur.get(key); old=prev.get(key)
        main=f'{val:,.1f}%'.replace(',', 'X').replace('.', ',').replace('X','.') if key=='er_reach' and pd.notna(val) else fmt_number(val)
        delta=fmt_pct((val-old)/abs(old)*100) if pd.notna(val) and pd.notna(old) and old!=0 else None
        col.metric(label,main,delta)

    st.subheader('Evolución')
    for metric in ['reach','impressions','interactions']:
        fig=time_series(filtered,metric,'W')
        if fig: st.plotly_chart(fig,use_container_width=True)

    st.subheader('Contenido')
    table=add_relative_performance(filtered)
    display_cols=[c for c in ['date','platform','format','copy','reach','interactions','er_reach','video_views','shares','comments','performance_relative','url'] if c in table]
    st.dataframe(table[display_cols].sort_values('date',ascending=False),use_container_width=True,hide_index=True)

    st.subheader('Top contenidos')
    tabs=st.tabs(['Alcance','Interacciones','Engagement','Compartidos','Comentarios','Reproducciones'])
    for tab,metric in zip(tabs,['reach','interactions','er_reach','shares','comments','video_views']):
        with tab:
            top=top_contents(filtered,metric)
            if top.empty: st.info('Dato no disponible para este ranking.')
            else: st.dataframe(top,use_container_width=True,hide_index=True)

    st.subheader('Análisis por formato')
    fs=format_summary(filtered)
    if not fs.empty:
        st.plotly_chart(bar_summary(fs,'format','alcance_promedio','Alcance promedio por formato'),use_container_width=True)
        st.dataframe(fs,use_container_width=True,hide_index=True)

    st.subheader('Análisis por día')
    ws=weekday_summary(filtered)
    if not ws.empty:
        st.plotly_chart(bar_summary(ws,'weekday','alcance_promedio','Alcance promedio por día'),use_container_width=True)
        st.dataframe(ws,use_container_width=True,hide_index=True)

    st.subheader('Insights')
    for insight in generate_insights(filtered,previous): st.write('• '+insight)

    st.subheader('Exportación')
    st.download_button('Descargar dataset procesado',filtered.to_csv(index=False).encode('utf-8-sig'),'dataset_procesado.csv','text/csv')
    st.download_button('Descargar publicaciones',table[display_cols].to_csv(index=False).encode('utf-8-sig'),'publicaciones.csv','text/csv')
    st.download_button('Descargar resumen KPIs',pd.DataFrame([cur]).to_csv(index=False).encode('utf-8-sig'),'kpis.csv','text/csv')
