KIRMA AUTOMATION DISCOVERY V0.3.2
=================================

1. Instalar:
   pip install psutil

2. Ejecutar:
   python kirma_automation_v032.py

3. Prueba:
   - Responder SI solo con autorizacion.
   - Cambiar deliberadamente entre Chrome y Excel varias veces.
   - Abrir Word u Outlook para probar otros cambios.
   - Revisar registro_pc.txt.

Registra solo la aplicacion en primer plano, cambios y duraciones aproximadas.
No registra teclas, contraseñas, capturas, contenido de documentos ni URLs.

Una secuencia repetitiva es una observacion tecnica, no una conclusion de que
exista una oportunidad de automatizacion. Debe validarse el proceso con el usuario.


EJECUCION CON DOBLE CLIC
========================

1. Coloque estos dos archivos en la misma carpeta:
   - EJECUTAR_KIRMA_AUTOMATION.bat
   - kirma_automation_v032.py

2. Haga doble clic en:
   EJECUTAR_KIRMA_AUTOMATION.bat

El lanzador:
- busca Python;
- comprueba si psutil está instalado;
- intenta instalar psutil si falta;
- ejecuta el script;
- deja la ventana abierta al terminar;
- genera registro_pc.txt en la misma carpeta.

Requisitos:
- Windows.
- Python instalado.
- Internet solamente si hace falta instalar psutil.

No ejecute el archivo .py directamente con doble clic si quiere ver claramente
los mensajes y errores; utilice el archivo .bat.
