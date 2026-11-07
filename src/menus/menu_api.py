from complementos.complementos import limpiar_pantalla, validar_entero_positivo
from entradas import pedir_dato
from servicios.api import (
    obtener_datos, mostrar_indicador, convertir_clp_a_usd,
    obtener_pronostico_clima_3_dias, deserializar_indicador,
    DATOS_RESPALDO, DATOS_RESPALDO_CLIMA
)
from persistencia.indicador_dao import IndicadorDAO


def menu_api():
    while True:
        limpiar_pantalla()
        print("==================================================")
        print("         MÓDULO API - SERVICIOS Y CLIMA           ")
        print("==================================================")
        print("1. Consultar Dólar (y guardar en BD)")
        print("2. Ver Historial del Dólar (BD Local)")
        print("3. Calculadora de Pago (CLP -> USD)")
        print("4. Pronóstico del Clima (3 días)")
        print("0. Volver")
        print("==================================================")
        opcion = input("\nOpción: ").strip()
        limpiar_pantalla()

        if opcion == "0":
            return
            
        elif opcion == "1":
            try:
                datos, origen = obtener_datos()
                indicador = deserializar_indicador(datos)
                mostrar_indicador(datos, origen)
                
                if IndicadorDAO.guardar(indicador):
                    print("\n[OK] El dato se ha guardado en el historial local.")
                else:
                    print("\n[AVISO] No se pudo guardar en la base de datos.")
            except Exception:
                print("\n[AVISO] No se pudo conectar al servicio. Usando respaldo local.")
                mostrar_indicador(DATOS_RESPALDO, "respaldo local")
            input("\nPresione Enter...")
            
        elif opcion == "2":
            historial = IndicadorDAO.listar_historial()
            if not historial:
                print("\n[AVISO] No hay historial guardado en la base de datos.")
            else:
                print("\n--- HISTORIAL DEL DÓLAR (BD Local) ---")
                print(f"{'Fecha':<12} | {'Valor':<15} | {'Fuente'}")
                print("-" * 50)
                for f in historial:
                    print(f"{f[0]:<12} | ${f[1]:,.2f} {f[2]:<5} | {f[3]}")
            input("\nPresione Enter...")
            
        elif opcion == "3":
            try:
                monto = pedir_dato("Monto CLP: $",
                                   lambda v: validar_entero_positivo(v, "Monto"))
                usd, tasa, origen = convertir_clp_a_usd(float(monto))
                print(f"\nMonto: ${monto:,.0f} CLP")
                print(f"Tasa: ${tasa:.2f} CLP/USD")
                print(f"Origen: {origen}")
                print(f"Total: ${usd:,.2f} USD")
            except Exception:
                print("Error: No se pudo realizar la conversión con datos en vivo.")
            input("\nPresione Enter...")
            
        elif opcion == "4":
            try:
                clima, fuente = obtener_pronostico_clima_3_dias()
                print(f"Fuente: {fuente}\n")
                print(f"{'Jornada':<15} | {'Mínima':<8} | {'Máxima':<8} | {'Humedad':<10}")
                print("-" * 50)
                for c in clima:
                    mn = f"{c['temp_min']} °C" if c['temp_min'] != "N/A" else "N/A"
                    mx = f"{c['temp_max']} °C" if c['temp_max'] != "N/A" else "N/A"
                    hum = f"{c['humedad']}%" if c.get('humedad') != "N/A" else "N/A"
                    print(f"{c['dia']:<15} | {mn:<8} | {mx:<8} | {hum:<10}")
            except Exception:
                print("\n[AVISO] No se pudo conectar al servicio del clima. Usando respaldo local.\n")
                print(f"Fuente: respaldo local\n")
                print(f"{'Jornada':<15} | {'Mínima':<8} | {'Máxima':<8} | {'Humedad':<10}")
                print("-" * 50)
                for c in DATOS_RESPALDO_CLIMA:
                    print(f"{c['dia']:<15} | {c['temp_min']} °C   | {c['temp_max']} °C   | {c['humedad']}%")
            input("\nPresione Enter...")
            
        else:
            print("Opción inválida.")
            input("\nPresione Enter...")