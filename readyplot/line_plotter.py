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
import seaborn as sns
from .base_plotter import BasePlotter

class LinePlotter(BasePlotter):
    def __init__(self, input_dict, **kwargs):
        super().__init__(input_dict, **kwargs)
        if self.markers == False:
            self.markers = [False]
        
    def just_plot(self,**kwargs):
        print(self.style)
        kwargs, DF, palette, style, markers, ax = super().kwarg_conflict_resolver(
            kwargs, ['DF', 'palette', 'style', 'markers', 'ax'])

        defaults_list = [self.colors[0:len(self.unique)], self.zlab, self.markers, self.ax]

        palette, style, markers, ax = super().var_existence_check(
            [palette, style, markers, ax],
            ['palette', 'style', 'markers', 'ax'],
            defaults_list, kwargs=kwargs)
        print(self.xlab,self.ylab,self.zlab,style)
        sns.lineplot(
            x=self.xlab, y=self.ylab, data=DF, hue=self.zlab,
            palette=palette, style=style, markers=markers,
            ax=ax, **kwargs)
            
    def plot(self,save=True,**kwargs):
        super().plot(save=save)
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