#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A child class for the base plotter which produces line plots
@author: Shawn Pavey
"""
#%% IMPORT PACKAGES
import seaborn as sns
from .base_plotter import BasePlotter
from .utils import check_labels_in_DF

#%% INITIALIZE CHILD CLASS
class LinePlotter(BasePlotter):
    def __init__(self, input_dict, **kwargs):
        super().__init__(input_dict, **kwargs)
        self.plot_type = 'line'
        if self.markers == False:
            self.markers = [False]

    # %% DEFINE PLOTTER, PREPARE INPUTS
    def just_plot(self,**kwargs):
        kwargs, DF, palette, style, markers, ax = super().kwarg_conflict_resolver(
            kwargs, ['DF', 'palette', 'style', 'markers', 'ax'])

        defaults_list = [self.colors[0:len(self.unique)], self.zlab, self.markers, self.ax]

        palette, style, markers, ax = super().var_existence_check(
            [palette, style, markers, ax],
            ['palette', 'style', 'markers', 'ax'],
            defaults_list, kwargs=kwargs)

        xlab,ylab,zlab = check_labels_in_DF(self.DF,self.xlab,self.ylab,self.zlab)
        if zlab is None:
            zlab = xlab

        # %% PLOT WITH SEABORN
        sns.lineplot(
            x=self.xlab, y=self.ylab, data=DF, hue=self.zlab,
            palette=palette, style=style, markers=markers,
            ax=ax, **kwargs)

        #%% EXTRA PLOT EDITING


    # %% LOAD ALL PARENT METHODS UNLESS THEY EXIST HERE
    def __getattr__(self, name):
        super().__getattr__(name)

    # %% CUSTOM METHODS
    #%% FIX
    def generate_resolver_lists(self,loc_vars,kwargs):
        conflict_vars = ['DF','markers','palette','dodge','ax','capsize','linewidth','width']
        defaults_list = [self.colors[0:len(self.unique)], self.def_line_w, self.box_width]
        kwargs, DF, markers, palette, dodge, ax, capsize, linewidth, width = super().kwarg_conflict_resolver(kwargs,conflict_vars)
        inputs = [palette, linewidth, width]
        input_keys = ['palette', 'linewidth', 'width']

        outputs = [DF, markers, palette, dodge, ax, capsize, linewidth, width]

        return conflict_vars, defaults_list, inputs, input_keys, outputs