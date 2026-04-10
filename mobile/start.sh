#!/bin/bash
# Always run from the mobile/ directory regardless of where you call this from
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"
ulimit -n 65536
npm run lan
