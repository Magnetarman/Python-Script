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
    if ($pythonPath -eq $null) {
        $pythonPath = Get-Command "py" -ErrorAction SilentlyContinue
        if ($pythonPath -ne $null) {
            try {
                $output = py -$version --version 2>$null
                return $output -match "Python $version"
            }
            catch {
                return $false
            }
        }
    }
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
        "3.11" { winget install --id Python.Python.3.11 -e --source winget }
        "3.12" { winget install --id Python.Python.3.12 -e --source winget }
        default { 
            Write-Host "Versione Python non supportata. Procedo con Python.Launcher."
            winget install --id Python.Launcher -e --source winget
        }
    }
}

# Funzione per verificare i requisiti delle librerie
function Check-Requirements {
    $scriptDir = Get-Location
    $requirementsFile = Join-Path $scriptDir "requirements.txt"
    
    if (Test-Path $requirementsFile) {
        Write-Host "Trovato file requirements.txt. Controllo compatibilità versioni Python..."
        
        $content = Get-Content $requirementsFile
        $needsPython311 = $false
        
        foreach ($line in $content) {
            if ($line -match "numpy==2\.[3-9]" -or $line -match "numpy>=2\.[3-9]") {
                $needsPython311 = $true
                Write-Host "Rilevata dipendenza numpy 2.3+ che richiede Python 3.11+"
                break
            }
        }
        
        return $needsPython311
    }
    
    return $false
}

# Controllo dei requisiti per determinare la versione Python necessaria
$needsPython311 = Check-Requirements
$pythonVersion = if ($needsPython311) { "3.11" } else { "3.10" }

Write-Host "Versione Python richiesta: $pythonVersion"

# Controllo e installazione per la versione Python necessaria
if (-not (Check-PythonVersion -version $pythonVersion)) {
    Install-Python -version $pythonVersion
} else {
    Write-Host "Python $pythonVersion è già installato."
}

# Funzione per installare le dipendenze Python
function Install-PythonDependencies {
    $scriptDir = Get-Location
    $requirementsFile = Join-Path $scriptDir "requirements.txt"
    
    if (Test-Path $requirementsFile) {
        Write-Host "Installando le dipendenze da requirements.txt..."
        
        # Aggiorna pip alla versione più recente
        Write-Host "Aggiornamento di pip..."
        py -$pythonVersion -m pip install --upgrade pip
        
        # Installa le dipendenze
        Write-Host "Installazione delle librerie richieste..."
        py -$pythonVersion -m pip install -r $requirementsFile
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Tutte le dipendenze sono state installate con successo."
        } else {
            Write-Host "Errore durante l'installazione delle dipendenze. Tentativo con versioni compatibili..."
            
            # Se fallisce, prova con versioni compatibili
            $content = Get-Content $requirementsFile
            foreach ($line in $content) {
                if ($line -match "numpy==2\.[3-9]") {
                    Write-Host "Installando numpy versione compatibile con Python $pythonVersion..."
                    if ($pythonVersion -eq "3.10") {
                        py -$pythonVersion -m pip install "numpy>=1.21.0,<2.3.0"
                    } else {
                        py -$pythonVersion -m pip install numpy
                    }
                } elseif ($line -match "^[a-zA-Z]" -and -not $line.StartsWith("#")) {
                    Write-Host "Installando: $line"
                    py -$pythonVersion -m pip install $line
                }
            }
        }
    } else {
        Write-Host "File requirements.txt non trovato. Installando librerie comuni..."
        
        # Installa librerie comuni se non c'è requirements.txt
        $commonLibraries = @("numpy", "pandas", "matplotlib", "requests")
        
        foreach ($lib in $commonLibraries) {
            Write-Host "Installando $lib..."
            py -$pythonVersion -m pip install $lib
        }
    }
}

# Installa le dipendenze Python
Install-PythonDependencies

# Visualizzare il messaggio "Attendere..." per 2 secondi
Write-Host "Attendere..."
Start-Sleep -Seconds 2

# Ottieni il percorso della cartella in cui è stato eseguito lo script PowerShell
$scriptDir = Get-Location

# Verifica se il file main.py esiste nella stessa cartella dello script PowerShell
$mainScript = Join-Path $scriptDir "main.py"
if (Test-Path $mainScript) {
    Write-Host "Eseguo main.py con Python $pythonVersion..."

    # Esegui main.py con la versione Python corretta
    py -$pythonVersion $mainScript
} else {
    Write-Host "Il file main.py non è stato trovato nella stessa cartella dello script PowerShell."
}

Write-Host "Installazione completata. Premere un tasto per continuare..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")