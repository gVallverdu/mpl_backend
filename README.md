# mpl_backend

Helper function and a context manager to switch between backends in a Jupyter notebook.

## Rationale

The aim of this short project is to address the following use case in 
a jupyter notebook.

When working in a jupyter notebook with data and plots, one may need to
get two different kind of visualizations:

* an interactive figure, with capabilities to zoom in/out, pan ...
* a picture embedded in the notebook for further export it in pdf or html or other

This very short package provides two functions that help
switching between two different matplotlib backends depending on what
you need.

A standard workflow could be:

* use the `widget` backend for data exploration, region selection
* use the `inline` backend for a final figure production

## Documentation

The main concept is to switch between `widget` and `inline` backends in
the jupyter notebook. That can be achieve through an ipython magic command
with

```python
%matplotlib inline
plt.close('all')
plt.figure()
ax.plot(x, y)
# plt.show()

%matplotlib widget
plt.close('all')
plt.figure()
ax.plot(x, y)
plt.show()
```

### How to use the functions

The `mpl_use()` function is an helper function to switch the current notebook 
to the `widget` backend. You can also pass the name of the backend as argument
if you want to select another.
The function closes all figures before switching and the switch if done
only if the required backend is not already active.

```python
mpl_use()
plt.figure()
plt.plot(x, y)
plt.show()

mpl_use("inline")
plt.figure()
plt.plot(x, y)
plt.show()
```

The module provides also a context manager, in order to keep globaly the
`widget` backend active but to use locally the `inline` backend. It is not possible
to do the opposite, using globally the `inline` backend and use locally
the `widget` backend.

```ipython
# this figure will be an interactive widget
plt.figure()
plt.plot(x, y)
plt.show()

with mpl_inline_ctx():
    # this figure inline
    plt.figure()
    plt.plot(x, y)
```

### Caveats

1. Before switching from one backend to another, be sure to close all figures.

```python
plt.close("all")
```

2. While `inline` does not need the instruction `plt.show()`, it is highly 
  recommended to use it with the `widget` backend to force the process to end
  the figure production.


3. One figure needs one `plt.Figure` object. If not, the next plotting instructions
  will be added to the same first figure.

> [!TIP]
> 1 widget => 1 figure => 1 explicit call to plt.Figure() or plt.subplots() ...


## Installation / Configuration

Here is a quick start procedure. You need to install `ipympl` in the
environment you are using:

```bash
pip install ipympl

or

conda install -c conda-forge ipympl
```

You can the install the package or drop the function in a folder that is
convenient for you and accessible from you python environment.

```
pip install git+https://github.com/gVallverdu/mpl_backend.git
```

Use then the functions:

```python
from mpl_backend import mpl_use

mpl_use("widget")
plt.figure()
plt.plot(x, y)
plt.show()

from mpl_backend import mpl_inline_ctx

with mpl_inline_ctx():
    # this figure inline
    plt.figure()
    plt.plot(x, y)
    plt.show()
```

### Visula studio code

I use jupyter notebook in visual studio code. The widget works fine after
the installation of `ipympl`.

That lines may help if the
widgets does not appear. You have to add them in `settings.json`.

```json
"jupyter.widgetScriptSources": [
    "jsdelivr.com",
    "unpkg.com"
]
```


## Alternatives

One alternative, if available in the context of your project, is to use
a different python package that natively allows you to get interactive plots.
Among others, you can take a look at [plotly](https://plotly.com/python/) 
or [bokeh](https://bokeh.org).