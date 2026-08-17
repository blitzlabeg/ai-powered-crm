#!/usr/bin/env bash
# =============================================================================
#  ai-powered-crm - macOS startup script
#  Double-click this file in Finder to set up and launch the application.
#
#  If macOS refuses to run it the first time (Gatekeeper warning), right-click
#  the file, choose "Open", then click "Open" again in the dialog that appears.
#  You only need to do that once.
# =============================================================================

set -u
cd "$(dirname "$0")"

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
RESET='\033[0m'

info()  { echo -e "${GREEN}==>${RESET} $1"; }
warn()  { echo -e "${YELLOW}[WARNING]${RESET} $1"; }
fail()  {
  echo ""
  echo -e "${RED}[ERROR]${RESET} $1"
  echo ""
  echo "-----------------------------------------------------------"
  echo " Something went wrong. Read the message above for details."
  echo " This window will stay open. Press Enter to close it."
  echo "-----------------------------------------------------------"
  read -r
  exit 1
}

echo ""
echo "=========================================================="
echo "  ai-powered-crm  -  AI-Powered CRM"
echo "=========================================================="
echo ""

# ---------------------------------------------------------------------------
# 1. Check whether Python is installed
# ---------------------------------------------------------------------------
info "[1/6] Checking for Python..."
if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN="python"
else
  fail "Python was not found on your system.

Please install Python 3.11 or newer from:
  https://www.python.org/downloads/

Then double-click this file again."
fi
PY_VERSION="$("$PYTHON_BIN" --version 2>&1)"
info "      Found $PY_VERSION"

# ---------------------------------------------------------------------------
# 2. Create the virtual environment if it doesn't exist yet
# ---------------------------------------------------------------------------
info "[2/6] Checking for virtual environment..."
if [ ! -f ".venv/bin/activate" ]; then
  info "      Creating virtual environment in .venv ..."
  "$PYTHON_BIN" -m venv .venv || fail "Failed to create the virtual environment."
  info "      Virtual environment created."
else
  info "      Virtual environment already exists."
fi

# ---------------------------------------------------------------------------
# 3. Activate the virtual environment
# ---------------------------------------------------------------------------
info "[3/6] Activating virtual environment..."
# shellcheck disable=SC1091
source ".venv/bin/activate" || fail "Failed to activate the virtual environment."
info "      Activated."

# ---------------------------------------------------------------------------
# 4. Install / verify dependencies
# ---------------------------------------------------------------------------
info "[4/6] Installing dependencies from requirements.txt..."
info "      (this may take a minute the first time)"
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet || fail "Failed to install dependencies. Check your internet connection and try again."
info "      Dependencies OK."

# ---------------------------------------------------------------------------
# 5. Verify the .env file
# ---------------------------------------------------------------------------
info "[5/6] Checking for .env configuration file..."
if [ ! -f ".env" ]; then
  if [ -f ".env.example" ]; then
    info "      No .env file found - creating one from .env.example ..."
    cp ".env.example" ".env"
    info "      Created .env with default settings."
    warn "      Edit .env and add your OPENAI_API_KEY to enable AI features."
  else
    warn "      No .env or .env.example file found. The app will run with built-in defaults."
  fi
else
  info "      .env file found."
fi

# ---------------------------------------------------------------------------
# 6. Launch the application
# ---------------------------------------------------------------------------
info "[6/6] Starting ai-powered-crm..."
echo ""
echo "=========================================================="
echo "  The app will open at:  http://127.0.0.1:8000"
echo "  Press CTRL+C in this window to stop the server."
echo "=========================================================="
echo ""

( sleep 2 && open "http://127.0.0.1:8000" ) &

uvicorn app.main:app --host 127.0.0.1 --port 8000
STATUS=$?

if [ $STATUS -ne 0 ]; then
  fail "The application exited with an error. See the messages above for details."
fi
