#!/usr/bin/env bash
# Build script for creating multi-architecture Docker images

set -e

# Configuration
IMAGE_NAME="bluetooth-manager"
REPOSITORY="ghcr.io/burhanyldz"
VERSION=$(grep '"version"' config.json | cut -d'"' -f4)

echo "Building Bluetooth Manager v${VERSION}"
echo "Repository: ${REPOSITORY}/${IMAGE_NAME}"

# Supported architectures
ARCHS=("amd64" "armv7" "aarch64")

# Build for each architecture
for ARCH in "${ARCHS[@]}"; do
    echo ""
    echo "Building for ${ARCH}..."
    
    docker build \
        --build-arg BUILD_FROM="ghcr.io/home-assistant/${ARCH}-base:latest" \
        --tag "${REPOSITORY}/${IMAGE_NAME}-${ARCH}:${VERSION}" \
        --tag "${REPOSITORY}/${IMAGE_NAME}-${ARCH}:latest" \
        .
    
    echo "✓ Built ${ARCH}"
done

echo ""
echo "Build complete!"
echo ""
echo "To push images, run:"
echo "  docker push ${REPOSITORY}/${IMAGE_NAME}-<arch>:${VERSION}"
echo "  docker push ${REPOSITORY}/${IMAGE_NAME}-<arch>:latest"
