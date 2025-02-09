#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A child class for the base plotter which produces scatter plots with potential trendline overlays
@author: Shawn Pavey
"""
#%% IMPORT PACKAGES
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
from .base_plotter import BasePlotter
from .utils import check_labels_in_DF

#%% INITIALIZE CHILD CLASS
class ScatterPlotter(BasePlotter):
    def __init__(self, input_dict, **kwargs):
        super().__init__(input_dict, **kwargs)
        self.plot_type = 'scatter'
        self.trendline = input_dict['trendline']
        self.show_r2 = input_dict['show_r2']
        if not self.trendline or not self.show_r2:
            self.plot_type = "scatter"

    # %% DEFINE PLOTTER, PREPARE INPUTS
    def just_plot(self,**kwargs):
        kwargs, DF, palette, style, markers, ax = super().kwarg_conflict_resolver(
            kwargs,['DF','palette', 'style', 'markers', 'ax'])

        defaults_list = [self.colors[0:len(self.unique)], self.zlab, self.markers, self.ax]

        palette, style, markers, ax = super().var_existence_check(
            [palette, style, markers, ax],
            ['palette', 'style', 'markers', 'ax'],
            defaults_list, kwargs=kwargs)

        xlab,ylab,zlab = check_labels_in_DF(self.DF,self.xlab,self.ylab,self.zlab)
        if zlab is None:
            zlab = xlab

        # %% PLOT WITH SEABORN
        sns.scatterplot(
            x=xlab, y=ylab, data=DF, hue=zlab,
            palette=palette, style=style, markers=markers,
            ax=ax, **kwargs)

        #%% EXTRA PLOT EDITING
        g_counter = 0
        for g in self.unique:
            if self.trendline:
                sns.regplot(
                    x=self.xlab, y=self.ylab, data=self.DF.loc[self.DF[self.zlab] == g],
                    ci=None,color = self.colors[self.unique.index(g)],
                    scatter=False,ax=self.ax)

                if self.show_r2:
                    tempDF =  self.DF.loc[self.DF[self.zlab] == g]
                    x = tempDF[self.xlab].to_numpy()
                    y = tempDF[self.ylab].to_numpy()
                    slope, intercept, r_value, p_value, std_err = stats.linregress(x.astype(float),y.astype(float))
                    r_squared = r_value ** 2
                    plt.text(self.max_list_x[self.DF_counter]*self.annote_x_start,
                                self.max_list_y[self.DF_counter]*(self.annote_y_start - 0.05*g_counter),
                                f"R-squared = {r_squared:.2f}",
                                fontsize=int(0.75*self.def_font_sz),color = self.colors[self.unique.index(g)])
            g_counter += 1


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