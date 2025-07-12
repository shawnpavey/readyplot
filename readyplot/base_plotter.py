#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A parent class, base plotter, which initializes plotters and holds common 'self'-referring functions
@author: Shawn Pavey
"""
# %% IMPORT PACKAGES
import numpy as np
import pandas as pd
import os
import seaborn as sns
import matplotlib
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker
from pathlib import Path
from .utils import (numeric_checker, min_maxer, is_mostly_strings, ensure_data_frame, check_labels_in_DF,
                    dict_update_nested, is_transparent, delete_ticks_by_sig_figs, mini_kwarg_resolver)
import matplotlib.patches as patches
from matplotlib.patches import Patch
import matplotlib.lines as mlines
import warnings
from matplotlib.colors import to_rgb

#%%---------------------------------------------------------------------------------------------------------------------
# PARENT CLASS MAIN
#-----------------------------------------------------------------------------------------------------------------------
# %% INITIALIZE PARENT CLASS
class BasePlotter:
    def __init__(self,input_dict, **kwargs):
        # IGNORE WARNINGS ABOUT MARKER LISTS BEING TOO LONG, THE LOOPING BEHAVIOR IS SOMETIMES INTERNALLY EXPECTED
        warnings.filterwarnings("ignore", message="The markers list has more values")
        warnings.simplefilter("ignore", category=UserWarning)

        # ITERATE THROUGH THE SORTED INPUT DICT AND INITIALIZE WITH: self.name = value
        for name, value in input_dict.items(): setattr(self, name, value)
        self.input_dict = input_dict

        # IF ANY X,Y,Z INPUTS ARE LISTS OR ARRAYS, FORCE THEM INTO DATA FRAME FORM
        if any(isinstance(i,(list,np.ndarray)) for i in (self.x,self.y,self.z)): self.DF = self.force_data_frame()

        # INITIALIZE REQUIRED BACKGROUND VARIABLES
        self.DF_counter,self.kwargs,self.max_list_x,self.max_list_y = 0,kwargs,[],[]

        # POPULATE SOME BACKGROUND VARIABLES
        self.__dict__.update(**kwargs)
        try: self.max_list_x.append(self.DF[self.xlab].max())
        except: pass
        try: self.max_list_y.append(self.DF[self.ylab].max())
        except: pass

        # FORCE SOME INPUTS TO BE LISTS IF THEY AREN'T ALREADY
        if not isinstance(self.colors, list): self.colors = [self.colors]
        if not isinstance(self.xlines, list): self.xlines = [self.xlines]
        if not isinstance(self.ylines, list): self.ylines = [self.ylines]

        # RESOLVE THE INPUT ERROR BARS AS MULTIPLE OPTIONS ARE AVAILABLE TO THE USER
        self.resolve_err_list()

        # DETECT UNIQUE GROUPS IN ZLAB AS THIS WILL BE USED FOR COLOR AND MARKER SELECTION
        try: self.unique = list(self.DF[self.zlab].unique())
        except KeyError: self.unique = [self.zlab]

        # CREATE DICTIONARY OF MARKERS AND GROUPS FOR EASIER MARKER HANDLING LATER
        try:
            while len(self.unique) > len(self.markers): self.markers.extend(self.markers)
            self.marker_dict = dict(zip(self.unique,self.markers))
        except TypeError: self.marker_dict = {}

        # RESOLVE INPUTS FOR SUBPLOTS SUCH AS EXISTING LEGENDS
        try: self.add_to_legend([],[])
        except: pass

    # %% PLOT
    def plot(self,save=True,**kwargs):
        self.pre_format()
        self.just_plot(**kwargs)
        self.post_format()
        if save:
            self.save()
        return self.fig,self.ax

    # %% PRE FORMAT THE PLOT
    def pre_format(self):
        self.format_colors()
        self.manage_figure()
        self.set_xlabel()
        self.set_ylabel()
        return self.fig,self.ax

    # %% POST FORMAT THE PLOT
    def post_format(self):
        self.manage_legend()
        self.set_titles()
        self.manage_axes()
        return self.fig, self.ax

    # %% SAVE THE PLOT
    def save(self,**kwargs):
        # IF THE FOLDER NAME DOES NOT HAVE A '.' USE SAVE NAME AUTOPOPULATED FUNCTION WHICH BUILDS A NAME
        if '.' not in self.folder_name: save_name,dir_name = self.save_name_autopopulated()

        # IF A '.' IS IN THE FOLDER NAME, JUST USE THAT AS THE ENTIRE SAVE
        else:
            self.dir_name = self.folder_name.split(os.sep)[:-1]
            self.dir_name = os.path.join(os.sep,*self.dir_name) if self.folder_name[0]==os.sep else os.path.join('',*self.dir_name)
            save_name,dir_name = self.folder_name,self.dir_name

        # TRY TO MAKE A DIRECTORY OR USE THE CURRENT ONE
        try: os.mkdir(dir_name)
        except FileExistsError: pass#print(f"Directory '{dir_name}' already exists, overwriting and/or adding data.")
        #print(f"Directory '{dir_name}' created successfully.")

        # SAVE FIGURE
        self.fig.savefig(save_name, bbox_inches='tight',transparent=self.transparent, **kwargs)
        return self.fig, self.ax

    # %% SHOW WITH PLT.SHOW WHICH WIPES OUT THE FIGURE
    def show(self,**kwargs):
        plt.show(self.fig,**kwargs)
        return self.fig, self.ax

#%%---------------------------------------------------------------------------------------------------------------------
# ORGANIZED METHODS
#-----------------------------------------------------------------------------------------------------------------------
    # %% FIGURE CREATION OR ACCESS A FIGURE IF STEPS PERFORMED OUT OF ORDER, CAN TURN THIS OFF WITH use_existing_figure
    def manage_figure(self,use_existing_figure=True, subplot_loc = (1,1,1)):
        # CREATE FIGURE AND AX IF NONE EXISTS OR USE_EXISTING FIGURE UNLESS SET TO FALSE
        if use_existing_figure:
            # USE INPUT_FIGURE IF PROVIDED
            if self.input_fig is not None: self.fig = self.input_fig
            if hasattr(self,'fig'): self.fig.set_dpi(self.dpi)
            elif self.input_ax is None: self.fig = plt.figure(dpi=self.dpi)

            # USE INPUT_AX IF PROVIDED, RESOLVE NEW FIGURE LOCATION
            if self.input_ax is not None:
                self.ax = self.input_ax
                self.fig = self.ax.get_figure()
            elif not self.fig.axes: self.ax = self.fig.add_subplot(*subplot_loc)
            else: self.ax = self.fig.add_subplot(*subplot_loc)
        else:
            # CREATE NEW FIG AND AX
            self.fig = plt.figure(dpi=self.dpi)
            self.ax = self.fig.add_subplot(111)

        # INITIALIZE LEGEND
        if self.legend is None: self.legend = self.ax.legend()
        else:
            if self.first_time_legend: self.plot_copied_legend()
        self.first_time_legend = False

        # SET FIGURE DIMENSIONS
        self.fig.set_figwidth(self.fig_width)
        self.fig.set_figheight(self.fig_height)

        return self.fig, self.ax

    # %% TITLES AND AXIS LABELS
    def set_title(self,*args,fontweight=False, fontsize=False, color=False, **kwargs):
        # PARSE ARGS AND KWARGS
        label = "" if len(args) == 0 else args[0]
        fontweight = self.fontweight if not fontweight else fontweight
        fontsize = self.def_font_sz if not fontsize else fontsize
        color = self.line_color if not color else color

        # CREATE TITLE
        self.ax.set_title(label, fontweight=fontweight, fontsize=fontsize, color=color, **kwargs)

    def set_xlabel(self,*args,fontweight=False, fontsize=False, color=False, **kwargs):
        # PARSE ARGS AND KWARGS
        label = "" if len(args) == 0 else args[0]
        fontweight = self.fontweight if not fontweight else fontweight
        fontsize = self.def_font_sz if not fontsize else fontsize
        color = self.line_color if not color else color

        # CREATE XLABEL
        self.custom_x_label = label
        self.ax.set_xlabel(self.custom_x_label, fontweight=fontweight, fontsize=fontsize, color=color, **kwargs)

    def set_ylabel(self,*args,fontweight=False, fontsize=False, color=False,**kwargs):
        # PARSE ARGS AND KWARGS
        label = "" if len(args) == 0 else args[0]
        fontweight = self.fontweight if not fontweight else fontweight
        fontsize = self.def_font_sz if not fontsize else fontsize
        color = self.line_color if not color else color

        # CREATE YLABEL
        self.custom_y_label = label
        self.ax.set_ylabel(self.custom_y_label, fontweight=fontweight, fontsize=fontsize, color=color,**kwargs)

    def set_titles(self,*args,title=None,custom_x=None,custom_y=None,**kwargs):
        # PARSE ARGS IF PROVIDED
        if len(args) > 0:   title = args[0]
        if len(args) > 1:  custom_x= args[1]
        if len(args) > 2:   custom_y= args[2]

        # RESOLVE INPUT TITLE WITH SELF VALUES, USE EMPTY STRING '' TO REMOVE AN EXISTING TITLE, CLEAN NONE TO '' AFTER
        # Process title
        if self.ax.get_title() != '' and title is None: title = self.ax.get_title()
        elif title == '' : self.title = False
        elif title is None: title = ''
        # Process x
        if self.ax.get_xlabel() != '' and custom_x is None: custom_x = self.ax.get_xlabel()
        elif custom_x == '': self.custom_x_label = False
        elif custom_x is None: custom_x = ''
        # Process y
        if self.ax.get_ylabel() != '' and custom_y is None: custom_y = self.ax.get_ylabel()
        elif custom_y == '': self.custom_y_label = False
        elif custom_y is None: custom_y = ''

        # MANAGE SELF VARIABLES WITH CLEANED INPUTS
        self.title = self.title if (self.title and title == '') else title
        self.custom_y_label = self.custom_y_label if (self.custom_y_label and custom_y == '') else custom_y
        self.custom_x_label = self.custom_x_label if (self.custom_x_label and custom_x == '') else custom_x

        # CALL OTHER LOCAL FUNCTIONS TO PROPERLY HANDLE LABEL SETTING
        self.set_xlabel(self.custom_x_label,**kwargs)
        self.set_ylabel(self.custom_y_label,**kwargs)
        self.set_title(self.title,**kwargs)

        # UPDATE THE DATA FRAME NAME, ONLY USED IN NICHE SAVING SCENARIOS FOR AUTOMATIC FILE NAMING
        if self.title != '' and self.title is not None: self.DF.name = self.title
        elif self.custom_y_label != '' and self.custom_y_label is not None: self.DF.name = self.custom_y_label
        elif self.custom_x_label != '' and self.custom_x_label is not None: self.DF.name = self.custom_x_label

    # %% PLOTING XLINE AND YLINE ANNOTATIONS
    def plot_xline_yline(self,xlines=[None],ylines=[None],zorder=2,**kwargs):
        if (xlines[0] is None and len(self.internal_xlines) == 0) and (ylines[0] is None and len(self.internal_ylines) == 0):
            xlines = self.xlines
            ylines = self.ylines
            zorder = 1
        elif (xlines[0] is None and ylines[0] is None) and (len(self.internal_xlines) > 0 or len(self.internal_ylines) > 0):
            self.plot_copied_xlines_ylines()
        else:
            xlines = xlines
            ylines = ylines
            zorder = 3

        if xlines[0] is not None:
            for line in xlines:
                temp_line = self.ax.axvline(x=line,color=self.line_color,linewidth=self.def_line_w,linestyle='--',zorder=zorder,**kwargs)
                self.internal_xlines.append(temp_line)
        if ylines[0] is not None:
            for line in ylines:
                temp_line = self.ax.axhline(y=line,color=self.line_color,linewidth=self.def_line_w,linestyle='--',zorder=zorder,**kwargs)
                self.internal_ylines.append(temp_line)

    # %% PLOTTING COPIED XLINES AND YLINES FOR INSTANCE IN A SUBPLOT
    def plot_copied_xlines_ylines(self,zorder=None,**kwargs):
        excluded_keywords = ['bbox', 'label', 'picker', 'transform', 'axes',
                             'children', 'path', 'path_effects', 'tightbbox', 'transformed_clip_path_and_affine',
                             'window_extent', 'xydata', 'figure', 'data', 'xdata', 'ydata','zorder']
        temp_list = []
        for line in self.internal_xlines:
            filtered_properties = {key: value for key, value in line.properties().items() if
                                   key not in excluded_keywords}
            temp_line = self.ax.axvline(x=line.properties()['xdata'][0], **filtered_properties)
            temp_list.append(temp_line)
        self.internal_xlines = temp_list

        temp_list = []
        for line in self.internal_ylines:
            filtered_properties = {key: value for key, value in line.properties().items() if
                                   key not in excluded_keywords}
            if zorder is not None: filtered_properties['zorder'] = zorder
            temp_line = self.ax.axhline(y=line.properties()['ydata'][0], **filtered_properties)
            temp_list.append(temp_line)
        self.internal_ylines = temp_list

    # %% PLOTTING COPIED LINES FOR INSTANCE IN A SUBPLOT
    def plot_copied_lines(self,zorder=None):
        excluded_keywords = ['bbox', 'label', 'picker', 'transform', 'axes',
                             'children', 'path', 'path_effects', 'tightbbox', 'transformed_clip_path_and_affine',
                             'window_extent', 'xydata', 'figure', 'data', 'xdata', 'ydata','zorder']
        temp_list = []
        for line in self.internal_lines:
            filtered_properties = {key: value for key, value in line.properties().items() if
                                   key not in excluded_keywords}
            if zorder is not None: filtered_properties['zorder'] = zorder
            temp = mlines.Line2D(line.properties()['xdata'],line.properties()['ydata'], **filtered_properties)
            temp_line = self.ax.add_line(temp)
            temp_list.append(temp_line)
        self.internal_xlines = temp_list

    # %% PLOTTING COPIED PATCHES FOR INSTANCE IN A SUBPLOT
    def plot_copied_patches(self,zorder=None,**kwargs):
        included_keywords = ['agg_filter','antialiased','aa', 'capstyle', 'clip_box', 'clip_on', 'clip_path', 'color',
                             'edgecolor', 'facecolor', 'fill', 'hatch', 'joinstyle', 'label', 'linestyle', 'linewidth',
                             'picker', 'snap', 'url', 'visible','in_layout',
                             'angle','rotation_point','zorder']

        temp_list = []
        for patch in self.internal_patches:
            filtered_properties = {key: value for key, value in patch.properties().items() if key in included_keywords}

            if zorder is not None: filtered_properties['zorder'] = zorder

            if isinstance(patch, patches.Rectangle):
                corners = patch.properties()['corners']
                xy = tuple(corners[0])
                width = corners[1][0] - corners[0][0]
                height = corners[3][1] - corners[0][1]
                rec_args = xy,width,height
                new_patch = patches.Rectangle(*rec_args,**filtered_properties)
            elif isinstance(patch, patches.Circle):
                xy = patch.properties()['center']
                radius = patch.properties()['width']/2
                circle_args = xy, radius
                new_patch = patches.Circle(*circle_args,**filtered_properties)
            elif isinstance(patch, patches.Polygon):
                path = patch.properties()['path']
                xy = [tuple(pos) for pos in path.vertices]
                poly_args = xy[:-1]
                new_patch = patches.Polygon(poly_args,**filtered_properties)
            else:
                print ('PATCH TYPE NOT CURRENTLY SUPPORTED, SUBMIT REQUEST ON GITHUB TO ADD')
                return

            temp_patch = self.ax.add_patch(new_patch)
            temp_list.append(temp_patch)

        self.internal_patches = temp_list

    # %% LEGEND METHODS
    def manage_legend(self):
        # GET HANDLES AND LABELS
        if not hasattr(self, 'copied_legend'):
            handles, labels = self.ax.get_legend_handles_labels()

            if self.plot_type == 'strip':
                temp_handles, temp_labels = [],[]
                for i in range(len(self.unique)):
                    temp_handles.append(handles[i*(len(self.unique)+1)])#+2*len(self.unique)])
                    temp_labels.append(labels[i*(len(self.unique)+1)])#+2*len(self.unique)])
                handles,labels = temp_handles,temp_labels
                self.handles, self.labels = handles,labels

            # MANAGE STRANGE HISTOGRAM BEHAVIOR
            if self.plot_type == 'hist':
                labels,handles = self.unique.copy(),[]
                for counter, lab in enumerate(labels): handles.append(Patch(color=self.colors[counter], label=lab))
            if not labels and not handles or (self.plot_type == 'hist' and len(self.unique) < 2):
                try: self.set_legend([],[],visible=False)#self.legend.set_visible(False)
                except: pass
            else:

                # CREATE THE LEGEND AND CATCH ALL TEXT TO ADJUST COLOR, WITHIN MANAGE LEGEND USE GLOBAL TRANSPARENCY VALUE
                self.legend_kwargs['framealpha'] = 0 if self.transparent else 1
                if is_transparent(self.back_color): self.legend_kwargs['framealpha'] = 0
                self.set_legend(handles[:self.handles_in_legend],labels[:self.handles_in_legend],**self.legend_kwargs)

            if self.plot_type != 'strip': self.handles,self.labels = self.get_legend_handles_labels()
            if self.plot_type in ['strip','boxwhisker','bar'] and len(self.unique)<2: self.add_to_legend([],[],visible=False)

        else:
            self.set_legend(self.handles,self.labels)

    def set_legend(self,handles,labels,visible=True, text_color=None,**kwargs):
        # IF A TITLE IS PASSED ENSURE APPROPRIATE FONT, PREPARE COLOR SETTING FOR LATER
        if 'title' in kwargs and 'title_fontsize' not in kwargs: kwargs['title_fontproperties'] = {'size':self.def_font_sz}
        if 'title' in kwargs and 'title_fontweight' not in kwargs: kwargs['title_fontproperties'].update({'weight':self.fontweight})
        if text_color is None: text_color = self.line_color

        # UPDATE THE LEGEND KWARGS WITH ANY NEW KWARGS
        self.legend_kwargs = dict_update_nested(self.legend_kwargs, kwargs)

        # PLOT THE LEGEND
        self.legend = self.ax.legend(handles,labels,**self.legend_kwargs)
        self.legend.set_visible(visible)

        # RESET COLORS OF ALL LEGEND TEXT TO MATCH OVERALL THEME OR INPUT COLOR
        for text in self.legend.get_texts(): text.set_color(text_color)
        self.legend.get_title().set_color(text_color)

    def get_legend_handles_labels(self):
        # NEATLY AND INTERNALLY HANDLE GETTING LEGEND HANDLES AND LABELS
        handles, labels = self.ax.get_legend_handles_labels()
        return handles, labels

    def add_to_legend(self,new_handles,new_labels,visible=True, text_color=None,**kwargs):
        # UPDATE THE LEGEND KWARGS WITH ANY NEW KWARGS
        self.legend_kwargs = dict_update_nested(self.legend_kwargs,kwargs)

        # GET OLD HANDLES AND LABELS, EXTEND WITH THE NEW INPUTS
        handles, labels = self.get_legend_handles_labels()

        if self.plot_type == 'strip':
            temp_handles, temp_labels = [], []
            for i in range(len(self.unique)):
                temp_handles.append(handles[i * (len(self.unique) + 1)])  # +2*len(self.unique)])
                temp_labels.append(labels[i * (len(self.unique) + 1)])  # +2*len(self.unique)])
            handles, labels = temp_handles, temp_labels

        handles.extend(new_handles)
        labels.extend(new_labels)

        # RE-PLOT THE LEGEND WITH INTERNAL set_legend() CALL
        if self.legend is not None:
            self.set_legend(handles,labels,visible=visible, text_color=text_color, **self.legend_kwargs)

    def plot_copied_legend(self):
        included_keywords = ['loc', 'numpoints', 'markerscale',
        'markerfirst', 'reverse', 'scatterpoints', 'scatteryoffsets', 'prop',
        'fontsize', 'labelcolor', 'borderpad', 'labelspacing', 'handlelength',
        'handleheight', 'handletextpad', 'borderaxespad', 'columnspacing', 'ncols',
        'mode', 'fancybox', 'shadow', 'title', 'title_fontsize', 'framealpha',
        'edgecolor', 'facecolor', 'bbox_to_anchor', 'bbox_transform', 'frameon',
        'handler_map', 'title_fontproperties', 'alignment', 'ncol', 'draggable']
        filtered_properties = {key: value for key, value in self.legend.properties().items() if key in included_keywords}
        handles, labels = self.handles,self.labels
        legend = self.ax.legend(handles,labels,**filtered_properties)
        self.legend = legend
        self.copied_legend = [handles,labels]

    def get_legend(self):
        # SIMPLE WAY TO GET THE LEGEND OBJECT OUT OF READYPLOT
        if self.legend is not None: return self.legend
        else: pass

    # %% ERROR BARS
    def plot_errors(self,xlab,ylab,zlab):
        # INITIALIZE VARS FOR ERROR BAR EXISTENCE AND GET AXIS TICKS IN CASE AN AXIS HAS STRING LABELS NOT NUMERIC
        err_xvars = [self.xerror_vals,self.hi_xerror_vals,self.low_xerror_vals]
        err_yvars = [self.yerror_vals, self.hi_yerror_vals, self.low_yerror_vals]
        err_vars = err_xvars.copy()
        err_vars.extend(err_yvars)
        #print(err_vars)

        x_ticks = self.ax.get_xticks()
        x_labels = self.ax.get_xticklabels()
        y_ticks = self.ax.get_yticks()
        y_labels = self.ax.get_yticklabels()

        x_min, x_max = self.ax.get_xlim()
        y_min, y_max = self.ax.get_ylim()

        # START LOOP IF ANY ERROR KEYWORDS HAVE BEEN PASSED< CREATE A TEMPORARY DF PER GROUP
        if any(error_var is not None for error_var in err_vars):
            for i,group in enumerate(self.unique):
                try: tempDF = self.DF[self.DF[zlab] == group]
                except KeyError: tempDF = self.DF

                # GET THE X,Y POSITION OF EVERY POINT, IF THE X OR Y IS A STRING, MAP BY AXIS TICKS
                for j,row in tempDF.iterrows():
                    tempx = row[xlab]
                    tempy = row[ylab]

                    if isinstance(tempx, str):
                        for k, label in enumerate(x_labels):
                            if label.get_text() == tempx:
                                tempx = x_ticks[i]
                                break
                    if isinstance(tempy, str):
                        for k, label in enumerate(y_labels):
                            if label.get_text() == tempy:
                                tempy = y_ticks[i]
                                break

                    # PLOT ERROR BARS AND FIX THE ISSUE WHERE ONLY A HIGH OR LOW ERROR LEADS TO MISSING CONNECTION
                    temp_x_err = np.array([row['x_errs'][0],row['x_errs'][1]])
                    temp_y_err = np.array([row['y_errs'][0],row['y_errs'][1]])
                    if tempx+temp_x_err[1] > x_max and self.error_lim_affect and any(a is not None for a in err_xvars):
                        x_max = tempx+temp_x_err[1]
                        self.ax.set_xlim(x_min,x_max)
                    if tempy+temp_y_err[1] > y_max and self.error_lim_affect and any(a is not None for a in err_yvars):
                        y_max = tempy+temp_y_err[1]
                        self.ax.set_ylim(y_min,y_max)
                    if tempx - temp_x_err[0] < x_min and self.error_lim_affect  and any(a is not None for a in err_xvars):
                        x_min = tempx - temp_x_err[0]
                        self.ax.set_xlim(x_min, x_max)
                    if tempy - temp_y_err[0] < y_min and self.error_lim_affect and any(a is not None for a in err_yvars):
                        y_min = tempy - temp_y_err[0]
                        self.ax.set_ylim(y_min, y_max)
                    linewidth = getattr(self, 'linewidth', self.def_line_w)
                    self.fix_trailing_errors(tempx, tempy, temp_x_err, temp_y_err, self.colors[i],linewidth)
                    self.ax.errorbar(tempx,tempy,xerr=temp_x_err.reshape(2,1),yerr=temp_y_err.reshape(2,1),
                                     capsize = self.capsize,color=self.colors[i],linewidth=linewidth,capthick=linewidth)

                    if any(a is not None for a in err_xvars): self.ax.set_xlim(x_min, x_max)
                    if any(a is not None for a in err_yvars): self.ax.set_ylim(y_min, y_max)

        # PASS IF NO ERROR KEYWORDS HAVE BEEN PASSED
        else:
            pass

    def fix_trailing_errors(self,tx,ty,txe,tye,c,l):
        # FOR EACH ERROR, PLOT A LINE CONNECTING IT TO THE MAIN POINT IF IT EXISTS WITHOUT THE HI/LOW COUNTERPART
        if not np.isnan(txe[0]) and np.isnan(txe[1]): self.ax.plot([tx, tx-txe[0]], [ty, ty], color=c, linewidth=l)
        if not np.isnan(txe[1]) and np.isnan(txe[0]): self.ax.plot([tx, tx+txe[1]], [ty, ty], color=c, linewidth=l)
        if not np.isnan(tye[0]) and np.isnan(tye[1]): self.ax.plot([tx, tx], [ty, ty-tye[0]], color=c, linewidth=l)
        if not np.isnan(tye[1]) and np.isnan(tye[0]): self.ax.plot([tx, tx], [ty, ty+tye[1]], color=c, linewidth=l)

    def resolve_err_list(self):
        # INITIALIZE OUPUTS AND STORE VARIABLES FOR KEY,VAL DICTIONARY ITERATION LATER
        output_x = []
        output_y = []
        variables = {
            'xerror_vals':self.xerror_vals,'low_xerror_vals':self.low_xerror_vals,'hi_xerror_vals':self.hi_xerror_vals,
            'yerror_vals':self.yerror_vals,'low_yerror_vals':self.low_yerror_vals,'hi_yerror_vals':self.hi_yerror_vals}

        # ITERATE THROUGH VARIABLES AND IF ANY ARE STRINGS RETRIEVE ERROR BAR DATA FROM THE DATA FRAME COLUMN
        for key, val in variables.items():
            if isinstance(val, str):
                setattr(self, key, self.DF[val].tolist())

        # ITERATE AND GET X AND Y ERRORS TO BE LIST VALUES WITH LOW AND HIGH, SET NONES TO NP.NAN
        for i, row in self.DF.iterrows():
            # Process x
            if self.low_xerror_vals is None and self.hi_xerror_vals is None:
                low_x = self.xerror_vals[i] if self.xerror_vals is not None else np.nan
                hi_x = self.xerror_vals[i] if self.xerror_vals is not None else np.nan
            else:
                low_x = self.low_xerror_vals[i] if self.low_xerror_vals is not None else np.nan
                hi_x = self.hi_xerror_vals[i] if self.hi_xerror_vals is not None else np.nan

            # Process y
            if self.low_yerror_vals is None and self.hi_yerror_vals is None:
                low_y = self.yerror_vals[i] if self.yerror_vals is not None else np.nan
                hi_y = self.yerror_vals[i] if self.yerror_vals is not None else np.nan
            else:
                low_y = self.low_yerror_vals[i] if self.low_yerror_vals is not None else np.nan
                hi_y = self.hi_yerror_vals[i] if self.hi_yerror_vals is not None else np.nan

            # Build output lists
            output_x.append([low_x,hi_x])
            output_y.append([low_y,hi_y])

        # SET DATA FRAME'S X AND Y ERRORS AS [low,high] LIST ELEMENTS
        self.DF['x_errs'] = [arr for arr in output_x]
        self.DF['y_errs'] = [arr for arr in output_y]
        return output_x,output_y

    # %% AXIS AND TICK MANAGEMENT
    def manage_axes(self):
        # MANAGE GENERAL AXES
        for axis in self.box_edges:
            self.ax.spines[axis].set_linewidth(self.def_line_w)
        sns.despine()
        for tick in self.ax.get_xticklabels():
            tick.set_fontweight(self.fontweight)
            tick.set_fontsize(self.def_font_sz * self.xtick_font_ratio)
        for tick in self.ax.get_yticklabels():
            tick.set_fontweight(self.fontweight)
            tick.set_fontsize(self.def_font_sz * self.ytick_font_ratio)
        try: self.manage_x_axis()
        except TypeError: pass
        try: self.manage_y_axis()
        except TypeError: pass


    def manage_x_axis(self):
        # MANAGE X AXIS
        xtexts = []
        for label in self.ax.get_xticklabels():
            xtexts.append(label.get_text())
        if all([numeric_checker(tick) for tick in xtexts]):
            try:
                x_min, x_max = self.ax.get_xlim()
                abs_max = x_max if abs(x_max) > abs(x_min) else x_min
                self.ax.xaxis.set_major_formatter(ticker.ScalarFormatter())
                self.ax.ticklabel_format(axis='x', style='sci', scilimits=self.sci_x_lims)
                if abs(abs_max) < 10**self.sci_x_lims[0] or abs(abs_max) > 10**self.sci_x_lims[1]:
                    x_min, x_max = self.ax.get_xlim()
                    if abs(x_min) < abs(0.2 * (x_max - x_min)): self.ax.set_xlim(0, x_max)
                    elif abs(x_max) < abs(0.2 * (x_max - x_min)): self.ax.set_xlim(x_min, 0)
                    x_min, x_max = self.ax.get_xlim()
                else:
                    pass#self.ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda val, pos: f'{val:.{self.x_axis_sig_figs}g}'))

            except AttributeError:pass
            except KeyError:pass

            x_min, x_max = self.ax.get_xlim()
            if abs(x_min) < abs(0.2 * (x_max - x_min)) and self.plot_type not in ['bar','boxwhisker','strip']: self.ax.set_xlim(0, x_max)
            elif abs(x_max) < abs(0.2 * (x_max - x_min)): self.ax.set_xlim(x_min, 0)
        elif hasattr(self,'width'):
            self.x_margin = (1-self.width)/2
            lims = self.ax.get_xlim()
            self.ax.margins(x=0)
            self.ax.set_xlim(lims[0]-self.x_margin, lims[1]+self.x_margin)


        # MANAGE EXPONENTS
        tx = self.ax.xaxis.get_offset_text()
        tx.set_fontweight(self.fontweight)
        tx.set_fontsize(self.def_font_sz * 0.9)
        tx.set_position((1.05, self.x_exp_location))

    def manage_y_axis(self):
        # MANAGE Y AXIS
        ytexts = []
        for label in self.ax.get_yticklabels():
            ytexts.append(label.get_text())
        if all([numeric_checker(tick) for tick in ytexts]):
            try:
                y_min, y_max = self.ax.get_ylim()
                abs_max = y_max if abs(y_max) > abs(y_min) else y_min
                self.ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
                self.ax.ticklabel_format(axis='y', style='sci', scilimits=self.sci_y_lims)
                if abs(abs_max) < 10**self.sci_y_lims[0] or abs(abs_max) > 10**self.sci_y_lims[1]:
                    y_min, y_max = self.ax.get_ylim()
                    if abs(y_min) < abs(0.2 * (y_max - y_min)):self.ax.set_ylim(0, y_max)
                    elif abs(y_max) < abs(0.2 * (y_max - y_min)): self.ax.set_ylim(y_min, 0)
                    y_min, y_max = self.ax.get_ylim()
                else:
                    pass#self.ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda val, pos: f'{val:.{self.y_axis_sig_figs}g}'))

            except AttributeError:pass
            except KeyError:pass

            y_min, y_max = self.ax.get_ylim()
            if abs(y_min) < abs(0.2 * (y_max - y_min)): self.ax.set_ylim(0, y_max)
            elif abs(y_max) < abs(0.2 * (y_max - y_min)): self.ax.set_ylim(y_min, 0)
        elif hasattr(self, 'width'):
            self.y_margin = (1 - self.width) / 2
            lims = self.ax.get_ylim()
            self.ax.margins(y=0)
            self.ax.set_xlim(lims[0] - self.y_margin, lims[1] + self.y_margin)

        # MANAGE EXPONENTS
        ty = self.ax.yaxis.get_offset_text()
        ty.set_fontweight(self.fontweight)
        ty.set_fontsize(self.def_font_sz * 0.9)
        ty.set_position((self.y_exp_location, 1.05))

    # %% GET AND SET FUNCTION FOR HANDLING VARIABLES EXTERNAL TO READYPLOT
    def get(self,key):
        # GET WHICHEVER ATTRIBUTE IS PROVIDED IN KEY, ITERATE IF LIST
        output = []
        if isinstance(key, list): output = [getattr(self, i) for i in key]
        else: output = getattr(self, key)
        return output

    def set(self,key,value):
        # SET WHICHEVER ATTRIBUTE IS PROVIDED IN KEY TO THE PROVIDED VALUE, ITERATE IF LIST
        if isinstance(key, list):
            for i,key in enumerate(key):
                setattr(self, key, value[i])
        else: setattr(self, key, value)

    def get_all(self,include_problematic = True):
        # GET ALL VARIABLES, EXCLUDE POTENTIALLY PROBLEMATIC VARIABLES IF TRYING TO PORT SETTINGS TO ANOTHER PLOT
        problematic = ['DF','x','y','z','xlab','ylab','zlab','DF_counter','max_list_x','max_list_y',
                       'unique','marker_dict','fig','ax','plot_type','dir_name','input_dict']
        output = {key: value for key, value in vars(self).items() if (key not in problematic or include_problematic)}
        return output

    def set_all(self,input_dict):
        # SET ALL VARIABLES
        for key, value in input_dict.items():
            setattr(self, key, value)

    def get_copy_settings(self,include_problematic = False):
        # OUTPUT ALL THE INPUT SETTINGS INTO THIS GRAPH FOR REPEATABILITY WITH OTHERS
        problematic = ['DF', 'x', 'y', 'z', 'xlab', 'ylab', 'zlab','imported_settings','legend','first_time_legend']
        if include_problematic: output = {key: value for key, value in self.input_dict.items()}
        else: output = {key: value for key, value in self.input_dict.items() if key not in problematic}
        current_settings = self.get_all()
        for key, value in output.items():
            if key in self.get_all():
                output[key] = current_settings[key]
        return output

#%%---------------------------------------------------------------------------------------------------------------------
# INTERNAL METHODS FOR HANDLING INPUTS, GENERAL ESTHETICS, AND SAVE HELPER FUNCTIONS
#-----------------------------------------------------------------------------------------------------------------------
    # %% RESOLVE VARIABLES
    def kwarg_conflict_resolver(self, kwargs, conflict_vars):
        # COMBINE INPUT KWARGS WITH GENERAL KWARGS
        if len(kwargs) != 0: kwargs = {**self.kwargs, **kwargs}
        else: kwargs = self.kwargs

        # FOR VAR IN THE SUPPLIED CONFLICT_VARS LIST, IF IT IS IN THE SUPPLIED KWARGS USE IT, ELSE GET SELF.VAR
        outputs = []
        for var in conflict_vars:
            if var in kwargs:
                outputs.append(kwargs[var])
                del kwargs[var]
            else: outputs.append(getattr(self,var,None))

        # RETURN UPDATED KWARGS LIST AND UNPACKED OUTPUTS
        return kwargs, *outputs

    def var_existence_check(self,inputs,input_keys,defaults_list,kwargs={}):
        # IF THE INPUT VAR DOES NOT ALREADY EXIST IN KWARGS, ASSIGN THE PROVIDED DEFAULT TO IT
        outputs = []
        for var in inputs:
            if var is None and var not in kwargs: var = defaults_list[len(outputs)]
            outputs.append(var)

        # RETURN TUPLE COMPATIBLE OUTPUTS
        if len(outputs) == 1: return outputs[0]
        else: return tuple(outputs)

    def force_data_frame(self):
        # CREATE A TEMPORARY DATA FRAME, WE KNOW X IS PROVIDED BUT TRY/EXCEPT THE Y AND Z VALUES
        DF = pd.DataFrame()
        DF[self.xlab] = pd.DataFrame(ensure_data_frame(self.x))
        try: DF[self.ylab] = pd.DataFrame(ensure_data_frame(self.y))
        except ValueError: pass
        try: DF[self.zlab] = pd.DataFrame(ensure_data_frame(self.z))
        except (TypeError,ValueError) as e:

        # IF Z GIVES AN ERROR, CHECK X AND Y AND POPULATE WITH EMPTY STRINGS FOR THE LONGEST DATAFRAME (OBSOLETE?)
            if isinstance(self.y, list):
                if any(self.y):
                    DF[self.zlab] = pd.DataFrame(
                        ['' for i in self.x]) if len(self.x) > len(self.y) else pd.DataFrame(['' for i in self.y])
                else: DF[self.zlab] = pd.DataFrame(['' for i in self.x])
            else: DF[self.zlab] = pd.DataFrame(['' for i in self.x])

        # RETURN TEMPORARY DATAFRAME
        return DF

    def ensure_fig_ax_exist(self):
        # CREATE A FIG IF IT DOESN'T EXIST
        if not hasattr(self, 'fig'):
            self.fig = plt.figure(dpi=self.dpi)
            self.ax = self.fig.add_subplot(111)
        # CREATE AN AX IF IT DOESN'T EXIST
        if not hasattr(self, 'ax'):
            self.ax = self.fig.add_subplot(111)

    # %% ESTHETICS
    def format_colors(self):
        # UPDATE SNS BACKGROUND SETTINGS
        sns.color_palette(self.sns_palette)
        sns.set_style(self.sns_style)
        sns.set_context(self.sns_context)

        # HANDLE DARKMODE
        if self.darkmode:
            self.line_color = 'white'
            self.back_color = 'black'
            sns.set_palette("muted")  # or "bright" or "pastel"
        else:
            sns.set_palette("deep")  # or "bright" or "pastel"

        # TRANSLATE BACKGROUND COLOR TO TRANSPARENT IF TRANSPARENCY IS SET
        self.back_color = to_rgb(self.back_color) + tuple([0]) if self.transparent else self.back_color

        # SET ALL PLT DEFAULT COLORS BASED ON LINE AND BACK COLOR AND GRID_COLOR
        plt.rcParams["figure.facecolor"] = self.back_color  # Background color of the plot
        plt.rcParams["axes.facecolor"] = self.back_color  # Axes background color
        plt.rcParams["axes.edgecolor"] = self.line_color  # Axes border color
        plt.rcParams["axes.labelcolor"] = self.line_color  # Axis labels color
        plt.rcParams['legend.facecolor'] = self.back_color  # Legend background
        plt.rcParams["xtick.color"] = self.line_color  # X-axis tick color
        plt.rcParams["ytick.color"] = self.line_color  # Y-axis tick color
        plt.rcParams["grid.color"] = self.grid_color  # Gridline color

    # %% SAVE HELPER FUNCTION
    def save_name_autopopulated(self):
        # MAKE SAVE NAME FROM DF.NAME (SET DURING SET_TITLES) AND PLOT TYPE, HANDLE "/"
        self.save_name = self.DF.name + '_' + self.plot_type
        self.save_name = self.save_name.replace("/", "_per_")

        # MAKE AND RETURN SAVE NAME AND DIRECTORY NAME
        save_name = Path(os.path.join(self.folder_name + os.sep, self.save_name + '.png'))
        dir_name = self.folder_name
        return save_name,dir_name

#%%---------------------------------------------------------------------------------------------------------------------
# GENERAL METHODS FOR CLASS HANDLING AND PLACEHOLDERS
#-----------------------------------------------------------------------------------------------------------------------
    # %% PLACEHOLDER FOR CHILD CLASSES
    def just_plot(self,**kwargs):
        xlims = self.ax.get_xlim()
        ylims = self.ax.get_ylim()
        self.plot_xline_yline()
        self.plot_copied_lines()
        self.plot_copied_patches()
        self.ax.set_xlim(xlims)
        self.ax.set_ylim(ylims)
        return self.fig, self.ax

    # %% PASS METHODS TO CHILDREN
    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        for base in type(self).mro():
            if name in base.__dict__:
                return base.__dict__[name].__get__(self)
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

#%%---------------------------------------------------------------------------------------------------------------------
# EXTRA MATPLOTLIB TYPE FUNCTIONS WHICH USERS MIGHT EXPECT TO NEED
#-----------------------------------------------------------------------------------------------------------------------
    # %% AXES
    def xlim(self,*args,**kwargs):
        self.fig.xlim(*args,**kwargs)
    def ylim(self,*args,**kwargs):
        self.fig.ylim(*args,**kwargs)
    def set_xlim(self,*args,**kwargs):
        self.ax.set_xlim(*args,**kwargs)
    def set_ylim(self,*args,**kwargs):
        self.ax.set_ylim(*args,**kwargs)
    def get_xlim(self, *args, **kwargs):
        return self.ax.get_xlim(*args, **kwargs)
    def get_ylim(self, *args, **kwargs):
        return self.ax.get_ylim(*args, **kwargs)

    def xticks(self,*args,**kwargs):
        self.fig.xticks(*args,**kwargs)
    def yticks(self,*args,**kwargs):
        self.fig.yticks(*args,**kwargs)
    def get_xticks(self, *args, **kwargs):
        return self.ax.get_xticks(*args, **kwargs)
    def get_yticks(self, *args, **kwargs):
        return self.ax.get_yticks(*args, **kwargs)
    def get_xticklabels(self, *args, **kwargs):
        return self.ax.get_xticklabels(*args, **kwargs)
    def get_yticklabels(self, *args, **kwargs):
        return self.ax.get_yticklabels(*args, **kwargs)

    def gca(self,*args,**kwargs):
        plt.gca(*args,**kwargs)
    def gcf(self,*args,**kwargs):
        plt.gcf(*args,**kwargs)

    def axhline(self,*args,**kwargs):
        self.fig.axhline(*args,**kwargs)
    def axvline(self,*args,**kwargs):
        self.fig.axvline(*args,**kwargs)
    def grid(self,*args,**kwargs):
        self.ax.grid(*args,**kwargs)

    def set_facecolor(self,*args,**kwargs):
        self.ax.set_facecolor(*args,**kwargs)
    def get_facecolor(self,*args,**kwargs):
        return self.ax.get_facecolor(*args,**kwargs)

    # %% TITLES, LABELS
    def title(self,*args,**kwargs):
        self.set_title(*args,**kwargs)
    def xlabel(self,*args,**kwargs):
        self.set_xlabel(*args,**kwargs)
    def ylabel(self,*args,**kwargs):
        self.set_ylabel(*args,**kwargs)
    def get_title(self, *args, **kwargs):
        return self.ax.get_title(*args, **kwargs)
    def get_xlabel(self, *args, **kwargs):
        return self.ax.get_xlabel(*args, **kwargs)
    def get_ylabel(self, *args, **kwargs):
        return self.ax.get_ylabel(*args, **kwargs)

    # %% LEGENDS + ANNOTATIONS
    def create_legend(self,*args,**kwargs):
        self.legend = self.ax.legend(*args, **kwargs)

    def text(self,*args,**kwargs):
        self.fig.text(*args,**kwargs)
    def figtext(self,*args,**kwargs):
        self.fig.figtext(*args,**kwargs)
    def annotate(self,*args,**kwargs):
        self.fig.annotate(*args,**kwargs)
    def get_texts(self,*args,**kwargs):
        return self.fig.get_texts(*args,**kwargs)

    def set_xlines(self,xlines):
        if not isinstance(xlines,list): xlines = [xlines]
        for line in self.internal_xlines: line.remove()
        self.internal_xlines = []
        self.xlines = xlines
        self.plot_xline_yline()
    def set_ylines(self,ylines):
        if not isinstance(ylines, list): ylines = [ylines]
        for line in self.internal_ylines: line.remove()
        self.internal_ylines = []
        self.ylines = ylines
        self.plot_xline_yline()
    def add_xlines(self,xlines):
        if not isinstance(xlines, list): xlines = [xlines]
        if self.xlines[0] is None: self.xlines = xlines
        else: self.xlines.extend(xlines)
        self.plot_xline_yline(xlines=xlines)
    def add_ylines(self,ylines):
        if not isinstance(ylines, list): ylines = [ylines]
        if self.ylines[0] is None: self.ylines = ylines
        else: self.ylines.extend(ylines)
        self.plot_xline_yline(ylines=ylines)
    def get_xlines(self,*args,**kwargs):
        return self.internal_xlines
    def get_ylines(self,*args,**kwargs):
        return self.internal_ylines
    def set_patches(self,*args,**kwargs):
        if not isinstance(args, list): args = list(args)
        for patch in self.internal_patches: patch.remove()
        self.internal_patches = []
        for arg in args:
            temp_patch = self.ax.add_patch(arg)
            self.internal_patches.append(temp_patch)
    def add_patches(self,*args,**kwargs):
        if not isinstance(args, list): args = list(args)
        for arg in args:
            self.ax.add_patch(arg)
            self.internal_patches.append(arg)

    def add_rectangle(self,*args,**kwargs):
        clip_on, kwargs = mini_kwarg_resolver('clip_on',True,kwargs)
        in_layout, kwargs = mini_kwarg_resolver('in_layout',True,kwargs)

        rect = patches.Rectangle((args[0], args[1]), args[2], args[3], clip_on=clip_on,in_layout=in_layout, **kwargs)
        self.ax.add_patch(rect)
        self.internal_patches.append(rect)
    def add_circle(self,*args,**kwargs):
        if len(args) > 1: radius = args[1]
        else:
            radius = kwargs['radius']
            del kwargs['radius']
        circle = patches.Circle(args[0], radius = radius, **kwargs)
        self.ax.add_patch(circle)
        self.internal_patches.append(circle)
    def add_polygon(self,*args,**kwargs):
        poly = patches.Plygon(args[0], **kwargs)
        self.ax.add_patch(poly)
        self.internal_patches.append(poly)
    def get_patches(self,*args,**kwargs):
        return self.internal_patches
    def add_line(self,*args,**kwargs):
        line = mlines.Line2D(args[0],args[1],**kwargs)
        temp_line = self.ax.add_line(line)
        self.internal_lines.append(temp_line)
    def get_lines(self,*args,**kwargs):
        return self.internal_lines


    # %% FIGURE AND LAYOUT CUSTOMIZATION
    def set_aspect(self,*args,**kwargs):
        self.ax.set_aspect(*args,**kwargs)
        # self.fig_height = self.get_figheight()
        # self.fig_width = self.get_figwidth()
    def get_aspect(self, *args, **kwargs):
        return self.ax.get_aspect(*args, **kwargs)
    def set_figheight(self,val,**kwargs):
        self.fig_height = val
        self.fig.set_figheight(self.fig_height,**kwargs)
    def set_figwidth(self,val,**kwargs):
        self.fig_width = val
        self.fig.set_figwidth(self.fig_width,**kwargs)
    def get_figheight(self,*args,**kwargs):
        return self.fig.get_figheight(*args,**kwargs)
    def get_figwidth(self,*args,**kwargs):
        return self.fig.get_figwidth(*args,**kwargs)
