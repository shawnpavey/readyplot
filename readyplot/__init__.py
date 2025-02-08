#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 14:34:59 2025
Custom plotter function which copies styles used by Shawn Pavey in Prism. Many
inputs are customizable, but defaults work well. This script contains two
functions: custom_plotter (full plotting + formating) and prism_reskin (only
reformats given figures).
@author: paveyboys
"""
# readyplot/__init__.py

from .bar_plotter import BarPlotter
from .boxwhisker_plotter import BoxWhiskerPlotter
from .hist_plotter import HistPlotter
from .scatter_plotter import ScatterPlotter
from .line_plotter import LinePlotter

expected_keys = ['DFs','x','y','z','xlab','ylab','zlab','input_fig','input_ax',
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
                 'capsize', 'trendline', 'show_r2','style']


def bar(**kwargs):
    initialized_inputs, new_kwargs = initialize_common_defaults(kwargs)
    return BarPlotter(initialized_inputs,**new_kwargs)

def boxwhisker(**kwargs):
    initialized_inputs, new_kwargs = initialize_common_defaults(kwargs)
    return BoxWhiskerPlotter(initialized_inputs,**new_kwargs)

def hist(**kwargs):
    initialized_inputs, new_kwargs = initialize_common_defaults(kwargs)
    return HistPlotter(initialized_inputs,**new_kwargs)

def line(**kwargs):
    initialized_inputs, new_kwargs = initialize_common_defaults(kwargs)
    return LinePlotter(initialized_inputs,**new_kwargs)

def scatter(**kwargs):
    initialized_inputs, new_kwargs = initialize_common_defaults(kwargs)
    return ScatterPlotter(initialized_inputs,**new_kwargs)


def initialize_common_defaults(input_dict):
    DFs = None
    x = None
    y = None
    z = None
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
    box_width = 0.6
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
