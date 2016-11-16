#!/bin/bash

sudo touch /dev/rtbuzzer0
sudo chmod 666 /dev/rtbuzzer0
echo "0 0 0 0" | sudo tee /dev/rtlightsensor0
sudo chmod 666 /dev/rtlightsensor0
