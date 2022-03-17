Write-Host "`nCreating a json gmail list by name with 'used flag' indicator for signup" -ForegroundColor Cyan

$inputchoice = [string]::Empty
$signupmails = @{mails=@()}
$mail_list = @()
$mail = [string]::Empty

do {
    $inputchoice = Read-Host "`nEnter a gmail account name ('q' for exit)"
    if ($inputchoice -notin 'q') {
        for($i=0; $i -lt $inputchoice.Length; $i++) {
            if ($i -eq 0) {
                $mail = $inputchoice + "@gmail.com"
            } else {
                $mail = $inputchoice.Insert($i,".") + "@gmail.com"
            }
            $mail_list += @(@{id=$mail; used=$false})
        }
    }
    #https://stackoverflow.com/questions/12860830/how-do-i-populate-an-array-of-unknown-length-in-powershell
    $signupmails["mails"] += $mail_list
    $signupmails | ConvertTo-Json | Out-File -Encoding ascii -FilePath .\signupmails.json
    # need to be ascii encoding for json out file to work https://stackoverflow.com/questions/33936043/modify-a-json-file-with-powershell-without-writing-bom
}
until ($inputchoice -eq 'q')

Write-Host "Bye`n"

#switching between gmail and googlemail
#omitting double provider extension here, using @gmail only 