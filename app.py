import streamlit as st,pandas as pd
from config.config import BRANDS
from src.ingestion import ingest_files
from src.metrics import kpis,by_format
from src.content_analysis import top_posts
from src.comparisons import period_comparison
st.set_page_config(page_title='Dashboard RRSS',layout='wide')
st.title('Dashboard de Redes Sociales')
st.caption('Meta Business Suite — Elebar / Punto Blu')
brand=st.sidebar.selectbox('Marca',list(BRANDS),format_func=lambda x:BRANDS[x]['label'])
files=st.sidebar.file_uploader('Subir CSV de Meta Business Suite',type='csv',accept_multiple_files=True)
if 'data' not in st.session_state:st.session_state.data={b:pd.DataFrame() for b in BRANDS}
if files and st.sidebar.button('Procesar archivos',type='primary'):
    data,res=ingest_files(files,brand);st.session_state.data[brand]=data
    st.sidebar.success(f"{res['files_processed']} archivo(s) procesado(s).")
    if res['duplicates']:st.sidebar.info(f"Duplicados: {res['duplicates']}")
    for x in res['warnings']:st.warning(x)
    for x in res['errors']:st.error(x)
df=st.session_state.data.get(brand,pd.DataFrame())
if df.empty:st.info('Subí uno o más CSV y hacé clic en «Procesar archivos».');st.stop()
st.subheader('Resumen ejecutivo');kp=kpis(df);cols=st.columns(len(kp))
for c,(k,v) in zip(cols,kp.items()):c.metric(k,'—' if v is None else f'{v:,.1f}')
st.subheader('Filtros');p1,p2=st.columns(2);plats=sorted(df.platform.dropna().unique());fmts=sorted(df.format.dropna().unique());sp=p1.multiselect('Plataforma',plats,plats);sf=p2.multiselect('Formato',fmts,fmts);f=df[df.platform.isin(sp)&df.format.isin(sf)].copy()
st.subheader('Publicaciones');st.dataframe(f,use_container_width=True,hide_index=True)
st.subheader('Análisis por formato');st.dataframe(by_format(f),use_container_width=True,hide_index=True)
st.subheader('Top 10 por alcance');st.dataframe(top_posts(f,'reach'),use_container_width=True,hide_index=True)
if f.date.notna().any():
    d=pd.to_datetime(f.date,errors='coerce');st.subheader('Comparación con período anterior equivalente');st.dataframe(period_comparison(f,d.min().date(),d.max().date()),use_container_width=True,hide_index=True)
st.download_button('Descargar dataset procesado',f.to_csv(index=False).encode('utf-8-sig'),f'{brand.lower()}_procesado.csv','text/csv')
