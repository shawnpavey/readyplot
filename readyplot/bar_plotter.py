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
from .utils import match_rgba_to_color, check_labels_in_DF
import warnings


class BarPlotter(BasePlotter):
    def __init__(self, input_dict,**kwargs):
        super().__init__(input_dict,**kwargs)
        self.plot_type = 'bar'
        
    def just_plot(self,**kwargs):
        self.DF[self.xlab] = self.DF[self.xlab].astype(str)

        kwargs,DF,markers,palette,dodge,ax,capsize,linewidth,width = super().kwarg_conflict_resolver(
            kwargs, ['DF','markers','palette','dodge','ax','capsize','linewidth','width'])

        defaults_list = [self.colors[0:len(self.unique)], self.def_line_w, self.box_width]

        palette, linewidth, width = super().var_existence_check(
            [palette, linewidth, width],
            ['palette', 'linewidth', 'width'],
            defaults_list, kwargs=kwargs)

        xlab,ylab,zlab = check_labels_in_DF(self.DF,self.xlab,self.ylab,self.zlab)
        if zlab is None:
            zlab = xlab
            dodge = False

        sns.barplot(
            x=xlab, y=ylab, data=DF,
            hue =zlab,
            palette=palette,
            linewidth=linewidth,width=width,
            dodge = dodge,ax=ax, err_kws={'color': self.line_color,'linewidth': self.def_line_w}, capsize=capsize,
            **kwargs)

        if markers:
            plt.ylim(DF[ylab].min(),DF[ylab].max())

        dark_palette = []
        try:
            unique = self.DF[self.zlab].unique()
        except KeyError:
            unique = ['placeholder']

        if self.apply_color_lines_only:
            dark_palette = palette
        else:
            for i in range(len(unique)):
                dark_palette.append(self.line_color)

        for i, category in enumerate(unique):
            df_copy = self.DF.copy()
            if unique[0] != 'placeholder':
                df_copy.loc[df_copy[self.zlab] != category, self.ylab] = np.nan
            try:
                sns.stripplot(
                    data=df_copy, x=xlab, y=ylab,hue=zlab,
                    dodge = dodge,palette=dark_palette,
                    marker=self.marker_dict[category],ax=ax)
            except KeyError:
                pass

        while len(self.unique) > len(self.hatches):
            self.hatches.extend(self.hatches)

        counter = 0
        for bar in self.ax.patches:
            hue_group = bar.get_label()
            match_rgba_to_color(bar.get_facecolor(), self.colors)
            current_face_color =  match_rgba_to_color(bar.get_facecolor(), self.colors)
            bar.set_hatch(self.hatches[self.colors.index(current_face_color)])
            if self.apply_color_lines_only:
                bar.set_edgecolor(current_face_color)
                bar.set_facecolor(self.back_color)
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
            counter +=1

        plt.xlabel(" ")

    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        for base in type(self).mro():
            if name in base.__dict__:
                return base.__dict__[name].__get__(self)
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
            
    
