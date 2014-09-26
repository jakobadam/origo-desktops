# whereis.ps1 - locate the binary given a string
#
# It searches through links in the start menu to do so
#
# EXAMPLES
#   Find the path of binary of firefox
#     PS whereis.ps1 firefox 
#   Find paths of all items in start menu
#     PS whereis.ps1 *
$probe = $args[0]
$path = "$env:ProgramData\Microsoft\Windows\Start Menu\Programs"
$start_menu = ls $path -Recurse -Include *.lnk | sort -property Name

ForEach($lnk in $start_menu){
   $shell = New-Object -ComObject WScript.Shell

   $name = $lnk.BaseName
   $program_path = $shell.CreateShortcut($lnk).targetpath   
 
   if($probe -eq "" -or $probe -eq "*"){
       echo "$name|$program_path" 
   }

   elseif($name -match $probe){
       echo "$name|$program_path"   
   }
   
}

