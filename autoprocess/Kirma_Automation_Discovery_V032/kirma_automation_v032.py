import ctypes
import time
from datetime import datetime
from collections import Counter
from pathlib import Path
import psutil

DURACION = 5 * 60
INTERVALO = 1
MIN_REPETICIONES = 3
LONGITUD_SECUENCIA = 4
ARCHIVO = "registro_pc.txt"

def obtener_aplicacion_activa():
    try:
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        if not hwnd:
            return "DESCONOCIDO"

        pid = ctypes.c_ulong()
        ok = ctypes.windll.user32.GetWindowThreadProcessId(
            hwnd, ctypes.byref(pid)
        )
        if ok == 0 or pid.value == 0:
            return "DESCONOCIDO"

        return psutil.Process(pid.value).name()

    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        return "DESCONOCIDO"
    except Exception:
        return "DESCONOCIDO"

def registrar(texto):
    with open(ARCHIVO, "a", encoding="utf-8") as f:
        f.write(texto + "\n")

def comprimir_historial(eventos):
    resultado = []
    for evento in eventos:
        if not resultado or resultado[-1]["app"] != evento["app"]:
            resultado.append(evento)
    return resultado

def detectar_secuencias(aplicaciones):
    return [
        tuple(aplicaciones[i:i + LONGITUD_SECUENCIA])
        for i in range(max(0, len(aplicaciones) - LONGITUD_SECUENCIA + 1))
    ]

def contar_no_solapadas(secuencias):
    posiciones = {}
    for pos, secuencia in enumerate(secuencias):
        posiciones.setdefault(secuencia, []).append(pos)

    resultado = {}
    for secuencia, lista in posiciones.items():
        contador = 0
        ultima = -LONGITUD_SECUENCIA
        for pos in lista:
            if pos >= ultima + LONGITUD_SECUENCIA:
                contador += 1
                ultima = pos
        resultado[secuencia] = contador
    return resultado

def analizar(eventos):
    cambios = comprimir_historial(eventos)

    registrar("")
    registrar("=" * 70)
    registrar("ANALISIS KIRMA AUTOMATION DISCOVERY V0.3.2")
    registrar("=" * 70)

    registrar("")
    registrar("RESUMEN")
    registrar("-" * 70)
    registrar(f"Muestras: {len(eventos)}")
    registrar(f"Cambios detectados: {max(0, len(cambios) - 1)}")
    registrar(f"Aplicaciones diferentes: {len(set(e['app'] for e in cambios))}")

    registrar("")
    registrar("DURACION APROXIMADA POR APLICACION")
    registrar("-" * 70)

    duraciones = Counter()
    for i, evento in enumerate(cambios):
        inicio = evento["timestamp"]
        fin = cambios[i + 1]["timestamp"] if i + 1 < len(cambios) else eventos[-1]["timestamp"]
        duraciones[evento["app"]] += max(0, (fin - inicio).total_seconds())

    for app, segundos in duraciones.most_common():
        registrar(f"{app}: {segundos:.1f} segundos ({segundos / 60:.1f} minutos)")

    registrar("")
    registrar("TRANSICIONES MAS FRECUENTES")
    registrar("-" * 70)

    transiciones = Counter(
        (cambios[i - 1]["app"], cambios[i]["app"])
        for i in range(1, len(cambios))
    )

    for (anterior, actual), cantidad in transiciones.most_common(10):
        registrar(f"{anterior} -> {actual}: {cantidad} veces")

    registrar("")
    registrar("SECUENCIAS REPETITIVAS")
    registrar("-" * 70)

    apps = [e["app"] for e in cambios]
    cantidades = contar_no_solapadas(detectar_secuencias(apps))
    encontradas = False

    for secuencia, cantidad in sorted(cantidades.items(), key=lambda x: x[1], reverse=True):
        if cantidad >= MIN_REPETICIONES:
            encontradas = True
            registrar("")
            registrar("PATRON DETECTADO")
            registrar(f"Secuencia: {' -> '.join(secuencia)}")
            registrar(f"Ocurrencias independientes: {cantidad}")
            registrar("Nivel de evidencia: OBSERVACION")
            registrar("Estado: REQUIERE VALIDACION HUMANA")
            registrar("Pregunta: ¿Que tarea realiza cuando repite esta secuencia?")

    if not encontradas:
        registrar("No se encontraron secuencias que superen el umbral.")

    registrar("")
    registrar("=" * 70)
    registrar("INTERPRETACION")
    registrar("=" * 70)
    registrar("El sistema detecta cambios de aplicacion en primer plano.")
    registrar("Las duraciones son aproximadas y dependen del intervalo de comprobacion.")
    registrar("Una secuencia repetitiva NO demuestra que exista una automatizacion viable.")
    registrar("Se requiere validar con la persona el proceso empresarial.")
    registrar("No se registran teclas, contraseñas, capturas, contenido ni URLs.")

def main():
    print("=" * 70)
    print("KIRMA AUTOMATION DISCOVERY - V0.3.2")
    print("=" * 70)

    autorizacion = input("\n¿Tiene autorizacion para analizar este equipo? (SI/NO): ").strip().upper()
    if autorizacion != "SI":
        print("\nAnalisis cancelado.")
        return

    print(f"\nDuracion: {DURACION // 60} minutos")
    print(f"Comprobacion: cada {INTERVALO} segundo(s)")
    print(f"Secuencia: {LONGITUD_SECUENCIA} aplicaciones")
    print(f"Umbral: {MIN_REPETICIONES} ocurrencias")
    print(f"Salida: {ARCHIVO}")
    print("\nSolo se registra la aplicacion en primer plano.")
    print("No se registran teclas, contraseñas, capturas, contenido ni URLs.")

    input("\nPresione ENTER para comenzar...")

    Path(ARCHIVO).write_text("", encoding="utf-8")
    registrar("=" * 70)
    registrar("KIRMA AUTOMATION DISCOVERY V0.3.2")
    registrar("=" * 70)
    registrar(f"Inicio: {datetime.now():%Y-%m-%d %H:%M:%S}")
    registrar(f"Duracion prevista: {DURACION} segundos")
    registrar(f"Intervalo: {INTERVALO} segundo(s)")
    registrar("Autorizacion confirmada por el operador.")
    registrar("")
    registrar("REGISTRO DE CAMBIOS")
    registrar("-" * 70)

    eventos = []
    inicio = time.monotonic()
    ultima_app = None

    try:
        while time.monotonic() - inicio < DURACION:
            ahora = datetime.now()
            app = obtener_aplicacion_activa()
            eventos.append({"timestamp": ahora, "app": app})

            if app != ultima_app:
                registrar(f"{ahora:%H:%M:%S} | {ultima_app or 'INICIO'} -> {app}")
                print(f"{ahora:%H:%M:%S} | {ultima_app or 'INICIO'} -> {app}")
                ultima_app = app

            time.sleep(INTERVALO)

    except KeyboardInterrupt:
        print("\nAnalisis detenido manualmente.")

    if eventos:
        analizar(eventos)

    registrar("")
    registrar(f"Fin: {datetime.now():%Y-%m-%d %H:%M:%S}")
    print(f"\nPrueba terminada. Resultado: {ARCHIVO}")

if __name__ == "__main__":
    main()
