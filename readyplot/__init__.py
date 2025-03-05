#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
An initialization file which also holds shared expected inputs (differentiates them from kwargs) and sets defaults
@author: Shawn Pavey
"""
# readyplot/__init__.py
# %% IMPORT PACKAGES
from .bar_plotter import BarPlotter
from .boxwhisker_plotter import BoxWhiskerPlotter
from .hist_plotter import HistPlotter
from .scatter_plotter import ScatterPlotter
from .line_plotter import LinePlotter
from .strip_plotter import StripPlotter
from .subplots import SubPlots
import pandas as pd
import numpy as np
from .utils import dict_update_nested
from matplotlib import pyplot as plt

#%%---------------------------------------------------------------------------------------------------------------------
# MAIN INITIALIZATION
#-----------------------------------------------------------------------------------------------------------------------
# %% PARSE ARGS AND PREPARE DATA FRAME COLUMN NAMES TO HANDLE ANY COMBINATION OF STRING INPUTS (OR NON-INPUTS)
def initialize_common_defaults(args,input_dict):
    input_dict = parse_args(locals())
    input_dict,xlab,ylab,zlab = prepare_data_frame_col_names(locals())
    for var in ['xlab','ylab','zlab']:
        if locals()[var] is None: del locals()[var]
    del args, var

    # %% INITIALIZE DEFAULT VALUES
    # GENERAL ESSENTIALS IN FRONT-END OR BACK-END
    # Input Data
    DF = None
    x = None
    y = None
    z = None
    excel_path = None
    sheet_name = None
    csv_path = None

    # Groups (xlab,ylab,zlab maybe created above during prepare_data_frame_col_names)
    colors = ['#199940', 'r', 'b', 'y', 'c', 'm', 'k', 'w']
    markers = ['o', 's', 'D', 'p', 'h', '*', 'x', '+', '^', 'v', '>', '<']
    hatches = ['....', '---', '//', '++', 'OO', '**']
    style = None

    # Input Handles
    input_fig = None
    input_ax = None
    plot_type = None
    first_time_legend = True
    handles = None
    labels = None

    # Output Fig
    folder_name = "OUTPUT_FIGURES"
    dpi = 300
    fig_width = 7
    fig_height = 5

    # ERRORS, GENERAL TEXT, ESTHETICS
    # Errors
    capsize = 0.4
    yerror_vals = None
    hi_yerror_vals = None
    low_yerror_vals = None
    xerror_vals = None
    hi_xerror_vals = None
    low_xerror_vals = None
    err_names = ['xerror_vals','yerror_vals','low_xerror_vals','hi_xerror_vals','low_yerror_vals','hi_yerror_vals']
    error_lim_affect = False

    # General Text
    custom_x_label = None
    custom_y_label = None
    title = None
    def_font_sz = 16
    fontweight = 'bold'

    # General Esthetics
    line_color = 'black'
    back_color = 'white'
    darkmode = False
    apply_color_lines_only = False
    transparent = False
    sns_palette = "deep"
    sns_style = "ticks"
    sns_context = "notebook"
    grid_color = "#444444"

    # AXIS-RELATED SETTINGS
    # Lines & Axes
    box_edges = ['bottom', 'left']
    def_line_w = 1.5
    xtick_font_ratio = 1
    ytick_font_ratio = 1
    x_axis_sig_figs = 3
    y_axis_sig_figs = 3

    # Scientific Notation
    x_exp_location = 0
    y_exp_location = 0
    low_x_cap0 = False
    low_y_cap0 = False
    sci_x_lims = (-1,3)
    sci_y_lims = (-1,3)

    # XLines and YLines
    xlines = [None]
    ylines = [None]
    internal_xlines = []
    internal_ylines = []
    internal_patches = []
    internal_lines = []

    # NICHE FEATURES GENERALLY PLOT-TYPE DEPENDENT
    # Legend Tool for Strip-Plot Overlay
    handles_in_legend = 10

    # Bar and Box Features
    dodge = True
    box_width = 0.8
    plot_line_palette = None

    # Trendline
    trendline = False
    show_r2 = False
    annote_x_start = 0.7
    annote_y_start = 0.7

    # DICTIONARIES TO PASS AS KWARGS TO OTHER PACKAGES
    # Grouped Kwargs
    legend = None
    legend_kwargs = {'prop': {'weight': 'bold'}, 'framealpha': 1}
    trendline_kwargs = None
    xylines_kwargs = None
    imported_settings = {}

    # %% PREPARE FOR INPUT SORTING
    # EVERY VARIABLE INITIALIZED WITH A DEFAULT SO FAR IS EXPECTED IN SORTING, EVERY OTHER VARIABLE WILL BE A KWARG
    expected_keys = list(locals().keys())
    initialized_dict = {}
    kwargs = {}

    # SPECIFY LISTS OF VARIABLES TO IGNORE IN INPUT HANDLING
    special_entries = ['special_entries','nested_kwargs','input_dict','expected_keys','initialized_dict','kwargs']
    nested_kwargs = ['legend_kwargs','custom_error_kwargs']

    # UNPACK THE INPUT KEYWORDS INTO LOCALS TO PREPARE FOR ITERATING
    for name, value in input_dict.items():
        if name in special_entries:
            kwargs[name] = value
        if name not in locals():
            locals()[name] = value
    del name, value

    # APPLY IMPORTED SETTINGS BEFORE POPULATING THE REST OF THE INITIALIZED_DICT, SO OTHER INPUTS CAN OVERWRITE THESE
    if 'imported_settings' in input_dict:
        for key, value in input_dict['imported_settings'].items(): initialized_dict[key] = value
        del key, value
    else: input_dict['imported_settings'] = {}

    # %% SORT USER INPUTS INTO REGULAR VARIABLES AND SEABORN KWARGS, HANDLE NESTED KWARG DICTIONARIES RECURSIVELY
    for name, value in locals().items():
        # IGNORE IMPORTED SETTINGS
        if name == 'imported_settings' or (name in input_dict['imported_settings'] and name not in input_dict):
            pass
        # IF THE VARIABLE IS A NESTED KWARG USE RECURSIVE METHOD TO RESOLVE NESTED DICTIONARIES, NOT OVERWRITE ENTIRELY
        elif name in nested_kwargs:
            initialized_dict[name] = dict_update_nested(value,input_dict[name]) if name in input_dict else value

        # SORT VARIABLE INTO REGULAR VARIABLES OR SEABORN KWARGS IF IT IS NOT A SPECIAL LOCAL VARIABLE
        elif name not in special_entries and name != 'DFs':
            if name in expected_keys: initialized_dict[name] = input_dict[name] if name in input_dict else value
            else: kwargs[name] = value

        # LEGACY CATCH, SOME PEOPLE MAY USE DFs INSTEAD OF DF AND THIS WILL CATCH THAT
        elif name == 'DFs':
            initialized_dict['DF'] = value

    return initialized_dict, kwargs

#%%---------------------------------------------------------------------------------------------------------------------
# METHODS
#-----------------------------------------------------------------------------------------------------------------------
# %% PARSE USER ARGUMENTS
def parse_args(l):
    # UNPACK LOCALS INTO VARIABLES
    args,input_dict = l['args'],l['input_dict']

    # PARSE ARGS INTO DF IF PROVIDED, BEHAVIOR VARIES BY TEH NUMBER OF ARGS
    if len(args) == 1:
        if isinstance(args[0], pd.DataFrame): input_dict['DF'] = args[0]
        elif isinstance(args[0], str) and not isinstance(args[0], (list, np.ndarray)):
            if '.csv' in args[0]: input_dict['DF'] = pd.read_csv(args[0])
            else: input_dict['DF'] = pd.read_excel(args[0])
        else: input_dict['x'] = args[0]
    elif len(args) == 2:
        if (isinstance(args[0], str) and not isinstance(args[0], (list, np.ndarray))) and (
                isinstance(args[1], str) and not isinstance(args[1], (list, np.ndarray))):
            input_dict['DF'] = pd.read_excel(args[0], sheet_name=args[1])
        else:
            input_dict['x'] = args[0]
            input_dict['y'] = args[1]
    elif len(args) == 3:
        input_dict['x'] = args[0]
        input_dict['y'] = args[1]
        input_dict['z'] = args[2]

    # IF NO ARGS (OR MORE THAN 3) PROVIDED
    else:
        if ('excel_path' in input_dict and input_dict['excel_path'] is not None) and (
                'sheet_name' in input_dict and input_dict['sheet_name'] is not None):
            input_dict['DF'] = pd.read_excel(input_dict['excel_path'], sheet_name=input_dict['sheet_name'])
        elif 'excel_path' in input_dict and input_dict['excel_path'] is not None:
            input_dict['DF'] = pd.read_excel(input_dict['excel_path'])
        elif 'csv_path' in input_dict and input_dict['csv_path'] is not None:
            input_dict['DF'] = pd.read_csv(input_dict['csv_path'])

    return input_dict

# %% PREPARE XLAB,YLAB,ZLAB HANDLING TO PROPERLY COMBINE REQUIRED INNER DEFAULTS WITH USER INPUT
def prepare_data_frame_col_names(l):
    input_dict = l['input_dict']
    if 'DF' in input_dict and all(item not in input_dict for item in ['xlab','ylab','zlab']):
        if 'xlab' not in input_dict:
            try:
                input_dict['xlab'] = input_dict['DF'].columns[0]
                xlab = 'xlab'
            except:
                pass
        if 'ylab' not in input_dict:
            try:
                input_dict['ylab'] = input_dict['DF'].columns[1]
                ylab = 'ylab'
            except:
                pass
        if 'zlab' not in input_dict:
            try:
                input_dict['zlab'] = input_dict['DF'].columns[2]
                zlab = 'zlab'
            except:
                pass
    elif 'DF' in input_dict:
        if 'xlab' not in input_dict:
            xlab = 'xlab' if len(input_dict['DF'].columns) == 1 else None
        else:
            xlab = input_dict['xlab']
        if 'ylab' not in input_dict:
            ylab = 'ylab' if len(input_dict['DF'].columns) == 2 else None
        else:
            ylab = input_dict['ylab']
        if 'zlab' not in input_dict:
            zlab = 'zlab' if len(input_dict['DF'].columns) == 3 else None
        else:
            zlab = input_dict['zlab']
    else:
        xlab = 'xlab'
        ylab = 'ylab'
        zlab = 'zlab'

    for var in ['xlab', 'ylab', 'zlab']:
        if var not in locals():
            locals()[var] = None

    return input_dict,xlab,ylab,zlab

#%%---------------------------------------------------------------------------------------------------------------------
# ROUTING CHILD PLOTTER INITIALIZATION: THESE CALL THE ABOVE FUNCTION AND PASS ARGS AND KWARGS SUPPLIED BY USER
#-----------------------------------------------------------------------------------------------------------------------
# %% BAR PLOTS
def bar(*args,**kwargs):
    initialized_inputs, new_kwargs = initialize_common_defaults(args,kwargs)
    return BarPlotter(initialized_inputs,**new_kwargs)

# %% BOX-WHISKER PLOTS
def boxwhisker(*args,**kwargs):
    initialized_inputs, new_kwargs = initialize_common_defaults(args,kwargs)
    return BoxWhiskerPlotter(initialized_inputs,**new_kwargs)

# %% HISTOGRAM PLOTS
def hist(*args,**kwargs):
    initialized_inputs, new_kwargs = initialize_common_defaults(args,kwargs)
    return HistPlotter(initialized_inputs,**new_kwargs)

# %% LINE PLOTS
def line(*args,**kwargs):
    initialized_inputs, new_kwargs = initialize_common_defaults(args,kwargs)
    return LinePlotter(initialized_inputs,**new_kwargs)

# %% SCATTER PLOTS
def scatter(*args,**kwargs):
    initialized_inputs, new_kwargs = initialize_common_defaults(args,kwargs)
    return ScatterPlotter(initialized_inputs,**new_kwargs)

# %% STRIP PLOTS
def strip(*args,**kwargs):
    initialized_inputs, new_kwargs = initialize_common_defaults(args,kwargs)
    return StripPlotter(initialized_inputs,**new_kwargs)

# %% SUB PLOTS
def subplots(*args,**kwargs):
    return SubPlots(*args,**kwargs)

# %% EXPLICITLY STATE HOW TO IMPORT THE ENTIRE MODULE (eg: import *)
__all__ = ['boxwhisker',
           'scatter',
           'line',
           'bar',
           'hist',
           'strip',
           'BoxWhiskerPlotter',
           'ScatterPlotter',
           'LinePlotter',
           'BarPlotter',
           'HistPlotter',
           'StripPlotter',
           'SubPlots']
