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

#-----------------------------------------------------------------------------------------------------------------------
# CHILD CLASS MAIN
#-----------------------------------------------------------------------------------------------------------------------
#%% INITIALIZE CHILD CLASS
class LinePlotter(BasePlotter):
    def __init__(self, input_dict,**kwargs):
        super().__init__(input_dict,**kwargs)
        self.plot_type = 'line'
        self.markers = [False] if self.markers == False else self.markers

    # %% DEFINE PLOTTER, PREPARE INPUTS
    def just_plot(self,**kwargs):
        conflict_vars,defaults_list,inputs,input_keys,outputs = self.generate_resolver_lists(locals(),kwargs)
        DF, kwargs, palette, style, markers, ax = outputs
        palette, style, markers, ax = super().var_existence_check(inputs,input_keys,defaults_list, kwargs=kwargs)
        xlab,ylab,zlab = self.label_prep(locals())

        # %% PLOT WITH SEABORN
        sns.lineplot(
            x=xlab, y=ylab, data=DF, hue=zlab,
            palette=palette, style=style, markers=markers,
            ax=ax, **kwargs)

        #%% EXTRA PLOT EDITING
        self.plot_errors(xlab,ylab,zlab)
# -----------------------------------------------------------------------------------------------------------------------
# LOCAL METHODS
# -----------------------------------------------------------------------------------------------------------------------
    # %% LOAD ALL PARENT METHODS UNLESS THEY EXIST HERE
    def __getattr__(self, name):
        super().__getattr__(name)

    # %% CUSTOM METHODS
    #%% FIX
    def generate_resolver_lists(self,l,kwargs):
        conflict_vars = ['DF','palette', 'style', 'markers', 'ax']
        defaults_list = [self.colors[0:len(self.unique)], self.zlab, self.markers, self.ax]
        kwargs, DF, palette, style, markers, ax = super().kwarg_conflict_resolver(kwargs,conflict_vars)

        inputs = [palette, style, markers, ax]
        input_keys = ['palette', 'style', 'markers', 'ax']
        outputs =  [DF, kwargs, palette, style, markers, ax]

        return conflict_vars, defaults_list, inputs, input_keys, outputs

    def label_prep(self, l):
        xlab, ylab, zlab = check_labels_in_DF(self.DF, self.xlab, self.ylab, self.zlab)
        return xlab, ylab, zlab
