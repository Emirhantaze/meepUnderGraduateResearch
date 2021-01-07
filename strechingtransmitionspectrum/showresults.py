import numpy as np
import json
import matplotlib.pyplot as plt

f = open("./silvergoldpolimer.json")
data = json.load(f)

incident = data["EZ"]["Gold: 100.0%, Silver: 0.0%, Pdms: 0.0%"]["Spacing_0.5"]["Incident"]
tra = data["EZ"]["Gold: 100.0%, Silver: 0.0%, Pdms: 0.0%"]["Spacing_0.5"]["Reflected"]
w = data["Wavelengths"]
plt.plot(w, np.divide(tra, incident))
plt.show()
