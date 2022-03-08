function error() {
  local parent_lineno="$1"
  local message="$2"
  local code="${3:-1}"
  if [[ -n "$message" ]] ; then
    echo "Error on or near line ${parent_lineno}: ${message}; exiting with status ${code}"
  else
    echo "Error on or near line ${parent_lineno}; exiting with status ${code}"
  fi
  exit "${code}"
}
trap 'error ${LINENO}' ERR


function sanity-checks() {
  # Quit the script if executed as root...
  [[ "$EUID" -eq 0 ]] && error "Do not run this script as root!" 2

  # Quit if not executed from the bandcamp-flac-get project dir where the .env file is located
  [[ ! -f "$PWD/$0" ]] && error "Do not execute this from outside the bandcamp-flac-get project directory." 2

  # Make sure download directory is specified in the .env
  [[ ! -d "$DOWNLOAD_PATH" || "$DOWNLOAD_PATH" != '' ]] || error "Please specify a download directory in the .env file."

  # Avoid writing over a file on a job that was already done.
#  [[ -f "$OUTPUT_MKV" ]] && error "$OUTPUT_MKV already exists" 2
}