#! /bin/bash

################################################################################
# Jupyter SLURM job submission template
################################################################################
# Environmental variables available via SLURM:
#     JUPYTER_SIF: singularity .sif image location
#     BIND_PATHS: (can be blank) additional bind paths for singularity
################################################################################

################################################################################
# Functions
################################################################################

# Trap function to end the process from scancel/timeout
cancel() {
    # Pass SIGTERM to allow graceful shutdown
    if [[ -n "${JUPYTER_PID}" ]]; then
        kill -SIGTERM ${JUPYTER_PID}
    fi
    sleep 10
}

# Trap function to handle job teardown
cleanup() {
    # Clean up temporary directories
    rm -rf ${SESSION_TMP} \
    && exit 0
}

# Retrieve an unused port from the OS, restricted to a given range
freeport() {
    comm -23 \
        <(seq 44000 44099) \
        <(ss -Htan | awk '{gsub(/.*:/, "", $4); print $4}' | sort -u) \
    | shuf \
    | head -1
}

################################################################################
# Setup the execution environment
################################################################################

module load singularityce

# Acquire an available port from the OS
IP=$(hostname -i)
PORT=$(freeport)
echo "${IP}:${PORT}"

# Create temporary working area within scratch
SESSION_TMP="${TMPDIR}/jupyter_${SLURM_JOB_ID}"
mkdir -p ${SESSION_TMP}

# Prevent OpenMP over-allocation
export OMP_NUM_THREADS=${SLURM_CPUS_ON_NODE}

################################################################################
# Launch Jupyter
################################################################################

# Wrapped with the signal and exit traps ...
trap cancel SIGTERM
trap cleanup EXIT
# ... start the containerised Jupyter Server
singularity exec \
    --bind "${SESSION_TMP}:/tmp" \
    --bind "/opt/resources" \
    $([[ -n "${BIND_PATHS}" ]] && echo "--bind ${BIND_PATHS}") \
    $([[ $(hostname) == gpu* ]] && echo "--nv") \
    "${JUPYTER_SIF}" \
    jupyter-lab \
       --no-browser \
       --ip ${IP} \
       --port ${PORT} \
       --ServerApp.token '' &

JUPYTER_PID=$!
wait ${JUPYTER_PID}
