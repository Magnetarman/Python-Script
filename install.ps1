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

# Funzione per ottenere tutte le versioni Python realmente disponibili
function Get-AvailablePythonVersions {
    $availableVersions = @()
    
    try {
        # Usa py -0 per ottenere la lista delle versioni installate
        $output = py -0 2>&1
        
        if ($output) {
            foreach ($line in $output) {
                if ($line -match '-(\d+\.\d+)') {
                    $version = $matches[1]
                    if ($version -notin $availableVersions) {
                        $availableVersions += $version
                    }
                }
            }
        }
    }
    catch {
        Write-Host "Errore nel rilevamento versioni Python: $($_.Exception.Message)"
    }
    
    # Se py -0 non funziona, prova metodi alternativi
    if ($availableVersions.Count -eq 0) {
        # Prova con comandi diretti
        $testVersions = @("3.12", "3.11", "3.10", "3.9", "3.8")
        foreach ($version in $testVersions) {
            try {
                $result = py -$version --version 2>$null
                if ($result -and $result -match "Python $version") {
                    $availableVersions += $version
                }
            }
            catch {
                # Versione non disponibile
            }
        }
    }
    
    return $availableVersions
}

# Funzione per installare Python tramite winget se necessario
function Install-PythonIfNeeded {
    param (
        [string]$version
    )
    
    Write-Host "Tentativo di installazione Python $version tramite winget..."
    
    try {
        switch ($version) {
            "3.10" { 
                winget install --id Python.Python.3.10 -e --source winget --accept-source-agreements --accept-package-agreements --silent
            }
            "3.11" { 
                winget install --id Python.Python.3.11 -e --source winget --accept-source-agreements --accept-package-agreements --silent
            }
            "3.12" { 
                winget install --id Python.Python.3.12 -e --source winget --accept-source-agreements --accept-package-agreements --silent
            }
        }
        
        # Attendi e ricontrolla
        Start-Sleep -Seconds 5
        
        # Verifica se ora è disponibile
        try {
            $result = py -$version --version 2>$null
            if ($result -and $result -match "Python $version") {
                Write-Host "Python $version installato e verificato con successo."
                return $true
            }
        }
        catch {
            # Installazione fallita
        }
        
        Write-Host "Installazione di Python $version non riuscita o non verificabile."
        return $false
    }
    catch {
        Write-Host "Errore durante l'installazione di Python $version : $($_.Exception.Message)"
        return $false
    }
}

# Funzione per installare le dipendenze
function Install-Dependencies {
    param (
        [string]$pythonVersion
    )
    
    $scriptDir = Get-Location
    $requirementsFile = Join-Path $scriptDir "requirements.txt"
    
    Write-Host "Installando dipendenze con Python $pythonVersion..."
    
    # Verifica che la versione sia realmente disponibile prima di procedere
    try {
        $testResult = py -$pythonVersion --version 2>$null
        if (-not ($testResult -match "Python $pythonVersion")) {
            Write-Host "ERRORE: Python $pythonVersion non è realmente disponibile!"
            return $false
        }
    }
    catch {
        Write-Host "ERRORE: Impossibile verificare Python $pythonVersion!"
        return $false
    }
    
    # Aggiorna pip
    Write-Host "Aggiornamento di pip..."
    try {
        py -$pythonVersion -m pip install --upgrade pip --quiet
        Write-Host "Pip aggiornato con successo."
    }
    catch {
        Write-Host "Errore nell'aggiornamento di pip, continuo comunque..."
    }
    
    if (Test-Path $requirementsFile) {
        Write-Host "Trovato requirements.txt. Installando dipendenze..."
        try {
            py -$pythonVersion -m pip install -r $requirementsFile
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host "Dipendenze installate con successo da requirements.txt"
                return $true
            } else {
                Write-Host "Errore durante l'installazione da requirements.txt (codice: $LASTEXITCODE)"
                
                # Prova installazione delle dipendenze una per una
                Write-Host "Tentativo di installazione individuale delle dipendenze..."
                $content = Get-Content $requirementsFile
                $success = $true
                
                foreach ($line in $content) {
                    $line = $line.Trim()
                    if ($line -and -not $line.StartsWith("#")) {
                        Write-Host "Installando: $line"
                        try {
                            py -$pythonVersion -m pip install $line
                            if ($LASTEXITCODE -ne 0) {
                                Write-Host "Errore con $line, continuo con le altre..."
                                $success = $false
                            }
                        }
                        catch {
                            Write-Host "Eccezione durante l'installazione di $line"
                            $success = $false
                        }
                    }
                }
                
                return $success
            }
        }
        catch {
            Write-Host "Eccezione durante l'installazione delle dipendenze: $($_.Exception.Message)"
            return $false
        }
    } else {
        Write-Host "File requirements.txt non trovato. Installando librerie comuni..."
        
        $commonLibraries = @("numpy", "pandas", "matplotlib", "requests")
        $allSuccess = $true
        
        foreach ($lib in $commonLibraries) {
            Write-Host "Installando $lib..."
            try {
                py -$pythonVersion -m pip install $lib --quiet
                if ($LASTEXITCODE -eq 0) {
                    Write-Host "$lib installato con successo."
                } else {
                    Write-Host "Errore durante l'installazione di $lib"
                    $allSuccess = $false
                }
            }
            catch {
                Write-Host "Eccezione durante l'installazione di $lib"
                $allSuccess = $false
            }
        }
        
        return $allSuccess
    }
}

Write-Host "=== INIZIO CONTROLLO E INSTALLAZIONE PYTHON ==="

# Ottieni versioni Python realmente disponibili
Write-Host "Rilevamento versioni Python disponibili..."
$availableVersions = Get-AvailablePythonVersions

if ($availableVersions.Count -gt 0) {
    Write-Host "Versioni Python trovate:"
    foreach ($version in $availableVersions) {
        Write-Host "  - Python $version"
    }
} else {
    Write-Host "Nessuna versione Python trovata. Installazione di Python 3.11..."
    
    # Installa Python Launcher se non presente
    Write-Host "Installando Python Launcher..."
    winget install --id Python.Launcher -e --source winget --accept-source-agreements --accept-package-agreements --silent
    
    # Installa Python 3.11
    if (Install-PythonIfNeeded -version "3.11") {
        $availableVersions += "3.11"
    }
    
    # Se 3.11 fallisce, prova 3.10
    if ($availableVersions.Count -eq 0) {
        if (Install-PythonIfNeeded -version "3.10") {
            $availableVersions += "3.10"
        }
    }
}

# Installa versioni aggiuntive se necessario
$targetVersions = @("3.11", "3.12")
foreach ($targetVersion in $targetVersions) {
    if ($targetVersion -notin $availableVersions) {
        Write-Host "Tentativo di installazione Python $targetVersion..."
        if (Install-PythonIfNeeded -version $targetVersion) {
            $availableVersions += $targetVersion
        }
    }
}

# Ri-rileva le versioni dopo le installazioni
Write-Host "Ri-rilevamento versioni Python dopo installazioni..."
$finalVersions = Get-AvailablePythonVersions

Write-Host "Versioni Python finali disponibili:"
if ($finalVersions.Count -gt 0) {
    foreach ($version in $finalVersions) {
        Write-Host "  - Python $version"
    }
} else {
    Write-Host "ATTENZIONE: Nessuna versione Python rilevata!"
}

# Scegli la versione migliore per installare le dipendenze
$versionToUse = ""
$preferenceOrder = @("3.11", "3.12", "3.10", "3.9", "3.8")

foreach ($preferredVersion in $preferenceOrder) {
    if ($preferredVersion -in $finalVersions) {
        $versionToUse = $preferredVersion
        break
    }
}

if ($versionToUse -ne "") {
    Write-Host "Usando Python $versionToUse per installare le dipendenze..."
    $installResult = Install-Dependencies -pythonVersion $versionToUse
    
    if ($installResult) {
        Write-Host "Dipendenze installate con successo!"
    } else {
        Write-Host "Problemi durante l'installazione delle dipendenze."
    }
} else {
    Write-Host "ERRORE: Nessuna versione Python utilizzabile trovata!"
}

# Funzione per aggiungere Python e pip al PATH di Windows
function Add-PythonToPath {
    param (
        [string]$pythonVersion
    )
    
    Write-Host "Aggiungendo Python $pythonVersion al PATH di Windows..."
    
    try {
        # Ottieni il percorso di installazione di Python
        $pythonOutput = py -$pythonVersion -c "import sys; print(sys.executable)" 2>$null
        
        if ($pythonOutput) {
            $pythonPath = Split-Path $pythonOutput
            $scriptsPath = Join-Path $pythonPath "Scripts"
            
            Write-Host "Percorso Python: $pythonPath"
            Write-Host "Percorso Scripts: $scriptsPath"
            
            # Ottieni il PATH corrente
            $currentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
            
            # Controlla se i percorsi sono già nel PATH
            $pathsToAdd = @()
            
            if ($currentPath -notlike "*$pythonPath*") {
                $pathsToAdd += $pythonPath
                Write-Host "Aggiungendo $pythonPath al PATH..."
            } else {
                Write-Host "Python path già presente nel PATH."
            }
            
            if ($currentPath -notlike "*$scriptsPath*") {
                $pathsToAdd += $scriptsPath
                Write-Host "Aggiungendo $scriptsPath al PATH..."
            } else {
                Write-Host "Scripts path già presente nel PATH."
            }
            
            # Aggiungi i percorsi al PATH se necessario
            if ($pathsToAdd.Count -gt 0) {
                $newPath = $currentPath
                foreach ($pathToAdd in $pathsToAdd) {
                    if ($newPath -ne "") {
                        $newPath += ";"
                    }
                    $newPath += $pathToAdd
                }
                
                # Imposta il nuovo PATH per l'utente corrente
                [Environment]::SetEnvironmentVariable("PATH", $newPath, "User")
                
                # Aggiorna il PATH nella sessione corrente
                $env:PATH = $newPath
                
                Write-Host "PATH aggiornato con successo!"
                Write-Host "I percorsi Python sono ora disponibili globalmente."
                
                return $true
            } else {
                Write-Host "Tutti i percorsi Python sono già nel PATH."
                return $true
            }
        } else {
            Write-Host "Impossibile ottenere il percorso di Python $pythonVersion"
            return $false
        }
    }
    catch {
        Write-Host "Errore durante l'aggiunta di Python al PATH: $($_.Exception.Message)"
        return $false
    }
}

# Aggiungi la versione Python principale al PATH
if ($versionToUse -ne "") {
    Write-Host "Configurazione PATH per Python $versionToUse..."
    $pathResult = Add-PythonToPath -pythonVersion $versionToUse
    
    if ($pathResult) {
        Write-Host "PATH configurato correttamente!"
    } else {
        Write-Host "Problemi nella configurazione del PATH, continuo comunque..."
    }
}

# Visualizzare il messaggio "Attendere..." per 2 secondi
Write-Host ""
Write-Host "Attendere..."
Start-Sleep -Seconds 2

# Ottieni il percorso della cartella in cui è stato eseguito lo script PowerShell
$scriptDir = Get-Location

# Verifica se il file main.py esiste nella stessa cartella dello script PowerShell
$mainScript = Join-Path $scriptDir "main.py"
Write-Host "Verifica esistenza main.py in: $scriptDir"

if (Test-Path $mainScript) {
    Write-Host "Trovato main.py nella cartella dello script."
    
    # Usa la versione Python migliore disponibile
    $executionVersion = ""
    foreach ($preferredVersion in $preferenceOrder) {
        if ($preferredVersion -in $finalVersions) {
            $executionVersion = $preferredVersion
            break
        }
    }
    
    if ($executionVersion -ne "") {
        Write-Host "Eseguo main.py con Python $executionVersion..."
        
        # Aggiungi anche questa versione al PATH se diversa da quella usata per le dipendenze
        if ($executionVersion -ne $versionToUse) {
            Write-Host "Configurazione PATH per Python $executionVersion..."
            Add-PythonToPath -pythonVersion $executionVersion
        }
        
        # Verifica finale che la versione sia utilizzabile
        try {
            $testResult = py -$executionVersion --version 2>$null
            if ($testResult -match "Python $executionVersion") {
                # Esegui main.py con la versione Python corretta
                Write-Host "Avvio di main.py..."
                py -$executionVersion $mainScript
            } else {
                Write-Host "Versione $executionVersion non verificabile, uso comando generico..."
                py $mainScript
            }
        }
        catch {
            Write-Host "Errore nella verifica finale, uso comando generico..."
            py $mainScript
        }
    } else {
        Write-Host "Nessuna versione Python valida, tentativo con comando generico..."
        try {
            py $mainScript
        }
        catch {
            Write-Host "Tentativo con 'python'..."
            python $mainScript
        }
    }
} else {
    Write-Host "Il file main.py non è stato trovato nella stessa cartella dello script PowerShell."
    Write-Host "Cartella corrente: $scriptDir"
    Write-Host "File cercato: $mainScript"
    
    # Lista i file .py nella cartella per debug
    $pyFiles = Get-ChildItem -Path $scriptDir -Filter "*.py" -ErrorAction SilentlyContinue
    if ($pyFiles.Count -gt 0) {
        Write-Host "File Python trovati nella cartella:"
        foreach ($file in $pyFiles) {
            Write-Host "  - $($file.Name)"
        }
    } else {
        Write-Host "Nessun file Python trovato nella cartella."
    }
}

Write-Host ""
Write-Host "=== SCRIPT COMPLETATO ==="
Write-Host "Premere un tasto per chiudere..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")