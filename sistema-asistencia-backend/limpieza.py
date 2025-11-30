import pandas as pd

df = pd.read_excel("lista_cooperativistas_agosto.xlsx")

# Eliminar espacios al inicio y final a todas las columnas tipo texto
df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)

df.to_excel("archivo_limpio.xlsx", index=False)
