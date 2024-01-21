import os
import sys


env_dict = {}
with open("env.txt", "r", encoding="utf-8") as f_read:
    for data_line in f_read.readlines():
        data_split = data_line.strip("\n").split(":")
        env_dict[data_split[0]] = data_split[1]

bind = f"{env_dict['ip']}:{env_dict['port']}"
workers = int(env_dict["workers"])
threads = int(env_dict["threads"])
timeout = 300000
backlog = 10240
start_cuda_index = 0


def on_starting(server):
    """
    Attach a set of IDs that can be temporarily re-used.
    Used on reloads when each worker exists twice.
    """
    server._worker_id_overload = set()


def nworkers_changed(server, new_value, old_value):
    """
    Gets called on startup too.
    Set the current number of workers.  Required if we raise the worker count
    temporarily using TTIN because server.cfg.workers won't be updated and if
    one of those workers dies, we wouldn't know the ids go that far.
    """
    server._worker_id_current_workers = new_value


def _next_worker_id(server):
    """
    If there are IDs open for re-use, take one.  Else look for a free one.
    """
    if server._worker_id_overload:
        return server._worker_id_overload.pop()

    in_use = set(w._worker_id for w in server.WORKERS.values() if w.alive)
    free = set(range(1, server._worker_id_current_workers + 1)) - in_use

    return free.pop()


def on_reload(server):
    """
    Add a full set of ids into overload so it can be re-used once.
    """
    server._worker_id_overload = set(range(1, server.cfg.workers + 1))


def pre_fork(server, worker):
    """
    Attach the next free worker_id before forking off.
    """
    worker._worker_id = _next_worker_id(server)


def post_fork(server, worker):
    """
    Put the worker_id into an env variable for further use within the app.
    """
    os.environ["APP_WORKER_ID"] = str(worker._worker_id)
    gpu_index = worker._worker_id - 1 + start_cuda_index
    os.environ["CUDA_VISIBLE_DEVICES"] = f"{gpu_index}"

