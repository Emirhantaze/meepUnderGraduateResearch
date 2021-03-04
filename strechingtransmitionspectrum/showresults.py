import numpy as np
import json
import matplotlib.pyplot as plt

f = open("./results.json")
data50 = json.load(f)
f.close()
f = open("./data.json")
data25 = json.load(f)
f.close()
f = open("./data1.json")
data75 = json.load(f)
f.close()

data25 = data50

incident = data25["EZ"]["Gold: 100.0%, Silver: 0.0%, Pdms: 0.0%"]["Spacing_0.5"]["Incident"]
ez = data25["EZ"]["Gold: 100.0%, Silver: 0.0%, Pdms: 0.0%"]["Spacing_0.5"]["Transmission"]
ey = data25["EY"]["Gold: 100.0%, Silver: 0.0%, Pdms: 0.0%"]["Spacing_0.5"]["Transmission"]
w = data25["Wavelengths"]
plt.plot(w, (np.divide(ey, incident)**2) /
         (np.divide(ez, incident)**2), label="Gold 100%, Silver 0%")

incident = data25["EZ"]["Gold: 80.0%, Silver: 20.0%, Pdms: 0.0%"]["Spacing_0.5"]["Incident"]
ez = data25["EZ"]["Gold: 80.0%, Silver: 20.0%, Pdms: 0.0%"]["Spacing_0.5"]["Transmission"]
ey = data25["EY"]["Gold: 80.0%, Silver: 20.0%, Pdms: 0.0%"]["Spacing_0.5"]["Transmission"]


w = data25["Wavelengths"]
plt.plot(w,  (np.divide(ey, incident)**2) /
         (np.divide(ez, incident)**2), label="Gold 80%, Silver 20%")

incident = data25["EZ"]["Gold: 60.0%, Silver: 40.0%, Pdms: 0.0%"]["Spacing_0.5"]["Incident"]
ez = data25["EZ"]["Gold: 60.0%, Silver: 40.0%, Pdms: 0.0%"]["Spacing_0.5"]["Transmission"]
ey = data25["EY"]["Gold: 60.0%, Silver: 40.0%, Pdms: 0.0%"]["Spacing_0.5"]["Transmission"]

w = data25["Wavelengths"]
plt.plot(w,  (np.divide(ey, incident)**2) /
         (np.divide(ez, incident)**2), label="Gold 60%, Silver 40%")

incident = data25["EZ"]["Gold: 40.0%, Silver: 60.0%, Pdms: 0.0%"]["Spacing_0.5"]["Incident"]
ez = data25["EZ"]["Gold: 40.0%, Silver: 60.0%, Pdms: 0.0%"]["Spacing_0.5"]["Transmission"]
ey = data25["EZ"]["Gold: 40.0%, Silver: 60.0%, Pdms: 0.0%"]["Spacing_0.5"]["Transmission"]

w = data25["Wavelengths"]
plt.plot(w,  (np.divide(ey, incident)**2) /
         (np.divide(ez, incident)**2), label="Gold 40%, Silver 60%")

incident = data25["EZ"]["Gold: 20.0%, Silver: 80.0%, Pdms: 0.0%"]["Spacing_0.5"]["Incident"]
ey = data25["EY"]["Gold: 20.0%, Silver: 80.0%, Pdms: 0.0%"]["Spacing_0.5"]["Transmission"]
ez = data25["EZ"]["Gold: 20.0%, Silver: 80.0%, Pdms: 0.0%"]["Spacing_0.5"]["Transmission"]

w = data25["Wavelengths"]
plt.plot(w, (np.divide(ey, incident)**2) /
         (np.divide(ez, incident)**2), label="Gold 20%, Silver 80%")

incident = data25["EZ"]["Gold: 0.0%, Silver: 100.0%, Pdms: 0.0%"]["Spacing_0.5"]["Incident"]
ey = data25["EY"]["Gold: 0.0%, Silver: 100.0%, Pdms: 0.0%"]["Spacing_0.5"]["Transmission"]
ez = data25["EZ"]["Gold: 0.0%, Silver: 100.0%, Pdms: 0.0%"]["Spacing_0.5"]["Transmission"]

w = data25["Wavelengths"]
plt.plot(w,  (np.divide(ey, incident)**2) /
         (np.divide(ez, incident)**2), label="Gold 0%, Silver 100%")
plt.legend()
plt.show()
