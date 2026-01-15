import os

import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio


# Whether the frames of the animation should be saved.
# Warning: This takes an ungodly amount of time.
WRITE_FRAMES = False
# At what stride should the frames be sampled.
DSAMP_FRAMES = 5


def base_name(name):
    """
    Returns the base name from the name, e.g. 5 JUPITER BARYCENTER
    becomes JUPITER.

    :param name: The name of the celestial body in the csv.
    :returns: The extracted base name.
    """
    return name.upper().split()[1] if ' ' in name else name.upper()


def export_frames(fig, frames, out_dir='frames', scale=2):
    """
    Exports the frames into a seperate folder for further processing
    using ffmpeg.

    :param fig: The Plotly figure.
    :param frames: A list of Plotly frames.
    :param out_dir: The output directory for the generated frames.
    :param scale: The scale of the image.
    """
    os.makedirs(out_dir, exist_ok=True)

    for i, frame in enumerate(frames):
        fig.update(data=frame.data)
        fig.write_image(
            f'{out_dir}/frame_{i:04d}.png',
            scale=scale
        )

        
def visualize():
    """
    Runs the visualization process, reading the dataframe, extracting and
    processing the planet data into frames, and finally, showing the plot
    in the browser.
    """
    print('Reading dataframe')
    df = pd.read_csv("solar_system_positions_with_velocity.csv")
    df = df.sort_values(['name', 'date'])
    planets = df['name'].unique()
    dates = sorted(df['date'].unique())

    print('    Unique names:', len(planets))
    print('    Unique dates:', len(dates))
    
    PLANET_STYLE = {
        'SUN': dict(color='yellow', size=12),
        'MERCURY': dict(color='gray', size=4),
        'VENUS': dict(color='orange', size=6),
        'EARTH': dict(color='blue', size=6),
        'MOON': dict(color='blue', size=2),
        'MARS': dict(color='red', size=5),
        'JUPITER': dict(color='orange', size=10),
        'SATURN': dict(color='gold', size=9),
        'URANUS': dict(color='cyan', size=8),
        'NEPTUNE': dict(color='blue', size=8),
    }
    
    pio.templates.default = pio.templates['plotly_dark']
    
    print('Generating frames')
    positions = {
        planet: df[df['name'] == planet][['x_au', 'y_au', 'z_au']].to_numpy()
        for planet in planets
    }

    traces = []
    for planet in planets:
        planet_name = base_name(planet)
        style = PLANET_STYLE.get(planet_name, None)
        if style is None:
            style = dict(size=5)
        
        traces.append(go.Scatter3d(
            x=[positions[planet][0, 0]],
            y=[positions[planet][0, 1]],
            z=[positions[planet][0, 2]],
            mode='markers',
            marker=style,
            name=planet
        ))

    frames = []
    for i, date in enumerate(dates):
        frame_data = []
        for planet in planets:
            x0, y0, z0 = positions[planet][i]
            frame_data.append(dict(
                type='scatter3d',
                x=[x0],
                y=[y0],
                z=[z0]
            ))
        frames.append(go.Frame(data=frame_data, name=str(date)))

    slider_steps = [{
        'method': 'animate',
        'label': str(date),
        'args': [
            [str(date)],
            {
                'mode': 'immediate',
                'frame': {'duration': 0, 'redraw': True},
                'transition': {'duration': 0}
            }
        ],
    } for date in dates]
        
    fig = go.Figure(
        data=traces,
        frames=frames
    )

    fig.update_layout(
        scene=dict(
            aspectmode='data',
            xaxis=dict(title='AU'),
            yaxis=dict(title='AU'),
            zaxis=dict(title='AU'),
        ),
        font=dict(color='white'),
        updatemenus=[{
            'type': 'buttons',
            'buttons': [{
                'label': 'Play',
                'method': 'animate',
                'args': [None, {'frame': {'duration': 50}, 'fromcurrent': True}]
            },
            {
                'label': 'Reset',
                'method': 'animate',
                'args': [None, {'frame': {'duration': 0}, 'mode': 'immediate'}]
            },
            {
                'label': 'Pause',
                'method': 'animate',
                'args': [frames[0].name, {'frame': {'duration': 0}, 'mode': 'immediate'}]
            }]
        }],
        sliders=[{
            'active': 0,
            'pad': {'t': 50},
            'steps': slider_steps,
            'x': 0.1,
            'len': 0.8
        }]
    )

    if WRITE_FRAMES:
        print('Saving frames')
        # Downsample frames.
        d_frames = frames[::DSAMP_FRAMES]
        export_frames(fig, d_frames)
    
    fig.show()
    

def main():
    visualize()


if __name__ == "__main__":
    main()
