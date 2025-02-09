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
import numpy as np
from .base_plotter import BasePlotter
from .utils import check_labels_in_DF, match_rgba_to_color, find_closest

class BoxWhiskerPlotter(BasePlotter):
    def __init__(self, input_dict, **kwargs):
        super().__init__(input_dict, **kwargs)
        self.plot_type = 'boxwhisker'
        
    def just_plot(self,**kwargs):
        self.DF[self.xlab] = self.DF[self.xlab].astype(str)

        kwargs,DF,boxprops,showfliers,showmeans,meanprops,palette,linecolor,linewidth, width,dodge,ax = super().kwarg_conflict_resolver(
            kwargs, ['DF','boxprops','showfliers','showmeans','meanprops','palette','linecolor','linewidth','width','dodge','ax'])

        defaults_list =[self.colors[0:len(self.unique)],{'alpha': 1, 'edgecolor': self.line_color},
                        False,True,{"marker": "x", "markeredgecolor": self.line_color},self.line_color,self.def_line_w,
                        self.box_width,True,self.ax]

        palette,boxprops,showfliers,showmeans,meanprops,linecolor,linewidth,width,dodge,ax = super().var_existence_check(
            [palette,boxprops,showfliers,showmeans,meanprops,linecolor,linewidth,width,dodge,ax],
            ['palette','boxprops','showfliers','showmeans','meanprops','linecolor','linewidth','width','dodge','ax'],
            defaults_list,kwargs=kwargs)

        try:
            temp = DF[self.ylab]
        except KeyError:
            DF[self.ylab] = np.nan
        if DF[self.ylab].isna().all():
            DF[self.ylab] = DF[self.xlab]
            DF[self.xlab] = self.ylab

        xlab,ylab,zlab = check_labels_in_DF(self.DF,self.xlab,self.ylab,self.zlab)
        if zlab is None:
            zlab = xlab
            dodge = False

        sns.boxplot(
            x=xlab, y=ylab, data=DF,
            hue=zlab,
            showfliers=showfliers,showmeans=showmeans,
            meanprops=meanprops,
            palette=palette,linecolor=linecolor,
            linewidth=linewidth, width=width,
            dodge = dodge,ax=ax,fill=not self.apply_color_lines_only,**kwargs)

        dark_palette = []
        for i in range(len(self.DF[self.zlab].unique())):
            dark_palette.append(self.line_color)
        if self.apply_color_lines_only:
            dark_palette = palette
        for i, category in enumerate(self.DF[self.zlab].unique()):
            df_copy = self.DF.copy()
            df_copy.loc[df_copy[self.zlab] != category, self.ylab] = np.nan
            sns.stripplot(
                data=df_copy, x=xlab, y=ylab,hue=zlab,
                dodge = dodge,palette=dark_palette,
                marker=self.marker_dict[category],ax=ax,size=3)
        plt.xlabel(" ")

    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        for base in type(self).mro():
            if name in base.__dict__:
                return base.__dict__[name].__get__(self)
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

            
    
