import os
import socket


def is_running_in_container():
    """
    Check if the code is running inside a container (e.g., Docker, Kubernetes).

    Returns:
        bool: True if running in a container, False otherwise.
    """
    try:
        if os.path.exists('/.dockerenv'):
            return True
        if os.path.exists('/run/.containerenv'):
            return True
        with open('/proc/1/cgroup', 'r') as f:
            if any("docker" in line or "kubepods" in line for line in f):
                return True
        return False
    except Exception:
        return False
