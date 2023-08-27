from multiprocessing import get_context, Pool
from multiprocessing.pool import ThreadPool
import os
from typing import Optional

from mock_pool import MockPool

class MultiPool:

    def __init__(self, processes : Optional[int] =None, backend : str ="multiprocessing_spawn", never_mock: bool =False, **kwds):
        
        if processes is None:
            processes = os.cpu_count()

        if backend == "mock" or (processes == 1 and not never_mock):
            self.backend = MockPool()
        elif backend == "multiprocessing_spawn":
            self.backend = get_context("spawn").Pool(processes, **kwds)
        elif backend == "multiprocessing_fork":
            self.backend = get_context("fork").Pool(processes, **kwds)
        elif backend == "multiprocessing_forkserver":
            self.backend = get_context("forkserver").Pool(processes, **kwds)
        elif backend == "multiprocessing_default":
            self.backend = Pool(processes, **kwds)
        elif backend == "threads":
            self.backend = ThreadPool(processes, **kwds)
        else:
            raise ValueError("Illegal value for backend: " + str(backend))

    def __enter__(self):
        return self.backend.__enter__()
    
    def __exit__(self, *exc):
        return self.backend.__exit__(*exc)
    