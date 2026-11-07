from persistencia.conexion import abrir_conexion, marcador_sql

class IndicadorDAO:
    @staticmethod
    def guardar(indicador):
        conexion = None
        try:
            conexion = abrir_conexion()
            cursor = conexion.cursor()
            marca = marcador_sql()
            
            if conexion.__class__.__name__ == "Connection" and "sqlite3" in str(type(conexion)):
                sql = f"""
                    INSERT INTO indicador_api (fuente, codigo, fecha, valor, unidad)
                    VALUES ({marca}, {marca}, {marca}, {marca}, {marca})
                    ON CONFLICT (fuente, codigo, fecha) DO UPDATE SET
                    valor = excluded.valor,
                    unidad = excluded.unidad
                """
            else:
                sql = f"""
                    INSERT INTO indicador_api (fuente, codigo, fecha, valor, unidad)
                    VALUES ({marca}, {marca}, {marca}, {marca}, {marca})
                    ON DUPLICATE KEY UPDATE
                    valor = VALUES(valor),
                    unidad = VALUES(unidad)
                """
            
            cursor.execute(sql, (indicador.fuente, indicador.codigo, indicador.fecha, indicador.valor, indicador.unidad))
            conexion.commit()
            return True
        except Exception as e:
            if conexion:
                conexion.rollback()
            print(f"Error al guardar en BD: {e}")
            return False
        finally:
            if conexion:
                conexion.close()

    @staticmethod
    def listar_historial():
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT fecha, valor, unidad, fuente FROM indicador_api ORDER BY fecha DESC LIMIT 10")
            filas = cursor.fetchall()
            return filas
        finally:
            conexion.close()