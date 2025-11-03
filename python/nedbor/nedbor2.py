# Import
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.lines import Line2D
from matplotlib.widgets import RadioButtons
from matplotlib.widgets import Cursor
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn import preprocessing
from sklearn.preprocessing import PolynomialFeatures

# Farger
# fra: https://github.com/romainl/Apprentice
colors = {
0:'#1C1C1C',
1:'#AF5F5F',
2:'#5F875F',
3:'#87875F',
4:'#5F87AF',
5:'#5F5F87',
6:'#5F8787',
7:'#6C6C6C',
8:'#444444',
9:'#FF8700',
10:'#87AF87',
11:'#FFFFAF',
12:'#87AFD7',
13:'#8787AF',
14:'#5FAFAF',
15:'#FFFFFF',
'fg':'#BCBCBC',
'bg':'#262626',
}
theme = {
    'fg': 'blue',
    'bg':'lightgrey',
    'ax_bg':'lightgrey',
    'radio_face': 'black',
    'precipitation': [ 'orange', 'gray', 'blue', 'darkblue', 'black' ],
    'line': 'black',
    'line_avg': 'red',
    'cursor': 'red',
    'bar_label': colors['fg'],
    'precipitation_circle_fg':'white',
    'precipitation_circle_border':'white',
    'precipitation_circle_sel_border': 'red',
    'precipitation_circle_font_size':6,
    'precipitation_circle_size':600,
}

mpl.rcParams['text.color'] = theme['fg']
mpl.rcParams['axes.labelcolor'] = theme['fg']
mpl.rcParams['xtick.color'] = theme['fg']
mpl.rcParams['ytick.color'] = theme['fg']
mpl.rcParams['axes.edgecolor'] = theme['fg']

# Import av data
map_img = mpimg.imread('map.png')
data = pd.read_csv('data.csv')


# Variabler
p = None
sel_time=0
time_options=['monthly', 'quarterly']
time_names=['måned', 'kvartal']
poly = PolynomialFeatures(degree=3)
model = LinearRegression()
fig, ax = plt.subplot_mosaic(
    [
        ['map','graph'],
        ['map_btns','graph_btns'],
    ],
    width_ratios=[5,5],
    height_ratios=[9,1],
    layout='constrained',
    figsize=(16, 6),
    facecolor=theme['bg'],
)
for a in ax:
    ax[a].set_facecolor(theme['ax_bg'])
cursor = Cursor(ax['map'], useblit=True, color=theme['cursor'], linewidth=1)


# Entry-point for programmet
def main():
    # Matplotlib oppsett
    graph_btns = RadioButtons(
        ax['graph_btns'], (time_names[0].title(), time_names[1].title()),
        radio_props={'facecolor': theme['radio_face']})
    map_btns = RadioButtons(
        ax['map_btns'], ('Nedbør', 'Vind'),
        radio_props={'facecolor': theme['radio_face']})
    plt.connect('button_press_event', map_click)
    graph_btns.on_clicked(change_timeframe)
    map_btns.on_clicked(change_datatype)
    ax['graph_btns'].axis('off')
    ax['map_btns'].axis('off')

    # Sklearn oppsett
    data_precipitation = data['precipitation']
    X = data.drop('precipitation',  axis=1)
    X_poly = poly.fit_transform(X)
    X_train, X_test, Y_train, Y_test = train_test_split(
        X_poly, data_precipitation, test_size=0.25)
    model.fit(X_train, Y_train)
    Y_pred = model.predict(X_test)
    r_squared = r2_score(Y_test, Y_pred)
    print(f"R-squared: {r_squared:.2f}")
    print('mean_absolute_error (mnd) : ', mean_absolute_error(Y_test, Y_pred))
    
    # Tegn grafikk
    draw_map()
    draw_graph()
    plt.show()


# Håndter av klikking på kartet
def map_click(event):
    global p
    if event.inaxes != ax['map']:
        return
    p = {'x': event.xdata, 'y': event.ydata}
    vectors = []
    months = np.linspace(1,12,12)
    for mnd in months:
        vectors.append([p['x'],p['y'],mnd])
    at_point = np.vstack(vectors)
    at_point_m = poly.fit_transform(at_point)
    pred = model.predict(at_point_m)
    p['year']=int(sum(pred))
    p['monthly']={
        'graph_y': pred,
        'graph_x': months
    }
    # Kvartal
    p['quarterly']={
        'graph_y': [pred[i*3]+pred[i*3+1]+pred[i*3+2] for i in range(4)],
        'graph_x': np.linspace(1,4,4)
    }
    draw()

# Tegn grafikk
def draw():
    draw_map()
    draw_graph()
    fig.canvas.draw()

# Endre mellom månedlig og kvartal
def change_timeframe(label):
    global sel_time
    sel_time = (sel_time + 1) % len(time_options)
    draw()

# Endre datatype mellom vind / nedbør
def change_datatype(label):
    global sel_type
    sel_type = (sel_type + 1) % len(type_options)
    draw()

# Finn farge som tilsvarer nedbørsmengde
def precipitation_color(n):
    if n < 1300: return theme['precipitation'][0]
    if n < 1700: return theme['precipitation'][1]
    if n < 2500: return theme['precipitation'][2]
    if n < 3200: return theme['precipitation'][3]
    return theme['precipitation'][4]

# Tegn graf
def draw_graph():
    ax['graph'].cla()
    ax['graph'].set_title('Velg kartkoordinat for å vise værdata')
    if (p is not None):
        graph_x=p[time_options[sel_time]]['graph_x']
        graph_y=p[time_options[sel_time]]['graph_y']
        '''ax['graph'].plot(
            graph_x,
            graph_y,
           color=theme['line']
        )'''
        l2=ax['graph'].plot(
            graph_x,
            [p['year']/len(graph_x) for i in range(len(graph_x))],
            color=theme['line_avg'],
            label='test',
        )
        ax['graph'].set_title('Nedbør per ' + time_names[sel_time] + ' for valgt kartkoordinat ('+str(p['year'])+'mm per år)')
        ax['graph'].set_xticks(
            np.linspace(
                1, 
                len(graph_x),
                len(graph_y)
            )
        )
        bar = ax['graph'].bar(
            graph_x,
            graph_y,
            color=[precipitation_color(n*10) for n in graph_y],
        )
        ax['graph'].bar_label(
            bar,
            fmt='{:,.0f}\nmm',
            label_type='center',
            fontweight='bold',
            color=theme['bar_label']
        )
        legend_colors=[Line2D([0], [0], color=(theme['precipitation'][i-1] if i > 0 else 'red'), lw=4) for i in reversed(range(len(theme['precipitation'])+1))]
        legend_titles=['Over 320', '250-320', '170 - 250', '130 - 170', 'Under 130', 'Gjennomsnitt']
        ax['graph'].legend(
            legend_colors,
            legend_titles,
            loc="upper left",
        )

# Tegn kart
def draw_map():
    # Variabler
    data_year = data.groupby(['x', 'y']).agg({'precipitation': 'sum'}).reset_index()
    map_x = data_year['x'].tolist()
    map_y = data_year['y'].tolist()
    precipitation_year = data_year['precipitation']
    # Tegn bakgrunnsbilde
    ax['map'].cla()
    ax['map'].set_title('kart')
    ax['map'].axis('off')
    ax['map'].imshow(map_img, extent=(0, 13, 0, 10))

    # Tegn fargede punkter totalnedbør per år
    ax['map'].scatter(
        map_x, map_y, 
        c=[precipitation_color(n) for n in precipitation_year],
        edgecolors=theme['precipitation_circle_border'],
        s=theme['precipitation_circle_size'],
    )
    # Tegn tekst for punktene
    for i, y in enumerate(map_x):
        


        ax['map'].text(
            map_x[i], 
            map_y[i], 
            s=str(int((precipitation_year[i]))),
            color=theme['precipitation_circle_fg'], 
            fontsize=theme['precipitation_circle_font_size'],
            fontweight='bold',
            ha='center',
            va='center'
        )
    # Tegn sirkel for valgt punkt
    if (p is not None):
        ax['map'].scatter(
            p['x'],
            p['y'],
            c=precipitation_color(p['year']),
            edgecolors=theme['precipitation_circle_sel_border'],
            s=theme['precipitation_circle_size']*2, 
            marker="o"
            )
        ax['map'].scatter(
            p['x'],
            p['y'],
            c=theme['precipitation_circle_sel_border'],
            edgecolors=theme['precipitation_circle_sel_border'],
            s=theme['precipitation_circle_size'], 
            marker="o"
            )
        ax['map'].text(
            p['x'],
            p['y'],
            s=str(p['year']),
            color=theme['precipitation_circle_fg'], 
            fontsize=theme['precipitation_circle_font_size'],
            fontweight='bold',
            ha='center',
            va='center'
        )

# Kall på main funksjonen
if __name__ == '__main__':
    main()