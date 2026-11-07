# Integración y Uso Ético de Inteligencia Artificial en EcoTech Solutions

**Asignatura:** Programación Orientada a Objeto Seguro (TI3021)  
**Evaluación:** Sumativa 3 - Unidad 3  
**Autor:** Juan Pablo Miranda

## 1. Introducción
En el desarrollo de la extensión del sistema EcoTech Solutions (Unidad 3), se utilizaron herramientas de Inteligencia Artificial (IA) como asistentes de codificación. El objetivo fue acelerar la implementación de los servicios externos y proponer soluciones a los problemas de manejo de errores. Sin embargo, todo el código generado fue sometido a un riguroso análisis crítico, pruebas y refactorización manual para asegurar que cumpliera con los estándares de seguridad y los requerimientos de la evaluación.

## 2. Proceso de Análisis Crítico y Ajustes Técnicos

A continuación, se detallan los fragmentos de código propuestos inicialmente por la IA, las vulnerabilidades o falencias detectadas, y la justificación de los cambios adoptados.

### Caso 1: Consumo de la API del Clima (Open-Meteo)
*   **Código sugerido por la IA:** La IA generó una solicitud HTTP a Open-Meteo básica, obteniendo únicamente `temperature_2m_max`, `temperature_2m_min` y `weathercode`, manejando los errores con un `try/except` genérico que imprimía el error en consola (`print(e)`).
*   **Análisis y Vulnerabilidades detectadas:**
    1.  **Falta de requerimiento:** El sistema requería información sobre la humedad para la planificación operativa, y la IA no la incluyó en la petición.
    2.  **Exposición de información:** Imprimir el objeto de error directamente podía exponer la URL de la API o detalles del entorno en caso de fallo.
    3.  **Manejo de errores deficiente:** No se diferenciaba entre un error de timeout, un error de conexión o un error del servidor (HTTP 404 o 500).
*   **Ajuste adoptado:** 
    *   Se modificó la URL para incluir `relative_humidity_2m` en los parámetros diarios.
    *   Se implementó la validación del código de estado HTTP (si es distinto de 200, se lanza una excepción controlada).
    *   Se capturaron excepciones específicas (`requests.exceptions.Timeout` y `requests.exceptions.ConnectionError`) para lanzar mensajes amigables y evitar que el sistema se detenga abruptamente.
    *   Se implementó un sistema de "datos de respaldo" (fallback) para garantizar la continuidad del sistema si la API falla.

### Caso 2: Interfaz de Usuario y Manejo de Excepciones
*   **Código sugerido por la IA:** La IA generó la función para el menú de la API imprimiendo el error capturado directamente en pantalla: `except Exception as error: print("Error:", error)`.
*   **Análisis y Vulnerabilidades detectadas:** Esto viola el principio de no exponer información sensible al usuario final. Un usuario malintencionado podría usar los mensajes de error del sistema para mapear la infraestructura del backend.
*   **Ajuste adoptado:** Se modificaron los bloques `except` para que el usuario solo vea un mensaje genérico (ej: *"No se pudo conectar al servicio del clima. Usando respaldo local."*), mientras que el sistema recurre a los datos locales de manera transparente, cumpliendo con el criterio de continuidad y estabilidad.

### Caso 3: Autenticación y Seguridad
*   **Código sugerido por la IA:** Para la función `solicitar_registro` en `menu_usuario.py`, la IA intentó pasar la función `getpass` como parámetro de lectura dentro de la función `pedir_dato`.
*   **Análisis y Vulnerabilidades detectadas:** Esto generaba un conflicto de tipos y un error de ejecución (crash) al intentar solicitar la contraseña, ya que la firma de la función no coincidía con la forma en que `getpass` espera ser invocado.
*   **Ajuste adoptado:** Se refactorizó el código para llamar a `getpass` de forma nativa y directa, asignando el resultado a la variable `clave`, garantizando así que la contraseña nunca se muestre en pantalla (seguridad básica) y que el flujo no se interrumpa.

## 3. Conclusión sobre el Uso Ético de la IA

El uso de la IA en este proyecto se limitó a un rol de **copiloto**. Ningún fragmento de código fue aceptado sin antes comprender su funcionamiento. Se descartó el código que no cumplía con los estándares de seguridad (como la exposición de trazas de error) y se adaptó el código para que se integrara con la arquitectura de capas (Dominio, Persistencia, Presentación) ya establecida en las Unidades 1 y 2.

El código final es el resultado de un refinamiento técnico propio, donde la IA sirvió como punto de partida, pero la seguridad, la validación de entradas y el manejo robusto de errores fueron implementados y auditados de forma individual, de acuerdo con los criterios de la evaluación.