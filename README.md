# ecotech_poos

El sistema permite:

- **Empleados**: alta, baja, modificación, búsqueda y listado.
- **Departamentos**: gestión y asignación de empleados.
- **Proyectos**: creación, asignación de empleados y seguimiento.
- **Registros de tiempo**: horas trabajadas por tarea y cálculo de costos.

Soporta persistencia en **SQLite** o **MySQL**, configurable mediante variables de entorno.

## Requisitos previos

- Python 3.12 o superior.
- Visual Studio Code (recomendado).
- MySQL 8+ (solo si usas `DB_ENGINE=mysql`).

### 1. Clonar el repositorio

bash
git clone <url-del-repositorio>
cd ecotech_poos


### 2. Crear y activar el entorno virtual:
En Windows:
bash
python -m venv .venv
.venv\Scripts\activate


En macOS / Linux:
bash
python3 -m venv .venv
source .venv/bin/activate

### 3. Instalar dependencias

bash
pip install -r requirements.txt


3. Configurar las variables de entorno:
Duplica el archivo de ejemplo o crea un archivo llamado `.env` en la raíz del proyecto.
Completa los valores requeridos (por ejemplo, claves API o credenciales).



## Ejecución

Para ejecutar el proyecto, asegúrate de tener el entorno virtual activado y corre:

bash
python main.py

## Arquitectura

El proyecto sigue una arquitectura en capas:

1. **Dominio** (`dominio/`): entidades puras del negocio, sin dependencias externas.
2. **Persistencia** (`persistencia/`): DAOs que traducen entre objetos y la base de datos.
3. **Presentación** (`menus/`): interfaz de consola que orquesta las operaciones.

## Autor

- Juan Pablo Miranda y Benjamin Espinosa

## Licencia

Proyecto académico 