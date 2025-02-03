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
    
    if s_min < 0 and (cap0 == True or mn >= 0):
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

def ensure_data_frame(input_data):
    """
    Converts the input to a Pandas DataFrame whether it's a list, NumPy array, or already a DataFrame.
    """
    import pandas as pd
    import numpy as np
    if isinstance(input_data, pd.DataFrame):
        # If it's already a DataFrame, return it as is
        return input_data
    elif isinstance(input_data, list):
        # If it's a list, convert to DataFrame
        return pd.DataFrame(input_data)
    elif isinstance(input_data, np.ndarray):
        # If it's a NumPy array, convert to DataFrame
        return pd.DataFrame(input_data)
    else:
        # Raise an error if it's an unsupported type
        raise ValueError("Input data must be a list, NumPy array, or Pandas DataFrame.")

# Function to get the closest named color to a given RGB
def rgba_to_named_color(rgba):
    import matplotlib.colors as mcolors
    import numpy as np
    # List of single-letter color names
    single_letter_colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k',]
    single_letter_colors = list(mcolors.CSS4_COLORS.keys())

    # Extract RGB (ignore alpha channel for matching)
    rgba_rgb = rgba[:3]

    # Initialize variables to store closest matches
    min_distance = float('inf')
    closest_color = None

    # First, check for closest match among single-letter color names
    for color in single_letter_colors:
        # Get RGB of each single-letter color
        named_rgb = mcolors.to_rgb(color)

        # Calculate Euclidean distance between given RGBA and the single-letter RGB
        distance = np.linalg.norm(np.array(rgba_rgb) - np.array(named_rgb))

        if distance < min_distance:
            min_distance = distance
            closest_color = color

    # If a single-letter color is found, return it
    if closest_color:
        return closest_color

    # If no single-letter color is a close match, check against all CSS4 named colors
    named_colors = list(mcolors.CSS4_COLORS.keys())
    for color in named_colors:
        # Get RGB of each named color (they are already normalized to [0, 1] range)
        named_rgb = mcolors.to_rgb(color)

        # Calculate Euclidean distance between given RGBA and the named RGB
        distance = np.linalg.norm(np.array(rgba_rgb) - np.array(named_rgb))

        if distance < min_distance:
            min_distance = distance
            closest_color = color

    return closest_color


def match_rgba_to_color(rgba, color_list):
    import matplotlib.colors as mcolors
    import numpy as np
    # Extract the RGB values from the given RGBA (ignore alpha)
    rgba_rgb = rgba[:3]

    # Initialize a variable to track the minimum distance and closest color
    min_distance = float('inf')
    closest_color = None

    # Loop through the color names in the provided list
    for color_name in color_list:
        # Convert the named color to RGB using matplotlib's to_rgb function
        color_rgb = mcolors.to_rgb(color_name)

        # Calculate Euclidean distance between the input RGBA (RGB) and each color's RGB
        distance = np.linalg.norm(np.array(rgba_rgb) - np.array(color_rgb))

        # Update the closest color if a smaller distance is found
        if distance < min_distance:
            min_distance = distance
            closest_color = color_name

    return closest_color