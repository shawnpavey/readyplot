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
import scipy.stats as stats
from .base_plotter import BasePlotter

class ScatterPlotter(BasePlotter):
    def __init__(self, DFs=None, xlab=None, ylab=None, zlab=None,
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
                 fig_height = 10,
                 xtick_font_ratio = 1,
                 ytick_font_ratio = 0.9,
                 x_exp_location = 0,
                 y_exp_location = 0,
                 annote_x_start = 0.7,
                 annote_y_start = 0.7,
                 x_axis_sig_figs = 0,
                 y_axis_sig_figs = 2,
                 low_x_cap0=False,
                 low_y_cap0=False,
                 dodge = True,
                 handles_in_legend = 10,
                 box_width = 0.6,
                 custom_x_label = None,
                 custom_y_label = None,
                 title = None,
                 plot_type = 'scatter_R2'):
        super().__init__(DFs=DFs, xlab=xlab, ylab=ylab, zlab=zlab,
                         input_fig=input_fig,
                         input_ax=input_ax,
                         colors=colors,
                         markers=markers,
                         def_font_sz=def_font_sz,
                         def_line_w = def_line_w,
                         folder_name = folder_name,
                         dpi = dpi,
                         sns_palette= sns_palette,
                         sns_style = sns_style,
                         sns_context = sns_context,
                         fontweight = fontweight,
                         box_edges = box_edges,
                         fig_width = fig_width,
                         fig_height = fig_height,
                         xtick_font_ratio = xtick_font_ratio,
                         ytick_font_ratio = ytick_font_ratio,
                         x_exp_location = x_exp_location,
                         y_exp_location = y_exp_location,
                         annote_x_start = annote_x_start,
                         annote_y_start = annote_y_start,
                         x_axis_sig_figs = x_axis_sig_figs,
                         y_axis_sig_figs = y_axis_sig_figs,
                         low_x_cap0=low_x_cap0,
                         low_y_cap0=low_y_cap0,
                         dodge = dodge,
                         handles_in_legend = handles_in_legend,
                         box_width = box_width,
                         custom_x_label = custom_x_label,
                         custom_y_label = custom_y_label,
                         plot_type = plot_type,
                         title = title)
        self.plot_type = plot_type
        
    def plot(self):
        sns.scatterplot(
                x=self.xlab ,y=self.ylab ,data=self.DF,
                hue=self.zlab,palette=self.colors[0:len(self.unique)],
                style=self.zlab,markers=self.marker_dict,
                ax=self.ax,**self.kwargs)
        g_counter = 0
        for g in self.unique:
            sns.regplot(
                x=self.xlab, y=self.ylab, data=self.DF.loc[self.DF[self.zlab] == g],
                ci=None,color = self.colors[self.unique.index(g)],
                scatter=False,ax=self.ax)       
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
            
    def large_loop(self,plot_type = 'scatter_R2',save = True):
        super().large_loop(save=save)
    
    def pre_format(self,DF):
        super().pre_format(DF)
    
    def post_format(self):
        super().post_format()

    def save(self):
        super().save()