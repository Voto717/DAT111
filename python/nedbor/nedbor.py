# Import
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.lines import Line2D
from matplotlib.widgets import RadioButtons
from matplotlib.widgets import Cursor
from matplotlib.backend_tools import Cursors
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn import preprocessing
from sklearn.preprocessing import PolynomialFeatures

# Farger (fra: https://github.com/romainl/Apprentice)
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

# Oppsett av utseende
theme = {
    'fg': colors['fg'],
    'bg': colors[0],
    'ax_bg': colors['bg'],
    'radio_face': colors['fg'],
    'radio_edge': colors['fg'],
    'precipitation': [ colors[2], colors[6], colors[4], colors[13], colors[5] ],
    'line': colors['fg'],
    'line_avg': colors[1],
    'cursor': colors['fg'],
    'bar_label': colors[15],
    'precipitation_map_circle_fg':colors[15],
    'precipitation_map_circle_shadow':colors['bg'],
    'precipitation_map_circle_border':colors['fg'],
    'precipitation_map_sel_fg': colors[15],
    'precipitation_map_sel_shadow': colors['bg'],
    'precipitation_map_circle_font_size':6,
    'precipitation_map_sel_font_size':8,
    'precipitation_map_circle_size':600,
    'precipitation_map_sel_point_size':300,
    'shadow_dist':0.04,
}

# Default verdier for mpl
mpl.rcParams['text.color'] = theme['fg']
mpl.rcParams['axes.labelcolor'] = theme['fg']
mpl.rcParams['xtick.color'] = theme['fg']
mpl.rcParams['ytick.color'] = theme['fg']
mpl.rcParams['axes.edgecolor'] = theme['fg']
mpl.rcParams['legend.labelcolor'] = theme['fg']
mpl.rcParams["legend.edgecolor"] = theme['fg']
mpl.rcParams["legend.facecolor"] = theme['bg']
mpl.rcParams['axes.titlepad'] = 12

# Import av data
map_img = mpimg.imread('map.png')
data = pd.read_csv('data.csv')

# Globale variabler
p = None
sel_time = 0
color_limits = [1300, 1700, 2500, 3200]
time_options = ['monthly', 'quarterly']
time_names = ['måned', 'kvartal']

# Oppsett av globale mpl og sklearn variabler
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
poly = PolynomialFeatures(degree=4)
model = LinearRegression()


# Main funksjon
def main():
    # Matplotlib oppsett
    graph_btns = RadioButtons(
        ax['graph_btns'], (time_names[0].title(), time_names[1].title()),
        radio_props={'facecolor': theme['radio_face'], 'edgecolor': theme['radio_edge']})
    map_btns = RadioButtons(
        ax['map_btns'], ('Nedbør', 'Vind (ikke implementert!)'),
        radio_props={'facecolor': theme['radio_face'], 'edgecolor': theme['radio_edge']})
    plt.connect('button_press_event', map_click)
    fig.canvas.mpl_connect('motion_notify_event', map_hover)
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


# Håndter musbevegelse
def map_hover(event):
    fig.canvas.set_cursor(Cursors.SELECT_REGION if event.inaxes == ax['map'] else Cursors.POINTER)


# Håndter klikking på kartet
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
    p['quarterly']={
        'graph_y': [pred[i*3]+pred[i*3+1]+pred[i*3+2] for i in range(4)],
        'graph_x': np.linspace(1,4,4)
    }
    draw()


# Endre mellom månedlig og kvartal visning
def change_timeframe(label):
    global sel_time
    sel_time = (sel_time + 1) % len(time_options)
    draw()


# Endre datatype mellom vind / nedbør
def change_datatype(label):
    print('ERR! Vind er ikke implementert!')


# Finn farge som tilsvarer nedbørsmengde
def precipitation_color(n):
    if n < color_limits[0]: return theme['precipitation'][0]
    if n < color_limits[1]: return theme['precipitation'][1]
    if n < color_limits[2]: return theme['precipitation'][2]
    if n < color_limits[3]: return theme['precipitation'][3]
    return theme['precipitation'][4]


# Tegn grafikk
def draw():
    draw_map()
    draw_graph()
    fig.canvas.draw()


# Tegn graf
def draw_graph():
    ax['graph'].cla()
    ax['graph'].set_title('Velg kartkoordinat for å vise værdata',fontweight='bold')
    if (p is not None):
        graph_x=p[time_options[sel_time]]['graph_x']
        graph_y=p[time_options[sel_time]]['graph_y']
        num=len(graph_x)
        ax['graph'].plot(
            graph_x,
            graph_y,
            color=theme['line'],
            linewidth=2,
        )
        ax['graph'].plot(
            graph_x,
            [p['year']/num for i in range(num)],
            color=theme['line_avg'],
            linestyle='--',
            linewidth=2,
        )
        ax['graph'].set_title('Estimert nedbør per ' + time_names[sel_time] + ' for valgt kartkoordinat ('+str(p['year'])+' mm per år)',fontweight='bold')
        ax['graph'].set_xticks(
            np.linspace(
                1, 
                num,
                len(graph_y)
            )
        )
        bar = ax['graph'].bar(
            graph_x,
            graph_y,
            color=[precipitation_color(n*num) for n in graph_y],
        )
        ax['graph'].bar_label(
            bar,
            fmt='{:,.0f}\nmm',
            label_type='center',
            fontweight='bold',
            color=theme['bar_label']
        )
        ax['graph'].set_xticklabels(['JAN', 'FEB', 'MAR', 'APR', 'MAI', 'JUN', 'JUL', 'AUG', 'SEP', 'OKT', 'NOV', 'DES'] if sel_time==0 else ['Q1', 'Q2', 'Q3', 'Q4'])
        legend_colors=[Line2D([0], [0], color=(theme['precipitation'][i-1] if i > 0 else theme['line_avg']), lw=4) for i in reversed(range(len(theme['precipitation'])+1))]
        legend_titles=[
            'Over '+str(int((color_limits[3]/num))), 
            str(int((color_limits[2]/num)))+' - '+str(int((color_limits[3]/num))), 
            str(int((color_limits[1]/num)))+' - '+str(int((color_limits[2]/num))), 
            str(int((color_limits[0]/num)))+' - '+str(int((color_limits[1]/num))), 
            'Under '+str(int((color_limits[0]/num))), 
            'Gjennomsnitt'
        ]
        ax['graph'].legend(
            legend_colors,
            legend_titles,
            loc="upper left",
            fancybox=False,
            #framealpha=0,
        )
        ax['graph'].set_axisbelow(True)
        ax['graph'].grid(
            alpha=0.5,
            color=colors[7],
            linestyle=':',
            axis='y',
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
    ax['map'].set_title('Kartoversikt med årlig nedbørgjennomsnitt i mm',fontweight='bold')
    #ax['map'].axis('off')
    ax['map'].set_yticks([])
    ax['map'].set_xticks([])
    ax['map'].imshow(map_img, extent=(0, 13, 0, 10))
    # Tegn fargede punkter totalnedbør per år
    ax['map'].scatter(
        map_x, map_y, 
        c=[precipitation_color(n) for n in precipitation_year],
        edgecolors=theme['precipitation_map_circle_border'],
        s=theme['precipitation_map_circle_size'],
        linewidths=2,
    )
    # Tegn tekst for punktene
    for i in range(len(map_x)):
        for j in reversed(range(2)):
            ax['map'].text(
                map_x[i], 
                map_y[i]-theme['shadow_dist']*j, 
                s=str(int((precipitation_year[i]))),
                color=theme['precipitation_map_circle_fg'] if j==0 else theme['precipitation_map_circle_shadow'],
                fontsize=theme['precipitation_map_circle_font_size'],
                fontweight='bold',
                ha='center',
                va='center'
            )
    # Tegn sirkel for valgt punkt
    if (p is not None):
        ax['map'].scatter(
            [p['x'],p['x']],
            [p['y']-theme['shadow_dist'],p['y']],
            c=[theme['precipitation_map_sel_shadow'],theme['precipitation_map_sel_fg']],
            marker="x",
            linewidths=2.5,
            s=theme['precipitation_map_sel_point_size'],
            )
        for i in reversed(range(2)):
            ax['map'].text(
                p['x'],
                p['y']+0.6-theme['shadow_dist']*i,
                s=str(p['year'])+'\n(estimert)',
                color=theme['precipitation_map_sel_fg'] if i==0 else theme['precipitation_map_sel_shadow'],
                fontsize=theme['precipitation_map_sel_font_size'],
                fontweight='bold',
                ha='center',
                va='center'
            )


# Kall på main funksjonen når programmet kjøres
if __name__ == '__main__':
    main()