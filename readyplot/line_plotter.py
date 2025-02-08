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

class LinePlotter(BasePlotter):
    def __init__(self, input_dict, **kwargs):
        super().__init__(input_dict, **kwargs)
        if self.markers == False:
            self.markers = [False]
        
    def just_plot(self,**kwargs):
        kwargs, DF, palette, style, markers, ax = super().kwarg_conflict_resolver(
            kwargs, ['DF', 'palette', 'style', 'markers', 'ax'])

        defaults_list = [self.colors[0:len(self.unique)], self.zlab, self.markers, self.ax]

        palette, style, markers, ax = super().var_existence_check(
            [palette, style, markers, ax],
            ['palette', 'style', 'markers', 'ax'],
            defaults_list, kwargs=kwargs)

        xlab,ylab,zlab = check_labels_in_DF(self.DF,self.xlab,self.ylab,self.zlab)
        if zlab is None:
            zlab = xlab

        sns.lineplot(
            x=self.xlab, y=self.ylab, data=DF, hue=self.zlab,
            palette=palette, style=style, markers=markers,
            ax=ax, **kwargs)

    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        for base in type(self).mro():
            if name in base.__dict__:
                return base.__dict__[name].__get__(self)
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")