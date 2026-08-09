#!/bin/bash
set -e

APP_NAME="Distant Realms Editor"
MAIN="main.py"
UPDATER_MAIN="updater.py"
UPDATER_NAME="updater"

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

DIST_ROOT="$ROOT/executable"
WORK_ROOT="$ROOT/build"
SPEC_ROOT="$ROOT/specs"

cleanup() {
  echo "Cleaning temporary build artifacts..."

  rm -rf "$WORK_ROOT"
  rm -rf "$SPEC_ROOT"
  rm -rf "$DIST_ROOT/linux_tmp"
  rm -rf "$DIST_ROOT/updater_tmp"

  echo "Cleanup complete."
}

trap cleanup EXIT

copy_assets() {
  local TARGET="$1"

  echo "ROOT=$ROOT"
  echo "TARGET=$TARGET"

  echo "Engine persistence source:"
  find "$ROOT/enginepersistence" -type f

  echo "Copying assets..."

  cp -r "$ROOT/assets" "$TARGET"
  cp -r "$ROOT/saves" "$TARGET"
  cp -r "$ROOT/environment" "$TARGET"
  cp -r "$ROOT/enginepersistence" "$TARGET"

  cp "$ROOT/changelog.txt" "$TARGET"
  cp "$ROOT/README.md" "$TARGET"
  cp "$ROOT/LICENSE" "$TARGET"
  cp "$ROOT/instructions.md" "$TARGET"

  echo "Creating logs/ directory..."
  mkdir -p "$TARGET/logs"

  echo "Setting build environment to production mode..."
  mkdir -p "$TARGET/environment"
  echo "false" > "$TARGET/environment/dev"
}

cleanup_internal() {
  local INTERNAL_DIR="$1/_internal"

  if [ -d "$INTERNAL_DIR" ]; then
    echo "Cleaning up _internal directory..."

    rm -rf "$INTERNAL_DIR/assets"
    rm -rf "$INTERNAL_DIR/logs"
    rm -rf "$INTERNAL_DIR/saves"
    rm -rf "$INTERNAL_DIR/environment"
  fi
}

build_main() {
  echo "========================================"
  echo "Building Linux game executable..."
  echo "========================================"

  local TMP_DIST="$DIST_ROOT/linux_tmp"
  local FINAL_DIST="$DIST_ROOT/DR_Editor_Linux"

  rm -rf "$TMP_DIST"
  rm -rf "$FINAL_DIST"

  mkdir -p "$TMP_DIST"
  mkdir -p "$WORK_ROOT/linux"
  mkdir -p "$SPEC_ROOT/linux"

  pyinstaller "$ROOT/$MAIN" \
    --onedir \
    --icon="$ROOT/assets/images/build/linux.png" \
    --noconsole \
    --windowed \
    --clean \
    --name "$APP_NAME" \
    --add-data "$ROOT/assets:assets" \
    --add-data "$ROOT/logs:logs" \
    --add-data "$ROOT/saves:saves" \
    --add-data "$ROOT/environment:environment" \
    --distpath "$TMP_DIST" \
    --workpath "$WORK_ROOT/linux" \
    --specpath "$SPEC_ROOT/linux" \
    --debug all

  mkdir -p "$FINAL_DIST"

  mv "$TMP_DIST/$APP_NAME"/* "$FINAL_DIST"/

  rm -rf "$TMP_DIST"

  copy_assets "$FINAL_DIST"
  cleanup_internal "$FINAL_DIST"

  echo "Main editor build complete."
}

build_updater() {
  echo "========================================"
  echo "Building Linux updater executable..."
  echo "========================================"

  local TMP_DIST="$DIST_ROOT/updater_tmp"
  local FINAL_DIST="$DIST_ROOT/linux"

  rm -rf "$TMP_DIST"

  mkdir -p "$TMP_DIST"
  mkdir -p "$FINAL_DIST"
  mkdir -p "$WORK_ROOT/updater"
  mkdir -p "$SPEC_ROOT/updater"

  pyinstaller "$ROOT/$UPDATER_MAIN" \
    --onefile \
    --console \
    --clean \
    --name "$UPDATER_NAME" \
    --distpath "$TMP_DIST" \
    --workpath "$WORK_ROOT/updater" \
    --specpath "$SPEC_ROOT/updater"

  mv "$TMP_DIST/$UPDATER_NAME" "$FINAL_DIST/$UPDATER_NAME"

  rm -rf "$TMP_DIST"

  echo "Updater build complete."
}

echo "========================================"
echo "Distant Realms Editor Linux Build"
echo "========================================"

rm -rf "$WORK_ROOT"
rm -rf "$SPEC_ROOT"

mkdir -p "$DIST_ROOT"

build_main
build_updater

echo
echo "========================================"
echo "Build completed successfully."
echo "========================================"
echo "Output:"
echo "  $DIST_ROOT/DR_Editor_Linux"
echo "  $DIST_ROOT/linux/updater"
