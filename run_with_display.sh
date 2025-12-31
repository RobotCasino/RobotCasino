#!/bin/bash
# Script to run the YouTube automation with X11 display from WSL to Windows

# Set DISPLAY to Windows host
# Get Windows host IP from WSL
export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0.0

echo "DISPLAY set to: $DISPLAY"
echo "Make sure xLaunch/VcXsrv is running on Windows with:"
echo "  - Multiple windows"
echo "  - Display number: 0"
echo "  - 'Disable access control' checked"
echo ""

# Run the Python script
python youtube_automation.py
