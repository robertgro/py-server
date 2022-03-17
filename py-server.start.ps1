Add-Type -AssemblyName System.Windows.Forms
Split-Path $myinvocation.mycommand.path | Set-Location
$host_name = "127.0.0.1"
$port = "8000"
#Get-Location
#https://stackoverflow.com/questions/4724290/powershell-run-command-from-scripts-directory
$res = [System.Windows.Forms.MessageBox]::Show("Launching python listener$([System.Environment]::NewLine)`nHost:`t$($host_name)$([System.Environment]::NewLine)Port:`t$($port)$([System.Environment]::NewLine)`nAre you sure?", "Python TCP Listener Localhost", 4, [System.Windows.Forms.MessageBoxIcon]::Question)
$binpath = ".\env\Scripts\python.exe"

# switch statement not matching assembly class enumerations
if ($res -eq [System.Windows.Forms.DialogResult]::Yes) {
    Start-Process -FilePath $binpath -ArgumentList "main.py $($host_name) $($port)"
} elseif ($res -eq [System.Windows.Forms.DialogResult]::No) {
    Start-Process explorer.exe -ArgumentList (Split-Path $myinvocation.mycommand.path)
} else {
    # custom exit code for error debugging
    exit 4
}