# Funzione per verificare privilegi amministratore
function Check-Admin {
    return [bool]([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Richiedi privilegi amministratore se necessario
if (-not (Check-Admin)) {
    Write-Host "PowerShell non è in modalità amministratore. Avvio con privilegi di amministratore..."
    Start-Process powershell -ArgumentList "Start-Process powershell -Verb runAs -ArgumentList '$PSCommandPath'" -Verb runAs
    exit
}

# Funzione per ottenere versioni Python disponibili
function Get-AvailablePythonVersions {
    $versions = @()
    try {
        $output = py -0 2>&1
        if ($output) {
            $versions = $output | Where-Object { $_ -match '-(\d+\.\d+)' } | ForEach-Object { $matches[1] } | Sort-Object -Unique
        }
        
        # Fallback se py -0 non funziona
        if ($versions.Count -eq 0) {
            @("3.12", "3.11", "3.10", "3.9", "3.8") | ForEach-Object {
                try {
                    if ((py -$_ --version 2>$null) -match "Python $_") { $versions += $_ }
                } catch { }
            }
        }
    } catch { }
    return $versions
}

# Funzione per installare Python tramite winget
function Install-PythonIfNeeded {
    param([string]$version)
    
    Write-Host "Installando Python $version tramite winget..."
    try {
        $packageId = switch ($version) {
            "3.10" { "Python.Python.3.10" }
            "3.11" { "Python.Python.3.11" }
            "3.12" { "Python.Python.3.12" }
            default { return $false }
        }
        
        winget install --id $packageId -e --source winget --accept-source-agreements --accept-package-agreements --silent | Out-Null
        Start-Sleep -Seconds 5
        
        $result = py -$version --version 2>$null
        if ($result -match "Python $version") {
            Write-Host "Python $version installato con successo."
            return $true
        }
    } catch { }
    
    Write-Host "Installazione di Python $version fallita."
    return $false
}

# Funzione per aggiungere Python al PATH
function Add-PythonToPath {
    param([string]$pythonVersion)
    
    Write-Host "Configurando PATH per Python $pythonVersion..."
    try {
        $pythonExe = py -$pythonVersion -c "import sys; print(sys.executable)" 2>$null
        if (-not $pythonExe) { return $false }
        
        $pythonPath = Split-Path $pythonExe
        $scriptsPath = Join-Path $pythonPath "Scripts"
        $currentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
        $pathsToAdd = @($pythonPath, $scriptsPath) | Where-Object { $currentPath -notlike "*$_*" }
        
        if ($pathsToAdd.Count -gt 0) {
            $newPath = ($currentPath, $pathsToAdd) -join ";"
            [Environment]::SetEnvironmentVariable("PATH", $newPath, "User")
            $env:PATH = $newPath
            Write-Host "PATH aggiornato: $($pathsToAdd -join ', ')"
            return $true
        } else {
            Write-Host "PATH già configurato correttamente."
            return $true
        }
    } catch {
        Write-Host "Errore configurazione PATH: $($_.Exception.Message)"
        return $false
    }
}

# Funzione per installare dipendenze
function Install-Dependencies {
    param([string]$pythonVersion)
    
    # Verifica disponibilità versione
    if (-not ((py -$pythonVersion --version 2>$null) -match "Python $pythonVersion")) {
        Write-Host "ERRORE: Python $pythonVersion non disponibile!"
        return $false
    }
    
    Write-Host "Installando dipendenze con Python $pythonVersion..."
    
    # Aggiorna pip
    try {
        py -$pythonVersion -m pip install --upgrade pip --quiet | Out-Null
        Write-Host "Pip aggiornato."
    } catch {
        Write-Host "Warning: Errore aggiornamento pip."
    }
    
    $scriptDir = Get-Location
    $requirementsFile = Join-Path $scriptDir "requirements.txt"
    
    if (Test-Path $requirementsFile) {
        Write-Host "Installando da requirements.txt..."
        py -$pythonVersion -m pip install -r $requirementsFile
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Dipendenze installate con successo."
            return $true
        } else {
            # Installazione individuale come fallback
            Write-Host "Tentativo installazione individuale..."
            $success = $true
            Get-Content $requirementsFile | Where-Object { $_.Trim() -and -not $_.StartsWith("#") } | ForEach-Object {
                Write-Host "Installando: $_"
                py -$pythonVersion -m pip install $_ --quiet
                if ($LASTEXITCODE -ne 0) { $success = $false }
            }
            return $success
        }
    } else {
        Write-Host "Installando librerie comuni..."
        $libs = @("numpy", "pandas", "matplotlib", "requests")
        $success = $true
        
        $libs | ForEach-Object {
            Write-Host "Installando $_..."
            py -$pythonVersion -m pip install $_ --quiet
            if ($LASTEXITCODE -ne 0) { 
                Write-Host "Errore con $_"
                $success = $false
            }
        }
        return $success
    }
}

# === ESECUZIONE PRINCIPALE ===
Write-Host "=== SETUP PYTHON E DIPENDENZE ==="

# Rileva versioni disponibili
Write-Host "Rilevamento versioni Python..."
$availableVersions = Get-AvailablePythonVersions

if ($availableVersions.Count -gt 0) {
    Write-Host "Versioni trovate: $($availableVersions -join ', ')"
} else {
    Write-Host "Nessuna versione trovata. Installando Python..."
    winget install --id Python.Launcher -e --source winget --accept-source-agreements --accept-package-agreements --silent | Out-Null
    
    # Installa 3.11 come priorità
    if (Install-PythonIfNeeded -version "3.11") { $availableVersions += "3.11" }
    elseif (Install-PythonIfNeeded -version "3.10") { $availableVersions += "3.10" }
}

# Installa versioni target se mancanti
@("3.11", "3.12") | Where-Object { $_ -notin $availableVersions } | ForEach-Object {
    if (Install-PythonIfNeeded -version $_) { $availableVersions += $_ }
}

# Ri-rileva versioni finali
$finalVersions = Get-AvailablePythonVersions
Write-Host "Versioni finali: $($finalVersions -join ', ')"

# Seleziona versione ottimale
$versionToUse = @("3.11", "3.12", "3.10", "3.9", "3.8") | Where-Object { $_ -in $finalVersions } | Select-Object -First 1

if ($versionToUse) {
    Write-Host "Usando Python $versionToUse per dipendenze..."
    $installResult = Install-Dependencies -pythonVersion $versionToUse
    
    # Configura PATH
    Add-PythonToPath -pythonVersion $versionToUse | Out-Null
    
    Write-Host "Attendere..."
    Start-Sleep -Seconds 2
    
    # === ESECUZIONE MAIN.PY ===
    $scriptDir = Get-Location
    $mainScript = Join-Path $scriptDir "main.py"
    
    Write-Host "Verifica main.py in: $scriptDir"
    
    if (Test-Path $mainScript) {
        Write-Host "Trovato main.py. Eseguendo con Python $versionToUse..."
        
        # Verifica ed esegui
        try {
            if ((py -$versionToUse --version 2>$null) -match "Python $versionToUse") {
                py -$versionToUse $mainScript
            } else {
                Write-Host "Fallback a comando generico..."
                py $mainScript
            }
        } catch {
            Write-Host "Tentativo con python..."
            python $mainScript
        }
    } else {
        Write-Host "main.py non trovato in: $scriptDir"
        
        # Debug: mostra file Python disponibili
        $pyFiles = Get-ChildItem -Path $scriptDir -Filter "*.py" -ErrorAction SilentlyContinue
        if ($pyFiles) {
            Write-Host "File Python disponibili: $($pyFiles.Name -join ', ')"
        } else {
            Write-Host "Nessun file Python trovato."
        }
    }
} else {
    Write-Host "ERRORE: Nessuna versione Python utilizzabile!"
}

Write-Host "`n=== COMPLETATO ==="
Write-Host "Premere un tasto per chiudere..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")