#!/bin/bash
set -x

pids=()

# 为了确保能够清理后台子进程，我们设置trap来捕捉退出信号
#cleanup() {
#    echo "Cleaning up background tasks..."
#    kill -9 $(jobs -p) > log.txt 2>&1
#}
cleanup() {
    echo "Cleaning up background tasks..."
    for pid in "${pids[@]}"; do
        if kill -0 "$pid" 2>/dev/null; then
            kill -TERM "$pid" 2>/dev/null
        fi
    done
    wait
}
trap cleanup EXIT SIGINT SIGTERM

llama_server=/home/lizhen/test/code/llama.cpp/server
#llm_model_path=/home/lizhen/test/model_file/01-yi/Yi-34B-Chat/ggml-model-q4_0.gguf
llm_model_path=/home/lizhen/test/model_file/01-yi/01-yi-6b-chat/ggml-model-q4_0.gguf
gpu_ngl=0
threads=4
ctx_size=4096
split_mode=layer
port=9000
host=192.168.31.137
${llama_server} -m ${llm_model_path} -ngl ${gpu_ngl} -t ${threads} -c ${ctx_size} -sm ${split_mode} --port ${port} --host ${host} &
pids+=($!)

sleep 20

gunicorn -c gunicorn_conf.py llm_server:app &
#python llm_server.py &

pids+=($!)

sleep 5
echo -e "LLama server的pid: ""${pids[0]}"
echo -e "llm server的pid: ""${pids[1]}"

wait