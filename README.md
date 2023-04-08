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
    "map": """{
        rect 4 5, rect 12 8, rect 10 5 , rect 2 6, L 5 1 12 2, L -5 2 -7 2, L -18 2 -12 4,
        L 4 1 -5 1, L -6 1 6 2, rect 1 1, rect 3 4, rect 2 2, rect 2 2, rect 1 1, rect 2 4
     }""",
    'planner': GreedyPlanner(),
    'seed': 7
}
```
`map` can be a path to a png file or a pattern for generating maps randomly containing given shapes. Currently, rectangle and L shapes are available. The pattern includes a list of shapes separated with commas and surrounded between { }.<br>
- To add rectangle to the map use `rect` keyword followed by its height and width separated with spaces.<br>
- To add L shape to the map use `L` keyword followed by 4 numbers.<br>
    1. Lenght of the vertical bar of L. if a negative number is given, L shape will be flipped vertically
    2. thickness of vertical bar
    3. Lenght of the horizontal bar of L. if a negative number is given, L shape will be flipped horizontally
    4. thickness of horizontal bar
NOTE: models using maps from image file ignore width and height parameters and use image size instead. 

## Batch run
To run the model with different parameter sets, execute `batch_run.py`. Locate the desired maps folder using `--path` argument. Run `batch_run.py -h` for more information.
