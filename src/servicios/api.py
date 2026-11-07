import math
import requests
from dominio.indicador import Indicador

TIMEOUT_API = 4

DATOS_RESPALDO = {
    "codigo": "dolar", "nombre": "Dólar observado", "unidad_medida": "Pesos",
    "serie": [{"fecha": "2026-11-06T00:00:00.000Z", "valor": 950.50}]
}

DATOS_RESPALDO_CLIMA = [
    {"dia": "Hoy", "temp_max": 26.5, "temp_min": 12.0, "humedad": 60, "estado": "Soleado"},
    {"dia": "Mañana", "temp_max": 28.0, "temp_min": 13.5, "humedad": 55, "estado": "Despejado"},
    {"dia": "Pasado mañana", "temp_max": 24.0, "temp_min": 11.0, "humedad": 70, "estado": "Parcialmente nublado"}
]


def obtener_datos():
    url = "https://mindicador.cl/api/dolar"
    try:
        respuesta = requests.get(url, timeout=TIMEOUT_API)
        if respuesta.status_code == 200:
            return respuesta.json(), "mindicador.cl (consulta real)"
        elif respuesta.status_code == 404:
            raise ValueError("API del dólar no encontrada (404).")
        else:
            raise ValueError(f"Error en servidor de indicadores (HTTP {respuesta.status_code}).")
    except requests.exceptions.Timeout:
        raise ConnectionError("Tiempo de espera agotado al conectar con la API del dólar.")
    except requests.exceptions.ConnectionError:
        raise ConnectionError("Error de conexión a la API del dólar.")


def mostrar_indicador(datos: dict, origen: str):
    print("===========================================")
    print(f" INDICADOR: {datos.get('nombre', 'N/A').upper()}")
    print("===========================================")
    print(f"Origen de datos : {origen}")
    serie = datos.get("serie", [])
    if serie:
        fecha = serie[0].get('fecha') or 'N/A'
        print(f"Última fecha   : {fecha[:10]}")
        print(f"Valor           : $ {serie[0].get('valor', 0):,.2f} CLP")
    print("===========================================")


def convertir_clp_a_usd(monto_clp: float) -> tuple[float, float, str]:
    try:
        datos, origen = obtener_datos()
        valor_dolar = datos["serie"][0]["valor"]
    except Exception:
        origen = "datos de respaldo (local)"
        valor_dolar = 950.50
    if not math.isfinite(valor_dolar) or valor_dolar <= 0:
        valor_dolar = 950.50
    return monto_clp / valor_dolar, valor_dolar, origen


def obtener_pronostico_clima_3_dias() -> tuple[list[dict], str]:
    url = ("https://api.open-meteo.com/v1/forecast?latitude=-33.4569&longitude=-70.6483"
           "&daily=temperature_2m_max,temperature_2m_min,relative_humidity_2m,weathercode&timezone=auto")
    try:
        respuesta = requests.get(url, timeout=TIMEOUT_API)
        if respuesta.status_code != 200:
            raise ValueError(f"Error en API del clima (HTTP {respuesta.status_code}).")
        
        datos = respuesta.json()
        daily = datos.get("daily", {})
        fechas = daily.get("time", [])[:3]
        maxs = daily.get("temperature_2m_max", [])[:3]
        mins = daily.get("temperature_2m_min", [])[:3]
        humedades = daily.get("relative_humidity_2m", [])[:3]
        
        pronostico = []
        etiquetas = ["Hoy", "Mañana", "Pasado mañana"]
        for i in range(len(fechas)):
            pronostico.append({
                "dia": etiquetas[i] if i < len(etiquetas) else fechas[i],
                "fecha": fechas[i],
                "temp_max": maxs[i] if i < len(maxs) else "N/A",
                "temp_min": mins[i] if i < len(mins) else "N/A",
                "humedad": humedades[i] if i < len(humedades) else "N/A"
            })
        return pronostico, "Open-Meteo API (en vivo)"
    except requests.exceptions.Timeout:
        raise ConnectionError("Tiempo de espera agotado al conectar con la API del clima.")
    except requests.exceptions.ConnectionError:
        raise ConnectionError("Error de conexión a la API del clima.")


def deserializar_indicador(datos_json):
    try:
        serie = datos_json.get("serie", [])
        if not serie:
            raise ValueError("No hay datos en la serie.")
        primer_dato = serie[0]
        return Indicador(fecha=primer_dato["fecha"][:10], valor=primer_dato["valor"])
    except Exception as e:
        raise ValueError(f"Datos de API inválidos: {e}")