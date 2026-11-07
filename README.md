# ecotech_poos

Sistema de gestión de empleados, departamentos, proyectos y registros de tiempo para **EcoTech Solutions**. Integra consumo de APIs externas para la gestión operativa y financiera.

## Características del sistema

- **Gestión Interna**: Empleados, departamentos, proyectos y registros de tiempo.
- **Autenticación y Seguridad**: Inicio de sesión con contraseñas encriptadas (PBKDF2) y control de acceso basado en permisos.
- **Servicios Externos (API)**: 
  - Consulta del valor del Dólar (Mindicador.cl).
  - Pronóstico del Clima con humedad (Open-Meteo).
  - Conversión de divisas (CLP a USD).
- **Manejo de Errores**: Sistema de "fallback" con datos locales en caso de fallo de red o APIs caídas.
- **Persistencia**: Soporta SQLite (por defecto) o MySQL, configurable mediante variables de entorno.

## Requisitos previos

- Python 3.10 o superior.
- Visual Studio Code (recomendado).
- MySQL 8+ (solo si usas `DB_ENGINE=mysql`).

## Instalación

1. ### Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd ecotech_poos
```

2. ### Crear y activar el entorno virtual

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. ### Instalar dependencias
```bash
pip install -r requirements.txt
```

4. ### Configurar variables de entorno
Duplica el archivo `.env.example` y renómbralo a `.env`. Ajusta los valores según tu motor de base de datos (SQLite por defecto).

## Ejecución

Asegúrate de tener el entorno virtual activado y corre:

```bash
python main.py
```

### Credenciales por defecto (Semilla):
- **Usuario**: `admin_eco`
- **Contraseña**: `eco2026`

## Arquitectura

El proyecto sigue una arquitectura en capas:

- **Dominio (`dominio/`)**: Entidades puras del negocio.
- **Persistencia (`persistencia/`)**: DAOs para la base de datos.
- **Presentación (`menus/`)**: Interfaz de consola.
- **Servicios (`servicios/`)**: Consumo de APIs externas y lógica administrativa.

## Integración de Inteligencia Artificial

Durante el desarrollo de esta unidad, se utilizaron herramientas de IA para la generación de fragmentos de código relacionados con el consumo de APIs. Todas las sugerencias fueron analizadas críticamente. Los detalles sobre los ajustes de seguridad, la corrección de vulnerabilidades y la justificación técnica se encuentran documentados en el archivo `integracion_ia.md`.

## Autor

Juan Pablo Miranda

## Licencia

Proyecto académico - INACAP (TI3021).