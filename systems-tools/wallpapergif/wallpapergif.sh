#!/bin/sh
 
#================================================#
# Simple script for animated wallpaper in feh. V2
# Creator: jgtux (Joao G.)
#================================================#

# PATH OF THE GIF
GIF_PATH="${HOME}/my.gif"

# FPS
FPS=144

# DELAY
DELAY=0.010

# #BACKGROUND (OPTIONS: center, max, scale, fill, tile )
BG_OPTION=""
BG="--bg-${BG_OPTION}"

# EXTRACTS IMAGES
FRAMES_PATH=$(mktemp -d /tmp/wp-frames.XXXXXX)
ffmpeg -i "${GIF_PATH}" -vf "fps=${FPS}" "${FRAMES_PATH}/%d.png"

# COUNT TOTAL FRAMES 
TOTALFRAMES=$(ls -1 "${FRAMES_PATH}"/*.png | wc -l)
TOTALFRAMES=$((TOTALFRAMES - 1)) # INDEX 0 BASED 


type feh >/dev/null 2>&1 || { echo "You need feh!"; exit 1; }
f="feh --no-fehbg ${BG}"

cleanup() {
    rm -rf "$FRAMES_PATH"
    exit
}
trap cleanup INT TERM EXIT

i=0
while true; do
    feh --no-fehbg --bg-${BG_OPTION} "${FRAMES_PATH}/${i}.png"
    sleep "$DELAY"
    i=$((i + 1))
    if [ "$i" -gt "$TOTALFRAMES" ]; then
        i=0
    fi
done

