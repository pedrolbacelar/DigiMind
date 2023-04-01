# How to set the files
1. Files must be organized in the same way as in the submission folder
2. In the File 'ml_model.joblib' is saved the Machine Learning model that is necessary to run the program
3. The 'test.csv' file is needed to organize the next point that will be introduced in the ML model,
this is done automatically by the program
4. All jsons files must be inside the models folder, exactly as in the delivery folder
5. The 'mosquitto' folder is also needed to run the program


# DEMONSTRATION

## Steps to follow to run the simulation
1. Run Mosquitto
2. Run Digimind_app.py
3. Copy the base URL generated from the terminal output of Digimind_app.py
4. Run Digimind_main.py
5. Sign into MindSphere
6. Open Visual Flow Creator
7. Select the project named "DigiMind"
8. Under the comment titled 'user input', open "send part id" node which is a 'http requests' node.
9. Paste the URL generated by the Digimind_app.py into URL.
10. Attach the endpoint '/RCT_part' to the base url. (example: <base url>/<end point>)
11. Press 'Done' button to save the changes.
12. The timestamp node used to inject flow is turned to none to not waste the coputation time available for the tenant. Hence, it have to be turned on. For that, open 'timestamp' node.
13. Select the choice 'interval' from the drop down list available belonging to the 'Repeat' function.
14. Enter '10' as the value and 'seconds' as the time unit. This provides a dashboard refresh rate of 10 seconds.
15. Press 'Done' to save the changes in the node.
16. Press the 'Save' button to commit the changes of the 
17. Launch the dashboard
18. Enter the desired part id as an integer into the 'Enter part ID [INTEGER]' text box in the 'Request RCT Prediction' section in the top left corner.
19. Press 'TRACK MY PART' button to start tracking the part.
20. The tracking can be interupted manually by pressing "CANCEL TRACKING" button.

Take care:
1. Make sure the Digimind_app.py is running and the terminal is showing an active connection.
2. Make sure to update the base URL generated by the Digimind_app.py is updated in the "https requests" node in the dashboard. Error code for this is usually 404 (displayed in the 'request feedback' text box of the Dashboard)
3. Make sure the "Mosquitto" application for MQTT-server-broker is running.
4. Make sure the part id sent is an integer value.
5. Make sure the timestamp node in the VFC is set to a reasonable refresh rate.
6. When you load the dashboard and there is already some data, that means, the dashboard is fetching last know value.