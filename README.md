# SciPyCubicSpline
SciPyCubicSpline is a simple lightweight wrapper for SciPy's [CubicSpline](https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.CubicSpline.html). This wrapper simplifies the interpolation of coarse path data and allows the user to compute the path profile, such as curvature and yaw. It is approximately 300x faster than Atsushi Sakai's [PyCubicSpline](https://github.com/AtsushiSakai/pycubicspline). Look at [test.ipynb](test.ipynb) for more information.

### generate_cubic_spline
```yaml
:param x:               (list) x-coordinate of the coarse path [m]
:param y:               (list) y-coordinate of the coarse path [m]
:param ds:              (float) desired distance between each point [m], defaults to 0.05
:param bc_type:         (string) type of bounding condition, defaults to 'natural'

:return x:              (list) x-coordinate of the cubic spline path [m]
:return y:              (list) y-coordinate of the cubic spline path [m]
:return yaw:            (list) discrete yaw of the cubic spline path [rad]
:return curvature:      (list) discrete curvature of the cubic spline path [1/m]
```

### generate_cubic_spline
```yaml
:param x:               (list) x-coordinate of the coarse path [m]
:param y:               (list) y-coordinate of the coarse path [m]
:param ds:              (float) desired distance between each point [m], defaults to 0.05
:param bc_type:         (string) type of bounding condition, defaults to 'natural'

:return x:              (list) x-coordinate of the cubic spline path [m]
:return y:              (list) y-coordinate of the cubic spline path [m]
```

### calculate_spline_yaw
```yaml
:param x:               (list) x-coordinate of the coarse path [m]
:param y:               (list) y-coordinate of the coarse path [m]
:param ds:              (float) desired distance between each point [m], defaults to 0.05
:param bc_type:         (string) type of bounding condition, defaults to 'natural'

:return yaw:            (list) discrete yaw of the cubic spline path [rad]
```

### calculate_spline_curvature
```yaml
:param x:               (list) x-coordinate of the coarse path [m]
:param y:               (list) y-coordinate of the coarse path [m]
:param ds:              (float) desired distance between each point [m], defaults to 0.05
:param bc_type:         (string) type of bounding condition, defaults to 'natural'

:return curvature:      (list) discrete curvature of the cubic spline path [1/m]
```
