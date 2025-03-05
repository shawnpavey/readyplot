#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A child class for the base plotter which produces histograms
@author: Shawn Pavey
"""
# %% IMPORT PACKAGES
import seaborn as sns
from .base_plotter import BasePlotter
from .utils import check_labels_in_DF
import matplotlib.pyplot as plt

#%%---------------------------------------------------------------------------------------------------------------------
# CHILD CLASS MAIN
#-----------------------------------------------------------------------------------------------------------------------
# %% INITIALIZE CHILD CLASS
class HistPlotter(BasePlotter):
    def __init__(self, input_dict,**kwargs):
        super().__init__(input_dict,**kwargs)
        self.plot_type = 'hist'

    # %% DEFINE PLOTTER, PREPARE INPUTS
    def just_plot(self,**kwargs):
        self.ensure_fig_ax_exist()
        kwargs, DF, palette, ax, legend = self.generate_resolver_lists(locals(), kwargs)
        xlab, ylab, zlab, palette = self.label_prep(locals())

        print(kwargs)

        # %% PLOT WITH SEABORN
        sns.histplot(
            x=xlab,y=ylab, data=DF,
            hue=zlab, palette=palette,
            ax=ax, fill=not self.apply_color_lines_only,**kwargs)

        # %% EXTRA PLOT EDITING
        if any(getattr(self, attr) is not None for attr in self.err_names): self.plot_errors(xlab, ylab, zlab)
        super().just_plot()
#%%---------------------------------------------------------------------------------------------------------------------
# LOCAL METHODS
#-----------------------------------------------------------------------------------------------------------------------
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
            zlab,palette = (None, None) if len(self.unique) == 1 else (self.zlab,self.colors[0:len(self.unique)])
        else:
            palette = l['palette']
            zlab = None if len(self.unique) == 1 else self.zlab
        xlab, ylab, zlab = check_labels_in_DF(self.DF, self.xlab, self.ylab, self.zlab)
        return xlab, ylab, zlab, palette