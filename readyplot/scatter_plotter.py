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
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
from .base_plotter import BasePlotter
from .utils import check_labels_in_DF

class ScatterPlotter(BasePlotter):
    def __init__(self, input_dict, **kwargs):
        super().__init__(input_dict, **kwargs)
        self.trendline = input_dict['trendline']
        self.show_r2 = input_dict['show_r2']
        if not self.trendline or not self.show_r2:
            self.plot_type = "scatter"
        
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

        sns.scatterplot(
            x=xlab, y=ylab, data=DF, hue=zlab,
            palette=palette, style=style, markers=markers,
            ax=ax, **kwargs)

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

    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        for base in type(self).mro():
            if name in base.__dict__:
                return base.__dict__[name].__get__(self)
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")