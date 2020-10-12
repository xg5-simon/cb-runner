<#
.Synopsis
   Update an erroneous line for AutoUpdate = 0

.NOTES
   You will to edit line 17 (-replace $line statememnt) with what you want the new value to be 
#>

(Get-Content -path 'C:\Program Files\Confer\cfg.ini' -Raw) -replace 'AutoUpdate=0','AutoUpdate=1' | Set-Content -Path 'C:\Program Files\Confer\cfg.ini'
