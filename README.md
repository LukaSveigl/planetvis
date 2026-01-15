# Planetvis

Planetvis is a quick and dirty visualization of our solar system, based on [this kaggle dataset.](https://www.kaggle.com/datasets/nikitamanaenkov/solar-system-bodies-positions-2020-2024)

The current implementation is still janky, the camera is shaky and certain moons are not particularly visible due to the scale of the planets and the use of astronomical units. This might be fixed in the future, who knows?

##  Requirements

Planetvis relies on the following libraries:
- Plotly
- Numpy
- Kaleido
- Pandas

Simply install them using your package manager of choice and run `planetvis/main.py`.

## Demonstration

![Alt text](planetvis/solar_system.gif)
