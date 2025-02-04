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
    def __init__(self, DFs=None, x=None, y=None, z=None, xlab='xlab', ylab='ylab', zlab='zlab',
                 input_fig = None,
                 input_ax = None,
                 colors=['g','r','b','y','c','m','k','w'],
                 markers=['o','s','D','p','h','*','x','+','^','v','>','<'],
                 def_font_sz = 16,
                 def_line_w = 1.5,
                 folder_name="OUTPUT_FIGURES",
                 dpi = 300,
                 sns_palette = "deep",
                 sns_style = "ticks",
                 sns_context = "notebook",
                 fontweight='bold',
                 box_edges = ['bottom','left'],
                 fig_width = 7,
                 fig_height = 5,
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
                 plot_type = 'box_whisker',
                 sci_x_lims = (0, 1),
                 sci_y_lims = (0, 1)):

        super().__init__(DFs=DFs, x=x, y=y, z=z, xlab=xlab, ylab=ylab, zlab=zlab,
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
                         low_y_cap0 = low_y_cap0,
                         dodge = dodge,
                         handles_in_legend = handles_in_legend,
                         box_width = box_width,
                         custom_x_label = custom_x_label,
                         custom_y_label = custom_y_label,
                         title = title,
                         sci_x_lims = sci_x_lims,
                         sci_y_lims = sci_y_lims)
        self.plot_type = plot_type
        
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


            
    
