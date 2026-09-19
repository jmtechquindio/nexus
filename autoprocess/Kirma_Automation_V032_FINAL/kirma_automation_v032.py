import ctypes
import time
from datetime import datetime
from collections import Counter
from pathlib import Path
import psutil

DURACION = 4 * 60 * 60
INTERVALO = 1
MIN_REPETICIONES = 3
LONGITUD_SECUENCIA = 4
ARCHIVO = Path(__file__).with_name("registro_pc.txt")

def obtener_aplicacion_activa():
    try:
        hwnd=ctypes.windll.user32.GetForegroundWindow()
        if not hwnd: return "DESCONOCIDO"
        pid=ctypes.c_ulong()
        if ctypes.windll.user32.GetWindowThreadProcessId(hwnd,ctypes.byref(pid))==0 or pid.value==0: return "DESCONOCIDO"
        return psutil.Process(pid.value).name()
    except Exception: return "DESCONOCIDO"

def registrar(texto):
    with ARCHIVO.open("a",encoding="utf-8") as f: f.write(texto+"\n")

def comprimir_historial(eventos):
    r=[]
    for e in eventos:
        if not r or r[-1]["app"]!=e["app"]: r.append(e)
    return r

def detectar_secuencias(apps):
    return [tuple(apps[i:i+LONGITUD_SECUENCIA]) for i in range(max(0,len(apps)-LONGITUD_SECUENCIA+1))]

def contar_no_solapadas(secuencias):
    posiciones={}
    for p,s in enumerate(secuencias): posiciones.setdefault(s,[]).append(p)
    resultado={}
    for s,lista in posiciones.items():
        c=0; ultima=-LONGITUD_SECUENCIA
        for p in lista:
            if p>=ultima+LONGITUD_SECUENCIA: c+=1; ultima=p
        resultado[s]=c
    return resultado

def analizar(eventos):
    cambios=comprimir_historial(eventos)
    registrar(""); registrar("="*70); registrar("ANALISIS KIRMA AUTOMATION DISCOVERY V0.3.2"); registrar("="*70)
    registrar(f"Muestras: {len(eventos)}")
    registrar(f"Cambios detectados: {max(0,len(cambios)-1)}")
    registrar(f"Aplicaciones diferentes: {len(set(e['app'] for e in cambios))}")
    duraciones=Counter()
    for i,e in enumerate(cambios):
        fin=cambios[i+1]["timestamp"] if i+1<len(cambios) else eventos[-1]["timestamp"]
        duraciones[e["app"]]+=max(0,(fin-e["timestamp"]).total_seconds())
    registrar(""); registrar("DURACION APROXIMADA POR APLICACION"); registrar("-"*70)
    for app,s in duraciones.most_common(): registrar(f"{app}: {s:.1f} segundos ({s/60:.1f} minutos)")
    trans=Counter((cambios[i-1]["app"],cambios[i]["app"]) for i in range(1,len(cambios)))
    registrar(""); registrar("TRANSICIONES MAS FRECUENTES"); registrar("-"*70)
    for (a,b),c in trans.most_common(10): registrar(f"{a} -> {b}: {c} veces")
    registrar(""); registrar("SECUENCIAS REPETITIVAS"); registrar("-"*70)
    encontradas=False
    for seq,c in sorted(contar_no_solapadas(detectar_secuencias([e["app"] for e in cambios])).items(),key=lambda x:x[1],reverse=True):
        if c>=MIN_REPETICIONES:
            encontradas=True; registrar(""); registrar("PATRON DETECTADO"); registrar(f"Secuencia: {' -> '.join(seq)}")
            registrar(f"Ocurrencias independientes: {c}"); registrar("Nivel de evidencia: OBSERVACION")
            registrar("Estado: REQUIERE VALIDACION HUMANA")
    if not encontradas: registrar("No se encontraron secuencias que superen el umbral.")
    registrar(""); registrar("="*70); registrar("INTERPRETACION"); registrar("="*70)
    registrar("El sistema detecta cambios de aplicacion en primer plano.")
    registrar("Las duraciones son aproximadas y dependen del intervalo de comprobacion.")
    registrar("Una secuencia repetitiva NO demuestra que exista una automatizacion viable.")
    registrar("No se registran teclas, contraseñas, capturas, contenido ni URLs.")

def main():
    print("="*70); print("KIRMA AUTOMATION DISCOVERY - V0.3.2"); print("="*70)
    if input("\n¿Tiene autorizacion para analizar este equipo? (SI/NO): ").strip().upper()!="SI":
        print("\nAnalisis cancelado."); return
    print("\nDuracion: 4 horas"); print("Comprobacion: cada 1 segundo")
    print("Solo se registra la aplicacion en primer plano.")
    input("\nPresione ENTER para comenzar las 4 horas...")
    ARCHIVO.write_text("",encoding="utf-8")
    registrar("="*70); registrar("KIRMA AUTOMATION DISCOVERY V0.3.2")
    registrar(f"Inicio real: {datetime.now():%Y-%m-%d %H:%M:%S}"); registrar("Duracion prevista: 4 horas")
    eventos=[]; inicio=time.monotonic(); ultima=None
    try:
        while time.monotonic()-inicio<DURACION:
            ahora=datetime.now(); app=obtener_aplicacion_activa(); eventos.append({"timestamp":ahora,"app":app})
            if app!=ultima:
                registrar(f"{ahora:%H:%M:%S} | {ultima or 'INICIO'} -> {app}"); print(f"{ahora:%H:%M:%S} | {ultima or 'INICIO'} -> {app}"); ultima=app
            time.sleep(INTERVALO)
    except KeyboardInterrupt: registrar("Detencion manual por el operador.")
    if eventos: analizar(eventos)
    registrar(f"Fin: {datetime.now():%Y-%m-%d %H:%M:%S}")
    print(f"\nPrueba terminada. Resultado: {ARCHIVO}")

if __name__=="__main__": main()
