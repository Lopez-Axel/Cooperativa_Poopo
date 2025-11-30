from database import engine, Base, SessionLocal
from models import User, Config, Cooperativista
from passlib.context import CryptContext
import pandas as pd
from datetime import datetime
import re

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def limpiar_ci(ci_str):
    """Limpiar y extraer CI"""
    if pd.isna(ci_str) or ci_str == "":
        return None, None
    
    ci_str = str(ci_str).strip()
    # Buscar patrón: números seguidos de letras (expedido)
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
        # Intentar varios formatos
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
            # Verificar si ya existen cooperativistas
            existing_count = db.query(Cooperativista).count()
            if existing_count > 0:
                print(f"Ya existen {existing_count} cooperativistas. ¿Deseas continuar? (s/n)")
                respuesta = input().lower()
                if respuesta != 's':
                    return
            
            cooperativistas_creados = 0
            cooperativistas_error = 0
            
            for index, row in df.iterrows():
                try:
                    # Extraer datos del Excel
                    nro = int(row.get('NRO.', 0)) if pd.notna(row.get('NRO.')) else None
                    if not nro:
                        print(f"Fila {index + 2}: NRO. faltante, omitiendo")
                        cooperativistas_error += 1
                        continue
                
                    # Procesar CI
                    ci, ci_expedido = limpiar_ci(row.get('CI'))
                    
                    # Crear cooperativista
                    cooperativista = Cooperativista(
                        nro=nro,
                        seccion=str(row.get('SECCION')) if pd.notna(row.get('SECCION')) else None,
                        cuadrilla=str(row.get('CUADRILLA', '')).strip() if pd.notna(row.get('CUADRILLA')) else None,
                        jefe_cuadrilla=str(row.get('JEFE DE CUADRILLA', '')).strip() if pd.notna(row.get('JEFE DE CUADRILLA')) else None,
                        delegado_seccion=str(row.get('DELEGADO', '')).strip() if pd.notna(row.get('DELEGADO')) else None,
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
                    cooperativistas_creados += 1
                    
                    if cooperativistas_creados % 50 == 0:
                        db.commit()
                        print(f"Procesados {cooperativistas_creados} cooperativistas...")
                
                except Exception as e:
                    print(f"Error en fila {index + 2}: {e}")
                    cooperativistas_error += 1
                    continue
            
            db.commit()
            print(f"\n✅ Cooperativistas cargados exitosamente:")
            print(f"   - Creados: {cooperativistas_creados}")
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
        # Verificar si ya existe el usuario admin
        existing_user = db.query(User).filter(User.username == "admin").first()
        if not existing_user:
            print("Creando usuario admin por defecto...")
            # Crear usuario admin con password hasheado
            admin_user = User(
                username="admin",
                password_hash=pwd_context.hash("admin123"),
                email="admin@cooperativa.com",
                full_name="Administrador Sistema",
                is_superuser=True,
                is_active=True
            )
            db.add(admin_user)
            print("Usuario admin creado (username: admin, password: admin123)")
        
        # Verificar configuraciones
        existing_config = db.query(Config).first()
        if not existing_config:
            print("Creando configuraciones iniciales...")
            configs = [
                Config(key="timezone", value="America/La_Paz", 
                       description="Zona horaria del sistema", data_type="string"),
                Config(key="max_devices_per_cooperativista", value="1", 
                       description="Máximo de dispositivos por cooperativista", data_type="integer"),
                Config(key="require_gps", value="true", 
                       description="Requerir ubicación GPS en asistencia", data_type="boolean"),
                Config(key="gps_radius_meters", value="50", 
                       description="Radio GPS permitido en metros", data_type="integer"),
                Config(key="sistema_nombre", value="Sistema de Asistencia - Cooperativa", 
                       description="Nombre del sistema", data_type="string"),
                Config(key="sistema_version", value="1.0.0", 
                       description="Versión del sistema", data_type="string"),
            ]
            for config in configs:
                db.add(config)
            print("Configuraciones creadas")
        
        db.commit()
        print("\n✅ Base de datos inicializada correctamente!")
        print("=" * 50)
        print("Credenciales de acceso:")
        print("Usuario: admin")
        print("Password: admin123")
        print("=" * 50)
        print("\n⚠️  IMPORTANTE: Cambiar el password en producción!\n")
        
        # Preguntar si cargar cooperativistas
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