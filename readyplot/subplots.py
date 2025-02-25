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
from pathlib import Path

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
    def plot(self,*temp_args,save=True,folder_name = "OUTPUT_FIGURES",adjust_mismatch=True,**kwargs):
        from .__init__ import bar, boxwhisker, hist, line, scatter
        kwargs = dict_update_nested(self.input_kwargs,kwargs)
        setattr(self,'folder_name',folder_name)
        args = []
        individual_kwargs_list = []

        for ar in temp_args:
            if isinstance(ar,dict):
                individual_kwargs_list[-1] = ar
            else:
                args.append(ar)
                individual_kwargs_list.append({})

        for name, value in kwargs.items(): setattr(self, name, value)

        if len(self.input_args) != 0 and len(args) == 0:  args = self.input_args

        if 'figsize' not in kwargs: self.figsize=(4,3)

        if not hasattr(self, 'shape'): self.shape = (1,len(args))
        self.empty_locator = np.zeros(shape=self.shape)

        try:
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

        self.fig, self.axs = plt.subplots(self.shape[0], self.shape[1],**kwargs)

        self.counter = 0
        self.abs_counter = 0
        self.rps = []

        for ar in args:
            row, col = self.get_next_position()
            rps = ar if isinstance(ar, list) or isinstance(ar, tuple) else [ar]

            for rp in rps:
                current_settings = rp.get_copy_settings(include_problematic=True)
                current_settings = dict_update_nested(current_settings,individual_kwargs_list[self.abs_counter])

                if self.shape[0] == 1: current_settings['input_ax'] = self.axs[col]
                elif self.shape[1] == 1: current_settings['input_ax'] = self.axs[row]
                else: current_settings['input_ax'] = self.axs[row, col]

                if first_plot_settings['transparent']: current_settings['transparent'] = True
                if first_plot_settings['darkmode']: current_settings['darkmode'] = True

                if 'fig' in current_settings: del current_settings['fig']
                if 'ax' in current_settings: del current_settings['ax']

                if rp.get('plot_type') == 'bar': new_rp = bar(**current_settings)
                elif rp.get('plot_type') == 'boxwhisker': new_rp = boxwhisker(**current_settings)#,input_ax=self.axs[row,col])
                elif rp.get('plot_type') == 'hist': new_rp = hist(**current_settings)
                elif rp.get('plot_type') == 'line': new_rp = line(**current_settings)
                elif rp.get('plot_type') == 'scatter': new_rp = scatter(**current_settings)
                else: new_rp = None
                new_rp.plot(save=False)

                self.rps.append(new_rp)


            self.empty_locator[row][col] = 1

            self.abs_counter += 1

        self.fig.set_size_inches(self.figsize[0]*self.shape[1],self.figsize[1]*self.shape[0])
        plt.tight_layout()

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

        for row in range(self.empty_locator.shape[0]):
            if np.any(self.empty_locator[row][:] == 0):
                filled_axes = []
                for col in range(self.empty_locator.shape[1]):
                    if self.empty_locator[row,col] == 1:
                        filled_axes.append(self.axs[row,col])

                first_pos = self.axs[0,0].get_position()
                second_pos = self.axs[0,1].get_position()
                sub_width = second_pos.x0 - first_pos.x0

                current_pos = filled_axes[0].get_position()
                current_x = current_pos.x0 + ((self.shape[1] - len(filled_axes))/2) * sub_width
                for ax in filled_axes:
                    pos = ax.get_position()
                    ax.set_position([current_x, pos.y0, pos.width, pos.height])
                    current_x += sub_width


        if save: self.save()

        return self.fig, self.axs

    def get_next_position(self):
        # Calculate the row and column indices based on the counter
        rows, cols = self.shape
        row = self.counter // cols  # Integer division to find the row
        col = self.counter % cols  # Modulo to find the column

        # Increment the counter, and wrap around when it exceeds the total number of subplots
        self.counter = (self.counter + 1) % (rows * cols)

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