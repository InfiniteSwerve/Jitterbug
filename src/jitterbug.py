import timeit
import time
from typing import Any, Callable, Dict
import functools


class Jitterbug:
    # TODO: Make sure reporting accounts for any nested functions
    def __init__(self, slowdown: float):
        self.slowed_down: Dict[str, bool] = {}
        self.runtimes: dict[str, dict[str, float]] = {}
        self.call_hierarchy: dict[str, list[str]] = {}
        self.slowdown = slowdown

    def slow_down(self, func_name: str):
        self.slowed_down[func_name] = True

    def slow_down_all(self):
        self.slowed_down = {key: True for key in self.slowed_down.keys()}

    def speed_up(self, func_name: str):
        self.slowed_down = {key: True for key in self.slowed_down.keys()}
        self.slowed_down[func_name] = False

    def restore(self, func_name: str):
        self.slowed_down[func_name] = False

    def restore_all(self):
        self.slowed_down = {key: False for key in self.slowed_down.keys()}

    def jitterbug(self):
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            self.slowed_down[func.__name__] = False

            # gives the 'wrapper' function the same metadata as the passed function
            @functools.wraps(func)
            def wrapper(*args: Any, **kwargs: Any):
                start_time = timeit.default_timer()
                result = func(*args, **kwargs)
                end_time = timeit.default_timer()
                runtime = end_time - start_time
                # TODO: Better way to track runtime over many runs. How slow is appending to a list? What about in-place averaging?
                self.runtimes[func.__name__]["default"] = runtime
                if self.slowed_down[func.__name__]:
                    slowdown = runtime * self.slowdown
                    time.sleep(slowdown)
                return result

            return wrapper

        return decorator

    def record_runtimes(
        self, slowdown: float, main_func: Callable[..., Any], *args: Any, **kwargs: Any
    ):
        self.slowdown = slowdown  # percentage of function time we slow down a function
        runtimes: dict["str", float] = {}
        print(f"main func is {main_func.__name__}")
        for func_name in self.slowed_down.keys():
            if func_name == main_func.__name__:
                print(f"timing main function: {main_func.__name__}...")
                self.slow_down_all()
            else:
                print(f"speeding up {func_name}")
                self.speed_up(func_name)
            start_time = timeit.default_timer()
            main_func(*args, **kwargs)
            end_time = timeit.default_timer()
            runtimes[func_name] = end_time - start_time
            self.restore_all()
        return runtimes

    # Should return a dict of effects of speed ups on runtime
    # TODO: should include both forwards and backwards
    def process_runtimes(self, runtimes: dict["str", float]):
        for func_name in runtimes:
            speed_up = 1 / (1.0 + self.slowdown)
            # TODO: I'm really unsure if this is the number we want
            print(
                f"func name: {func_name} | speed up: {speed_up * 100}% | inferred runtime:{runtimes[func_name] * speed_up}"
            )

    # This should calculate the effect of optimizing the main_func itself, and all the funcs it calls, on the runtime of main_func.
    def estimate_effects(self, main_func: str, effectual_func: str):
        terms = self.call_hierarchy[main_func]
        for func in terms:
            self.slow_down(func)
        self.slow_down(effectual_func)

        overhead = runtimes[main_func]["default"] - sum(
            [runtimes[func_name]["default"] for func_name in terms]
        )
