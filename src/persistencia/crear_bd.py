from persistencia.conexion import abrir_conexion, obtener_motor


def crear_tablas():
    conexion = None
    try:
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        if obtener_motor() == "sqlite":
            tablas = [
                """CREATE TABLE IF NOT EXISTS empleado (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    direccion TEXT NOT NULL,
                    numero TEXT NOT NULL,
                    correo TEXT NOT NULL,
                    fecha_contrato TEXT NOT NULL,
                    salario REAL NOT NULL,
                    cargo TEXT NOT NULL
                )""",
                """CREATE TABLE IF NOT EXISTS departamento (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    descripcion TEXT DEFAULT '',
                    id_gerente INTEGER
                )""",
                """CREATE TABLE IF NOT EXISTS proyecto (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    descripcion TEXT NOT NULL,
                    fecha_inicio TEXT NOT NULL,
                    fecha_fin TEXT,
                    estado TEXT NOT NULL DEFAULT 'pendiente'
                )""",
                """CREATE TABLE IF NOT EXISTS registro_tiempo (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    horas_trabajadas INTEGER NOT NULL CHECK (horas_trabajadas > 0),
                    fecha_trabajada TEXT NOT NULL,
                    descripcion_tarea TEXT NOT NULL,
                    empleado_id INTEGER NOT NULL,
                    proyecto_id INTEGER NOT NULL,
                    FOREIGN KEY (empleado_id) REFERENCES empleado(id),
                    FOREIGN KEY (proyecto_id) REFERENCES proyecto(id)
                )""",
                """CREATE TABLE IF NOT EXISTS departamento_empleado (
                    departamento_id INTEGER NOT NULL,
                    empleado_id INTEGER NOT NULL,
                    PRIMARY KEY (departamento_id, empleado_id),
                    FOREIGN KEY (departamento_id) REFERENCES departamento(id),
                    FOREIGN KEY (empleado_id) REFERENCES empleado(id)
                )""",
                """CREATE TABLE IF NOT EXISTS departamento_proyecto (
                    departamento_id INTEGER NOT NULL,
                    proyecto_id INTEGER NOT NULL,
                    PRIMARY KEY (departamento_id, proyecto_id),
                    FOREIGN KEY (departamento_id) REFERENCES departamento(id),
                    FOREIGN KEY (proyecto_id) REFERENCES proyecto(id)
                )""",
                """CREATE TABLE IF NOT EXISTS proyecto_empleado (
                    proyecto_id INTEGER NOT NULL,
                    empleado_id INTEGER NOT NULL,
                    PRIMARY KEY (proyecto_id, empleado_id),
                    FOREIGN KEY (proyecto_id) REFERENCES proyecto(id),
                    FOREIGN KEY (empleado_id) REFERENCES empleado(id)
                )""",
                """CREATE TABLE IF NOT EXISTS usuario (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre_usuario TEXT NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL,
                    id_empleado INTEGER NOT NULL UNIQUE,
                    permisos TEXT DEFAULT '[]',
                    FOREIGN KEY (id_empleado) REFERENCES empleado(id)
                )""",
                """CREATE TABLE IF NOT EXISTS indicador_api (
                    fuente TEXT NOT NULL,
                    codigo TEXT NOT NULL,
                    fecha TEXT NOT NULL,
                    valor REAL NOT NULL,
                    unidad TEXT NOT NULL,
                    PRIMARY KEY (fuente, codigo, fecha)
                )"""
            ]
        else:
            tablas = [
                """CREATE TABLE IF NOT EXISTS empleado (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    nombre VARCHAR(100) NOT NULL,
                    direccion VARCHAR(200) NOT NULL,
                    numero VARCHAR(30) NOT NULL,
                    correo VARCHAR(150) NOT NULL,
                    fecha_contrato DATE NOT NULL,
                    salario DECIMAL(12, 2) NOT NULL,
                    cargo VARCHAR(100) NOT NULL
                )""",
                """CREATE TABLE IF NOT EXISTS departamento (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    nombre VARCHAR(100) NOT NULL,
                    descripcion VARCHAR(255) DEFAULT '',
                    id_gerente INT
                )""",
                """CREATE TABLE IF NOT EXISTS proyecto (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    nombre VARCHAR(100) NOT NULL,
                    descripcion TEXT NOT NULL,
                    fecha_inicio DATE NOT NULL,
                    fecha_fin DATE NULL,
                    estado VARCHAR(20) NOT NULL DEFAULT 'pendiente'
                )""",
                """CREATE TABLE IF NOT EXISTS registro_tiempo (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    horas_trabajadas INT NOT NULL,
                    fecha_trabajada DATE NOT NULL,
                    descripcion_tarea TEXT NOT NULL,
                    empleado_id INT NOT NULL,
                    proyecto_id INT NOT NULL,
                    FOREIGN KEY (empleado_id) REFERENCES empleado(id),
                    FOREIGN KEY (proyecto_id) REFERENCES proyecto(id)
                )""",
                """CREATE TABLE IF NOT EXISTS departamento_empleado (
                    departamento_id INT NOT NULL,
                    empleado_id INT NOT NULL,
                    PRIMARY KEY (departamento_id, empleado_id),
                    FOREIGN KEY (departamento_id) REFERENCES departamento(id),
                    FOREIGN KEY (empleado_id) REFERENCES empleado(id)
                )""",
                """CREATE TABLE IF NOT EXISTS departamento_proyecto (
                    departamento_id INT NOT NULL,
                    proyecto_id INT NOT NULL,
                    PRIMARY KEY (departamento_id, proyecto_id),
                    FOREIGN KEY (departamento_id) REFERENCES departamento(id),
                    FOREIGN KEY (proyecto_id) REFERENCES proyecto(id)
                )""",
                """CREATE TABLE IF NOT EXISTS proyecto_empleado (
                    proyecto_id INT NOT NULL,
                    empleado_id INT NOT NULL,
                    PRIMARY KEY (proyecto_id, empleado_id),
                    FOREIGN KEY (proyecto_id) REFERENCES proyecto(id),
                    FOREIGN KEY (empleado_id) REFERENCES empleado(id)
                )""",
                """CREATE TABLE IF NOT EXISTS usuario (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    nombre_usuario VARCHAR(50) NOT NULL UNIQUE,
                    password_hash VARCHAR(255) NOT NULL,
                    id_empleado INT NOT NULL UNIQUE,
                    permisos TEXT,
                    FOREIGN KEY (id_empleado) REFERENCES empleado(id)
                )""",
                """CREATE TABLE IF NOT EXISTS indicador_api (
                    fuente VARCHAR(100) NOT NULL,
                    codigo VARCHAR(50) NOT NULL,
                    fecha DATE NOT NULL,
                    valor DECIMAL(12, 2) NOT NULL,
                    unidad VARCHAR(20) NOT NULL,
                    PRIMARY KEY (fuente, codigo, fecha)
                )"""
            ]
        for sql in tablas:
            cursor.execute(sql)
        conexion.commit()
    except Exception:
        if conexion:
            conexion.rollback()
        raise
    finally:
        if conexion:
            conexion.close()


if __name__ == "__main__":
    crear_tablas()
    print("Tablas de EcoTech preparadas correctamente.")    