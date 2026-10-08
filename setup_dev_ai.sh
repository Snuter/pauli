#!/bin/bash
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