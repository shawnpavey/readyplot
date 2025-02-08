#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 14:34:59 2025
Custom plotter function which copies styles used by Shawn Pavey in Prism. Many
inputs are customizable, but defaults work well. This script contains two
functions: custom_plotter (full plotting + formating) and prism_reskin (only
reformats given figures).
@author: paveyboys
"""
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
from .base_plotter import BasePlotter

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

        sns.scatterplot(
            x=self.xlab, y=self.ylab, data=DF, hue=self.zlab,
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
            
    # def large_loop(self,plot_type = 'scatter_R2',save = True):
    #     super().large_loop(save=save)
    def plot(self,save=True,**kwargs):
        super().plot(save=save,**kwargs)
        return self.fig, self.ax
    
    def pre_format(self):
        super().pre_format()
        return self.fig, self.ax
    
    def post_format(self):
        super().post_format()
        return self.fig, self.ax

    def save(self):
        super().save()
        return self.fig, self.ax

    def show(self):
        super().show()
        return self.fig, self.ax