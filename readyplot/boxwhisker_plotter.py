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
    def __init__(self,plot_type,DFs,xlab,ylab,
                       hues=None,
                       input_fig = None,
                       input_ax = None,
                       colors=['g','r','b','y','c','m','k','w'],
                       markers=['o','s','D','p','h','*','x','+','^','v','>','<'],
                       def_font_sz = 16,
                       def_line_w = 1.5,
                       folder_name=None,
                       dpi = 300,
                       sns_palette = "deep",
                       sns_style = "ticks",
                       sns_context = "notebook",
                       fontweight='bold',
                       box_edges = ['bottom','left'],
                       fig_width = 10,
                       xtick_font_ratio = 1,
                       ytick_font_ratio = 0.9,
                       x_exp_location = 0,
                       y_exp_location = 0,
                       annote_x_start = 0.7,
                       annote_y_start = 0.7,
                       x_axis_sig_figs = 0,
                       y_axis_sig_figs = 2,
                       low_cap0 = False,
                       dodge = False,
                       handles_in_legend = 10,
                       box_width = 0.6,
                       custom_x_label = None,
                       custom_y_label = None,
                       title = None):
        super().__init__(plot_type,DFs,xlab,ylab,
                           hues,
                           input_fig,
                           input_ax,
                           colors,
                           markers,
                           def_font_sz,
                           def_line_w,
                           folder_name,
                           dpi,
                           sns_palette,
                           sns_style,
                           sns_context,
                           fontweight,
                           box_edges,
                           fig_width,
                           xtick_font_ratio,
                           ytick_font_ratio,
                           x_exp_location,
                           y_exp_location,
                           annote_x_start,
                           annote_y_start,
                           x_axis_sig_figs,
                           y_axis_sig_figs,
                           low_cap0,
                           dodge,
                           handles_in_legend,
                           box_width,
                           custom_x_label,
                           custom_y_label,
                           title)
        self.custom = 0
        
    def plot(self):
        sns.boxplot(
            x=self.xlab, y=self.ylab, data=self.DF,
            boxprops={'alpha': 1,'edgecolor':'black'},hue =self.hues,
            showfliers=False,showmeans=True,
            meanprops={"marker": "x", "markeredgecolor": "black"},
            palette=self.colors[0:len(self.unique)],linecolor='k',
            linewidth=self.def_line_w,width = self.box_width,
            dodge = self.dodge,ax=self.ax,**self.kwargs)
        dark_palette = []
        for i in range(len(self.DF[self.hues].unique())):
            dark_palette.append('k')
        for i, category in enumerate(self.DF[self.hues].unique()):
            df_copy = self.DF.copy()
            df_copy.loc[df_copy[self.hues] != category, self.ylab] = np.nan
            sns.stripplot(
                data=df_copy, x=self.xlab, y=self.ylab,hue=self.hues,
                dodge = self.dodge,palette=dark_palette, 
                marker=self.marker_dict[category],ax=self.ax)
        plt.xlabel(" ")
            
    def large_loop(self):
        super().large_loop()
    
    def pre_format(self,DF):
        super().pre_format(DF)
    
    def post_format(self):
        super().post_format()
        
            
    
