#!/bin/bash

if (($# < 1)); then
    echo "Usage: $0 <binary_file>"
    exit 1
else
    echo "Finding DAPLink Device..."

    if [ ! -d "/media/$USER/DAPLINK" ]; then
        echo "DAPLink Device not found"
        exit 1
    else
        echo "DAPLink Device found"
        cp $1 "/media/$USER/DAPLINK"
    fi
fi
