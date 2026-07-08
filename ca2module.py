# Module containing extra functions to call in IT8701_CA2.ipynb
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from bokeh.models import ColumnDataSource, FactorRange, NumeralTickFormatter, Title
from bokeh.palettes import MediumContrast6, MediumContrast5
from bokeh.plotting import figure, show
from bokeh.transform import factor_cmap
from bokeh.io import output_notebook
output_notebook()

import math

annotation_text = "From database data with entry timestamp: "

def test_fn_1():
    output = 1 * 2
    print(f"Function successfully invoked from this module: return value {output}")
    return output

def annotate_on_plot_bottom(ax, line_annotate):
    ax.annotate(line_annotate, 
                xy=(1, 0), xycoords='axes fraction', 
                xytext=(-5, -40), textcoords='offset points', 
                ha='right', va='top', fontsize=9)	

def bokeh_annotate_plot_bottom(p, line_annotate):
    footnote = Title(text=line_annotate,  align="right", text_font_size="9pt")
    p.add_layout(footnote, "below")   

def annotate_plot_medians(ax):
    for i, line in enumerate(ax.get_lines()):
        if i % 6 == 4: 
            x_coords = line.get_xdata()
            y_coords = line.get_ydata()         
            x_center = x_coords.mean()
            y_val = y_coords[0] 
            ax.text(x_center, y_val, f'{y_val/1000:.0f}k', 
                    ha='center', va='center', fontweight='bold', 
                    size=11, color='white',
                    bbox=dict(facecolor="#A9B4B9D9", alpha=0.8, edgecolor='none', pad=1))
            
def plot_formatting(ax):
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f'{x/1000:g}k'))
    ax.grid(True, axis='y', linestyle='-', alpha=0.7)

def plot_dataset_fig_1(dataset_fig_1a, data_ts):
    fig, ax = plt.subplots(figsize=(10, 8)) 
    sns.set_theme(style="ticks", palette="pastel")
    sns.boxplot(x="year", y="premium", hue="vehicle_class", palette=["greenyellow", "skyblue", "orange"], data=dataset_fig_1a, ax=ax)
    annotate_plot_medians(ax)
    plot_formatting(ax)
    ax.set_title("Fig 1: Boxplot for COE categories A, B, E in study period", fontsize=12, fontweight='bold', pad=20)
    annotate_on_plot_bottom(ax, annotation_text + data_ts)
    plt.show()

def plot_dataset_fig_1c(dataset_fig_1c, data_ts):
    # Draw a heatmap with the numeric values in each cell
    f, ax = plt.subplots(figsize=(9, 6))
    hm_sns = sns.heatmap(dataset_fig_1c, annot=True, fmt=",d", linewidths=.5, cmap="viridis_r", ax=ax)
    cbar = hm_sns.collections[0].colorbar
    cbar.ax.invert_yaxis()
    cbar.set_label("S$", fontdict={'fontweight': 'bold', 'fontsize': 12})
    ax.set_xlabel("COE Category", fontdict={'fontweight': 'bold', 'fontsize': 12})
    ax.set_ylabel("Year", fontdict={'fontweight': 'bold', 'fontsize': 12})
    ax.set_title("Fig 1B: Heatmap of COE category A, B, E yearly median premium trend", pad=20, fontdict={'fontweight': 'bold', 'fontsize': 12})
    annotate_on_plot_bottom(ax, annotation_text + data_ts)
    plt.show()

def plot_dataset_fig_2_1(dataset_fig_2_1, data_ts):
    #print(dataset_fig_2_1)
    dataset_fig_2_1_dict = dataset_fig_2_1.to_dict(orient='list')
    years = list(dataset_fig_2_1.index)
    types = list(dataset_fig_2_1_dict.keys())
    data = {'years' : years}
    data = {**data, **dataset_fig_2_1_dict}
    # print(years)
    # print(data)
    x = [ (year, type) for year in years for type in types ]
    counts = sum(zip (data['Diesel'], data['Diesel-Electric'], data['Electric'], data['Petrol'], data['Petrol-CNG'], data['Petrol-Electric']) , ()) 
    source = ColumnDataSource(data=dict(x=x, counts=counts))
    tooltips = [("Year, Type", "@x"), ("Count", "@counts{0,0}")]
    p = figure(x_range=FactorRange(*x), height=600, width=800, title="Fig 2.1: Annual car population by fuel type",
               toolbar_location=None, tools="hover", tooltips=tooltips ,output_backend="svg")
    p.vbar(x='x', top='counts', width=0.9, source=source, line_color="white",
           fill_color=factor_cmap('x', palette=MediumContrast6, factors=types, start=1, end=2))
    p.y_range.start = 0
    p.x_range.range_padding = 0.1
    p.xaxis.major_label_orientation = 1
    p.xgrid.grid_line_color = None
    p.yaxis.formatter = NumeralTickFormatter(format="0,0")
    p.yaxis.axis_label = "Vehicle units"
    p.title.text_font_size = "16pt"
    p.title.align = "center"
    p.title.text_font_style = "bold"
    bokeh_annotate_plot_bottom(p, annotation_text + data_ts)
    show(p)

def plot_dataset_fig_2_2(dataset_fig_2_2, data_ts):
    #print(dataset_fig_2_2)
    dataset_fig_2_2_dict = dataset_fig_2_2.to_dict(orient='list')
    years = list(dataset_fig_2_2.index)
    types = list(dataset_fig_2_2_dict.keys())
    data = {'years' : years}
    data = {**data, **dataset_fig_2_2_dict}
    # print(years)
    # print(data)
    x = [ (year, type) for year in years for type in types ]
    counts = sum(zip (data['Diesel'], data['Electric'], data['Others'], data['Petrol'], data['Petrol-Electric']) , ()) 
    source = ColumnDataSource(data=dict(x=x, counts=counts))
    tooltips = [("Year, Type", "@x"), ("Count", "@counts{0,0}")]
    p = figure(x_range=FactorRange(*x), height=600, width=800, title="Fig 2.2: Annual new car registrations by fuel type",
            toolbar_location=None, tools="hover", tooltips=tooltips ,output_backend="svg")
    p.vbar(x='x', top='counts', width=0.9, source=source, line_color="white",
        fill_color=factor_cmap('x', palette=MediumContrast5, factors=types, start=1, end=2))
    p.y_range.start = 0
    p.x_range.range_padding = 0.1
    p.xaxis.major_label_orientation = 1
    p.xgrid.grid_line_color = None
    p.yaxis.formatter = NumeralTickFormatter(format="0,0")
    p.yaxis.axis_label = "Vehicle units"
    p.title.text_font_size = "16pt"
    p.title.align = "center"
    p.title.text_font_style = "bold"
    bokeh_annotate_plot_bottom(p, annotation_text + data_ts)
    show(p)

def plot_dataset_fig_2_3(dataset_fig_2_3, data_ts):
    #print(dataset_fig_2_3)
    cols_for_snsplot = (list(dataset_fig_2_3.columns))[1:]
    num_col = 2
    num_rows = math.ceil(len(cols_for_snsplot) / num_col)
    sns.set_theme(style="whitegrid")
    colors = sns.color_palette("muted")
    fig, axes = plt.subplots(num_rows, num_col, figsize=(10, 12))
    
    for i, column_name in enumerate(cols_for_snsplot):
        ax = axes.flat[i]
        ax.pie(dataset_fig_2_3[column_name], 
            labels=dataset_fig_2_3['DataSeries'], 
            autopct='%1.1f%%', 
            colors=colors,
            startangle=140,
            textprops={'fontsize': 10})
        ax.set_title(f'Year: {column_name}')
    for j in range(i + 1, num_rows * num_col):
        axes.flat[j].axis('off')
    plt.suptitle('Fig 2.3: Annual proportion of vehicle types', fontsize=12, fontweight='bold', y=0.99)
    # add foot note
    fig.text(0.5, 0.02, annotation_text + data_ts, ha='center', fontsize=10)
    plt.tight_layout(rect=[0, 0.04, 1, 0.96])
    plt.show()

def plot_dataset_fig_4_1(dataset_fig_4_1, dataset_fig_4_1b, data_ts):
    sns.set_theme(style="darkgrid")
    pearson_coefficients = dataset_fig_4_1b
    p = sns.lmplot(
        data=dataset_fig_4_1, x="COE cat A premium year median", y="ridership", col="dataset", hue="dataset",
        col_wrap=2, palette="muted", ci=None,
        height=5, 
        truncate=False,
        markers="x",
        scatter_kws={"s": 40, "alpha": 1},
        line_kws={"lw": 1}
    )
    for ax in p.axes.flat:
        ax.tick_params(axis="x", labelbottom=True)
        full_title = ax.get_title()
        dataset_name = full_title.split('= ')[-1]
        coef_val = pearson_coefficients.get(dataset_name, 0)
        ax.text(
            0.05, 0.9, 
            f"Coefficient: {coef_val:.4f}", 
            transform=ax.transAxes, 
            fontsize=11, 
            fontweight='normal',
            bbox=dict(facecolor='white', alpha=0.5, edgecolor='none')
        )    
    p.figure.subplots_adjust(hspace=0.2, top=0.92)
    p.figure.suptitle("Fig 4.1: Effect of COE Median Prices on daily ridership per year", fontsize=12, fontweight='bold')
    # Add footnote
    p.figure.text(0.5, -0.02, annotation_text + data_ts, ha='center', fontsize=9, color='black')
    p.figure.subplots_adjust(bottom=0.08) 