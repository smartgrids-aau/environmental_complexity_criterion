from typing import (
    Any,
    Counter,
    Dict,
    List,
    Optional,
    Tuple,
    Type,
)
from itertools import count
from mesa.model import Model
from functools import partial
from mesa.batchrunner import _model_run_func
from multiprocessing import Pool
from tqdm import tqdm

def batch_run(
    model_cls: Type[Model],
    parameters: List[Dict[str, Any]],
    number_processes: Optional[int] = None,
    data_collection_period: int = -1,
    max_steps: int = 1000,
    display_progress: bool = True,
) -> List[Dict[str, Any]]:

    process_func = partial(
        _model_run_func,
        model_cls,
        max_steps=max_steps,
        data_collection_period=data_collection_period,
    )

    total_iterations = len(parameters)
    run_counter = count()

    results: List[Dict[str, Any]] = []

    with tqdm(total_iterations, disable=not display_progress) as pbar:
        if number_processes == 1:
            for kwargs in parameters:
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
                for paramValues, rawdata in p.imap_unordered(process_func, parameters):
                    iteration_counter[paramValues] += 1
                    iteration = iteration_counter[paramValues]
                    run_id = next(run_counter)
                    data = []
                    for run_data in rawdata:
                        out = {"RunId": run_id, "iteration": iteration - 1}
                        out.update(run_data)
                        data.append(out)
                    results.extend(data)
                    pbar.update()

    return results

