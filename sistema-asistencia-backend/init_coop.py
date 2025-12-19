from database import SessionLocal
from models import Seccion, Cuadrilla, Cooperativista
from utils.qr_utils import generate_qr_code
import pandas as pd
from datetime import datetime
import re

def limpiar_ci(ci_str):
    """Limpiar y extraer CI"""
    if pd.isna(ci_str) or ci_str == "":
        return None, None
    
    ci_str = str(ci_str).strip()
    match = re.match(r'^(\d+)([A-Z]{2,5})?', ci_str.upper())
    if match:
        ci_numero = match.group(1)
        expedido = match.group(2) if match.group(2) else None
        return ci_numero, expedido
    return ci_str, None

def convertir_fecha(fecha_str):
    """Convertir fecha de Excel a date"""
    if pd.isna(fecha_str):
        return None
    
    if isinstance(fecha_str, datetime):
        return fecha_str.date()
    
    try:
        for formato in ['%d/%m/%Y', '%Y-%m-%d', '%d-%m-%Y']:
            try:
                return datetime.strptime(str(fecha_str), formato).date()
            except:
                continue
    except:
        pass
    
    return None

def insertar_cooperativistas_desde_fila(fila_inicio: int, archivo: str = "lista_cooperativistas_agosto.xlsx"):
    """
    Insertar cooperativistas desde una fila específica del Excel
    
    Args:
        fila_inicio: Número de fila desde donde empezar (1-indexed, considerando headers)
        archivo: Nombre del archivo Excel
    """
    try:
        print(f"Leyendo archivo Excel desde fila {fila_inicio}...")
        df = pd.read_excel(archivo)
        
        # Convertir fila_inicio a índice (0-indexed)
        # Si el usuario dice fila 770, en pandas sería índice 769 (770-1)
        indice_inicio = fila_inicio - 1
        
        if indice_inicio >= len(df):
            print(f"❌ Error: La fila {fila_inicio} está fuera del rango. El Excel tiene {len(df)} filas de datos.")
            return
        
        df = df.iloc[indice_inicio:]
        print(f"Se procesarán {len(df)} registros desde la fila {fila_inicio}")
        
        db = SessionLocal()
        try:
            # Cargar mapeos existentes de secciones y cuadrillas
            print("\n--- Cargando secciones y cuadrillas existentes ---")
            secciones_map = {}
            secciones = db.query(Seccion).all()
            for seccion in secciones:
                secciones_map[seccion.nombre] = seccion.id
            print(f"Secciones encontradas: {len(secciones_map)}")
            
            cuadrillas_map = {}
            cuadrillas = db.query(Cuadrilla).all()
            for cuadrilla in cuadrillas:
                # Obtener nombre de sección
                seccion = db.query(Seccion).filter(Seccion.id == cuadrilla.id_seccion).first()
                if seccion:
                    key = (cuadrilla.nombre, seccion.nombre)
                    cuadrillas_map[key] = cuadrilla.id
            print(f"Cuadrillas encontradas: {len(cuadrillas_map)}")
            
            # Crear secciones y cuadrillas nuevas si es necesario
            print("\n--- Verificando secciones y cuadrillas nuevas ---")
            secciones_nuevas = 0
            cuadrillas_nuevas = 0
            
            # Crear secciones nuevas
            secciones_unicas = df['SECCION'].dropna().unique()
            for nombre_seccion in secciones_unicas:
                nombre_seccion = str(nombre_seccion).strip()
                if nombre_seccion not in secciones_map:
                    nueva_seccion = Seccion(
                        nombre=nombre_seccion,
                        is_active=True
                    )
                    db.add(nueva_seccion)
                    db.flush()
                    secciones_map[nombre_seccion] = nueva_seccion.id
                    secciones_nuevas += 1
                    print(f"   ✓ Nueva sección '{nombre_seccion}' creada")
            
            # Crear cuadrillas nuevas
            df_cuadrillas = df[['CUADRILLA', 'SECCION']].dropna()
            cuadrillas_unicas = df_cuadrillas.drop_duplicates()
            
            for _, row in cuadrillas_unicas.iterrows():
                nombre_cuadrilla = str(row['CUADRILLA']).strip()
                nombre_seccion = str(row['SECCION']).strip()
                key = (nombre_cuadrilla, nombre_seccion)
                
                if key not in cuadrillas_map and nombre_seccion in secciones_map:
                    nueva_cuadrilla = Cuadrilla(
                        nombre=nombre_cuadrilla,
                        id_seccion=secciones_map[nombre_seccion],
                        is_active=True
                    )
                    db.add(nueva_cuadrilla)
                    db.flush()
                    cuadrillas_map[key] = nueva_cuadrilla.id
                    cuadrillas_nuevas += 1
                    print(f"   ✓ Nueva cuadrilla '{nombre_cuadrilla}' ({nombre_seccion}) creada")
            
            db.commit()
            print(f"Secciones nuevas: {secciones_nuevas}")
            print(f"Cuadrillas nuevas: {cuadrillas_nuevas}")
            
            # Insertar cooperativistas
            print(f"\n--- Insertando cooperativistas desde fila {fila_inicio} ---")
            cooperativistas_creados = 0
            cooperativistas_error = 0
            cooperativistas_duplicados = 0
            delegados_pendientes = []
            
            for index, row in df.iterrows():
                try:
                    ci, ci_expedido = limpiar_ci(row.get('CI'))
                    
                    # Verificar si el cooperativista ya existe (por CI)
                    if ci:
                        existente = db.query(Cooperativista).filter(Cooperativista.ci == ci).first()
                        if existente:
                            cooperativistas_duplicados += 1
                            print(f"   ⚠ Fila {index + 2}: CI {ci} ya existe (ID: {existente.id})")
                            continue
                    
                    nombre_seccion = str(row.get('SECCION')).strip() if pd.notna(row.get('SECCION')) else None
                    nombre_cuadrilla = str(row.get('CUADRILLA')).strip() if pd.notna(row.get('CUADRILLA')) else None
                    
                    id_seccion = secciones_map.get(nombre_seccion) if nombre_seccion else None
                    id_cuadrilla = None
                    if nombre_cuadrilla and nombre_seccion:
                        id_cuadrilla = cuadrillas_map.get((nombre_cuadrilla, nombre_seccion))
                    
                    rol_cuadrilla = str(row.get('JEFE DE CUADRILLA', '')).strip() if pd.notna(row.get('JEFE DE CUADRILLA')) else None
                    
                    qr_code = generate_qr_code()
                    while db.query(Cooperativista).filter(Cooperativista.qr_code == qr_code).first():
                        qr_code = generate_qr_code()
                    
                    cooperativista = Cooperativista(
                        qr_code=qr_code,
                        id_seccion=id_seccion,
                        id_cuadrilla=id_cuadrilla,
                        rol_cuadrilla=rol_cuadrilla,
                        apellido_paterno=str(row.get('AP.', '')).strip(),
                        apellido_materno=str(row.get('AM.', '')).strip() if pd.notna(row.get('AM.')) else None,
                        nombres=str(row.get('NOMBRES', '')).strip(),
                        ci=ci,
                        ci_expedido=ci_expedido,
                        fecha_ingreso=convertir_fecha(row.get('FECHA INGRESO')),
                        fecha_nacimiento=convertir_fecha(row.get('FECHA NAC.')),
                        codigo_asegurado=str(row.get('CODIGO', '')).strip() if pd.notna(row.get('CODIGO')) else None,
                        ocupacion=str(row.get('OCUPACION', '')).strip() if pd.notna(row.get('OCUPACION')) else None,
                        estado_asegurado=str(row.get('ASEGURADO', '')).strip() if pd.notna(row.get('ASEGURADO')) else None,
                        is_active=True
                    )
                    
                    db.add(cooperativista)
                    db.flush()
                    
                    if pd.notna(row.get('DELEGADO')) and str(row.get('DELEGADO')).strip():
                        delegados_pendientes.append({
                            'cooperativista_id': cooperativista.id,
                            'nombre_seccion': nombre_seccion
                        })
                    
                    cooperativistas_creados += 1
                    
                    if cooperativistas_creados % 50 == 0:
                        db.commit()
                        print(f"   Procesados {cooperativistas_creados} cooperativistas...")
                
                except Exception as e:
                    print(f"   ❌ Error en fila {index + 2}: {e}")
                    cooperativistas_error += 1
                    continue
            
            db.commit()
            
            # Actualizar delegados
            print("\n--- Actualizando delegados de secciones ---")
            delegados_actualizados = 0
            
            for delegado_info in delegados_pendientes:
                try:
                    nombre_seccion = delegado_info['nombre_seccion']
                    cooperativista_id = delegado_info['cooperativista_id']
                    
                    if nombre_seccion not in secciones_map:
                        continue
                    
                    seccion_id = secciones_map[nombre_seccion]
                    seccion = db.query(Seccion).filter(Seccion.id == seccion_id).first()
                    
                    if seccion and not seccion.id_delegado:
                        seccion.id_delegado = cooperativista_id
                        delegados_actualizados += 1
                        print(f"   ✓ Delegado asignado a sección '{nombre_seccion}'")
                
                except Exception as e:
                    print(f"   Error al asignar delegado: {e}")
            
            db.commit()
            
            print(f"\n✅ Inserción completada:")
            print(f"   - Fila inicial: {fila_inicio}")
            print(f"   - Registros procesados: {len(df)}")
            print(f"   - Secciones nuevas: {secciones_nuevas}")
            print(f"   - Cuadrillas nuevas: {cuadrillas_nuevas}")
            print(f"   - Cooperativistas creados: {cooperativistas_creados}")
            print(f"   - Duplicados omitidos: {cooperativistas_duplicados}")
            print(f"   - Delegados asignados: {delegados_actualizados}")
            print(f"   - Errores: {cooperativistas_error}")
            
        except Exception as e:
            print(f"❌ Error al procesar: {e}")
            db.rollback()
        finally:
            db.close()
            
    except Exception as e:
        print(f"❌ Error al leer archivo Excel: {e}")

if __name__ == "__main__":
    print("=== INSERCIÓN INCREMENTAL DE COOPERATIVISTAS ===\n")
    print("Ingrese el número de fila desde donde empezar (ej: 770):")
    
    try:
        fila_inicio = int(input().strip())
        
        print("\nIngrese el nombre del archivo Excel (default: lista_cooperativistas_agosto.xlsx):")
        archivo = input().strip()
        if not archivo:
            archivo = "lista_cooperativistas_agosto.xlsx"
        
        print(f"\n¿Deseas insertar cooperativistas desde la fila {fila_inicio}? (s/n)")
        respuesta = input().lower()
        
        if respuesta == 's':
            insertar_cooperativistas_desde_fila(fila_inicio, archivo)
        else:
            print("Operación cancelada")
    
    except ValueError:
        print("❌ Error: Debes ingresar un número válido")
    except KeyboardInterrupt:
        print("\n\nOperación cancelada por el usuario")