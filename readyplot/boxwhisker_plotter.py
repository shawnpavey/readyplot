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
import numpy as np
from .base_plotter import BasePlotter

class BoxWhiskerPlotter(BasePlotter):
    def __init__(self, input_dict, **kwargs):
        super().__init__(input_dict, **kwargs)
        
    def just_plot(self,**kwargs):
        self.DF[self.xlab] = self.DF[self.xlab].astype(str)

        kwargs,DF,boxprops,showfliers,showmeans,meanprops,palette,linecolor,linewidth, width,dodge,ax = super().kwarg_conflict_resolver(
            kwargs, ['DF','boxprops','showfliers','showmeans','meanprops','palette','linecolor','linewidth','width','dodge','ax'])

        defaults_list =[self.colors[0:len(self.unique)],{'alpha': 1, 'edgecolor': 'black'},
                        False,True,{"marker": "x", "markeredgecolor": "black"},'k',self.def_line_w,
                        self.box_width,True,self.ax]

        palette,boxprops,showfliers,showmeans,meanprops,linecolor,linewidth,width,dodge,ax = super().var_existence_check(
            [palette,boxprops,showfliers,showmeans,meanprops,linecolor,linewidth,width,dodge,ax],
            ['palette','boxprops','showfliers','showmeans','meanprops','linecolor','linewidth','width','dodge','ax'],
            defaults_list,kwargs=kwargs)

        sns.boxplot(
            x=self.xlab, y=self.ylab, data=DF,
            hue =self.zlab,boxprops=boxprops,
            showfliers=showfliers,showmeans=showmeans,
            meanprops=meanprops,
            palette=palette,linecolor=linecolor,
            linewidth=linewidth, width=width,
            dodge = dodge,ax=ax,**kwargs)
        dark_palette = []
        for i in range(len(self.DF[self.zlab].unique())):
            dark_palette.append('k')
        for i, category in enumerate(self.DF[self.zlab].unique()):
            df_copy = self.DF.copy()
            df_copy.loc[df_copy[self.zlab] != category, self.ylab] = np.nan
            sns.stripplot(
                data=df_copy, x=self.xlab, y=self.ylab,hue=self.zlab,
                dodge = self.dodge,palette=dark_palette, 
                marker=self.marker_dict[category],ax=ax,size=3)
        plt.xlabel(" ")
            
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


            
    
