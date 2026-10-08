#!/bin/bash
# DEV-ONLY setup for working ON this project (coding agent + its local model).
# NOT used by the P.A.U.L.I. app at runtime. In particular the app never uses
# the `ollama launch opencode` harness below. The app talks directly to
# user-configured Ollama (local or cloud) models
# (see docs/concept-technical.md §7, README.md).
# stop on errors
set -e

MODEL="qwen3.8:27b"

echo ">>>>>>>>>>>>>>>>>>>>>>>> ollama setup <<<<<<<<<<<<<<<<<<<<<<<<<"

if [ -x /usr/bin/zstd ]; then
    echo "reusing already installed zstd"
else
    sudo apt-get install zstd
fi

if [ -x /usr/local/bin/ollama ]; then
    echo "reusing already installed ollama"
else
    curl -fsSL https://ollama.com/install.sh | bash
fi

echo ">>>>>>>>>>>>>>>>>>>>>>> AI model setup <<<<<<<<<<<<<<<<<<<<<<<<"
sleep 5s # ollama server takes a while to start
ollama pull $MODEL

echo ">>>>>>>>>>>>>>>>>>>>>>> opencode setup <<<<<<<<<<<<<<<<<<<<<<<<"
# remove old settings
rm -rf  ~/.local/state/opencode

if [ -x ~/.opencode/bin/opencode ]; then
    echo "reusing already installed opencode"
else
    # install
    curl -fsSL https://opencode.ai/v2/install | bash
fi

# configure opencode for ollama
ollama launch opencode --model $MODEL