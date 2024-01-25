current_path=$(dirname $(readlink -f "$0"))
source $current_path/../.venv/bin/activate

uvicorn app.main:app --host 0.0.0.0 --port 5555 --workers 4
