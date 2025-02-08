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
import seaborn as sns
from .base_plotter import BasePlotter
from .utils import check_labels_in_DF

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

        xlab,ylab,zlab = check_labels_in_DF(self.DF,self.xlab,self.ylab,self.zlab)

        sns.histplot(
            x=xlab,y=ylab, data=DF,
            hue=zlab, palette=palette,
            ax=ax, legend=legend, **kwargs)

    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        for base in type(self).mro():
            if name in base.__dict__:
                return base.__dict__[name].__get__(self)
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")