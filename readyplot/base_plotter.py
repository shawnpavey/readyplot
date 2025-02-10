#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A parent class, base plotter, which initializes plotters and holds common 'self'-referring functions
@author: Shawn Pavey
"""
#%% IMPORT PACKAGES
import numpy as np
import pandas as pd
import os
import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker
from pathlib import Path
from .utils import numeric_checker, min_maxer, is_mostly_strings, ensure_data_frame, check_labels_in_DF
from matplotlib.patches import Patch
import warnings

class BasePlotter:
    def __init__(self,input_dict, **kwargs):
        warnings.filterwarnings("ignore", message="The markers list has more values")
        warnings.simplefilter("ignore", category=UserWarning)

        for name, value in input_dict.items():
            setattr(self, name, value)

        if self.excel_path and self.sheet_name:
            self.DFs = pd.read_excel(self.excel_path, sheet_name=self.sheet_name)


        if not isinstance(self.DFs, list):
            self.DFs = [self.DFs]
        self.DF = self.DFs[0]

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
            if not isinstance(self.DFs, list):
                self.DFs = [self.DFs]
            self.DFs = self.DFs
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

        if self.input_fig is None:
            self.fig_list = []
        if self.input_ax is None:
            self.ax_list = []

        if not isinstance(self.colors, list):
            self.colors = [self.colors]

        self.kwargs = kwargs
        self.__dict__.update(**kwargs)

    def plot(self,save=True,**kwargs):
        self.pre_format()
        self.just_plot(**kwargs)
        self.post_format()
        if save:
            self.save()
        #self.show()
        return self.fig,self.ax
    
    def pre_format(self):
        import seaborn as sns
        from matplotlib import pyplot as plt

        self.format_colors()

        if len(plt.get_fignums()) == 0:
            self.current_fig_num = 0
        else:
            self.current_fig_num = max(plt.get_fignums()) + 1

        self.fig = plt.figure(self.current_fig_num, dpi=self.dpi)
        self.ax = self.fig.add_subplot(111)
        self.fig.set_figwidth(self.fig_width)
        self.fig.set_figheight(self.fig_height)

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
                prop={'weight': 'bold'},)

            for text in plt.gca().get_legend().get_texts():
                text.set_color(self.line_color)

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
            try:
                self.ax.ticklabel_format(axis='y', style='sci', scilimits=self.sci_y_lims)
                y_min, y_max = self.ax.get_ylim()
                y_min,y_max,ybins = min_maxer(y_min,y_max,cap0=self.low_y_cap0)
                self.ax.set_ylim(y_min,y_max)
                self.ax.yaxis.set_major_locator(ticker.MaxNLocator(nbins=ybins))
            except AttributeError:
                pass

        tx = self.ax.xaxis.get_offset_text()
        tx.set_fontweight(self.fontweight)
        tx.set_fontsize(self.def_font_sz*0.9)
        tx.set_position((1.05,self.x_exp_location))
        
        ty = self.ax.yaxis.get_offset_text()
        ty.set_fontweight(self.fontweight)
        ty.set_fontsize(self.def_font_sz*0.9)
        ty.set_position((self.y_exp_location,1.05))
    
    def save(self,**kwargs):
        if '.' not in self.folder_name:
            xlab, ylab, zlab = check_labels_in_DF(self.DF, self.xlab, self.ylab, self.zlab)

            if self.title is None:
                if xlab and ylab:
                    if is_mostly_strings(self.DF[self.ylab]):
                        dependent_var_list = self.xlab.split(' ')
                    elif is_mostly_strings(self.DF[self.xlab]):
                        dependent_var_list = self.ylab.split(' ')
                    else:
                        # Assume y is the dependent variable
                        dependent_var_list = self.ylab.split(' ')
                else:
                    temp_string = (xlab if xlab is not None else "") + (ylab if ylab is not None else "")
                    dependent_var_list= temp_string.split(' ')
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

            self.fig.savefig(Path(os.path.join(self.folder_name + os.sep, self.save_name + '.png')),bbox_inches='tight',**kwargs)
        else:
            if self.folder_name[0] == os.sep:
                full_path = os.sep
            else:
                full_path = ''
            self.dir_name = self.folder_name.split(os.sep)[:-1]
            self.dir_name = os.path.join(full_path,*self.dir_name)
            print(self.dir_name)
            try:
                os.mkdir(self.dir_name)
                print(f"Directory '{self.dir_name}' created successfully.")
            except FileExistsError:
                print(f"Directory '{self.dir_name}' already exists.")
            self.fig.savefig(self.folder_name, bbox_inches='tight', **kwargs)
        return self.fig, self.ax
        
    def show(self,**kwargs):
        plt.show(self.fig,**kwargs)
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

    def force_data_frame(self):
        DFs = pd.DataFrame()
        DFs[self.xlab] = pd.DataFrame(ensure_data_frame(self.x))
        try:
            DFs[self.ylab] = pd.DataFrame(ensure_data_frame(self.y))
        except ValueError:
            pass
        try:
            DFs[self.zlab] = pd.DataFrame(ensure_data_frame(self.z))
        except (TypeError,ValueError) as e:
            if isinstance(self.y, list):
                if any(self.y):
                    if len(self.x) > len(self.y):
                        DFs[self.zlab] = pd.DataFrame(['' for i in self.x])
                    else:
                        DFs[self.zlab] = pd.DataFrame(['' for i in self.y])
                else:
                    DFs[self.zlab] = pd.DataFrame(['' for i in self.x])
            else:
                DFs[self.zlab] = pd.DataFrame(['' for i in self.x])

        return [DFs]

    def format_colors(self):
        sns.color_palette(self.sns_palette)
        sns.set_style(self.sns_style)
        sns.set_context(self.sns_context)

        if self.darkmode:
            self.line_color = 'white'
            self.back_color = 'black'
            sns.set_palette("muted")  # or "bright" or "pastel"
        else:
            sns.set_palette("deep")  # or "bright" or "pastel"

        plt.rcParams["figure.facecolor"] = self.back_color  # Background color of the plot
        plt.rcParams["axes.facecolor"] = self.back_color  # Axes background color
        plt.rcParams["axes.edgecolor"] = self.line_color  # Axes border color
        plt.rcParams["axes.labelcolor"] = self.line_color  # Axis labels color
        plt.rcParams['legend.facecolor'] = self.back_color  # Legend background
        plt.rcParams["xtick.color"] = self.line_color  # X-axis tick color
        plt.rcParams["ytick.color"] = self.line_color  # Y-axis tick color
        plt.rcParams["grid.color"] = "#444444"  # Gridline color

    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        for base in type(self).mro():
            if name in base.__dict__:
                return base.__dict__[name].__get__(self)
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")