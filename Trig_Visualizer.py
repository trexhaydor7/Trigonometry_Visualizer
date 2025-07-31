import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

#NUmber of decimal places following data points
accuracy = 2

#Area to create Unit Circle
plt.figure(figsize=(8,8))

#Define line start and end coordinates
x = [0, 1, 0, -1, 0]
y = [0, 0, 1, 0, -1]

#Plot quadrant lines
for i in range(len(x)):
    plt.plot([x[0],x[i]], [y[0],y[i]], color='black')

class Point:
    def __init__(self, degree):
        self.degree = degree
        self.radian = np.radians(degree)
        self.sin = np.round(np.sin(self.radian), accuracy)
        self.cos = np.round(np.cos(self.radian), accuracy)

        try:
            if np.abs(self.cos) < 1e-10:
                self.tan = float('inf')
            else:
                self.tan = np.round(np.tan(self.radian), accuracy)
        except:
            self.tan = float('inf')

    def __str__(self):
        return (f"Degree: {self.degree}°, Radian: {round(self.radian, 4)}, "
                f"sin: {self.sin}, cos: {self.cos}, tan: {self.tan}")

#Create Unit Cirle
unit_circle = plt.Circle(xy=(0,0), fill=False,radius=1,color='black')
midpoint = plt.Circle(xy=(0,0),radius=0.01,color='m',alpha=0.3)

#Add patches to figure
fig = plt.gcf()
ax = fig.gca()

plotted_elements = []

#Handle clicking
def onclick(event):
    if event.inaxes != ax or event.xdata is None or event.ydata is None:
        return 
    
    x, y = event.xdata, event.ydata
    distance = np.sqrt(x**2 + y**2)
    tolerance = 0.05

    if abs(distance - 1) < tolerance:
        theta_rad = np.arctan2(y, x)
        theta_deg = (np.degrees(theta_rad) + 360) % 360

        p = Point(theta_deg)
        print(p)

        if event.key != 'shift':
            for elem in plotted_elements:
                if hasattr(elem, 'remove'):
                    elem.remove()
            plotted_elements.clear()

        hypotenuse = plt.plot([0, p.cos], [0, p.sin], color='blue')[0]
        intersecting_point = plt.plot(p.cos, p.sin, 'ro')[0]  
        opposite = plt.plot([p.cos, p.cos], [0, p.sin], color='green')[0]
        label = plt.text(p.cos, p.sin + 0.05, f"{str(p.radian)[:5]}/{p.sin}/{p.cos}/{p.tan}", ha='center', 
                         bbox=dict(facecolor='white', edgecolor='none'))

        plotted_elements.extend([hypotenuse, intersecting_point, opposite, label])

        fig.canvas.draw()

#Instructions/Information
plt.figtext(0.3, 0.02,
    "Click on the edge of the circle to create a triangle.\n"
    "Shift + Click to add more. Click alone to reset.",
    ha='center',
    fontsize=9,
    wrap=True,
    bbox=dict(facecolor='lightyellow', boxstyle='round', edgecolor='black')
)

plt.figtext(0.75, 0.025,
    "Label Format : Radian/sin/cos/tan",
    ha='center',
    fontsize=9,
    wrap=True,
    bbox=dict(facecolor='#FFCCCC', boxstyle='round', edgecolor='black')
)

cid = fig.canvas.mpl_connect('button_press_event', onclick)
ax.add_patch(unit_circle)
ax.add_patch(midpoint)

#Size of graph
plt.xlim(-1,1)
plt.ylim(-1,1)

plt.title("Trigonmetry Visualizer", pad=30)
plt.savefig('Trigonometry Visualizer.png', dpi=300)
plt.grid(True)
plt.show()
