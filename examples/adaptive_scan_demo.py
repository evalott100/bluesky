import matplotlib.pyplot as plt

from bluesky import RunEngine, Mover, SynGauss
from bluesky.examples import adaptive_scan


RE = RunEngine()
RE.verbose = False
motor = Mover('motor', ['pos'])
det = SynGauss('sg', motor, 'pos', center=0, Imax=1, sigma=1)


def live_scalar_plotter(ax, y, x):
    x_data, y_data = [], []
    line, = ax.plot([], [], 'ro', markersize=10)

    def update_plot(doc):
        # Update with the latest data.
        x_data.append(doc['data'][x])
        y_data.append(doc['data'][y])
        line.set_data(x_data, y_data)
        # Rescale and redraw.
        ax.relim(visible_only=True)
        ax.autoscale_view(tight=True)
        ax.figure.canvas.draw()
        ax.figure.canvas.flush_events()

    return update_plot

fig, ax = plt.subplots()
plt.show()
ax.set_xlim([-15, 5])
ax.set_ylim([0, 2])
# Point the function to our axes above, and specify what to plot.
my_plotter = live_scalar_plotter(ax, 'intensity', 'pos')
ad_scan = adaptive_scan(motor, det, 'pos', 'intensity', -15, 5, .01, 1, .05)
RE.run(ad_scan, subscriptions={'event': my_plotter})
