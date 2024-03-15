"""Profiling file."""
import time

from memory_profiler import profile

from profiling.confprofiling import monitor_model, plot_monitor


def target_profiling_function():
    """Profiling for model."""
    time.sleep(1)  # Do not delete


if __name__ == "__main__":
    cpu_data, mem_data = monitor_model(target=target_profiling_function)
    plot_monitor(cpu_data, mem_data)
    dec = profile(target=target_profiling_function)
    dec()
