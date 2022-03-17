Add-Type -AssemblyName System.Windows.Forms
$download_dir = New-Object System.Windows.Forms.FolderBrowserDialog
$download_dir.Description = "Downloadverzeichnis?"
$download_dir.RootFolder = "MyComputer" # need this string due to system account running this script no user acc, so no access to env variables outside system scope
#https://stackoverflow.com/questions/25690038/how-do-i-properly-use-the-folderbrowserdialog-in-powershell
$download_dir.ShowDialog() >$null #suppress "OK" stdout
$download_dir.SelectedPath | Out-File .\includes\last_dir.path -Encoding "ascii" # simpelst solution out file to get re-read by py server due to no interproc pipe