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
import numpy as np
import matplotlib as mpl
import pandas as pd
import os
import seaborn as sns
from matplotlib import pyplot as plt
import scipy.stats as stats
import matplotlib.ticker as ticker
from pathlib import Path
from .utils import numeric_checker,min_maxer

class BasePlotter:
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
                       title = None,
                       **kwargs):
        
        self.plot_type = plot_type
        
        if not isinstance(DFs, list):
            DFs = [DFs]
        self.DFs = DFs
        self.DF = self.DFs[0]
        
        self.max_list_x = []
        self.max_list_y = []
        for DF in DFs:
            self.max_list_x.append(DF[xlab].max())
            self.max_list_y.append(DF[ylab].max())
        self.DF_counter = 0
        
        self.xlab = xlab
        self.ylab = ylab
        self.hues = hues
        
        self.input_fig = input_fig
        self.input_ax = input_ax
        
        if self.input_fig is None:
            self.fig_list = []
        if self.input_ax is None:
            self.ax_list = []
        
        self.colors = colors
        self.markers = markers
        self.def_font_sz = def_font_sz
        self.def_line_w = def_line_w
        self.folder_name = folder_name
        self.dpi = dpi
        self.sns_palette = sns_palette
        self.sns_style = sns_style
        self.sns_context = sns_context
        self.fontweight = fontweight
        self.box_edges = box_edges
        self.fig_width = fig_width
        self.xtick_font_ratio = xtick_font_ratio
        self.ytick_font_ratio = ytick_font_ratio
        self.x_exp_location = x_exp_location
        self.y_exp_location = y_exp_location
        self.annote_x_start = annote_x_start
        self.annote_y_start = annote_y_start
        self.x_axis_sig_figs = x_axis_sig_figs
        self.y_axis_sig_figs = y_axis_sig_figs
        self.low_cap0 = low_cap0
        self.dodge = dodge
        self.handles_in_legend = handles_in_legend
        self.box_width = box_width
        self.custom_x_label = custom_x_label
        self.custom_y_label = custom_y_label
        self.title = title
        self.__dict__.update(**kwargs)
        self.kwargs = kwargs
    
    def large_loop(self):
        for DF in self.DFs:
            # PRE-FORMAT PLOT
            self.pre_format(DF)
            
            # PLOT
            self.plot()
                
            # POST-FORMAT PLOT
            self.post_format()
            
            # SAVE CURRENT FIGURE
            self.save()
            
            # HANDLE LOOPER
            self.fig_list.append(self.fig)
            self.ax_list.append(self.ax)
            self.DF_counter += 1
            print(self.fig_list)
        return self.fig_list,self.ax_list
    
    def pre_format(self,DF):
        import seaborn as sns
        from matplotlib import pyplot as plt
        
        self.DF = DF
        if len(plt.get_fignums()) == 0:
            self.current_fig_num = 0
        else:
            self.current_fig_num = max(plt.get_fignums()) + 1
        self.fig = plt.figure(self.current_fig_num,dpi=self.dpi)
        self.ax = self.fig.add_subplot(111)
        self.fig.set_figwidth(self.fig_width)
        sns.color_palette(self.sns_palette)
        sns.set_style(self.sns_style)
        sns.set_context(self.sns_context)
        plt.xlabel("",fontweight=self.fontweight,fontsize=self.def_font_sz)
        plt.ylabel("",fontweight=self.fontweight,fontsize=self.def_font_sz)
        
        self.unique = list(DF[self.hues].unique())
        while len(self.unique) > len(self.markers):
            self.markers.extend(self.markers)
        self.marker_dict = dict(zip(self.unique,self.markers))
    
    def post_format(self):
        handles, labels = self.ax.get_legend_handles_labels()
        plt.legend(
            handles[:self.handles_in_legend], 
            labels[:self.handles_in_legend],
            prop={'weight': 'bold'})
        if self.custom_x_label:
            plt.xlabel(self.custom_x_label)
        if self.custom_y_label:
            plt.ylabel(self.custom_y_label)
        
        for axis in self.box_edges:
            self.ax.spines[axis].set_linewidth(self.def_line_w)
        
        if self.title:
            self.DF.name = self.title
        else:
            self.DF.name = ""
        plt.title(self.DF.name,weight=self.fontweight,fontsize=self.def_font_sz)
        sns.despine()
        for tick in self.ax.get_xticklabels():
            tick.set_fontweight(self.fontweight)
            tick.set_fontsize(self.def_font_sz*self.xtick_font_ratio)
        for tick in self.ax.get_yticklabels():
            tick.set_fontweight(self.fontweight)
            tick.set_fontsize(self.def_font_sz*self.ytick_font_ratio)
         
        xtexts = []
        for label in self.ax.get_xticklabels():
            xtexts.append(label.get_text())
        if all([numeric_checker(tick) for tick in xtexts]):
            self.ax.ticklabel_format(axis='x', style='sci', scilimits=(0,0))
            x_min, x_max = self.ax.get_xlim()
            x_min,x_max,xbins = min_maxer(x_min,x_max,cap0=self.low_cap0)
            self.ax.set_xlim(x_min,x_max)
            self.ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=xbins))
        
        ytexts = []
        for label in self.ax.get_yticklabels():
            ytexts.append(label.get_text())  
        if all([numeric_checker(tick) for tick in ytexts]):
            self.ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
            y_min, y_max = self.ax.get_ylim()
            y_min,y_max,ybins = min_maxer(y_min,y_max,cap0=self.low_cap0)
            self.ax.set_ylim(y_min,y_max)
            self.ax.yaxis.set_major_locator(ticker.MaxNLocator(nbins=ybins))

        tx = self.ax.xaxis.get_offset_text()
        tx.set_fontweight(self.fontweight)
        tx.set_fontsize(self.def_font_sz*0.9)
        tx.set_position((1.05,self.x_exp_location))
        
        ty = self.ax.yaxis.get_offset_text()
        ty.set_fontweight(self.fontweight)
        ty.set_fontsize(self.def_font_sz*0.9)
        ty.set_position((self.y_exp_location,1.05))
    
    def save(self):
        ylab_list = self.ylab.split(' ')
        self.ylab_name = ''
        for seg in ylab_list:
            if "/" not in seg:
                self.ylab_name += seg + '_'
            else:
                self.ylab_name += 'per' + '_'
        self.save_name = self.DF.name + self.ylab_name + self.plot_type
        self.save_name.replace('/', "per") 
        
        try:
            os.mkdir(self.folder_name)
            print(f"Directory '{self.folder_name}' created successfully.")
        except FileExistsError:
            print(f"Directory '{self.folder_name}' already exists.")
        
        plt.savefig(Path(os.path.join(self.folder_name + os.sep, self.save_name + '.png')),bbox_inches='tight')
        
    def show(self,fig_num=0):
        print(self.fig_list)
        plt.show(self.fig_list[fig_num])
        return self.fig_list[fig_num]
    
    def plot(self):
        print('Parent placeholder for children plots')
    