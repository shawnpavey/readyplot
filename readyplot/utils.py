#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A utility file, utils, which holds many common small functions that are often mathematical/do not use 'self'
@author: Shawn Pavey
"""
#%% IMPORT PACKAGES
def numeric_checker(string):
    import re
    string = re.sub(r'−', '-', string)
    string.replace("–", "")
    string.replace("-", "")
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

def check_labels_in_DF(DF,xlab,ylab,zlab):
    column_names = DF.columns
    outputs = []
    for lab in [xlab,ylab,zlab]:
        if lab in column_names:
            pass
        else:
            lab = None
        outputs.append(lab)
    return outputs

def mini_kwarg_resolver(key,def_val,kwargs):
    if key not in kwargs:
        output = def_val
    else:
        output = kwargs[key]
        del kwargs[key]
    return output, kwargs

def find_closest(dictionary, x_pos):
    # Initialize variables to track the closest key and value
    closest_key = None
    closest_value = None
    min_diff = float('inf')  # Start with a very large difference

    # Iterate over the dictionary to find the closest key
    for key, value in dictionary.items():
        diff = abs(value - x_pos)  # Calculate the absolute difference between key and input x_pos
        if diff < min_diff:
            min_diff = diff
            closest_key = key
            closest_value = value

    return closest_key, closest_value

def dict_update_nested(default_dictionary, input_dictionary):
    """
    Recursively update a nested dictionary
    """
    for key, value in input_dictionary.items():
        if isinstance(value, dict):
            if key in default_dictionary:
                default_dictionary[key] = dict_update_nested(default_dictionary[key], value)
            else:
                default_dictionary[key] = value
        else:
            default_dictionary[key] = value
    return default_dictionary

def is_transparent(color):
    """
    Checks if a given color is transparent.

    :param color: Color (string, hex, or tuple)
    :return: True if the color is transparent (alpha == 0), else False
    """
    import matplotlib.colors as mcolors
    # If the color is a string, convert it to RGBA
    if isinstance(color, str):
        try:
            rgba = mcolors.to_rgba(color)
        except ValueError:
            raise ValueError(f"Invalid color string: {color}")

    # If it's a tuple, it's already in RGBA format, just use it directly
    elif isinstance(color, tuple):
        rgba = color

    # If it's hex, convert to RGBA
    elif isinstance(color, str) and color.startswith("#"):
        rgba = mcolors.hex2color(color) + (1,)  # Add alpha=1 for opaque

    else:
        raise ValueError(f"Unsupported color format: {color}")

    # Return True if alpha (last value) is 0 (transparent)
    return rgba[3] == 0


def count_number_characters(x):
    s = str(x).lstrip('.').lstrip('-')
    if '.' in s:
        s = s.replace('.', '')
    return len(s)


def delete_ticks_by_sig_figs(ax,max_sig_figs = 2,x_or_y = 'y'):
    if x_or_y not in ['x', 'y']:
        raise ValueError("x_or_y must be 'x' or 'y'")

        # Select the ticks and labels based on x_or_y argument
    if x_or_y == 'y':
        ticks = ax.yaxis.get_ticklines()
        labels = ax.get_yticklabels()
    else:
        ticks = ax.get_xticks()
        labels = ax.get_xticklabels()

    counter = 0
    for label in labels:
        if count_number_characters(label.get_text()) > max_sig_figs:
            while label.get_text()[-1] == '0' and count_number_characters(label.get_text()) > max_sig_figs:
                label.set_text(label.get_text()[:-1])

            if count_number_characters(label.get_text()) > max_sig_figs:
                label.set_color((0, 0, 0, 0))
            else: print('Its been fixed', label.get_text(),label)

            counter += 1

    label_counter = 0
    for tick in ticks:
        tick.set_color(labels[int(label_counter)].get_color())
        label_counter += 0.5


