import copy
from typing import (
    Any,
    Counter,
    Dict,
    List,
    Optional,
    Tuple,
    Type,
    Mapping,
    Union,
    Iterable
)
from itertools import count
from mesa.model import Model
from functools import partial
from mesa.batchrunner import _model_run_func, _make_model_kwargs
from multiprocessing import Pool
import numpy as np
from tqdm import tqdm

def batch_run(
    model_cls: Type[Model],
    parameters: Mapping[str, Union[Any, Iterable[Any]]],
    number_processes: Optional[int] = None,
    iterations: int = 1,
    data_collection_period: int = -1,
    max_steps: int = 1000,
    display_progress: bool = True,
) -> List[Dict[str, Any]]:

    kwargs_list = _make_model_kwargs(parameters)
    kwargs_list = [copy.deepcopy(kwargs) for run in range(iterations * 2) for kwargs in kwargs_list]

    ss = np.random.SeedSequence()
    total_rng = len(kwargs_list) + 1
    seeds = ss.spawn(total_rng)

    for i in range(len(kwargs_list)):
        if(i >= len(kwargs_list) / 2):
            kwargs_list[i]['obstacle_free'] = True
        else:
            kwargs_list[i]['obstacle_free'] = False
        kwargs_list[i]['position_seed'] = seeds[-1]
        kwargs_list[i]['model_seed'] = seeds[i]

    process_func = partial(
        _model_run_func,
        model_cls,
        max_steps=max_steps,
        data_collection_period=data_collection_period,
    )

    total_iterations = len(kwargs_list) * iterations
    run_counter = count()

    results: List[Dict[str, Any]] = []

    with tqdm(total_iterations, disable=not display_progress) as pbar:
        if number_processes == 1:
            for iteration in range(iterations):
                for kwargs in kwargs_list:
                    _, rawdata = process_func(kwargs)
                    run_id = next(run_counter)
                    data = []
                    for run_data in rawdata:
                        out = {"RunId": run_id, "iteration": iteration - 1}
                        out.update(run_data)
                        data.append(out)
                    results.extend(data)
                    pbar.update()

        else:
            iteration_counter: Counter[Tuple[Any, ...]] = Counter()
            with Pool(number_processes) as p:
                for paramValues, rawdata in p.imap_unordered(process_func, kwargs_list):
                    iteration_counter[paramValues[0:4]] += 1
                    iteration = iteration_counter[paramValues[0:4]]
                    run_id = next(run_counter)
                    data = []
                    for run_data in rawdata:
                        out = {"RunId": run_id, "iteration": iteration - 1}
                        out.update(run_data)
                        data.append(out)
                    results.extend(data)
                    pbar.update()

    return results
