# Builds dist\AION2-pet-tracker.exe (one file, no console).
# Requires: python -m pip install -r requirements.txt
$ErrorActionPreference = "Stop"
$root = $PSScriptRoot

python -m PyInstaller --noconfirm --onefile --windowed `
    --name AION2-pet-tracker `
    --icon "$root\assets\icon.ico" `
    --add-data "$root\data\names.json;data" `
    --collect-submodules scapy `
    --collect-all winocr `
    --collect-all winrt `
    --distpath "$root\dist" `
    --workpath "$root\build" `
    --specpath "$root\build" `
    "$root\aion2_pet_tracker.py"

if ($LASTEXITCODE -ne 0) { throw "PyInstaller failed" }
Write-Host "Built: $root\dist\AION2-pet-tracker.exe"
