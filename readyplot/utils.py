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
def numeric_checker(string):
    try:
        float(string)
        output = True
    except:
        output = False
    return output

def min_maxer(mn,mx,cap0 = False):
    from math import log10,floor
    mag = 10**int(floor(log10(abs(mx))))
    s_min = floor(mn / (0.5*mag)) * 0.5*mag
    s_max = floor(mx / (0.5*mag)) * 0.5*mag + 0.5*mag
    bins = round((s_max-s_min) / (0.5*mag))
    
    bins_even = bins % 2 == 0
    min_even = floor(s_min/(0.5*mag)) % 2 == 0
    max_even = floor(s_max/(0.5*mag)) % 2 == 0
    
    if bins_even:
        if min_even:
            s_min -= 0.5*mag
        if max_even:
            s_max += 0.5*mag
        bins = round((s_max-s_min) / (0.5*mag))
        
    if bins > 9:
        while bins % 3 != 0:
            s_min -= 0.5*mag
            bins = round((s_max-s_min) / (0.5*mag))
        bins = bins / 3
    
    if s_min < 0 and cap0 == True:
        s_max = s_max - s_min
        s_min = 0

    return s_min,s_max,bins

def is_mostly_strings(column, threshold=0.8):
    # Check if each element in the column is a string
    string_count = column.apply(lambda x: isinstance(x, str)).sum()

    # Calculate the proportion of strings
    proportion_strings = string_count / len(column)

    # Check if it exceeds the threshold
    return proportion_strings >= threshold
