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
from .utils import numeric_checker, min_maxer, is_mostly_strings, ensure_data_frame, rgba_to_named_color, match_rgba_to_color
from matplotlib.patches import Patch
import warnings


class BasePlotter:
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
                 fig_width = 5,
                 fig_height = 5,
                 xtick_font_ratio = 1,
                 ytick_font_ratio = 0.9,
                 x_exp_location = 0,
                 y_exp_location = 0,
                 annote_x_start = 0.7,
                 annote_y_start = 0.7,
                 x_axis_sig_figs = 0,
                 y_axis_sig_figs = 2,
                 low_x_cap0 = False,
                 low_y_cap0=False,
                 dodge = True,
                 handles_in_legend = 10,
                 box_width = 0.6,
                 custom_x_label = None,
                 custom_y_label = None,
                 title = None,
                 plot_type = 'plot',
                 sci_x_lims = (0,1),
                 sci_y_lims = (0,1),
                 **kwargs):

        warnings.filterwarnings("ignore", message="The markers list has more values")
        self.xlab = xlab
        self.ylab = ylab
        self.zlab = zlab

        if not isinstance(DFs, list):
            DFs = [DFs]
        self.DFs = DFs
        self.DF = self.DFs[0]

        self.x = x
        self.y = y
        self.z = z

        force_data_frame_booleans = []
        if isinstance(self.x,list) or isinstance(self.x,np.ndarray):
            force_data_frame_booleans.append(True)
        else:
            force_data_frame_booleans.append(False)
        if isinstance(self.x, list) or isinstance(self.x, np.ndarray):
            force_data_frame_booleans.append(True)
        else:
            force_data_frame_booleans.append(False)
        if isinstance(self.x, list) or isinstance(self.x, np.ndarray):
            force_data_frame_booleans.append(True)
        else:
            force_data_frame_booleans.append(False)

        if any(force_data_frame_booleans):
            self.DFs = self.force_data_frame()
            self.DF = self.DFs[0]
        else:
            if not isinstance(DFs, list):
                DFs = [DFs]
            self.DFs = DFs
            self.DF = self.DFs[0]
        
        self.max_list_x = []
        self.max_list_y = []
        for DF in self.DFs:
            try:
                self.max_list_x.append(DF[self.xlab].max())
            except:
                pass
            try:
                self.max_list_y.append(DF[self.ylab].max())
            except:
                pass
        self.DF_counter = 0
        
        self.input_fig = input_fig
        self.input_ax = input_ax
        
        if self.input_fig is None:
            self.fig_list = []
        if self.input_ax is None:
            self.ax_list = []

        if not isinstance(colors, list):
            colors = [colors]
        self.colors = colors

        self.markers = markers
        self.hatches = hatches
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
        self.fig_height = fig_height
        self.xtick_font_ratio = xtick_font_ratio
        self.ytick_font_ratio = ytick_font_ratio
        self.x_exp_location = x_exp_location
        self.y_exp_location = y_exp_location
        self.annote_x_start = annote_x_start
        self.annote_y_start = annote_y_start
        self.x_axis_sig_figs = x_axis_sig_figs
        self.y_axis_sig_figs = y_axis_sig_figs
        self.low_x_cap0 = low_x_cap0
        self.low_y_cap0 = low_y_cap0
        self.dodge = dodge
        self.handles_in_legend = handles_in_legend
        self.box_width = box_width
        self.custom_x_label = custom_x_label
        self.custom_y_label = custom_y_label
        self.title = title
        self.plot_type = plot_type
        self.sci_x_lims = sci_x_lims
        self.sci_y_lims = sci_y_lims
        self.__dict__.update(**kwargs)
        self.kwargs = kwargs

    def force_data_frame(self):
        DFs = pd.DataFrame()
        DFs[self.xlab] = pd.DataFrame(ensure_data_frame(self.x))
        DFs[self.ylab] = pd.DataFrame(ensure_data_frame(self.y))
        try:
            DFs[self.zlab] = pd.DataFrame(ensure_data_frame(self.z))
        except (TypeError,ValueError) as e:
            if len(self.x) > len(self.y):
                DFs[self.zlab] = pd.DataFrame(['' for i in self.x])
            else:
                DFs[self.zlab] = pd.DataFrame(['' for i in self.y])
        return [DFs]

    def plot(self,save=True,**kwargs):
        self.pre_format()
        self.just_plot(**kwargs)
        self.post_format()
        self.show()
        if save:
            self.save()
        return self.fig,self.ax
    
    def pre_format(self):
        import seaborn as sns
        from matplotlib import pyplot as plt

        if len(plt.get_fignums()) == 0:
            self.current_fig_num = 0
        else:
            self.current_fig_num = max(plt.get_fignums()) + 1
        self.fig = plt.figure(self.current_fig_num,dpi=self.dpi)
        self.ax = self.fig.add_subplot(111)
        self.fig.set_figwidth(self.fig_width)
        self.fig.set_figheight(self.fig_height)
        sns.color_palette(self.sns_palette)
        sns.set_style(self.sns_style)
        sns.set_context(self.sns_context)
        plt.xlabel("",fontweight=self.fontweight,fontsize=self.def_font_sz)
        plt.ylabel("",fontweight=self.fontweight,fontsize=self.def_font_sz)

        try:
            self.unique = list(self.DF[self.zlab].unique())
        except KeyError:
            self.unique = [self.zlab]

        try:
            while len(self.unique) > len(self.markers):
                self.markers.extend(self.markers)
            self.marker_dict = dict(zip(self.unique,self.markers))
        except TypeError:
            self.marker_dict = {}

    def post_format(self):
        handles, labels = self.ax.get_legend_handles_labels()

        if self.plot_type == 'hist':
            labels = self.unique.copy()
            handles = []
            counter = 0
            for lab in labels:
                handles.append(Patch(color=self.colors[counter],label=lab))
                counter +=1

        if not labels and not handles or (self.plot_type == 'hist' and len(self.unique) <2):
            plt.legend([]).set_visible(False)
        else:
            plt.legend([]).set_visible(True)
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
            if self.plot_type != 'box_whisker':
                self.ax.ticklabel_format(axis='x', style='sci', scilimits=self.sci_x_lims)
                x_min, x_max = self.ax.get_xlim()
                x_min,x_max,xbins = min_maxer(x_min,x_max,cap0=self.low_x_cap0)
                self.ax.set_xlim(x_min,x_max)
                self.ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=xbins))
        
        ytexts = []
        for label in self.ax.get_yticklabels():
            ytexts.append(label.get_text())  
        if all([numeric_checker(tick) for tick in ytexts]):
            self.ax.ticklabel_format(axis='y', style='sci', scilimits=self.sci_y_lims)
            y_min, y_max = self.ax.get_ylim()
            y_min,y_max,ybins = min_maxer(y_min,y_max,cap0=self.low_y_cap0)
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
        if self.title is None:
            if is_mostly_strings(self.DF[self.ylab]):
                dependent_var_list = self.xlab.split(' ')
            elif is_mostly_strings(self.DF[self.xlab]):
                dependent_var_list = self.ylab.split(' ')
            else:
                # Assume y is the dependent variable
                dependent_var_list = self.ylab.split(' ')

            self.dependent_var_name = ''
            for seg in dependent_var_list:
                if "/" not in seg:
                    self.dependent_var_name += seg + '_'
                else:
                    self.dependent_var_name += 'per' + '_'
        else:
            self.dependent_var_name = '_'
        self.save_name = self.DF.name + self.dependent_var_name + self.plot_type
        self.save_name.replace('/', "per") 
        
        try:
            os.mkdir(self.folder_name)
            print(f"Directory '{self.folder_name}' created successfully.")
        except FileExistsError:
            print(f"Directory '{self.folder_name}' already exists.")
        
        plt.savefig(Path(os.path.join(self.folder_name + os.sep, self.save_name + '.png')),bbox_inches='tight')
        
    def show(self):
        plt.show(self.fig)
        return self.fig
    
    def just_plot(self,**kwargs):
        pass

    def kwarg_conflict_resolver(self, kwargs, conflict_vars):
        if len(kwargs) != 0:
            kwargs = {**self.kwargs, **kwargs}
        else:
            kwargs = self.kwargs
        outputs = []
        for var in conflict_vars:
            if var in kwargs:
                outputs.append(kwargs[var])
                del kwargs[var]
            else:
                outputs.append(getattr(self,var,None))
        return kwargs, *outputs

    def var_existence_check(self,inputs,input_keys,defaults_list,kwargs={}):
        outputs = []
        for var in inputs:
            if var is None and var not in kwargs:
                var = defaults_list[len(outputs)]
            outputs.append(var)
        if len(outputs) == 1:
            return outputs[0]
        else:
            return tuple(outputs)
    