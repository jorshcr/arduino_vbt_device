# Data pipeline figure

The figure documents the Python runtime implementation at commit `8c6756b45db64e805f58fc5c8c94de9cf32d0bde`. It is an architecture figure, not evidence of predictive accuracy or a validation study.

## Source mapping

| Figure component | Implementation |
| --- | --- |
| Sensor conversion, high-pass filtering, integration, serial CSV | `apexinitialcode_arduino.ino`: `HPF_filter`, `loop` |
| Startup model fitting | `apexbackend.py`: embedded `data`, `X`, `y`, `model.fit` |
| Serial parsing, speed magnitude, segmentation, stopping rules | `apexbackend.py`: `collect_data` |
| Feature vector, inference, analytics, results event | `apexbackend.py`: `X_new`, `model.predict`, `socketio.emit('results', ...)` |
| Load input, start/stop controls, live chart, result display | `apexfrontend.html`: fetch requests and Socket.IO handlers |

## Reading the figure

- The device uses USB serial at 115200 baud. BLE is part of the board name; it is not the implemented transport.
- The active filters are first-order high-pass filters with a 0.3 Hz cutoff. The sketch defines a low-pass function but never calls it. The high-pass stage suppresses DC/slow components; it is not a high-frequency noise filter.
- Filter coefficients assume 119 Hz. Integration uses elapsed microseconds between readings; the figure does not imply a measured, perfectly fixed sample rate.
- Rep windows use negative z velocity for the mounted sensor orientation. Only completed windows longer than 0.3 seconds are retained. Python computes per-rep statistics over `vt[start:end]`.
- Model inputs, in order, are `load_percent`, `mean_velocity_last_rep`, and `reps_completed`. Embedded `actual_RIR` values are training labels. Training happens at startup, and inference happens after recording, rather than once per live sample.
- Live data is emitted every five processed samples. Rep counts are emitted on accepted rep completion. The Socket.IO arrow summarizes these backend-to-browser events.
- Mean and peak speed arrays, velocity loss, and a fitted peak-speed trend are included in the final results event alongside RIR. The analytics box is a parallel output branch and is not a fourth model feature.
- The inactivity test examines the latest 476 samples once more than 476 samples exist. It stops if their speed range is below 0.1 m/s; “4 seconds” assumes 119 Hz. Recording also stops at the 70-second loop limit or a manual stop request.
- `VelocityDataCollection.m` is a separate MATLAB acquisition/analysis path. `quickdataacq.py` is an auxiliary formatter that emits `add_training_example(...)` text; it is not wired into the current backend. Neither is a required intermediate stage in this figure.
- The repository does not implement a held-out model-evaluation stage. No accuracy or generalization claim is implied.

## Rebuilding

Run `python docs/figures/render_data_pipeline.py` with Matplotlib installed. This regenerates the editable SVG and 220-dpi PNG beside the script. SVG text remains editable.
