param (
    [string]$u,       # Add subparam
    [string]$f,
    [string]$scan,
    [string]$help
)

# Default -help
if (-not $u -and -not $f -and -not $scan -and -not $help) {
    Write-Host "Usage: .\unit3dup.ps1 -u <path> -f <file> -scan <path> -help"
}

# Only one flag at once
if (($u -and ($f -or $scan)) -or ($f -and $scan)) {
    Write-Host "Error: Only one flag can be used at a time"
    exit 1
}

# [HOST] mounts : EDITABLE
$hostJsonPath = "C:\Users\PC\AppData\Local\Unit3Dup_config\Unit3Dbot.json"
$hostDataPath = "C:\vm_share"

# [DOCKER] mounts : NOT Editable
$DockerDataPath = "/home/me/"
$DockerJsonPath = "/home/me/Unit3Dup_config/Unit3Dbot.json"

# Verifica se il file JSON esiste
if (-not (Test-Path $hostJsonPath)) {
    Write-Host "Errore: configuration file not found : $hostJsonPath"
    exit 1
}

# Host <--> Docker
Write-Host "[mount] $hostJsonPath -> $DockerJsonPath"
Write-Host "[mount] $hostDataPath -> $DockerDataPath"

# Docker "run string"
$dockerFlags = ""

# flag -u and subparam
if ($u) {
    $dockerFlags = "-u $([System.IO.Path]::Combine($DockerDataPath, $u))"

}

# flag -f and subparam
if ($f) {
    $dockerFlags = " -f $([System.IO.Path]::Combine($DockerDataPath, $f))"
}

# flag -scan and subparam
if ($scan) {
    $dockerFlags = " -scan $([System.IO.Path]::Combine($DockerDataPath, $scan))"
}

Write-Host $dockerFlags
Write-Host $hostDataPath,$DockerDataPath
pause

# RUN
# -v mount
# -p qbittorrent host port 8080
docker run --rm `
    -v "${hostJsonPath}:${DockerJsonPath}" `
    -v "${hostDataPath}:${DockerDataPath}" `
    -p 8081:8080 `
    unit3dup $dockerFlags