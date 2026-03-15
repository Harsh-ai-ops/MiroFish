import os
import sys

# =====================================================================
# MEMORY OPTIMIZATION FOR RENDER FREE TIER (512MB RAM Limit)
# =====================================================================
# We eagerly import the heavily memory-consuming ML libraries (oasis, camel) 
# here in the WSGI entrypoint. 
# 
# Combined with Gunicorn's `--preload` flag, this forces the Master process 
# to load these ~400MB libraries into memory *before* forking the worker.
# Because Linux uses Copy-On-Write (COW) for forked processes, the worker 
# process will perfectly share this 400MB memory block with the Master,
# instead of duplicating it. 
# 
# Without this, the worker lazily imports them upon clicking "Start Simulation",
# which allocates a *new* 400MB inside the worker, pushing total container 
# memory to ~600MB and causing an instant OOM kill (502 Bad Gateway).
# =====================================================================
try:
    print("Preloading heavy ML libraries for memory sharing (COW)...")
    import camel
    import oasis
    print("Successfully preloaded ML libraries.")
except Exception as e:
    print(f"Warning: Failed to preload ML libraries: {e}")

from app import create_app

app = create_app()
