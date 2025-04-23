#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A class which produces subplots existing ready plot objects
@author: Shawn Pavey
"""
# %% IMPORT PACKAGES
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import scipy.stats as stats
import os
from .base_plotter import BasePlotter
from .utils import check_labels_in_DF, dict_update_nested
from matplotlib.colors import to_rgb
import matplotlib.patches as patches
from pathlib import Path
import matplotlib.lines as mlines

#%%---------------------------------------------------------------------------------------------------------------------
# CHILD CLASS MAIN
#-----------------------------------------------------------------------------------------------------------------------
# %% INITIALIZE SUB PLOTTER
class SubPlots(BasePlotter):
    def __init__(self, *args,**kwargs):
        for name, value in kwargs.items(): setattr(self, name, value)
        self.input_args = list(args)
        self.input_kwargs = kwargs

        if len(args) == 1: self.shape = args[0]
        elif len(args) == 2: self.shape = (args[0],args[1])

    # %% DEFINE PLOTTER, PREPARE INPUTS
    def plot(self,*temp_args,save=True,folder_name = "OUTPUT_FIGURES",adjust_mismatch=True,ax_num=0,**kwargs):
        # INITIATE
        from .__init__ import bar, boxwhisker, hist, line, scatter, strip
        kwargs = dict_update_nested(self.input_kwargs,kwargs)
        setattr(self,'folder_name',folder_name)
        args = []
        individual_kwargs_list = []

        # HANDLE ARGS
        for ar in temp_args:
            if isinstance(ar,dict):
                individual_kwargs_list[-1] = ar
            else:
                args.append(ar)
                individual_kwargs_list.append({})

        # HANDLE KWARGS AND SET SELF ITEMS
        for name, value in kwargs.items(): setattr(self, name, value)
        if len(self.input_args) != 0 and len(args) == 0:  args = self.input_args

        # INITIALIZE SOME DEFAULTS
        if 'figsize' not in kwargs: self.figsize=(4,3)

        if not hasattr(self, 'shape'): self.shape = (1,len(args))
        self.empty_locator = np.zeros(shape=self.shape)

        try:
            # LOAD SETTINGS FROM THE FIRST PLOT TO CONTROL FIGURE THEME
            template_plot = args[0][0] if isinstance(args[0], list) or isinstance(args[0], tuple) else args[0]
            first_plot_settings = template_plot.get_copy_settings()

            self.back_color = first_plot_settings['back_color']
            self.line_color = first_plot_settings['line_color']
            self.grid_color = first_plot_settings['grid_color']

            if first_plot_settings['transparent']: self.back_color = to_rgb(self.back_color) + tuple([0])
            if first_plot_settings['darkmode']: self.line_color,self.back_color = 'white','black'

            # SET ALL PLT DEFAULT COLORS BASED ON LINE AND BACK COLOR AND GRID_COLOR
            plt.rcParams["figure.facecolor"] = self.back_color  # Background color of the plot
            plt.rcParams["axes.facecolor"] = self.back_color  # Axes background color
            plt.rcParams["axes.edgecolor"] = self.line_color  # Axes border color
            plt.rcParams["axes.labelcolor"] = self.line_color  # Axis labels color
            plt.rcParams['legend.facecolor'] = self.back_color  # Legend background
            plt.rcParams["xtick.color"] = self.line_color  # X-axis tick color
            plt.rcParams["ytick.color"] = self.line_color  # Y-axis tick color
            plt.rcParams["grid.color"] = self.grid_color  # Gridline color

        except AttributeError:
            print('SKIPPED LOADING SETTINGS')

        # INITIALIZE SUBPLOTS
        self.fig, self.axs = plt.subplots(self.shape[0], self.shape[1],**kwargs)
        self.set_ax_from_collection(ax_num=ax_num)

        self.counter = 0
        self.abs_counter = 0
        self.rps = []

        # ITERATE THROUGH THE EMPTY SUBPLOT POSITIONS
        for ar in args:
            row, col = self.get_next_position()
            rps = ar if isinstance(ar, list) or isinstance(ar, tuple) else [ar]

            # IF MULTIPLE READYPLOTS ARE PASSED IN A LIST TO ONE POSITION, STACK THEM, ELSE JUST APPLY FOR SINGLE
            for rp in rps:
                # COPY SETTINGS
                current_settings = rp.get_copy_settings(include_problematic=True)
                current_settings = dict_update_nested(current_settings,individual_kwargs_list[self.abs_counter])

                # HANDLE SOME UNIQUE VARIABLES FOR PROPER BEHAVIOR
                current_settings['first_time_legend'] = True
                if self.shape[0] == 1:
                    try:
                        current_settings['input_ax'] = self.axs[col]
                    except:
                        current_settings['input_ax'] = self.axs
                elif self.shape[1] == 1: current_settings['input_ax'] = self.axs[row]
                else: current_settings['input_ax'] = self.axs[row, col]

                if first_plot_settings['transparent']: current_settings['transparent'] = True
                if first_plot_settings['darkmode']: current_settings['darkmode'] = True

                # DELETE SOME PROBLEMATIC VARIABLES THAT MAY HAVE BEEN FETCHED LIKE FIG AND AX
                if 'fig' in current_settings: del current_settings['fig']
                if 'ax' in current_settings: del current_settings['ax']

                # CREATE A NEW READYPLOT ITEM WITH COPIED SETTINGS BASED ON PLOT TYPE
                if rp.get('plot_type') == 'bar': new_rp = bar(**current_settings)
                elif rp.get('plot_type') == 'boxwhisker': new_rp = boxwhisker(**current_settings)#,input_ax=self.axs[row,col])
                elif rp.get('plot_type') == 'hist': new_rp = hist(**current_settings)
                elif rp.get('plot_type') == 'line': new_rp = line(**current_settings)
                elif rp.get('plot_type') == 'scatter': new_rp = scatter(**current_settings)
                elif rp.get('plot_type') == 'strip': new_rp = strip(**current_settings)
                else: new_rp = None
                new_rp.plot(save=False)
                self.rps.append(new_rp)

            self.empty_locator[row][col] = 1
            self.abs_counter += 1

        # SET FIGURE SIZE BASED ON THE INPUT FIGSIZE AND THE TILE SHAPE
        self.fig.set_size_inches(self.figsize[0]*self.shape[1],self.figsize[1]*self.shape[0])
        plt.tight_layout()

        # FIND ALL THE EMPTY AXES AND SET THEM TO BE INVISIBELE
        while self.abs_counter < self.shape[0]*self.shape[1]:
            row, col = self.get_next_position()

            self.axs[row,col].spines['top'].set_visible(False)
            self.axs[row,col].spines['right'].set_visible(False)
            self.axs[row,col].spines['bottom'].set_visible(False)
            self.axs[row,col].spines['left'].set_visible(False)
            self.axs[row,col].tick_params(axis='both', which='both', length=0, width=0, colors='none')
            self.axs[row,col].set_xlabel('', color='none')
            self.axs[row,col].set_ylabel('', color='none')
            self.axs[row,col].set_xticklabels([], color='none')
            self.axs[row,col].set_yticklabels([], color='none')
            self.axs[row,col].grid(False)
            self.axs[row,col].set_facecolor('none')

            self.abs_counter += 1

        # LOCATE EMPTY AXES
        for row in range(self.empty_locator.shape[0]):
            if np.any(self.empty_locator[row][:] == 0):
                filled_axes = []
                for col in range(self.empty_locator.shape[1]):
                    if self.empty_locator[row,col] == 1:
                        filled_axes.append(self.axs[row,col])

                # GET WIDTH OF SUBPLOTS
                first_pos = self.axs[0,0].get_position()
                second_pos = self.axs[0,1].get_position()
                sub_width = second_pos.x0 - first_pos.x0

                # CENTER EXISTING SUBPLOTS TO FILL THE SPACE
                if len(filled_axes) > 0:
                    current_pos = filled_axes[0].get_position()
                    current_x = current_pos.x0 + ((self.shape[1] - len(filled_axes))/2) * sub_width
                    for ax in filled_axes:
                        pos = ax.get_position()
                        ax.set_position([current_x, pos.y0, pos.width, pos.height])
                        current_x += sub_width

        # SAVE AND RETURN FIG AND AXES
        if save: self.save()
        return self.fig, self.axs

#%%---------------------------------------------------------------------------------------------------------------------
# LOCAL METHODS
#-----------------------------------------------------------------------------------------------------------------------
    def get_next_position(self):
        # CALCULATE ROW AND COLUMN INDICES BASED ON COUNTER
        rows, cols = self.shape
        row = self.counter // cols
        col = self.counter % cols

        # INCREMENT AND WRAP AROUND WHEN COLS EXCEEDED
        self.counter = (self.counter + 1) % (rows * cols)
        return row, col

    def get_subplot_coordinates(self,sub_num):
        # GET COORDINATES BASED ON THE NUMBER OF THE FIGURE
        nrows,ncols = self.shape[0], self.shape[1]
        if sub_num < 0 or sub_num >= nrows * ncols:
            raise ValueError(f"Invalid subplot number. It should be between 1 and {nrows * ncols}.")
        row = sub_num // ncols
        col = sub_num % ncols
        return row, col

    def kwarg_conflict_resolver(self, kwargs, conflict_vars):
        # COMBINE INPUT KWARGS WITH GENERAL KWARGS
        if len(kwargs) != 0: kwargs = {**self.kwargs, **kwargs}
        else: kwargs = self.kwargs

        # FOR VAR IN THE SUPPLIED CONFLICT_VARS LIST, IF IT IS IN THE SUPPLIED KWARGS USE IT, ELSE GET SELF.VAR
        outputs = []
        for var in conflict_vars:
            if var in kwargs:
                outputs.append(kwargs[var])
                del kwargs[var]
            else: outputs.append(getattr(self,var,None))

        # RETURN UPDATED KWARGS LIST AND UNPACKED OUTPUTS
        return kwargs, *outputs

    def save(self, **kwargs):
        # IF THE FOLDER NAME DOES NOT HAVE A '.' USE SAVE NAME AUTOPOPULATED FUNCTION WHICH BUILDS A NAME
        if '.' not in self.folder_name:
            save_name, dir_name = self.save_name_autopopulated()

        # IF A '.' IS IN THE FOLDER NAME, JUST USE THAT AS THE ENTIRE SAVE
        else:
            self.dir_name = self.folder_name.split(os.sep)[:-1]
            self.dir_name = os.path.join(os.sep, *self.dir_name) if self.folder_name[0] == os.sep else os.path.join('',
                                                                                                                    *self.dir_name)
            save_name, dir_name = self.folder_name, self.dir_name

        # TRY TO MAKE A DIRECTORY OR USE THE CURRENT ONE
        try:
            os.mkdir(dir_name)
        except FileExistsError:
            print(f"Directory '{dir_name}' already exists, overwriting and/or adding data.")
        print(f"Directory '{dir_name}' created successfully.")

        # SAVE FIGURE
        self.fig.savefig(save_name, bbox_inches='tight', **kwargs) #transparent=self.transparent, **kwargs)
        return self.fig, self.axs

    def save_name_autopopulated(self):
        # MAKE SAVE NAME FROM DF.NAME (SET DURING SET_TITLES) AND PLOT TYPE, HANDLE "/"
        self.save_name = 'SUBPLOTS'

        # MAKE AND RETURN SAVE NAME AND DIRECTORY NAME
        save_name = Path(os.path.join(self.folder_name + os.sep, self.save_name + '.png'))
        dir_name = self.folder_name
        return save_name,dir_name

    def get_rps(self):
        return self.rps

    def set_ax_from_collection(self,ax_num=0):
        row, col = self.get_subplot_coordinates(ax_num)
        if self.shape[0] == 1:
            try:
                self.ax = self.axs[col]
            except:
                self.ax = self.axs
        elif self.shape[1] == 1: self.ax = self.axs[row]
        else: self.ax = self.axs[row][col]

#%%---------------------------------------------------------------------------------------------------------------------
# EXTRA MATPLOTLIB TYPE FUNCTIONS WHICH USERS MIGHT EXPECT TO NEED
#-----------------------------------------------------------------------------------------------------------------------
    # %% AXES
    def xlim(self,*args,**kwargs):
        self.set_xlim(*args,**kwargs)
    def ylim(self,*args,**kwargs):
        self.set_ylim(*args,**kwargs)
    def set_xlim(self,*args,**kwargs):
        self.ax.set_xlim(*args,**kwargs)
    def set_ylim(self,*args,**kwargs):
        self.ax.set_ylim(*args,**kwargs)
    def get_xlim(self,*args,**kwargs):
        self.ax.get_xlim(*args,**kwargs)
    def get_ylim(self,*args,**kwargs):
        self.ax.get_ylim(*args,**kwargs)

    def xticks(self,*args,**kwargs):
        self.fig.xticks(*args,**kwargs)
    def yticks(self,*args,**kwargs):
        self.fig.yticks(*args,**kwargs)
    def get_xticks(self,*args,**kwargs):
        self.ax.get_xticks(*args,**kwargs)
    def get_yticks(self,*args,**kwargs):
        self.ax.get_yticks(*args,**kwargs)
    def get_xticklabels(self,*args,**kwargs):
        self.ax.get_xticklabels(*args,**kwargs)
    def get_yticklabels(self,*args,**kwargs):
        self.ax.get_yticklabels(*args,**kwargs)

    def gca(self,*args,**kwargs):
        plt.gca(*args,**kwargs)
    def gcf(self,*args,**kwargs):
        plt.gcf(*args,**kwargs)

    def axhline(self,*args,**kwargs):
        self.ax.axhline(*args,**kwargs)
    def axvline(self,*args,**kwargs):
        self.ax.axvline(*args,**kwargs)
    def grid(self,*args,**kwargs):
        self.ax.grid(*args,**kwargs)

    def set_aspect(self,*args,**kwargs):
        self.ax.set_aspect(*args,**kwargs)
    def get_aspect(self,*args,**kwargs):
        self.ax.get_aspect(*args,**kwargs)

    def set_facecolor(self,*args,**kwargs):
        self.ax.set_facecolor(*args,**kwargs)
    def get_facecolor(self,*args,**kwargs):
        self.ax.get_facecolor(*args,**kwargs)

    def set_position(self,*args,**kwargs):
        self.ax.set_position(*args,**kwargs)
    def get_position(self,*args,**kwargs):
        self.ax.get_position(*args,**kwargs)

    # %% TITLES, LABELS
    def title(self,*args,**kwargs):
        self.ax.set_title(*args,**kwargs)
    def get_title(self,*args,**kwargs):
        self.ax.get_title(*args,**kwargs)
    def xlabel(self,*args,**kwargs):
        self.ax.set_xlabel(*args,**kwargs)
    def get_xlabel(self,*args,**kwargs):
        self.ax.get_xlabel(*args,**kwargs)
    def ylabel(self,*args,**kwargs):
        self.ax.set_ylabel(*args,**kwargs)
    def get_ylabel(self,*args,**kwargs):
        self.ax.get_ylabel(*args,**kwargs)

    # %% LEGENDS
    def legend(self,*args,**kwargs):
        included_keywords = ['loc', 'numpoints', 'markerscale',
                             'markerfirst', 'reverse', 'scatterpoints', 'scatteryoffsets', 'prop',
                             'fontsize', 'labelcolor', 'borderpad', 'labelspacing', 'handlelength',
                             'handleheight', 'handletextpad', 'borderaxespad', 'columnspacing', 'ncols',
                             'mode', 'fancybox', 'shadow', 'title', 'title_fontsize', 'framealpha',
                             'edgecolor', 'facecolor', 'bbox_transform', 'frameon',
                             'handler_map', 'title_fontproperties', 'alignment', 'ncol', 'draggable']
        filtered_properties = {}
        for key,value in self.ax.get_legend().properties().items():
            if key in included_keywords: filtered_properties[key] = value
            if key == 'title': filtered_properties[key] = value.get_text()
        filtered_properties = dict_update_nested(filtered_properties, kwargs)

        handles, labels = self.ax.get_legend_handles_labels()

        text_color = self.ax.get_legend().get_texts()[0].get_color()
        text_fontweight = self.ax.get_legend().get_texts()[0].get_fontweight()
        text_fontsize = self.ax.get_legend().get_texts()[0].get_fontsize()

        legend = self.ax.legend(handles,labels,**filtered_properties)

        for text in legend.get_texts():
            text.set_color(text_color)
            text.set_fontweight(text_fontweight)
            text.set_fontsize(text_fontsize)

        legend.get_title().set_color(text_color)
        legend.get_title().set_fontweight(text_fontweight)

        return legend
    def get_legend(self,*args,**kwargs):
        self.legend = self.ax.get_legend(*args,**kwargs)
        return self.legend
    def text(self,*args,**kwargs):
        self.fig.text(*args,**kwargs)
    def get_texts(self,*args,**kwargs):
        self.fig.get_texts(*args,**kwargs)
    def figtext(self,*args,**kwargs):
        self.fig.figtext(*args,**kwargs)
    def annotate(self,*args,**kwargs):
        self.fig.annotate(*args,**kwargs)
    def suptitle(self,*args,**kwargs):
        self.fig.suptitle(*args,**kwargs)
    def get_suptitle(self,*args,**kwargs):
        self.fig.get_suptitle(*args,**kwargs)
    def add_patch(self,*args,**kwargs):
        if not isinstance(args, list): args = list(args)
        for arg in args:
            self.ax.add_patch(arg)
    def add_rectangle(self,*args,**kwargs):
        rect = patches.Rectangle((args[0], args[1]), args[2], args[3], **kwargs)
        self.ax.add_patch(rect)
    def add_line(self,*args,**kwargs):
        line = mlines.Line2D(args[0], args[1], **kwargs)
        self.ax.add_line(line)

    # %% FIGURE AND LAYOUT CUSTOMIZATION
    def set_figheight(self,val,**kwargs):
        self.fig_height = val
        self.fig.set_figheight(self.fig_height,**kwargs)
    def get_figheight(self,*args,**kwargs):
        self.fig.get_figheight(*args,**kwargs)
    def set_figwidth(self,val,**kwargs):
        self.fig_width = val
        self.fig.set_figwidth(self.fig_width,**kwargs)
    def get_figwidth(self,*args,**kwargs):
        self.fig.get_figwidth(*args,**kwargs)
    def show(self):
        self.fig.show()
    def draw(self):
        self.fig.draw()