Set shell=CreateObject("WScript.Shell")
d=CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
shell.Run """" & d & "\EJECUTAR_KIRMA_AUTOMATION.bat""",0,False
