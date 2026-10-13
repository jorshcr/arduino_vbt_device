# Apex-RIR-Prediction
This project utilizes the IMU embedded on an Arduino Nano BLE Sense 33 to collect and segment rep data from an exercise in real time, which is then used to predict the reps in reserve (failure proximity) of the user. 

## Data pipeline

![Research-style diagram of the Arduino VBT data pipeline](docs/figures/data-pipeline.svg)

**Figure 1.** On-device acceleration filtering and integration produce a serial velocity stream. The Python backend segments concentric repetitions and builds a three-input feature vector for a random forest fitted at startup. The browser displays live motion and post-set RIR estimates. Velocity loss and peak-speed trends are display analytics, not model inputs.

[Download PNG](docs/figures/data-pipeline.png) · [Figure details and source mapping](docs/data-pipeline.md)

This System includes the following code:

1. Arduino Code - Collects real time Acceleration data using IMU, applies a 1st order High Pass Filter to cancel out drift, calculates Velocity by integrating Acceleration with time, applies the filter once again, then streams Velocity data to MATLAB
2. Backend Code - (Built off of previous MATLAB code), Reads real-time serial data from the Arduino, detects reps in their concentric phase (weight going up), and extracts features based on data of each rep "window", then extracts set features to be used in the model. The backend also includes all of the ML model training and functions within it, so that the features are directly inputted into the model. Simultaneously, the back end streams live velocity to a chart in the front end, sends the RIR prediction, and plots the final set graph.

System Flow: Gym Weightstack -> Arduino Nano IMU -> Backend -> Python Random Forest Model -> RIR Prediction -> Front End HTML Interface

Tech Stack Pipeline: Arduino Code Streams Real-time Velocity -> Frontend Takes User Input (Load %) -> Backend Captures and Plots Data + Rep Tracking -> Backend Trains/Runs Temp Model -> Backend Predicts RIR based on Set Data -> Frontend Displays Predictions, Analytics, and Insights

Hardware Requirements:
Arduino Nano BLE Sense 33
Arduino Container + Adhesive (Alien Tape Preferred)
USB Cable + Extension (if needed)
Laptop

Use Guide:
1. Place Arduino in Container and Alien Tape around it, Place it ontop of Weight Stack
2. Plug in Arduino and upload Apexarduino code
3. Run the apexbackend file in VSCODE 
4. Open the apexfrontend html file (This should open up the interface in your browser)
5. For your desired set, input your load percent.
    Formula: (Current Weight of this excercise and machine / 1RM on this excercise and machine) * 100
6. Press START, and continue the set. Velocity data of your reps will be plotted in real time.
7. Once completed, the code will stop automatically, provide RIR estimation and give further analytics.

