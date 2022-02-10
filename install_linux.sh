function loadenv() {
# Check if .env file exists; initialize one if not.
  if [[ ! -f ".env" ]]; then
    touch .env;
    echo "Initializing .env file, which can be used for configuration."
    echo "DOWNLOAD_PATH=$HOME" >> .env;
    echo "CHROME_BINARY=$(which google-chrome || which chromium-browser || which chromium || which chrome)" >> .env;
    echo "Please adjust these paths values if they are not your needed paths."
  fi
  source .env
}

echo "$0"

if [[ "$(realpath "$0")" == "$(realpath ./install_linux.sh)" ]]; then
  loadenv
fi