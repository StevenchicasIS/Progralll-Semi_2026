from conexión import obtener_conexion

TABLA = "usuarios_USSS030624"

def gestionar_insertar(datos):
    db = obtener_conexion()
    if not db: return {"ok": False, "error": "No hay conexión a la BD"}
    try:
        cur = db.cursor()
        # Usamos comillas invertidas para columnas con tildes en MySQL
        sql = f"INSERT INTO {TABLA} (usuario, clave, nombre, `dirección`, `teléfono`) VALUES (%s, %s, %s, %s, %s)"
        cur.execute(sql, (datos['usuario'], datos['clave'], datos['nombre'], datos['direccion'], datos['telefono']))
        db.commit()
        return {"ok": True}
    except Exception as e:
        print(f"ERROR AL GUARDAR EN BD: {e}") 
        return {"ok": False, "error": str(e)}
    finally:
        cur.close()
        db.close()

def gestionar_buscar(filtro=""):
    db = obtener_conexion()
    cur = db.cursor(dictionary=True)
    if filtro:
        sql = f"SELECT * FROM {TABLA} WHERE nombre LIKE %s OR usuario LIKE %s"
        cur.execute(sql, (f'%{filtro}%', f'%{filtro}%'))
    else:
        cur.execute(f"SELECT * FROM {TABLA}")
    res = cur.fetchall()
    cur.close()
    db.close()
    return res

def gestionar_actualizar(id_u, datos):
    db = obtener_conexion()
    cur = db.cursor()
    sql = f"UPDATE {TABLA} SET usuario=%s, clave=%s, nombre=%s, `dirección`=%s, `teléfono`=%s WHERE idUsuario=%s"
    cur.execute(sql, (datos['usuario'], datos['clave'], datos['nombre'], datos['direccion'], datos['telefono'], id_u))
    db.commit()
    cur.close()
    db.close()
    return {"ok": True}

def gestionar_eliminar(id_u):
    db = obtener_conexion()
    cur = db.cursor()
    cur.execute(f"DELETE FROM {TABLA} WHERE idUsuario = %s", (id_u,))
    db.commit()
    cur.close()
    db.close()
    return {"ok": True}

def gestionar_login(u, p):
    db = obtener_conexion()
    cur = db.cursor(dictionary=True)
    cur.execute(f"SELECT * FROM {TABLA} WHERE usuario = %s AND clave = %s", (u, p))
    user = cur.fetchone()
    cur.close()
    db.close()
    return user