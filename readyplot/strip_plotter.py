#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A child class for the base plotter which produces stripplots
@author: Shawn Pavey
"""
# %% IMPORT PACKAGES
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from .base_plotter import BasePlotter
from .utils import match_rgba_to_color, check_labels_in_DF
from matplotlib.colors import to_rgb
import warnings

#%%---------------------------------------------------------------------------------------------------------------------
# CHILD CLASS MAIN
#-----------------------------------------------------------------------------------------------------------------------
# %% INITIALIZE CHILD CLASS
class StripPlotter(BasePlotter):
    def __init__(self, input_dict,**kwargs):
        super().__init__(input_dict,**kwargs)
        self.plot_type = 'strip'

    # %% DEFINE PLOTTER, PREPARE INPUTS
    def just_plot(self,**kwargs):
        self.ensure_fig_ax_exist()
        self.DF[self.xlab] = self.DF[self.xlab].astype(str)
        conflict_vars,defaults_list,inputs,input_keys,outputs = self.generate_resolver_lists(locals(),kwargs)
        DF,kwargs, markers,palette,dodge,ax,capsize,linewidth,width = outputs
        palette, linewidth, width = super().var_existence_check(inputs,input_keys,defaults_list, kwargs=kwargs)
        xlab,ylab,zlab,dodge = self.label_prep(locals())
        self.width = width

        # %% PLOT WITH SEABORN, FIRST INVISIBLE BAR PLOTS FOR ERRORS, THEN STRIPPLOT ITERATION FOR MARKER HANDLING
        self.pre_lines = self.ax.get_lines()
        # sns.barplot(legend=False,
        #     x=xlab, y=ylab, data=DF, hue=zlab,
        #     palette=palette, linewidth=linewidth, capsize=capsize, width=width, dodge=dodge,
        #     ax=ax, err_kws={'color': self.line_color, 'linewidth': self.def_line_w}, **kwargs)
        sns.pointplot(legend=False,
            data=DF, x=xlab, y=ylab, hue=zlab, capsize=capsize*0.9*0.7*2/len(self.unique), #capsize is user ratio * pad * smaller than mean*default gorup size/number of hues
            palette=palette, dodge=(0.8-0.8/len(self.unique)), errorbar='sd',linestyle="none",
            marker="_", markeredgewidth=self.def_line_w, markersize=self.fig_width/7*20*5*0.9*capsize/len(self.unique)/len(self.DF[self.xlab].unique())/0.133,err_kws={'linewidth': self.def_line_w},
            ax=ax, **kwargs
        )
        self.hatches_and_colors(locals())

        for i, u in enumerate(self.unique):
            marker = self.markers[i]
            tempDF = DF.copy()
            for v in self.unique:
                tempDF[ylab], tempDF.loc[tempDF[zlab] == v, ylab] = (
                    tempDF[ylab].astype(float), float("inf")) if v != u else (
                tempDF[ylab], tempDF.loc[tempDF[zlab] == v, ylab])

            sns.stripplot(
                x=xlab, y=ylab, data=tempDF, hue=zlab,
                palette=palette, linewidth=linewidth, dodge=dodge, marker=marker,
                ax=ax, **kwargs)

        # %% EXTRA PLOT EDITING
        if any(getattr(self, attr) is not None for attr in self.err_names): self.plot_errors(xlab, ylab, zlab)
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
    def generate_resolver_lists(self,loc_vars,kwargs):
        conflict_vars = ['DF','markers','palette','dodge','ax','capsize','linewidth','width']
        defaults_list = [self.colors[0:len(self.unique)], self.def_line_w, self.box_width]
        kwargs, DF, markers, palette, dodge, ax, capsize, linewidth, width = super().kwarg_conflict_resolver(kwargs,conflict_vars)

        inputs = [palette, linewidth, width]
        input_keys = ['palette', 'linewidth', 'width']
        outputs = [DF, kwargs, markers, palette, dodge, ax, capsize, linewidth, width]

        return conflict_vars, defaults_list, inputs, input_keys, outputs

    def label_prep(self,l):
        dodge,DF = l['dodge'],l['DF']
        xlab,ylab,zlab = check_labels_in_DF(self.DF,self.xlab,self.ylab,self.zlab)
        (zlab,dodge) = (xlab,False) if zlab is None else (zlab,dodge)
        plt.ylim(DF[ylab].min(), DF[ylab].max())
        return xlab,ylab,zlab,dodge

    def hatches_and_colors(self,l):
        ax = l['ax']
        counter = 0
        lines = [line for line in ax.lines if line not in self.pre_lines]
        for bar in self.ax.patches:
            if bar not in self.internal_patches:
                hue_group = bar.get_label()
                match_rgba_to_color(bar.get_facecolor(), self.colors)
                current_face_color =  match_rgba_to_color(bar.get_facecolor(), self.colors)

                bar.set_edgecolor('#FFFFFF00')
                bar.set_facecolor('#FFFFFF00')

                try: lines[counter].set_color(current_face_color)
                except IndexError: pass

                counter +=1


