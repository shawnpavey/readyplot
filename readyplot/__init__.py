#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
An initialization file which also holds shared expected inputs (differentiates them from kwargs) and sets defaults
@author: Shawn Pavey
"""
# readyplot/__init__.py
#%% IMPORT PACKAGES
from .bar_plotter import BarPlotter
from .boxwhisker_plotter import BoxWhiskerPlotter
from .hist_plotter import HistPlotter
from .scatter_plotter import ScatterPlotter
from .line_plotter import LinePlotter
import pandas as pd
import numpy as np

expected_keys = ['DFs','x','y','z','excel_path','sheet_name','xlab','ylab','zlab','input_fig','input_ax',
                 'colors','markers','hatches','def_font_sz','def_line_w','fontweight',
                 'folder_name','dpi',
                 'box_edges','fig_width','fig_height','xtick_font_ratio','ytick_font_ratio',
                 'x_exp_location','y_exp_location','annote_x_start','annote_y_start',
                 'x_axis_sig_figs','y_axis_sig_figs','low_x_cap0','low_y_cap0',
                 'sci_x_lims','sci_y_lims',
                 'dodge', 'handles_in_legend', 'box_width',
                 'custom_x_label','custom_y_label','title',
                 'sns_palette','sns_style','sns_context',
                 'plot_type',
                 'capsize', 'trendline', 'show_r2','style','line_color','back_color','darkmode','apply_color_lines_only',
                 'plot_line_palette']


def bar(*args,**kwargs):
    initialized_inputs, new_kwargs = initialize_common_defaults(args,kwargs)
    return BarPlotter(initialized_inputs,**new_kwargs)

def boxwhisker(*args,**kwargs):
    initialized_inputs, new_kwargs = initialize_common_defaults(args,kwargs)
    return BoxWhiskerPlotter(initialized_inputs,**new_kwargs)

def hist(*args,**kwargs):
    initialized_inputs, new_kwargs = initialize_common_defaults(args,kwargs)
    return HistPlotter(initialized_inputs,**new_kwargs)

def line(*args,**kwargs):
    initialized_inputs, new_kwargs = initialize_common_defaults(args,kwargs)
    return LinePlotter(initialized_inputs,**new_kwargs)

def scatter(*args,**kwargs):
    initialized_inputs, new_kwargs = initialize_common_defaults(args,kwargs)
    return ScatterPlotter(initialized_inputs,**new_kwargs)


def initialize_common_defaults(args,input_dict):
    if len(args) == 1:
        if isinstance(args[0], pd.DataFrame):
            input_dict['DFs'] = args[0]
        else:
            input_dict['x'] = args[0]
    elif len(args) == 2:
        if (isinstance(args[0], str) and not isinstance(args[0], (list, np.ndarray))) and (
                isinstance(args[1], str) and not isinstance(args[1], (list, np.ndarray))):
            input_dict['DFs'] = pd.read_excel(args[0], sheet_name=args[1])
        else:
            input_dict['x'] = args[0]
            input_dict['y'] = args[1]
    elif len(args) == 3:
        input_dict['x'] = args[0]
        input_dict['y'] = args[1]
        input_dict['z'] = args[2]
    else:
        pass
    del args

    if 'DFs' in input_dict and all(item not in input_dict for item in ['xlab','ylab','zlab']):
        if 'xlab' not in input_dict:
            try:
                input_dict['xlab'] = input_dict['DFs'].columns[0]
            except:
                pass
        if 'ylab' not in input_dict:
            try:
                input_dict['ylab'] = input_dict['DFs'].columns[1]
            except:
                pass
        if 'zlab' not in input_dict:
            try:
                input_dict['zlab'] = input_dict['DFs'].columns[2]
            except:
                pass

    DFs = None
    x = None
    y = None
    z = None
    excel_path = None
    sheet_name = None
    xlab = 'xlab'
    ylab = 'ylab'
    zlab = 'zlab'
    input_fig = None
    input_ax = None
    colors = ['g', 'r', 'b', 'y', 'c', 'm', 'k', 'w']
    markers = ['o', 's', 'D', 'p', 'h', '*', 'x', '+', '^', 'v', '>', '<']
    hatches = ['//', '...', '--', '++', 'OO', '**']
    def_font_sz = 16
    def_line_w = 1.5
    folder_name = "OUTPUT_FIGURES"
    dpi = 300
    sns_palette = "deep"
    sns_style = "ticks"
    sns_context = "notebook"
    fontweight = 'bold'
    box_edges = ['bottom', 'left']
    fig_width = 7
    fig_height = 5
    xtick_font_ratio = 1
    ytick_font_ratio = 0.9
    x_exp_location = 0
    y_exp_location = 0
    annote_x_start = 0.7
    annote_y_start = 0.7
    x_axis_sig_figs = 0
    y_axis_sig_figs = 2
    low_x_cap0 = False
    low_y_cap0 = False
    dodge = True
    handles_in_legend = 10
    box_width = 0.8
    custom_x_label = None
    custom_y_label = None
    title = None
    plot_type = 'bar'
    sci_x_lims = (0, 1)
    sci_y_lims = (0, 1)
    capsize = 0.4
    trendline = False
    show_r2 = False
    style = None
    line_color = 'black'
    back_color = 'white'
    darkmode = False
    apply_color_lines_only = False
    plot_line_palette = None

    initialized_dict = {}
    kwargs = {}

    for name, value in locals().items():
        if name != 'input_dict' and name != 'initialized_dict' and name != 'kwargs':
            if name in expected_keys:
                if name in input_dict:
                    initialized_dict[name] = input_dict[name]
                else:
                    initialized_dict[name] = value
            else:
                kwargs[name] = value
    return initialized_dict, kwargs


__all__ = ['boxwhisker',
           'scatter',
           'line',
           'bar',
           'hist',
           'BoxWhiskerPlotter',
           'ScatterPlotter',
           'LinePlotter',
           'BarPlotter',
           'HistPlotter']
