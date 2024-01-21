
set -x

pids=()

# 为了确保能够清理后台子进程，我们设置trap来捕捉退出信号
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

root_path=$1

cd ${root_path}/WebServer
python web_server.py &
pids+=($!)

cd ${root_path}/ModelServer
bash start_llm_server.sh &
pids+=($!)

wait