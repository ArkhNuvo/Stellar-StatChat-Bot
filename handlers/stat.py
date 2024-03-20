import pandas as pd
import numpy as np
from scipy.stats import trim_mean, iqr, median_abs_deviation
from utility.callbackdata import UserData
import seaborn as sns
import matplotlib.pyplot as plt
import os
import base64
from aiogram.types import BufferedInputFile
import io
import textwrap


def doc_import(doc_name):
    return pd.read_csv(f"{UserData.folder_path}/{doc_name}")
     

def columns_print(doc_name):

    df = doc_import(doc_name)
    column_list = []
    columns_type_dict = dict(df.dtypes)
    
    for column in df.columns:
        column_list.append(column)
    
    return columns_type_dict

    
def description_print(doc_name):
    
    df = doc_import(doc_name)
    describe_df = round(df.describe(include="all"), 2)
    describe_df.insert(0, 'Statistics', describe_df.index)

    buffer = io.BytesIO()
    
    fig, ax = plt.subplots(figsize=(len(describe_df.columns)*1.45, 7))
    ax.axis('tight')
    ax.axis('off')
    table = ax.table(cellText=describe_df.values,
                 colLabels=describe_df.columns,
                 cellLoc='center',
                 loc='center', 
                 bbox = [0.05, 0.05, 0.9, 0.9])
    
    #Adjusting the spacing between subplots
    table.auto_set_column_width(col=list(range(len(describe_df.columns))))
    plt.savefig(buffer, format="png")
    plt.clf()
    
    buffer.seek(0)
    image_str = base64.b64encode(buffer.read()).decode('utf-8')
    
    return image_str


def info_print(doc_name):
    from io import StringIO
    from contextlib import redirect_stdout
    
    df = doc_import(doc_name)
    buffer = StringIO()
    with redirect_stdout(buffer):
        df.info()
    df_info = buffer.getvalue()

    return df_info



"""
Variable Statistics
"""
def mean_count(doc_name, column_name):
    df = doc_import(doc_name)
    mean = df[column_name].mean()
    return mean

def median_count(doc_name, column_name):
    df = doc_import(doc_name)
    median = df[column_name].median()
    return median

def mode_count(doc_name, column_name):
    df = doc_import(doc_name)
    mode = df[column_name].mode()
    mode_number = str(mode).split()
    return mode_number[1]

def trim_mean_10_count(doc_name, column_name):
    df = doc_import(doc_name)
    trim_mean_10=trim_mean(df[column_name], proportiontocut = 0.1)
    return trim_mean_10

def range_count(doc_name, column_name):
    df = doc_import(doc_name)
    range = df[column_name].max() - df[column_name].min()
    return range

def iqrange_count(doc_name, column_name):
    df = doc_import(doc_name)
    iqrange = iqr(df[column_name])
    return iqrange

def var_count(doc_name, column_name):
    df = doc_import(doc_name)
    var = df[column_name].var()
    return var

def std_dev_count(doc_name, column_name):
    df = doc_import(doc_name)
    std_dev = df[column_name].std()
    return std_dev

def mad_count(doc_name, column_name):
    df = doc_import(doc_name)
    mad = median_abs_deviation(df[column_name])
    return mad



"""
Categorical Statistics
"""

def unique_count(doc_name, column_name):
    df = doc_import(doc_name)
    count_unique = len(df[column_name].unique())
    return count_unique

def unique(doc_name, column_name):
    df = doc_import(doc_name)
    unique_list = df[column_name].unique()
    return unique_list

def value_counts_count(doc_name, column_name):

    df = doc_import(doc_name)
    value_count = df[column_name].value_counts(normalize=True)
    return value_count


"""
Charts & Histograms

    Categorical Data:
"""
def pie_chart(doc_name, column_name):
    df = doc_import(doc_name)
    buffer = io.BytesIO()
    plt.subplots(figsize=(8, 8))
    if len(df[column_name].unique()) > 8: 
        value_counts = df[column_name].value_counts()
        top_categories = value_counts.head(5).index
        df[f'{column_name}_filtered'] = df[column_name].where(df[column_name].isin(top_categories), 'Others')
        sns.set_style("whitegrid")
        plt.pie(df[f'{column_name}_filtered'].value_counts(), 
                labels=df[f'{column_name}_filtered'].value_counts().index, 
                autopct="%0.2f%%", startangle=90, shadow=True, textprops={'fontsize':13} ) #, 'weight': 'bold'
        plt.gcf().subplots_adjust(left=0.1, top=0.83, right=0.9)
    
    else:
        unics = list(df[column_name].unique())
        sns.set_style("whitegrid")
        plt.pie(df[column_name].value_counts(), labels = unics, autopct="%0.2f%%", 
                startangle=90, shadow=True, textprops={'fontsize':13}) 
        plt.gcf().subplots_adjust(left=0.15, top=0.83)
     

    plt.title(f'{column_name} Proportions', fontdict={'size':20})
    plt.savefig(buffer, format="png")
    plt.clf()
    
    buffer.seek(0)
    image_str = base64.b64encode(buffer.read()).decode('utf-8')
    
    return image_str

def count_plot(doc_name, column_name):
    
    df = doc_import(doc_name)
    buffer = io.BytesIO()
    plt.subplots(figsize=(8, 8))
    if len(df[column_name].unique()) > 8:
        value_counts = df[column_name].value_counts()
        top_categories = value_counts.head(5).index
        df[f'{column_name}_filtered'] = df[column_name].where(df[column_name].isin(top_categories), 'Others')
        ax = sns.countplot(x=f'{column_name}_filtered', data=df, palette='Set2')
        ax.set_xticklabels([textwrap.fill(label, width=10) for label in df[f'{column_name}_filtered'].unique()])
        
    else:
        
        ax = sns.countplot(x = f'{column_name}', hue=f'{column_name}', data = df, palette='Set2')
        ax.set_xticklabels([textwrap.fill(label, width=10) for label in df[column_name].unique()])
    
    plt.title(f'Count Plot of {column_name}', fontdict={'size':22.5})
    
    for p in ax.patches:
        label_text = f'{int(p.get_height())}'
        label_text_wrapped = textwrap.fill(label_text, width = 12)
        ax.text(p.get_x() + p.get_width() / 2., p.get_height(), label_text_wrapped,
                ha='center', va='center', fontsize=8, rotation=0,
                bbox=dict(boxstyle='round,pad=0.3', edgecolor='white', facecolor='white'))

    plt.gcf().subplots_adjust(left=0.15, top=0.83)
    plt.savefig(buffer, format="png")
    plt.clf()
    
    buffer.seek(0)
    image_str = base64.b64encode(buffer.read()).decode('utf-8')
    
    return image_str

"""
    Numerical Data:
"""

def dis_plot_num(doc_name, column_name):
    df = doc_import(doc_name)
    buffer = io.BytesIO()

    plt.subplots(figsize=(15, 15))
    sns.displot(data = df, x = column_name, kind='hist', palette='winter', bins=15)
    plt.title(f'Count Plot of {column_name}', fontdict={'size':15})
    plt.gcf().subplots_adjust(left=0.15, top=0.83)
    plt.savefig(buffer, format="png")
    plt.clf()
    
    buffer.seek(0)
    image_str = base64.b64encode(buffer.read()).decode('utf-8')
    
    return image_str

def box_plot(doc_name, column_name):
    df = doc_import(doc_name)
    
    buffer = io.BytesIO()
    
    plt.subplots(figsize=(8, 8))
    sns.boxplot(y = column_name, data=df, palette = "winter")
    plt.title(f'Box Plot of {column_name}', fontdict={'size':15})
    plt.savefig(buffer, format="png")
    plt.clf()
    
    buffer.seek(0)
    image_str = base64.b64encode(buffer.read()).decode('utf-8')
    
    return image_str

def strip_plot(doc_name, column_name):
    df = doc_import(doc_name)
    
    buffer = io.BytesIO()

    plt.subplots(figsize=(8, 8))
    sns.stripplot(x=df[f'{column_name}'], alpha=.2)
    plt.title(f'Strip Plot of {column_name}', fontdict={'size':15})
    plt.savefig(buffer, format="png")
    plt.clf()

    buffer.seek(0)
    image_str = base64.b64encode(buffer.read()).decode('utf-8')
    
    return image_str

def swarm_plot(doc_name, column_name):
    df = doc_import(doc_name)    
    
    buffer = io.BytesIO()    
    
    if len(df) >= 10000:
        perc = 0.002
    elif len(df) >= 5000:
        perc = 0.1
    elif len(df) >= 2500:
        perc = 0.2
    elif len(df) >= 1000:
        perc = 0.5
    else:
        perc = 1    
    df_sub = df.sample(n=int(df.shape[0]*perc))
    
    plt.subplots(figsize=(8, 8))
    sns.swarmplot(x=df_sub[f'{column_name}'])
    plt.title(f'Swarm Plot of {column_name}', fontdict={'size':15})
    plt.savefig(buffer, format="png")
    plt.clf()

    
    buffer.seek(0)
    image_str = base64.b64encode(buffer.read()).decode('utf-8')
    
    return image_str


def violin_plot(doc_name, column_name):
    df = doc_import(doc_name)
    
    buffer = io.BytesIO()
    
    plt.subplots(figsize=(8, 8))
    sns.violinplot(df[f'{column_name}'], orient='vertical', palette='winter', alpha=0.5,  inner_kws=dict(box_width=20, whis_width=2, color=".3"))
    plt.title(f'Violin Plot of {column_name}', fontdict={'size':15})

    plt.savefig(buffer, format="png")
    plt.clf()

    buffer.seek(0)
    image_str = base64.b64encode(buffer.read()).decode('utf-8')
    
    return image_str
