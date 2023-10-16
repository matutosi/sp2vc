import pandas as pd
import numpy as np
import random
import unicodedata
import os
import shutil

def gen_dammy_veg(st = "st", sp = "sp", ab = None, ly = None):
    """
    Generate a Dummy Vegetation Data Frame

    This function creates a dummy data frame simulating vegetation data with
    customizable column names.

    Parameters:
    st (str): A string specifying the name of the column representing site or station. Default is "st".
    sp (str): A string specifying the name of the column representing species. Default is "sp".
    ab (str, optional): A string specifying the name of the column representing abundance. Default is None.
    ly (str, optional): A string specifying the name of the column representing layer. Default is None.

    Returns:
    DataFrame: A data frame containing dummy vegetation data.
    """
    veg = pd.DataFrame({
        st: [random.choice('ABCDEF') for _ in range(30)],
        sp: [random.choice('ABCDEF') for _ in range(30)]
    })
    if ab is not None:
        veg[ab] = np.random.rand(30)
    if ly is not None:
        veg[ly] = [random.choice('TSK') for _ in range(30)]
    return veg

def extract_veg(veg, st = "st", sp = "sp", ab = None, ly = None):
    """
    Extract and Rename Selected Vegetation Columns

    This function extracts selected columns from a vegetation dataset and renames them.

    Parameters:
    veg (DataFrame): A data frame containing vegetation data.
    st (str): A string specifying the name of the column representing site or station. Default is "st".
    sp (str): A string specifying the name of the column representing species. Default is "sp".
    ab (str, optional): A string specifying the name of the column representing abundance. Default is None.
    ly (str, optional): A string specifying the name of the column representing layer. Default is None.

    Returns:
    DataFrame: A data frame with selected and renamed columns from the input vegetation data.
    """
    cols = [st, sp]
    if ab is not None:
        cols.append(ab)
    if ly is not None:
        cols.append(ly)
    return veg[cols]

def replace_layers(veg):
    """
    Replace Vegetation Layers with New Nomenclature

    This function takes a vegetation data frame and replaces the layers with a new set of names.

    Parameters:
    veg (DataFrame): A data frame containing vegetation data with a layer column.

    Returns:
    DataFrame: A data frame with updated layer nomenclature.
    """
    ly_old = ["B", "B1", "B2", "T", "T1", "T2", "S", "S1", "S2",
              "H", "H1", "H2", "K", "K1", "K2",
              "高木層"   , "亜高木層",
              "低木層", "第1低木層", "第2低木層",
              "草本層", "第1草本層", "第2草本層"]
    ly_new = ["ly_10", "ly_11", "ly_12",
              "ly_10", "ly_11", "ly_12",
              "ly_20", "ly_21", "ly_22",
              "ly_30", "ly_31", "ly_32",
              "ly_30", "ly_31", "ly_32",
               "ly_11" ,  "ly_12",
              "ly_20" ,  "ly_21" ,  "ly_22",
              "ly_30" ,  "ly_31" ,  "ly_32"]
    layers = pd.DataFrame({'old': ly_old, 'new': ly_new})
    veg = pd.merge(veg, layers, left_on='old', right_on='new')
    return veg[['st', 'sp', 'ab', 'new']]

def bb2percent(bb):
    """
    Convert Braun-Blanquet scale (BB-scale) to Percentage Values

    This function takes a list of BB-scale 
    (e.g., "5", "4", "3", "2", "1", "+", "r") and converts 
    them into their corresponding percentage values.

    Parameters:
    bb (list): A list containing BB-scale.

    Returns:
    list: A list containing the corresponding percentage values.

    Note:
    BB-scale and their corresponding percentage values are as follows:
    "5" -> 87.5
    "4" -> 62.5
    "3" -> 37.5
    "2" -> 17.5
    "1" -> 6.5
    "+" -> 0.5
    "r" -> 0.1
    """
    
    bb = [87.5 if b=="5" else b for b in bb]
    bb = [62.5 if b=="4" else b for b in bb]
    bb = [37.5 if b=="3" else b for b in bb]
    bb = [17.5 if b=="2" else b for b in bb]
    bb = [6.5 if b=="1" else b for b in bb]
    bb = [0.5 if b=="+" else b for b in bb]
    bb = [0.1 if b=="r" else float(b) for b in bb]
    
    return bb

def aggregate_cover(veg, bb_scale = None, percent = None):
    """
    Aggregate Vegetation Cover Using Braun-Blanquet scale (BB-scale) and Percentage

    This function takes a vegetation data frame, and aggregates the cover by converting 
    BB-scale to percentages and then summing them with the given percentage column.

    Parameters:
    veg (DataFrame): A data frame containing vegetation data.
    bb_scale (str): The name of the column in `veg` that contains the BB-scale values.
    percent (str): The name of the column in `veg` that contains the percentage values.

    Returns:
    DataFrame: A data frame with an added 'cover' column representing the aggregated cover.

    Note:
    The function uses the `bb2percent` function to convert BB-scale values to percentages.
    The resulting 'cover' column is the sum of the converted BB-scale values and the provided percentage values.
    """
    
    if percent is None:
        veg[percent] = np.nan
    veg[bb_scale][~veg[percent].isna()] = 0
    veg = veg.fillna({'bb_scale': 0, 'percent': 0})
    
    bb_values = bb2percent(veg[bb_scale].tolist())
    
    veg['bb_scale'] = bb_values
    veg['percent'] = veg['percent'].astype(float)
    
    veg['cover'] = veg['

def convert_f2h(string):
    """
    Helper function for `convert_full2half()`

    This function converts any fullwidth characters in a string to their halfwidth form.

    Parameters:
    string (str): A character string possibly containing fullwidth characters.

    Returns:
    str: A character string with all fullwidth characters converted to halfwidth.
    """
    return unicodedata.normalize('NFKC', string)

def convert_full2half(path):
    """
    Convert Fullwidth Characters to Halfwidth in a File

    This function reads a delimited file, converts all fullwidth characters in it 
    to their halfwidth form, and then writes the converted data back to the file.

    Parameters:
    path (str): A string indicating the path to the file. Supports CSV and TSV files.

    Returns:
    bool: Logical `TRUE` indicating successful operation.

    Note:
    The delimiter of the file is inferred from the file extension.
    """
    
    # Backup the original file
    shutil.copy(path, path + ".back")
    
    # Determine the delimiter based on the file extension
    ext = os.path.splitext(path)[1]
    delim = ',' if ext == ".csv" else '\t'
    
    # Read the file
    df = pd.read_csv(path, delimiter=delim)
    
    # Convert all fullwidth characters to halfwidth
    df = df.applymap(lambda x: convert_f2h(x) if isinstance(x, str) else x)
    
    # Write the converted data back to the file
    df.to_csv(path, index=False, sep=delim)
    
    return True


def has_ab_ly(veg):
    """
    Check for Presence of Abundance and Layer Columns

    Checks if the provided vegetation data contains abundance (`ab`) and layer (`ly`) columns.

    Parameters:
    veg (DataFrame): A data frame containing vegetation data.

    Returns:
    str: A character string indicating the presence of `ab` and `ly` columns.
        Possible values: "has_both", "has_ab", "has_ly", "has_none".
    """
    
    has_ab = 'ab' in veg.columns
    has_ly = 'ly' in veg.columns
    
    if has_ab and has_ly:
        return 'has_both'
    elif has_ab and not has_ly:
        return 'has_ab'
    elif not has_ab and has_ly:
        return 'has_ly'
    else:
        return 'has_none'

def arrange_veg(veg):
    """
    Arrange Vegetation Data by Columns

    Arranges the vegetation data based on available columns: site (`st`), layer (`ly`), and abundance (`ab`).

    Parameters:
    veg (DataFrame): A data frame containing vegetation data.

    Returns:
    DataFrame: A data frame arranged based on the presence of `st`, `ly`, and `ab` columns.
    """
    
    ab_ly = has_ab_ly(veg)
    
    if ab_ly == 'has_both':
        return veg.sort_values(by=['st', 'ly', 'ab'], ascending=[True, True, False])
    elif ab_ly == 'has_ab':
        return veg.sort_values(by=['st', 'ab'], ascending=[True, False])
    elif ab_ly == 'has_ly':
        return veg.sort_values(by=['st', 'ly'])
    else:
        return veg


def align_sp(veg):
    """
    Align Species Names to generate Species2Vec input data

    Combines the species names in the `sp` column of the vegetation data into a single string.

    Parameters:
    veg (DataFrame): A data frame containing vegetation data.

    Returns:
    str: A character string of species names combined with spaces.
    """
    
    return ' '.join(veg['sp'])

def devide(df, col):
    """
    Wrapper function for `base::split()`

    Splits the provided data frame into a list of data frames based on the unique values of a specified column.

    Parameters:
    df (DataFrame): A data frame to be divided.
    col (str): A character string representing the name of the column used for division.

    Returns:
    dict: A dictionary of data frames, each corresponding to a unique value of the specified column.
    """
    
    return {group: df_group for group, df_group in df.groupby(col)}

def prep_sp2vec(veg, path = None):
    """
    Prepare sp2vec input data

    Prepares data for sp2vec by arranging the data, 
    dividing it by site, and aligning species names.

    Parameters:
    veg (DataFrame): A data frame containing vegetation data.
    path (str): A string indicating the path to the file. 

    Returns:
    DataFrame: A DataFrame containing species names aligned for vector conversion.
    """
    
    # Arrange the vegetation data
    veg = arrange_veg(veg)
    
    # Divide the vegetation data by site
    divided_veg = devide(veg, 'st')
    
    # Align species names
    sp_alignment = {site: align_sp(df) for site, df in divided_veg.items()}
    
    # Convert to DataFrame
    sp_alignment = pd.DataFrame(list(sp_alignment.items()), columns=['st', 'sp'])
    
    # Write to file if path is provided
    if path is not None:
        sp_alignment.to_csv(path, index=False, sep='\t')
    
    return sp_alignment
