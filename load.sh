#!/bin/bash

modules=("PCA9685" "drive" "RGBled" "detect")
main="robot.py"

CROSS="../micropython/mpy-cross/mpy-cross"
FIRMWARE="firmware.hex"


rm -r LOAD
mkdir LOAD

for module in "${modules[@]}"
do
    cp ${module}.py LOAD
    ${CROSS} LOAD/${module}.py
done

cp ${main} LOAD

cd LOAD
uflash --runtime ../${FIRMWARE} ${main}

sleep 2
for module in "${modules[@]}"
do
    echo "Loading ${module}"
    upload.py /dev/ttyACM0 ${module}.mpy
done

cd ..

