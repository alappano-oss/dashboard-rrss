import streamlit as st
from config.config import BRANDS
from src.repository import load_processed
from src.ingestion import ingest_files, ingest_raw_directory

st.set_page_config(page_title='Social Media Analytics',page_icon='📊',layout='wide')
st.markdown('''<style>
html,body,[class*="css"] { font-family: "Museo Sans Rounded", "Arial Rounded MT Bold", Arial, sans-serif; }
h1,h2,h3 { font-weight:700; } p,div { font-weight:300; }
</style>''',unsafe_allow_html=True)

brand=st.sidebar.selectbox('Marca',['ELEBAR','PUNTO BLU'])
with st.sidebar.expander('Actualizar datos',expanded=False):
    st.write('Cargá uno o varios CSV exportados desde Meta.')
    uploads=st.file_uploader('Archivos CSV',type=['csv'],accept_multiple_files=True)
    force=st.checkbox('Forzar marca seleccionada',value=False,help='Usalo solo si el nombre/contenido del archivo no permite identificar la marca.')
    if st.button('Procesar archivos',disabled=not uploads,use_container_width=True):
        result=ingest_files(uploads,brand if force else None)
        st.session_state['ingestion_result']=result; st.rerun()
    st.caption('También podés colocar CSV en data/raw/elebar o data/raw/blu.')
    if st.button('Sincronizar carpeta raw',use_container_width=True):
        result=ingest_raw_directory(brand)
        st.session_state['ingestion_result']=result; st.rerun()

if 'ingestion_result' in st.session_state:
    r=st.session_state['ingestion_result']
    with st.sidebar.expander('Resultado de la última carga',expanded=True):
        st.write(f"Archivos procesados: {r['files_processed']}")
        st.write(f"Registros nuevos: {r['new_records']}")
        st.write(f"Duplicados: {r['duplicates']}")
        st.write(f"Rechazados: {r['rejected']}")
        for e in r['errors']: st.error(e)
        for w in r['warnings']: st.warning(w)

if brand=='ELEBAR':
    from dashboards.elebar import render
else:
    from dashboards.blu import render
render(load_processed(brand))
