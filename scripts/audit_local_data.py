from pathlib import Path
import pandas as pd

WINDOWS_PATHS = {
    'ELEBAR': Path(r'C:\Users\alappano\Desktop\ELEBAR'),
    'PUNTO BLU': Path(r'C:\Users\alappano\Desktop\BLU'),
}

def inspect(folder: Path, brand: str):
    rows=[]
    for path in sorted(folder.rglob('*.csv')) if folder.exists() else []:
        try:
            df=pd.read_csv(path, nrows=5, encoding='utf-8-sig')
            rows.append({'brand':brand,'file':str(path),'size_bytes':path.stat().st_size,'columns':len(df.columns),'column_names':' | '.join(map(str,df.columns))})
        except Exception as exc:
            rows.append({'brand':brand,'file':str(path),'size_bytes':path.stat().st_size,'columns':'ERROR','column_names':str(exc)})
    return rows

if __name__ == '__main__':
    rows=[]
    for brand, folder in WINDOWS_PATHS.items(): rows.extend(inspect(folder,brand))
    out=pd.DataFrame(rows)
    out.to_csv('DATA_AUDIT_INVENTORY.csv',index=False,encoding='utf-8-sig')
    print(out.to_string(index=False) if not out.empty else 'No se encontraron CSV. Revisá las rutas configuradas.')
