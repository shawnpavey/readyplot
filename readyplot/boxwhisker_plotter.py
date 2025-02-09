#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A child class for the base plotter which produces box whisker plots with possible scatter overlays
@author: Shawn Pavey
"""
#%% IMPORT PACKAGES
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.patches import Rectangle
from spyder_kernels.utils import mpl

from .base_plotter import BasePlotter
from .utils import check_labels_in_DF, match_rgba_to_color, find_closest

#%% INITIALIZE CHILD CLASS
class BoxWhiskerPlotter(BasePlotter):
    def __init__(self, input_dict, **kwargs):
        super().__init__(input_dict, **kwargs)
        self.plot_type = 'boxwhisker'

    # %% DEFINE PLOTTER, PREPARE INPUTS
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

        DF,xlab,ylab,zlab,dodge = self.label_prep(locals())

        # %% PLOT WITH SEABORN
        for i,u in enumerate(self.unique):
            if self.plot_line_palette:
                line_palette = self.plot_line_palette[i]
            else:
                line_palette = self.line_color
            tempDF = DF.copy()
            for v in self.unique:
                if v != u:
                    tempDF[ylab] = tempDF[ylab].astype(float)
                    tempDF.loc[tempDF[zlab]==v,ylab] = float("inf")

            sns.boxplot(
                x=xlab, y=ylab, data=tempDF,
                hue=zlab,
                showfliers=showfliers,showmeans=showmeans,
                meanprops=meanprops,
                palette=palette,linecolor=line_palette,
                linewidth=linewidth, width=width,
                dodge = dodge,ax=ax,legend=i==0,fill=not self.apply_color_lines_only,**kwargs)

        #%% EXTRA PLOT EDITING
        self.legend_fixer(locals())
        self.local_scatter(locals())


    # %% LOAD ALL PARENT METHODS UNLESS THEY EXIST HERE
    def __getattr__(self, name):
        super().__getattr__(name)

    # %% CUSTOM METHODS
    #%% FIX
    def generate_resolver_lists(self,loc_vars,kwargs):
        conflict_vars = ['DF','markers','palette','dodge','ax','capsize','linewidth','width']
        defaults_list = [self.colors[0:len(self.unique)], self.def_line_w, self.box_width]
        kwargs, DF, markers, palette, dodge, ax, capsize, linewidth, width = super().kwarg_conflict_resolver(kwargs,conflict_vars)
        inputs = [palette, linewidth, width]
        input_keys = ['palette', 'linewidth', 'width']

        outputs = [DF, markers, palette, dodge, ax, capsize, linewidth, width]

        return conflict_vars, defaults_list, inputs, input_keys, outputs


    def label_prep(self,l):
        DF,dodge = l['DF'],l['dodge']

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
        plt.ylim(DF[ylab].min(), DF[ylab].max())
        return DF,xlab,ylab,zlab,dodge

    def legend_fixer(self,l):
        ax,palette = l['ax'],l['palette']

        handles, labels = ax.get_legend_handles_labels()

        for i, handle in enumerate(handles):
            if 'Rectangle' in str(handle):
                if self.plot_line_palette:
                    handle.set_edgecolor(self.plot_line_palette[i])
                elif self.apply_color_lines_only:
                    handle.set_edgecolor(palette[i])
                else:
                    handle.set_edgecolor(self.line_color)

    def local_scatter(self,l):
        palette = l['palette']
        xlab = l['xlab']
        ylab = l['ylab']
        zlab = l['zlab']
        dodge = l['dodge']
        ax = l['ax']

        dark_palette = []
        for i in range(len(self.DF[self.zlab].unique())):
            dark_palette.append(self.line_color)
        if self.apply_color_lines_only:
            dark_palette = palette
        if self.plot_line_palette:
            dark_palette = self.plot_line_palette

        for i, category in enumerate(self.DF[self.zlab].unique()):
            df_copy = self.DF.copy()
            df_copy.loc[df_copy[self.zlab] != category, self.ylab] = np.nan
            sns.stripplot(
                data=df_copy, x=xlab, y=ylab, hue=zlab,
                dodge=dodge, palette=dark_palette,
                marker=self.marker_dict[category], ax=ax, size=3, legend=False)
        plt.xlabel(" ")
    
