from database import engine, Base, SessionLocal
from models import User, Seccion, Cuadrilla, Cooperativista
from utils.security import hash_password
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

def cargar_cooperativistas_excel():
    """Cargar cooperativistas desde Excel"""
    try:
        print("Leyendo archivo Excel...")
        df = pd.read_excel("lista_cooperativistas_agosto.xlsx")
        print(f"Se encontraron {len(df)} registros en el Excel")
        
        db = SessionLocal()
        try:
            existing_count = db.query(Cooperativista).count()
            if existing_count > 0:
                print(f"Ya existen {existing_count} cooperativistas. ¿Deseas continuar? (s/n)")
                respuesta = input().lower()
                if respuesta != 's':
                    return
            
            # PASO 1: Crear secciones únicas
            print("\n--- PASO 1: Creando secciones ---")
            secciones_unicas = df['SECCION'].dropna().unique()
            secciones_map = {}
            
            for nombre_seccion in secciones_unicas:
                nombre_seccion = str(nombre_seccion).strip()
                
                seccion_existente = db.query(Seccion).filter(Seccion.nombre == nombre_seccion).first()
                if seccion_existente:
                    secciones_map[nombre_seccion] = seccion_existente.id
                    print(f"   Sección '{nombre_seccion}' ya existe (ID: {seccion_existente.id})")
                else:
                    nueva_seccion = Seccion(
                        nombre=nombre_seccion,
                        is_active=True
                    )
                    db.add(nueva_seccion)
                    db.flush()
                    secciones_map[nombre_seccion] = nueva_seccion.id
                    print(f"   ✓ Sección '{nombre_seccion}' creada (ID: {nueva_seccion.id})")
            
            db.commit()
            print(f"Secciones creadas: {len(secciones_map)}")
            
            # PASO 2: Crear cuadrillas únicas (cuadrilla + sección)
            print("\n--- PASO 2: Creando cuadrillas ---")
            cuadrillas_map = {}
            
            df_cuadrillas = df[['CUADRILLA', 'SECCION']].dropna()
            cuadrillas_unicas = df_cuadrillas.drop_duplicates()
            
            for _, row in cuadrillas_unicas.iterrows():
                nombre_cuadrilla = str(row['CUADRILLA']).strip()
                nombre_seccion = str(row['SECCION']).strip()
                
                if nombre_seccion not in secciones_map:
                    print(f"   ⚠ Sección '{nombre_seccion}' no encontrada para cuadrilla '{nombre_cuadrilla}'")
                    continue
                
                id_seccion = secciones_map[nombre_seccion]
                key = (nombre_cuadrilla, nombre_seccion)
                
                cuadrilla_existente = db.query(Cuadrilla).filter(
                    Cuadrilla.nombre == nombre_cuadrilla,
                    Cuadrilla.id_seccion == id_seccion
                ).first()
                
                if cuadrilla_existente:
                    cuadrillas_map[key] = cuadrilla_existente.id
                    print(f"   Cuadrilla '{nombre_cuadrilla}' ({nombre_seccion}) ya existe (ID: {cuadrilla_existente.id})")
                else:
                    nueva_cuadrilla = Cuadrilla(
                        nombre=nombre_cuadrilla,
                        id_seccion=id_seccion,
                        is_active=True
                    )
                    db.add(nueva_cuadrilla)
                    db.flush()
                    cuadrillas_map[key] = nueva_cuadrilla.id
                    print(f"   ✓ Cuadrilla '{nombre_cuadrilla}' ({nombre_seccion}) creada (ID: {nueva_cuadrilla.id})")
            
            db.commit()
            print(f"Cuadrillas creadas: {len(cuadrillas_map)}")
            
            # PASO 3: Crear cooperativistas
            print("\n--- PASO 3: Creando cooperativistas ---")
            cooperativistas_creados = 0
            cooperativistas_error = 0
            delegados_pendientes = []
            
            for index, row in df.iterrows():
                try:
                    ci, ci_expedido = limpiar_ci(row.get('CI'))
                    
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
                        print(f"Procesados {cooperativistas_creados} cooperativistas...")
                
                except Exception as e:
                    print(f"Error en fila {index + 2}: {e}")
                    cooperativistas_error += 1
                    continue
            
            db.commit()
            print(f"Cooperativistas creados: {cooperativistas_creados}")
            
            # PASO 4: Actualizar delegados en secciones
            print("\n--- PASO 4: Actualizando delegados de secciones ---")
            delegados_actualizados = 0
            
            for delegado_info in delegados_pendientes:
                try:
                    nombre_seccion = delegado_info['nombre_seccion']
                    cooperativista_id = delegado_info['cooperativista_id']
                    
                    if nombre_seccion not in secciones_map:
                        continue
                    
                    seccion_id = secciones_map[nombre_seccion]
                    seccion = db.query(Seccion).filter(Seccion.id == seccion_id).first()
                    
                    if seccion:
                        seccion.id_delegado = cooperativista_id
                        delegados_actualizados += 1
                        print(f"   ✓ Delegado asignado a sección '{nombre_seccion}' (Cooperativista ID: {cooperativista_id})")
                
                except Exception as e:
                    print(f"   Error al asignar delegado: {e}")
            
            db.commit()
            print(f"Delegados actualizados: {delegados_actualizados}")
            
            print(f"\n✅ Carga completada:")
            print(f"   - Secciones: {len(secciones_map)}")
            print(f"   - Cuadrillas: {len(cuadrillas_map)}")
            print(f"   - Cooperativistas creados: {cooperativistas_creados}")
            print(f"   - Delegados asignados: {delegados_actualizados}")
            print(f"   - Errores: {cooperativistas_error}")
            
        except Exception as e:
            print(f"❌ Error al procesar Excel: {e}")
            db.rollback()
        finally:
            db.close()
            
    except Exception as e:
        print(f"❌ Error al leer archivo Excel: {e}")
        print("Asegúrate de que el archivo 'lista_cooperativistas_agosto.xlsx' esté en el directorio actual")

def init_db():
    """Crear todas las tablas e insertar datos iniciales"""
    print("Creando tablas...")
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas exitosamente!")
    
    db = SessionLocal()
    try:
        existing_user = db.query(User).filter(User.username == "admin").first()
        if not existing_user:
            print("Creando usuario admin por defecto...")
            admin_user = User(
                username="admin",
                password_hash=hash_password("admin123"),
                email="admin@cooperativa.com",
                full_name="Administrador Sistema",
                is_superuser=True,
                is_active=True
            )
            db.add(admin_user)
            print("Usuario admin creado (username: admin, password: admin123)")
        
        db.commit()
        print("\n✅ Base de datos inicializada correctamente!")
        print("=" * 50)
        print("Credenciales de acceso:")
        print("Usuario: admin")
        print("Password: admin123")
        print("=" * 50)
        print("\n⚠️  IMPORTANTE: Cambiar el password en producción!\n")
        
        print("¿Deseas cargar los cooperativistas desde Excel? (s/n)")
        respuesta = input().lower()
        if respuesta == 's':
            cargar_cooperativistas_excel()
        
    except Exception as e:
        print(f"❌ Error al inicializar la base de datos: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()