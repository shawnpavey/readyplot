#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A child class for the base plotter which produces bar charts with potential scatter overlays
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
class BarPlotter(BasePlotter):
    def __init__(self, input_dict,**kwargs):
        super().__init__(input_dict,**kwargs)
        self.plot_type = 'bar'

    # %% DEFINE PLOTTER, PREPARE INPUTS
    def just_plot(self,**kwargs):
        self.ensure_fig_ax_exist()
        self.DF[self.xlab] = self.DF[self.xlab].astype(str)
        conflict_vars,defaults_list,inputs,input_keys,outputs = self.generate_resolver_lists(locals(),kwargs)
        DF,kwargs, markers,palette,dodge,ax,capsize,linewidth,width = outputs
        palette, linewidth, width = super().var_existence_check(inputs,input_keys,defaults_list, kwargs=kwargs)
        xlab,ylab,zlab,dodge = self.label_prep(locals())
        self.width = width

        # %% PLOT WITH SEABORN
        sns.barplot(
            x=xlab,y=ylab,data=DF,hue=zlab,
            palette=palette,linewidth=linewidth,capsize=capsize,width=width,dodge=dodge,
            ax=ax, err_kws={'color': self.line_color,'linewidth': self.def_line_w},**kwargs)

        # %% EXTRA PLOT EDITING
        if any(getattr(self, attr) is not None for attr in self.err_names): self.plot_errors(xlab, ylab, zlab)
        self.local_scatter(locals())
        self.hatches_and_colors(locals())
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

    def local_scatter(self,l):
        palette,xlab,ylab,zlab,dodge,ax = l['palette'],l['xlab'],l['ylab'],l['zlab'],l['dodge'],l['ax']
        dark_palette = []

        try:
            unique = self.DF[self.zlab].unique()
        except KeyError:
            unique = ['placeholder']

        if self.apply_color_lines_only:
            dark_palette = palette
        elif self.plot_line_palette:
            dark_palette = self.plot_line_palette
        else:
            for i in range(len(unique)):
                dark_palette.append(self.line_color)

        for i, category in enumerate(unique):
            df_copy = self.DF.copy()
            if unique[0] != 'placeholder':
                df_copy.loc[df_copy[self.zlab] != category, self.ylab] = np.nan

            try:
                sns.stripplot(
                    data=df_copy, x=xlab, y=ylab, hue=zlab,
                    dodge=dodge, palette=dark_palette,
                    marker=self.marker_dict[category], ax=ax,legend=False)
            except KeyError:
                pass

    def hatches_and_colors(self,l):
        ax = l['ax']
        while len(self.unique) > len(self.hatches):
            self.hatches.extend(self.hatches)
        counter = 0

        for bar in self.ax.patches :
            if bar not in self.internal_patches:
                hue_group = bar.get_label()
                match_rgba_to_color(bar.get_facecolor(), self.colors)
                current_face_color =  match_rgba_to_color(bar.get_facecolor(), self.colors)
                bar.set_hatch(self.hatches[self.colors.index(current_face_color)])

                if self.apply_color_lines_only:
                    bar.set_edgecolor(current_face_color)
                    bar_face_color = to_rgb(self.back_color) + tuple([0]) if self.transparent else self.back_color
                    bar.set_facecolor(bar_face_color)
                elif self.plot_line_palette:
                    bar.set_edgecolor(self.plot_line_palette[self.colors.index(current_face_color)])
                else:
                    bar.set_edgecolor(self.line_color)

                hatch_pattern = self.hatches[self.colors.index(current_face_color)]
                hatch_density = 1
                bar.set_hatch(f"{hatch_pattern * hatch_density}")
                bar.set_linewidth(self.def_line_w)

                if self.apply_color_lines_only:
                    try:
                        ax.lines[counter].set_color(current_face_color)
                    except IndexError:
                        pass
                elif self.plot_line_palette:
                    try:
                        ax.lines[counter].set_color(self.plot_line_palette[self.colors.index(current_face_color)])
                    except IndexError:
                        pass

                counter +=1



