# Coverage-Path-planning
Implementation of multi-agent coverage path planning algorithms using Mesa framework

## Model parameters
Model parameters can be tuned in `server.py`:
```
model_params = {
    "width": width,
    "height": height,
    "robot_count": UserSettableParameter(
        "slider", "Robots Count", 8, 1, 50
    ),
    "path_to_map": 'cpp\maps\star.png',
    'seed': 7
}
```
