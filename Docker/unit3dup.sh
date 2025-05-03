#!/bin/bash

# Parse parameters
while [[ $# -gt 0 ]]; do
    case "$1" in
        -u)
            u="$2"
            shift 2
            ;;
        -f)
            f="$2"
            shift 2
            ;;
        -scan)
            scan="$2"
            shift 2
            ;;
        -help)
            help=1
            shift
            ;;
        *)
            echo "Unknown parameter: $1"
            exit 1
            ;;
    esac
done

# Default -help
if [[ -z "$u" && -z "$f" && -z "$scan" && -z "$help" ]]; then
    echo "Usage: ./unit3dup.sh -u <path> -f <file> -scan <path> -help"
    exit 0
fi

# Only one flag at once
if { [[ -n "$u" && ( -n "$f" || -n "$scan" ) ]] || [[ -n "$f" && -n "$scan" ]]; }; then
    echo "Error: Only one flag can be used at a time"
    exit 1
fi

# [1] 
hostJsonPath="$HOME/Unit3Dup_config/"
DockerJsonPath="/home/parzival/Unit3Dup_config/"

# [2]
DockerDataPath="/home/parzival/data"
hostDataPath="/home/parzival/data"




# Check if JSON file exists
#if [[ ! -f "$hostJsonPath" ]]; then
#    echo "Error: configuration file not found : $hostJsonPath"
#    exit 1
#fi

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
read -p "Press ENTER to continue..."

# RUN
# -v mount
# -p qbittorrent host port 8080

docker run --rm \
    -u 1000:1000 \
    -v "${hostJsonPath}:${DockerJsonPath}" \
    -v "${hostDataPath}:${DockerDataPath}" \
    -p 8081:8080 \
    unit3dup $dockerFlags
