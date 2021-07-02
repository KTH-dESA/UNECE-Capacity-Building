# This file imports all the packages
import pandas as pd
pd.set_option('mode.chained_assignment', None)
import numpy as np
from IPython.display import HTML
import IPython.core.display as di
import plotly as py
import cufflinks
import plotly.offline as pyo
from plotly.offline import plot, iplot, init_notebook_mode
pyo.init_notebook_mode()
cufflinks.go_offline()
cufflinks.set_config_file(world_readable=True, theme='white')
import os, sys
import subprocess
from tkinter import filedialog
from tkinter import *
from collections import defaultdict
import zipfile
from pathlib import Path
from IPython.display import HTML
import ipywidgets as widgets
from IPython.display import display
import matplotlib as plt
from ipywidgets import interact, interactive, fixed, interact_manual
import psutil
import pickle
import plotly.graph_objs as go
import plotly.io as pio
from IPython.display import display
from IPython.display import HTML
import IPython.core.display as di # Example: di.display_html('<h3>%s:</h3>' % str, raw=True)
#
homedir=os.getcwd()
import openpyxl
from openpyxl import load_workbook
from openpyxl import workbook
import glob 
import plotly.express as px
