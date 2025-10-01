#!/bin/bash

# Create simple placeholder icons for the add-on
# These are base64-encoded minimal PNG files

cd "$(dirname "$0")/bluetooth_manager"

echo "Creating placeholder icon files..."

# Create a simple 256x256 blue PNG icon (base64 encoded minimal PNG)
# This is a very simple 1x1 blue pixel that we'll claim is 256x256
cat > icon.png.b64 << 'EOF'
iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==
EOF

# Decode to create actual PNG
base64 -d icon.png.b64 > icon.png 2>/dev/null || base64 -D icon.png.b64 > icon.png 2>/dev/null
rm icon.png.b64

# Copy for logo
cp icon.png logo.png

echo "✓ Created icon.png and logo.png"
echo ""
echo "NOTE: These are minimal placeholder images (1x1 pixel)"
echo "For a proper add-on, replace these with actual Bluetooth-themed icons:"
echo "  - icon.png: 256x256 PNG"
echo "  - logo.png: 512x512 or larger PNG"
echo ""
echo "You can create proper icons using:"
echo "  - Figma, Canva, or other design tools"
echo "  - Free icon sources (flaticon.com, icons8.com, etc.)"
echo "  - AI image generators (DALL-E, Midjourney, etc.)"
echo ""
echo "Suggested search terms: 'bluetooth icon', 'wireless icon', 'connectivity icon'"
