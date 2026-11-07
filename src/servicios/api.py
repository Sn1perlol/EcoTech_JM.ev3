import math
import requests

TIMEOUT_API = 4

DATOS_RESPALDO = {
    "codigo": "dolar", "nombre": "Dólar observado", "unidad_medida": "Pesos",
    "serie": [{"fecha": "2026-11-06T00:00:00.000Z", "valor": 950.50}]
}

DATOS_RESPALDO_CLIMA = [
    {"dia": "Hoy", "temp_max": 26.5, "temp_min": 12.0, "estado": "Soleado"},
    {"dia": "Mañana", "temp_max": 28.0, "temp_min": 13.5, "estado": "Despejado"},
    {"dia": "Pasado mañana", "temp_max": 24.0, "temp_min": 11.0, "estado": "Parcialmente nublado"}
]


def obtener_datos():
    url = "https://mindicador.cl/api/dolar"
    try:
        respuesta = requests.get(url, timeout=TIMEOUT_API)
        respuesta.raise_for_status()
        return respuesta.json(), "mindicador.cl (consulta real)"
    except Exception:
        return DATOS_RESPALDO, "datos de respaldo (local)"


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
           "&daily=temperature_2m_max,temperature_2m_min,weathercode&timezone=auto")
    try:
        respuesta = requests.get(url, timeout=TIMEOUT_API)
        respuesta.raise_for_status()
        datos = respuesta.json()
        daily = datos.get("daily", {})
        fechas = daily.get("time", [])[:3]
        maxs = daily.get("temperature_2m_max", [])[:3]
        mins = daily.get("temperature_2m_min", [])[:3]
        pronostico = []
        etiquetas = ["Hoy", "Mañana", "Pasado mañana"]
        for i in range(len(fechas)):
            pronostico.append({
                "dia": etiquetas[i] if i < len(etiquetas) else fechas[i],
                "fecha": fechas[i],
                "temp_max": maxs[i] if i < len(maxs) else "N/A",
                "temp_min": mins[i] if i < len(mins) else "N/A"
            })
        return pronostico, "Open-Meteo API (en vivo)"
    except Exception:
        return DATOS_RESPALDO_CLIMA, "datos de respaldo (local)"