# jupyter_manager

`jupyter_manager`: launch and manage Jupyter HPC jobs

`jupyter.py` controls the creation, deletion, and listing of `jupyter` server
sessions for the user, which are launched from the
[jupyter/minimal-notebook](https://quay.io/repository/jupyter/minimal-notebook)
container images.

Three subcommands are exposed to the user:

- `jupyter start`
  Launches an `jupyter` server session, returning the URL needed to connect

- `jupyter stop`
  Graceful shutdown of existing sessions

- `jupyter list`
  Lists the user's active sessions and their URLs
