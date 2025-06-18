# Funzione per verificare se PowerShell è in modalità amministratore
function Check-Admin {
    $isAdmin = [bool]([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
    return $isAdmin
}

# Se PowerShell non è in modalità amministratore, chiedi i privilegi di amministratore
if (-not (Check-Admin)) {
    Write-Host "PowerShell non è in modalità amministratore. Avvio con privilegi di amministratore..."
    
    # Crea un nuovo processo PowerShell con privilegi di amministratore
    Start-Process powershell -ArgumentList "Start-Process powershell -Verb runAs -ArgumentList '$PSCommandPath'" -Verb runAs
    exit
}

# Funzione per verificare se una versione specifica di Python è installata
function Check-PythonVersion {
    param (
        [string]$version
    )
    
    $pythonPath = Get-Command "python$version" -ErrorAction SilentlyContinue
    return $pythonPath -ne $null
}

# Funzione per installare Python tramite winget
function Install-Python {
    param (
        [string]$version
    )
    
    Write-Host "Installando Python $version tramite winget..."
    switch ($version) {
        "3.10" { winget install --id Python.Python.3.10 -e --source winget }
        default { Write-Host "Versione Python non supportata. Procedo con Python.Launcher." }
    }
}

# Controllo e installazione per Python 3.10
$pythonVersion = "3.10"
if (-not (Check-PythonVersion -version $pythonVersion)) {
    Install-Python -version $pythonVersion
} else {
    Write-Host "Python $pythonVersion è già installato."
}

# Visualizzare il messaggio "Attendere..." per 2 secondi
Write-Host "Attendere..."
Start-Sleep -Seconds 2

# Ottieni il percorso della cartella in cui è stato eseguito lo script PowerShell
$scriptDir = Get-Location

# Verifica se il file main.py esiste nella stessa cartella dello script PowerShell
$mainScript = Join-Path $scriptDir "main.py"
if (Test-Path $mainScript) {
    Write-Host "Eseguo main.py..."

    # Esegui main.py nella stessa finestra di PowerShell
    py $mainScript
} else {
    Write-Host "Il file main.py non è stato trovato nella stessa cartella dello script PowerShell."
}
