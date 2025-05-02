#!/bin/bash

# Parse parameters
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -u) u="$2"; shift ;;
        -f) f="$2"; shift ;;
        -scan) scan="$2"; shift ;;
        -help) help="true" ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

# Default -help
if [[ -z "$u" && -z "$f" && -z "$scan" && -z "$help" ]]; then
    echo "Usage: ./unit3dup.sh -u <path> -f <file> -scan <path> -help"
fi

# Only one flag at once
if { [[ -n "$u" ]] && { [[ -n "$f" ]] || [[ -n "$scan" ]]; }; } || { [[ -n "$f" ]] && [[ -n "$scan" ]]; }; then
    echo "Error: Only one flag can be used at a time"
    exit 1
fi

# [HOST] mounts : EDITABLE
hostJsonPath="$HOME/AppData/Local/Unit3Dup_config/Unit3Dbot.json"
hostDataPath="c:/vm_share"

# [DOCKER] mounts : NOT Editable
DockerDataPath="/home/me/"
DockerJsonPath="/home/me/Unit3Dup_config/Unit3Dbot.json"

# Check if JSON file exists
if [[ ! -f "$hostJsonPath" ]]; then
    echo "Errore: configuration file not found : $hostJsonPath"
    exit 1
fi

# Host <--> Docker
echo "[mount] $hostJsonPath -> $DockerJsonPath"
echo "[mount] $hostDataPath -> $DockerDataPath"

# Docker "run string"
dockerFlags=""

# flag -u and subparam
if [[ -n "$u" ]]; then
    dockerFlags="-u ${DockerDataPath}${u}"
fi

# flag -f and subparam
if [[ -n "$f" ]]; then
    dockerFlags="-f ${DockerDataPath}${f}"
fi

# flag -scan and subparam
if [[ -n "$scan" ]]; then
    dockerFlags="-scan ${DockerDataPath}${scan}"
fi

echo "$dockerFlags"
echo "$hostDataPath, $DockerDataPath"
read -p "Press any key to continue..."

# RUN
# -v mount
# -p qbittorrent host port 8080
docker run --rm \
    -v "${hostJsonPath}:${DockerJsonPath}" \
    -v "${hostDataPath}:${DockerDataPath}" \
    -p 8081:8080 \
    unit3dup $dockerFlags
