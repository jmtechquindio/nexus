import ctypes
import json
import os
import sys
import time
from datetime import datetime
from collections import Counter
from pathlib import Path

try:
    import psutil
except ImportError:
    psutil = None

BASE_DIR = Path(__file__).resolve().parent
CONFIG_FILE = BASE_DIR / "config.json"
LOG_FILE = BASE_DIR / "registro_pc.txt"
RESULT_FILE = BASE_DIR / "resultado.json"

DEFAULT_CONFIG = {
    "duracion_horas": 4,
    "intervalo_segundos": 1,
    "min_repeticiones": 3,
    "longitud_secuencia": 4
}


def cargar_config():
    try:
        if CONFIG_FILE.exists():
            data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
            cfg = DEFAULT_CONFIG.copy()
            cfg.update({k: data[k] for k in DEFAULT_CONFIG if k in data})
            return cfg
    except Exception:
        pass
    CONFIG_FILE.write_text(json.dumps(DEFAULT_CONFIG, indent=2, ensure_ascii=False), encoding="utf-8")
    return DEFAULT_CONFIG.copy()


def registrar(texto):
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(texto + "\n")


def obtener_aplicacion_activa():
    if sys.platform != "win32":
        return "PLATAFORMA_NO_WINDOWS"
    try:
        hwnd = ctypes.windll.user32.GetForegroundWindow()
        if not hwnd:
            return "DESCONOCIDO"
        pid = ctypes.c_ulong()
        ok = ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
        if ok == 0 or pid.value == 0:
            return "DESCONOCIDO"
        return psutil.Process(pid.value).name()
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        return "DESCONOCIDO"
    except Exception:
        return "DESCONOCIDO"


def comprimir_historial(eventos):
    resultado = []
    for evento in eventos:
        if not resultado or resultado[-1]["app"] != evento["app"]:
            resultado.append(evento)
    return resultado


def detectar_secuencias(aplicaciones, longitud):
    return [tuple(aplicaciones[i:i + longitud]) for i in range(max(0, len(aplicaciones) - longitud + 1))]


def contar_no_solapadas(secuencias, longitud):
    posiciones = {}
    for pos, secuencia in enumerate(secuencias):
        posiciones.setdefault(secuencia, []).append(pos)
    resultado = {}
    for secuencia, lista in posiciones.items():
        contador = 0
        ultima = -longitud
        for pos in lista:
            if pos >= ultima + longitud:
                contador += 1
                ultima = pos
        resultado[secuencia] = contador
    return resultado


def analizar(eventos, cfg):
    cambios = comprimir_historial(eventos)
    duraciones = Counter()
    for i, evento in enumerate(cambios):
        inicio = evento["timestamp"]
        fin = cambios[i + 1]["timestamp"] if i + 1 < len(cambios) else eventos[-1]["timestamp"]
        duraciones[evento["app"]] += max(0, (fin - inicio).total_seconds())

    transiciones = Counter((cambios[i - 1]["app"], cambios[i]["app"]) for i in range(1, len(cambios)))
    apps = [e["app"] for e in cambios]
    secuencias = contar_no_solapadas(detectar_secuencias(apps, cfg["longitud_secuencia"]), cfg["longitud_secuencia"])
    patrones = []
    for secuencia, cantidad in sorted(secuencias.items(), key=lambda x: x[1], reverse=True):
        if cantidad >= cfg["min_repeticiones"]:
            patrones.append({"secuencia": list(secuencia), "ocurrencias": cantidad, "evidencia": "OBSERVACION", "estado": "REQUIERE_VALIDACION_HUMANA"})

    resultado = {
        "version": "1.0.0",
        "inicio": eventos[0]["timestamp"].isoformat() if eventos else None,
        "fin": eventos[-1]["timestamp"].isoformat() if eventos else None,
        "muestras": len(eventos),
        "cambios_detectados": max(0, len(cambios) - 1),
        "aplicaciones_diferentes": len(set(apps)),
        "duracion_por_aplicacion_segundos": dict(duraciones),
        "transiciones": [{"de": a, "a": b, "cantidad": n} for (a, b), n in transiciones.most_common(10)],
        "patrones_repetitivos": patrones,
        "limitaciones": ["Solo se registra la aplicacion en primer plano.", "No se registran teclas, contraseñas, capturas, contenido de documentos ni URLs."]
    }
    RESULT_FILE.write_text(json.dumps(resultado, indent=2, ensure_ascii=False), encoding="utf-8")

    registrar("\n" + "=" * 70)
    registrar("ANALISIS KIRMA AUTOMATION V1.0.0")
    registrar("=" * 70)
    registrar(f"Muestras: {len(eventos)}")
    registrar(f"Cambios detectados: {max(0, len(cambios) - 1)}")
    registrar(f"Aplicaciones diferentes: {len(set(apps))}")
    registrar("\nDURACION APROXIMADA POR APLICACION")
    for app, segundos in duraciones.most_common():
        registrar(f"{app}: {segundos:.1f} segundos ({segundos / 60:.1f} minutos)")
    registrar("\nTRANSICIONES MAS FRECUENTES")
    for (anterior, actual), cantidad in transiciones.most_common(10):
        registrar(f"{anterior} -> {actual}: {cantidad} veces")
    registrar("\nSECUENCIAS REPETITIVAS")
    if patrones:
        for p in patrones:
            registrar(f"PATRON DETECTADO: {' -> '.join(p['secuencia'])} | Ocurrencias: {p['ocurrencias']}")
            registrar("Estado: REQUIERE VALIDACION HUMANA")
    else:
        registrar("No se encontraron secuencias que superen el umbral.")
    registrar("\nNo se registran teclas, contraseñas, capturas, contenido ni URLs.")


def main():
    if sys.platform != "win32":
        raise RuntimeError("Esta V1 está diseñada para Windows.")
    if psutil is None:
        raise RuntimeError("Falta la dependencia psutil. El lanzador debe instalarla antes de iniciar.")

    cfg = cargar_config()
    duracion = max(1, float(cfg["duracion_horas"])) * 3600
    intervalo = max(0.2, float(cfg["intervalo_segundos"]))

    LOG_FILE.write_text("", encoding="utf-8")
    registrar("=" * 70)
    registrar("KIRMA AUTOMATION V1.0.0")
    registrar("=" * 70)
    registrar(f"Inicio: {datetime.now():%Y-%m-%d %H:%M:%S}")
    registrar(f"Duracion prevista: {cfg['duracion_horas']} hora(s)")
    registrar(f"Intervalo: {intervalo} segundo(s)")
    registrar("Autorizacion: confirmada por el operador al iniciar el programa.")
    registrar("Solo se registra la aplicacion en primer plano.")

    eventos = []
    inicio = time.monotonic()
    ultima_app = None

    try:
        while time.monotonic() - inicio < duracion:
            ahora = datetime.now()
            app = obtener_aplicacion_activa()
            eventos.append({"timestamp": ahora, "app": app})
            if app != ultima_app:
                registrar(f"{ahora:%H:%M:%S} | {ultima_app or 'INICIO'} -> {app}")
                ultima_app = app
            time.sleep(intervalo)
    finally:
        if eventos:
            analizar(eventos, cfg)
        registrar(f"Fin: {datetime.now():%Y-%m-%d %H:%M:%S}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        registrar(f"ERROR: {type(exc).__name__}: {exc}")
        raise
