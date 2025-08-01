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
    
    try {
        $output = py -$version --version 2>$null
        if ($output -match "Python $version") {
            return $true
        }
    }
    catch {
        # Ignora l'errore e continua
    }
    
    return $false
}

# Funzione per installare Python tramite winget
function Install-Python {
    param (
        [string]$version
    )
    
    Write-Host "Installando Python $version tramite winget..."
    
    try {
        switch ($version) {
            "3.10" { 
                winget install --id Python.Python.3.10 -e --source winget --accept-source-agreements --accept-package-agreements
            }
            "3.11" { 
                winget install --id Python.Python.3.11 -e --source winget --accept-source-agreements --accept-package-agreements
            }
            "3.12" { 
                winget install --id Python.Python.3.12 -e --source winget --accept-source-agreements --accept-package-agreements
            }
            default { 
                Write-Host "Versione Python non supportata: $version"
                return $false
            }
        }
        
        # Aspetta un momento per permettere l'installazione
        Start-Sleep -Seconds 3
        
        # Verifica se l'installazione è riuscita
        if (Check-PythonVersion -version $version) {
            Write-Host "Python $version installato con successo."
            return $true
        } else {
            Write-Host "Installazione di Python $version completata, ma verifica fallita."
            return $false
        }
    }
    catch {
        Write-Host "Errore durante l'installazione di Python $version : $($_.Exception.Message)"
        return $false
    }
}

# Funzione per installare le dipendenze Python
function Install-Dependencies {
    param (
        [string]$pythonVersion
    )
    
    $scriptDir = Get-Location
    $requirementsFile = Join-Path $scriptDir "requirements.txt"
    
    Write-Host "Installando dipendenze con Python $pythonVersion..."
    
    # Aggiorna pip
    Write-Host "Aggiornamento di pip..."
    py -$pythonVersion -m pip install --upgrade pip
    
    if (Test-Path $requirementsFile) {
        Write-Host "Trovato requirements.txt. Installando dipendenze..."
        py -$pythonVersion -m pip install -r $requirementsFile
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Dipendenze installate con successo da requirements.txt"
            return $true
        } else {
            Write-Host "Errore durante l'installazione da requirements.txt"
            return $false
        }
    } else {
        Write-Host "File requirements.txt non trovato. Installando librerie comuni..."
        
        $commonLibraries = @("numpy", "pandas", "matplotlib", "requests", "pillow")
        $allSuccess = $true
        
        foreach ($lib in $commonLibraries) {
            Write-Host "Installando $lib..."
            py -$pythonVersion -m pip install $lib
            if ($LASTEXITCODE -ne 0) {
                Write-Host "Errore durante l'installazione di $lib"
                $allSuccess = $false
            }
        }
        
        return $allSuccess
    }
}

# Lista delle versioni Python da installare
$pythonVersions = @("3.10", "3.11", "3.12")
$installedVersions = @()
$primaryVersion = ""

Write-Host "Controllo e installazione delle versioni Python..."

# Controlla e installa ogni versione
foreach ($version in $pythonVersions) {
    Write-Host "`nControllo Python $version..."
    
    if (Check-PythonVersion -version $version) {
        Write-Host "Python $version è già installato."
        $installedVersions += $version
        if ($primaryVersion -eq "") {
            $primaryVersion = $version
        }
    } else {
        Write-Host "Python $version non trovato. Procedo con l'installazione..."
        if (Install-Python -version $version) {
            $installedVersions += $version
            if ($primaryVersion -eq "") {
                $primaryVersion = $version
            }
        }
    }
}

# Mostra riepilogo versioni installate
Write-Host "`nRiepilogo versioni Python installate:"
foreach ($version in $installedVersions) {
    Write-Host "  - Python $version"
}

# Determina la versione da usare per le dipendenze
if ($installedVersions.Count -gt 0) {
    # Preferisci 3.11 se disponibile, altrimenti usa la più recente
    if ($installedVersions -contains "3.11") {
        $primaryVersion = "3.11"
    } elseif ($installedVersions -contains "3.12") {
        $primaryVersion = "3.12"
    } else {
        $primaryVersion = $installedVersions[-1]
    }
    
    Write-Host "`nUsando Python $primaryVersion per installare le dipendenze..."
    Install-Dependencies -pythonVersion $primaryVersion
} else {
    Write-Host "`nNessuna versione di Python è stata installata correttamente."
    Write-Host "Tentativo di installazione del Python Launcher..."
    winget install --id Python.Launcher -e --source winget --accept-source-agreements --accept-package-agreements
}

# Visualizzare il messaggio "Attendere..." per 2 secondi
Write-Host "`nAttendere..."
Start-Sleep -Seconds 2

# Ottieni il percorso della cartella in cui è stato eseguito lo script PowerShell
$scriptDir = Get-Location

# Verifica se il file main.py esiste nella stessa cartella dello script PowerShell
$mainScript = Join-Path $scriptDir "main.py"
if (Test-Path $mainScript) {
    Write-Host "`nTrovato main.py nella cartella dello script."
    
    # Determina la versione Python migliore da usare
    $versionToUse = ""
    
    if ($installedVersions -contains "3.11") {
        $versionToUse = "3.11"
    } elseif ($installedVersions -contains "3.12") {
        $versionToUse = "3.12"
    } elseif ($installedVersions -contains "3.10") {
        $versionToUse = "3.10"
    }
    
    if ($versionToUse -ne "") {
        Write-Host "Eseguo main.py con Python $versionToUse..."
        
        # Esegui main.py con la versione Python corretta
        py -$versionToUse $mainScript
    } else {
        Write-Host "Nessuna versione Python valida trovata. Tentativo con 'python'..."
        python $mainScript
        
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Tentativo con 'py'..."
            py $mainScript
        }
    }
} else {
    Write-Host "`nIl file main.py non è stato trovato nella stessa cartella dello script PowerShell."
    Write-Host "Cartella corrente: $scriptDir"
    Write-Host "File cercato: $mainScript"
}

Write-Host "`nScript completato. Premere un tasto per chiudere..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")