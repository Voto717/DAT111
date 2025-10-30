# importing modules and packages
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.widgets import RadioButtons

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn import preprocessing
from sklearn.preprocessing import PolynomialFeatures

fig = plt.figure(figsize=(10, 4))
axGraph = fig.add_axes((0.05, 0.07, 0.35, 0.85))
axMap = fig.add_axes((0.41, 0.07, 0.59, 0.85))
colors = [ 'orange', 'gray', 'blue', 'darkblue', 'black']
img = mpimg.imread('map.png')
df = pd.read_csv('data.csv')
poly = PolynomialFeatures(degree=3)
model = LinearRegression()

# Entry-point for programmet
def main():
    draw_label_and_ticks()
    
    axMap.set_title("Årsnedbør, Stor Bergen")
    axGraph.set_title("Per måned")
    

    fig.subplots_adjust(left=0, right=1, top=1, bottom=0) # Adjust the figure to fit the image
    axMap.margins(x=0.01, y=0.01)  # Adjust x and y margins

    # Read rain data, and split in train and test.py data
    
    marked_point = (0,0)
    ns = df['Nedbor']
    X = df.drop('Nedbor',  axis=1)
    
    X_poly = poly.fit_transform(X)
    X_train, X_test, Y_train, Y_test = train_test_split(
        X_poly, ns, test_size=0.25)

    # creating a regression model
    
    model.fit(X_train, Y_train) # fitting the model
    Y_pred = model.predict(X_test)

    # Check model quality
    r_squared = r2_score(Y_test, Y_pred)
    print(f"R-squared: {r_squared:.2f}")
    print('mean_absolute_error (mnd) : ', mean_absolute_error(Y_test, Y_pred))

    
    draw_the_map()

    plt.connect('button_press_event', on_click)
    plt.show()

def draw_the_map():
    # Accumulate all months to year
    axMap.cla()
    plt.imshow(img, extent=(0, 13, 0, 10))
    df_year = df.groupby(['X', 'Y']).agg({'Nedbor': 'sum'}).reset_index()
    xr = df_year['X'].tolist()
    yr = df_year['Y'].tolist()
    nedborAar = df_year['Nedbor']
    ColorList = [color_from_nedbor(n) for n in nedborAar]
    axMap.scatter(xr, yr, c=ColorList, s=size_from_nedbor(nedborAar/12), alpha=1)
    labels = [label_from_nedbor(n) for n in nedborAar]
    for i, y in enumerate(xr):
        axMap.text(xr[i], yr[i], s=labels[i], color='white', fontsize=10, ha='center', va='center')
    axMap.axis('off')

def index_from_nedbor(x):
    if x < 1300: return 0
    if x < 1700: return 1
    if x < 2500: return 2
    if x < 3200: return 3
    return 4

def color_from_nedbor(nedbor):
    return colors[index_from_nedbor(nedbor)]
def size_from_nedbor(nedbor):
    return 350
def label_from_nedbor(nedbor):
    return str(int(nedbor / 100))

def on_click(event) :
    global marked_point
    if event.inaxes != axMap:
        return

    marked_point = (event.xdata, event.ydata)
    x,y = marked_point

    vectors = []
    months = np.linspace(1,12,12)
    for mnd in months:
        vectors.append([x,y,mnd])
    AtPoint = np.vstack(vectors)
    # fitting the model, and predict for each month
    AtPointM = poly.fit_transform(AtPoint)
    y_pred = model.predict(AtPointM)
    aarsnedbor = sum(y_pred)

    # ADDED:
    # ---------------
    y_pred_quarters=[y_pred[i*3]+y_pred[i*3+1]+y_pred[i*3+2] for i in range(4)]
    quarters = np.linspace(1,4,4)
    print(y_pred)
    print(y_pred_quarters)
    #for i, quarter in enumerate(quarters):
    #    quarters[i]=10
    # ---------------

    axGraph.cla()
    draw_the_map()
    axMap.set_title(f"C: ({x:.1f},{y:.1f}) - click rød er estimert")


    axMap.text(x, y, s=label_from_nedbor(aarsnedbor), color='white', fontsize=10, ha='center', va='center')
    axGraph.set_title(f"Nedbør per måned, Årsnedbør {int(aarsnedbor)} mm")

    colorsPred = [color_from_nedbor(nedbor * 10) for nedbor in y_pred]
    axMap.scatter(x, y, c=color_from_nedbor(aarsnedbor), s=size_from_nedbor(aarsnedbor) * 3.5, marker="o")
    axMap.scatter(x, y, c="red", s=size_from_nedbor(aarsnedbor)*2.5, marker="o")
    #axGraph.bar(months, y_pred, color=colorsPred)
    axGraph.bar(months, y_pred, color=colorsPred)
    draw_label_and_ticks()
    
    # ADDED:
    # ---------------
    #radio = RadioButtons(axGraph, ('2 Hz', '4 Hz', '8 Hz'))
    #radio = RadioButtons(axGraph, ("månedlig", "kvartal", "test"),
    #                 label_props={'color': 'cmy', 'fontsize': [12, 14, 16]},
    #                 radio_props={'s': [16, 32, 64]})

    #radio.on_clicked(radiofunc)

    axGraph.plot(months,y_pred)
    axGraph.plot([aarsnedbor/12 for i in range(14)], color="red")
    l_colors = {}
    l_colors["under 1300"] = colors[0]
    l_colors["1300 - 1700"] = colors[1]
    l_colors["1700 - 2500"] = colors[2]
    l_colors["2500 - 3200"] = colors[3]
    l_colors["over 3200"] = colors[4]
    l_labels = list(l_colors.keys())
    l_handles = [plt.Rectangle((0,0),1,1, color=l_colors[label]) for label in l_labels]
    axGraph.legend(l_handles, l_labels)
    # ---------------

    plt.draw()

def radiofunc(label):
    print("clicked")

def draw_label_and_ticks():
    xlabels = ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D']
    axGraph.set_xticks(np.linspace(1, 12, 12))
    axGraph.set_xticklabels(xlabels)

# Kall på main funksjonen
if __name__ == '__main__':
    main()