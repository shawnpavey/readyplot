#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 14:34:59 2025
Custom plotter function which copies styles used by Shawn Pavey in plotting software. Many
inputs are customizable, but defaults work well. This script contains two
functions: custom_plotter (full plotting + formating) and plotting software (only
reformats given figures).
@author: paveyboys
"""
#%% IMPORT PACKAGES
import seaborn as sns
from .base_plotter import BasePlotter
from .utils import check_labels_in_DF
import matplotlib.pyplot as plt

#%% INITIALIZE CHILD CLASS
class HistPlotter(BasePlotter):
    def __init__(self, input_dict, **kwargs):
        super().__init__(input_dict, **kwargs)
        self.plot_type = 'hist'

    # %% DEFINE PLOTTER, PREPARE INPUTS
    def just_plot(self,**kwargs):
        kwargs, DF, palette, ax, legend = self.generate_resolver_lists(locals(), kwargs)
        xlab, ylab, zlab, palette = self.label_prep(locals())

        # %% PLOT WITH SEABORN
        sns.histplot(
            x=xlab,y=ylab, data=DF,
            hue=zlab, palette=palette,
            ax=ax, fill=not self.apply_color_lines_only,**kwargs)

        #%% EXTRA PLOT EDITING

    # %% LOAD ALL PARENT METHODS UNLESS THEY EXIST HERE
    def __getattr__(self, name):
        super().__getattr__(name)

    # %% CUSTOM METHODS
    def generate_resolver_lists(self,l,kwargs):
        kwargs, DF, palette, ax, legend = super().kwarg_conflict_resolver(
            kwargs, ['DF', 'palette', 'ax', 'legend'])
        return kwargs, DF, palette, ax, legend

    def label_prep(self,l):
        if not l['palette']:
            if len(self.unique) == 1:
                zlab = None
                palette = None
            else:
                zlab = self.zlab
                palette = self.colors[0:len(self.unique)]
        else:
            palette = l['palette']
            if len(self.unique) == 1:
                zlab = None
            else:
                zlab = self.zlab

        xlab, ylab, zlab = check_labels_in_DF(self.DF, self.xlab, self.ylab, self.zlab)

        return xlab, ylab, zlab, palette