KIRMA AUTOMATION DISCOVERY V1.1.0
=================================

OBJETIVO
Detectar patrones repetitivos de uso de aplicaciones y generar candidatos a tareas que merecen una evaluación de automatización.

USO
1. Ejecutar INICIAR_KIRMA.bat.
2. El proceso funciona oculto y realiza la captura durante 4 horas desde el inicio.
3. No es necesario dejar una ventana CMD visible.
4. Al finalizar se generan/actualizan:
   - registro_pc.txt
   - resultado.json
   - candidatos_automatizacion.json
   - estado.json

NUEVO EN V1.1
- Detecta secuencias de 3, 4 y 5 aplicaciones (configurable).
- Cuenta repeticiones no solapadas.
- Genera candidatos_a_automatizacion en resultado.json.
- Genera candidatos_automatizacion.json como archivo independiente.
- Registra transiciones frecuentes.
- Mantiene estado.json para comprobar si el proceso sigue ejecutándose sin mostrar CMD.

INTERPRETACION
Un patrón repetitivo indica recurrencia, no demuestra por sí mismo que exista una automatización segura o conveniente. La tarea debe validarse observando las acciones reales, reglas, excepciones y resultado esperado.

PRIVACIDAD
Solo se registra el nombre del proceso/aplicación que está en primer plano y la hora del cambio. No se registran teclas, contraseñas, capturas, contenido de documentos ni URLs.
