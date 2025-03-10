#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A child class for the base plotter which produces box whisker plots with possible scatter overlays
@author: Shawn Pavey
"""
# %% IMPORT PACKAGES
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.patches import Rectangle

from .base_plotter import BasePlotter
from .utils import check_labels_in_DF, match_rgba_to_color, find_closest

#%%---------------------------------------------------------------------------------------------------------------------
# CHILD CLASS MAIN
#-----------------------------------------------------------------------------------------------------------------------
# %% INITIALIZE CHILD CLASS
class BoxWhiskerPlotter(BasePlotter):
    def __init__(self, input_dict,**kwargs):
        super().__init__(input_dict,**kwargs)
        self.plot_type = 'boxwhisker'

    # %% DEFINE PLOTTER, PREPARE INPUTS
    def just_plot(self,**kwargs):
        self.ensure_fig_ax_exist()
        self.DF[self.xlab] = self.DF[self.xlab].astype(str)
        conflict_vars, defaults_list, inputs, input_keys, outputs = self.generate_resolver_lists(locals(), kwargs)
        DF,kwargs,boxprops,showfliers,showmeans,meanprops,palette,linecolor,linewidth, width,dodge,ax = outputs
        palette,boxprops,showfliers,showmeans,meanprops,linecolor,linewidth,width,dodge,ax = super().var_existence_check(
            inputs,input_keys,defaults_list, kwargs=kwargs)
        DF,xlab,ylab,zlab,dodge = self.label_prep(locals())
        self.width = width

        # %% PLOT WITH SEABORN
        for i,u in enumerate(self.unique):
            line_palette = self.plot_line_palette[i] if self.plot_line_palette else self.line_color
            tempDF = DF.copy()
            if self.plot_line_palette is not None:
                for v in self.unique:
                    tempDF[ylab],tempDF.loc[tempDF[zlab]==v,ylab] = (
                        tempDF[ylab].astype(float),float("inf")) if v!=u else (tempDF[ylab],tempDF.loc[tempDF[zlab]==v,ylab])

            sns.boxplot(
                x=xlab, y=ylab, data=tempDF,
                hue=zlab,
                showfliers=showfliers,showmeans=showmeans,
                meanprops=meanprops,
                palette=palette,linecolor=line_palette,
                linewidth=linewidth, width=width,
                dodge = dodge,ax=ax,legend=i==0,fill=not self.apply_color_lines_only,**kwargs)

            if self.plot_line_palette is None:
                break

        # %% EXTRA PLOT EDITING
        if any(getattr(self, attr) is not None for attr in self.err_names): self.plot_errors(xlab, ylab, zlab)
        self.legend_fixer(locals())
        self.local_scatter(locals())
        if self.custom_x_label is None: self.ax.set_xlabel("")
        else: self.ax.set_xlabel(self.custom_x_label)
        super().just_plot()

    #%%---------------------------------------------------------------------------------------------------------------------
# LOCAL METHODS
#-----------------------------------------------------------------------------------------------------------------------
    # %% LOAD ALL PARENT METHODS UNLESS THEY EXIST HERE
    def __getattr__(self, name):
        super().__getattr__(name)

    # %% CUSTOM METHODS
    # %% FIX
    def generate_resolver_lists(self,l,kwargs):
        conflict_vars = ['DF','boxprops','showfliers','showmeans','meanprops','palette','linecolor','linewidth','width','dodge','ax']
        defaults_list = [self.colors[0:len(self.unique)],{'alpha': 1, 'edgecolor': self.line_color},
                        False,True,{"marker": "x", "markeredgecolor": self.line_color},self.line_color,self.def_line_w,
                        self.box_width,True,self.ax]
        kwargs,DF,boxprops,showfliers,showmeans,meanprops,palette,linecolor,linewidth, width,dodge,ax = super().kwarg_conflict_resolver(kwargs,conflict_vars)

        inputs = [palette,boxprops,showfliers,showmeans,meanprops,linecolor,linewidth,width,dodge,ax]
        input_keys = ['boxprops','showfliers','showmeans','meanprops','palette','linecolor','linewidth','width','dodge','ax']
        outputs = [DF,kwargs,boxprops,showfliers,showmeans,meanprops,palette,linecolor,linewidth, width,dodge,ax]

        return conflict_vars, defaults_list, inputs, input_keys, outputs

    def label_prep(self,l):
        DF,dodge = l['DF'],l['dodge']

        try:
            temp = DF[self.ylab]
        except KeyError:
            DF[self.ylab] = np.nan

        (DF[self.ylab],DF[self.xlab]) = (DF[self.xlab],DF[self.ylab]) if DF[self.ylab].isna().all() else (DF[self.ylab],DF[self.xlab])
        xlab,ylab,zlab = check_labels_in_DF(self.DF,self.xlab,self.ylab,self.zlab)
        (zlab,dodge) = (xlab,False) if zlab is None else (zlab,dodge)

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
        palette,xlab,ylab,zlab,dodge,ax = l['palette'],l['xlab'],l['ylab'],l['zlab'],l['dodge'],l['ax']

        dark_palette = []
        for i in range(len(self.DF[self.zlab].unique())):
            dark_palette.append(self.line_color)
        if self.apply_color_lines_only:
            dark_palette = palette
        elif self.plot_line_palette:
            dark_palette = self.plot_line_palette

        for i, category in enumerate(self.DF[self.zlab].unique()):
            df_copy = self.DF.copy()
            df_copy.loc[df_copy[self.zlab] != category, self.ylab] = np.nan

            sns.stripplot(
                data=df_copy, x=xlab, y=ylab, hue=zlab,
                dodge=dodge, palette=dark_palette,
                marker=self.marker_dict[category], ax=ax, size=3, legend=False)

        plt.xlabel(" ")
    
