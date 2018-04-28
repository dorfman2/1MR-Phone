#!/usr/bin/env bash
set -e
set -x
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd ${DIR}
mkdir -p logs
source venv/bin/activate

python -u src/osc_server.py 2>&1 | tee -a logs/osc_server.log