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
# readyplot/__init__.py

from .boxwhisker_plotter import BoxWhiskerPlotter
from .scatter_plotter import ScatterPlotter

def boxwhisker_plotter(DFs=None, x=None, y=None, z=None, xlab='Group', ylab='ylab', zlab='zlab',
                       folder_name='OUTPUT_FIGURES', colors=['c', 'm', 'g'], low_y_cap0=True,
                       handles_in_legend=3, fig_width=7, fig_height=5, box_width=0.9,
                       custom_y_label=None):
    return BoxWhiskerPlotter(DFs=DFs, x=x, y=y, z=z, xlab=xlab, ylab=ylab, zlab=zlab,
                             folder_name=folder_name, colors=colors, low_y_cap0=low_y_cap0,
                             handles_in_legend=handles_in_legend, fig_width=fig_width,
                             fig_height=fig_height, box_width=box_width,
                             custom_y_label=custom_y_label)

def scatter_plotter(DFs=None, x=None, y=None, z=None, xlab='Group', ylab='ylab', zlab='zlab',
                    folder_name='OUTPUT_FIGURES', colors=['c', 'm', 'g'], low_y_cap0=True,
                    handles_in_legend=3, fig_width=7, fig_height=5, box_width=0.9,
                    custom_y_label=None):
    return ScatterPlotter(DFs=DFs, x=x, y=y, z=z, xlab=xlab, ylab=ylab, zlab=zlab,
                          folder_name=folder_name, colors=colors, low_y_cap0=low_y_cap0,
                          handles_in_legend=handles_in_legend, fig_width=fig_width,
                          fig_height=fig_height, box_width=box_width,
                          custom_y_label=custom_y_label)

__all__ = ['boxwhisker_plotter', 'scatter_plotter', 'BoxWhiskerPlotter', 'ScatterPlotter']