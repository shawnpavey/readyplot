#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A child class for the base plotter which produces scatter plots with potential trendline overlays
@author: Shawn Pavey
"""
# %% IMPORT PACKAGES
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
from .base_plotter import BasePlotter
from .utils import check_labels_in_DF

#%%---------------------------------------------------------------------------------------------------------------------
# CHILD CLASS MAIN
#-----------------------------------------------------------------------------------------------------------------------
# %% INITIALIZE CHILD CLASS
class ScatterPlotter(BasePlotter):
    def __init__(self, input_dict,**kwargs):
        super().__init__(input_dict,**kwargs)
        self.plot_type,self.trendline,self.show_r2 = 'scatter',input_dict['trendline'],input_dict['show_r2']

    # %% DEFINE PLOTTER, PREPARE INPUTS
    def just_plot(self,**kwargs):
        self.ensure_fig_ax_exist()
        conflict_vars,defaults_list,inputs,input_keys,outputs = self.generate_resolver_lists(locals(),kwargs)
        DF, kwargs, palette, style, markers, ax = outputs
        palette, style, markers, ax = super().var_existence_check(inputs,input_keys,defaults_list, kwargs=kwargs)
        xlab,ylab,zlab = self.label_prep(locals())

        # %% PLOT WITH SEABORN
        sns.scatterplot(
            x=xlab, y=ylab, data=DF, hue=zlab,
            palette=palette, style=style, markers=markers,
            ax=ax, **kwargs)

        # %% EXTRA PLOT EDITING
        if any(getattr(self, attr) is not None for attr in self.err_names): self.plot_errors(xlab, ylab, zlab)
        self.local_trendline(locals())
        super().just_plot()

#%%---------------------------------------------------------------------------------------------------------------------
# LOCAL METHODS
#-----------------------------------------------------------------------------------------------------------------------
    # %% LOAD ALL PARENT METHODS UNLESS THEY EXIST HERE
    def __getattr__(self, name):
        super().__getattr__(name)

    # %% CUSTOM METHODS
    # %% FIX
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
        zlab = xlab if zlab is None else zlab
        return xlab, ylab, zlab

    def local_trendline(self,l):
        g_counter = 0

        for g in self.unique:
            if self.trendline:

                sns.regplot(
                    x=self.xlab, y=self.ylab, data=self.DF.loc[self.DF[self.zlab] == g],
                    ci=None, color=self.colors[self.unique.index(g)],
                    scatter=False, ax=self.ax)

                if self.show_r2:
                    tempDF = self.DF.loc[self.DF[self.zlab] == g]
                    x = tempDF[self.xlab].to_numpy()
                    y = tempDF[self.ylab].to_numpy()
                    slope, intercept, r_value, p_value, std_err = stats.linregress(x.astype(float), y.astype(float))
                    r_squared = r_value ** 2

                    plt.text(self.max_list_x[self.DF_counter] * self.annote_x_start,
                             self.max_list_y[self.DF_counter] * (self.annote_y_start - 0.05 * g_counter),
                             f"R-squared = {r_squared:.2f}",
                             fontsize=int(0.75 * self.def_font_sz), color=self.colors[self.unique.index(g)])

            g_counter += 1