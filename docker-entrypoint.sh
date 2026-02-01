#!/bin/sh
echo "[BOOT] Fixing permissions for uploads + model caches..."

chown -R appuser:appuser \
  /app/uploads \
  /app/.easyocr \
  /app/.models \
  2>/dev/null || true

exec "$@"
