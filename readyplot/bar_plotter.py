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
from .utils import rgba_to_named_color, match_rgba_to_color


class BarPlotter(BasePlotter):
    def __init__(self, DFs=None, x=None, y=None, z=None, xlab='xlab', ylab='ylab', zlab='zlab',
                 input_fig = None,
                 input_ax = None,
                 colors=['g','r','b','y','c','m','k','w'],
                 markers=['o','s','D','p','h','*','x','+','^','v','>','<'],
                 hatches = ['//','...','--','++','OO','**'],
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
                 plot_type = 'bar',
                 sci_x_lims = (0, 1),
                 sci_y_lims = (0, 1),
                 capsize=0.4):

        super().__init__(DFs=DFs, x=x, y=y, z=z, xlab=xlab, ylab=ylab, zlab=zlab,
                         input_fig=input_fig,
                         input_ax=input_ax,
                         colors=colors,
                         markers=markers,
                         hatches=hatches,
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
                         sci_y_lims = sci_y_lims,
                         capsize = capsize)
        self.plot_type = plot_type
        self.hatches = hatches
        self.capsize = capsize
        
    def just_plot(self,**kwargs):
        self.DF[self.xlab] = self.DF[self.xlab].astype(str)

        kwargs,DF,markers,palette,dodge,ax,capsize,linewidth,width = super().kwarg_conflict_resolver(
            kwargs, ['DF','markers','palette','dodge','ax','capsize','linewidth','width'])

        defaults_list = [self.colors[0:len(self.unique)], self.def_line_w, self.box_width]

        palette, linewidth, width = super().var_existence_check(
            [palette, linewidth, width],
            ['palette', 'linewidth', 'width'],
            defaults_list, kwargs=kwargs)

        sns.barplot(
            x=self.xlab, y=self.ylab, data=DF,
            hue =self.zlab,
            palette=palette,
            linewidth=linewidth,width=width,
            dodge = dodge,ax=ax, err_kws={'color': 'k','linewidth': self.def_line_w}, capsize=capsize,
            **kwargs)
        dark_palette = []
        while len(self.unique) > len(self.hatches):
            self.hatches.extend(self.hatches)

        for bar in self.ax.patches:
            hue_group = bar.get_label()
            match_rgba_to_color(bar.get_facecolor(), self.colors)
            current_face_color =  match_rgba_to_color(bar.get_facecolor(), self.colors)#rgba_to_named_color(bar.get_facecolor())
            bar.set_hatch(self.hatches[self.colors.index(current_face_color)])
            bar.set_edgecolor('black')
            hatch_pattern = self.hatches[self.colors.index(current_face_color)]
            hatch_density = 1
            bar.set_hatch(f"{hatch_pattern * hatch_density}")
            bar.set_linewidth(self.def_line_w)

        for i in range(len(self.DF[self.zlab].unique())):
            dark_palette.append('k')
        for i, category in enumerate(self.DF[self.zlab].unique()):
            df_copy = self.DF.copy()
            df_copy.loc[df_copy[self.zlab] != category, self.ylab] = np.nan
            try:
                sns.stripplot(
                    data=df_copy, x=self.xlab, y=self.ylab,hue=self.zlab,
                    dodge = self.dodge,palette=dark_palette,
                    marker=self.marker_dict[category],ax=self.ax)
            except KeyError:
                pass
        plt.xlabel(" ")

    def plot(self, save=True,**kwargs):
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


            
    
