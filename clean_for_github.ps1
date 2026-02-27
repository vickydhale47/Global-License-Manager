# ===============================================================
#  GLOBAL LICENSE MANAGER - SAFE GITHUB CLEANUP SCRIPT
#  Author  : Vicky Dhale
#  Version : 1.0.0
#  Purpose : Remove build artifacts before publishing to GitHub
# ===============================================================

Clear-Host

# -------------------- HEADER --------------------
Write-Host ""
Write-Host "==============================================================" -ForegroundColor Cyan
Write-Host "        GLOBAL LICENSE MANAGER - GITHUB CLEANUP TOOL         " -ForegroundColor Cyan
Write-Host "==============================================================" -ForegroundColor Cyan
Write-Host ""

# -------------------- CONFIRMATION --------------------
$confirm = Read-Host "Proceed with cleanup? Type YES to continue"
if ($confirm -ne "YES") {
    Write-Host "Cleanup cancelled." -ForegroundColor Red
    exit
}

Write-Host ""
Write-Host "Cleaning build artifacts..." -ForegroundColor Yellow
Write-Host ""

# -------------------- FOLDERS TO DELETE --------------------
$foldersToDelete = @(
    "dist",
    "build",
    "__pycache__",
    "logs"
)

foreach ($folder in $foldersToDelete) {
    if (Test-Path $folder -PathType Container) {
        Remove-Item $folder -Recurse -Force
        Write-Host "Removed folder: $folder" -ForegroundColor Green
    }
}

# -------------------- FILE PATTERNS TO DELETE --------------------
$filePatterns = @(
    "*.spec",
    "*.log",
    "license_engine.log",
    "license_report_*.txt",
    "error_log.txt"
)

foreach ($pattern in $filePatterns) {
    Get-ChildItem -Path . -Filter $pattern -File -ErrorAction SilentlyContinue | ForEach-Object {
        Remove-Item $_.FullName -Force
        Write-Host "Removed file: $($_.Name)" -ForegroundColor Green
    }
}

# -------------------- SUMMARY --------------------
Write-Host ""
Write-Host "Remaining files in project root:" -ForegroundColor Cyan
Write-Host "--------------------------------------------------------------"

Get-ChildItem | ForEach-Object {
    if ($_.PSIsContainer) {
        Write-Host "[Folder] $($_.Name)" -ForegroundColor Green
    }
    else {
        Write-Host "[File]   $($_.Name)" -ForegroundColor White
    }
}

# -------------------- FOOTER --------------------
Write-Host ""
Write-Host "==============================================================" -ForegroundColor DarkGray
Write-Host "Cleanup completed successfully." -ForegroundColor Green
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Magenta
Write-Host "  git init"
Write-Host "  git add ."
Write-Host '  git commit -m "Initial clean commit - Global License Manager v1.0.0"'
Write-Host "  git remote add origin https://github.com/vickydhale/global-license-manager.git"
Write-Host "  git push -u origin main"
Write-Host "==============================================================" -ForegroundColor DarkGray
Write-Host ""

Read-Host "Press Enter to exit"