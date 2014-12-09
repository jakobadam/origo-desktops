Option Explicit
Dim MSITarget

On Error Resume Next
If wscript.arguments.count = 1 Then 
   With CreateObject("WindowsInstaller.Installer")
      Set MSITarget = .ShortcutTarget(wscript.arguments(0))
      If Err = 0 then
         Wscript.Echo .ComponentPath(MSITarget.StringData(1), MSITarget.StringData(3))
      Else 
         Wscript.Echo wscript.arguments(0) & vbcrlf & "is not a legitimate MSI shortcut file or could not be found"
      End If
   End With
End If
On Error Goto 0