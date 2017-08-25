#!/bin/bash
script_dir=$(dirname "$(readlink -f "$0" || greadlink -f "$0")")
export PYTHONPATH=$script_dir/../lib:$PATH:$PYTHONPATH
python -u $script_dir/../lib/kb_SetUtilities/kb_SetUtilitiesServer.py $1 $2 $3
