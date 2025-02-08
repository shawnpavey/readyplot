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

class HistPlotter(BasePlotter):
    def __init__(self, input_dict, **kwargs):
        super().__init__(input_dict, **kwargs)
        if not self.markers == False:
            self.markers = [False]
        
    def just_plot(self,**kwargs):
        kwargs,DF,palette,ax,legend = super().kwarg_conflict_resolver(
            kwargs, ['DF','palette','ax','legend'])

        if not palette:
            if len(self.unique) == 1:
                zlab = None
                palette = None
            else:
                zlab = self.zlab
                palette = self.colors[0:len(self.unique)]
        else:
            if len(self.unique) == 1:
                zlab = None
            else:
                zlab = self.zlab

        self.DF[self.ylab] = 'fill'

        sns.histplot(
            x=self.xlab, data=DF,
            hue=zlab, palette=palette,
            ax=ax, legend=legend, **kwargs)
            
    def plot(self, save=True,**kwargs):
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