''' Import Libraries '''
import numexpr

numexpr.set_num_threads(numexpr.detect_number_of_cores())
# print(numexpr.detect_number_of_cores())

import os
# os.environ['NUMEXPR_MAX_THREADS'] = numexpr.detect_number_of_cores()

import warnings
warnings.filterwarnings('ignore')

import re
from datetime import datetime
import datetime
import sys
# import jwt
import time
import uuid
import base64
import getpass
import itertools
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont, ImageColor
from pytz import timezone
import webbrowser
import matplotlib

#Streamlit
import streamlit as st
from streamlit import runtime
# from streamlit import cli as stcli
from streamlit.web import cli as stcli
import streamlit.components.v1 as html

##Database Cnnecectivity
import sqlite3

#imageai
from imageai.Detection.Custom import CustomObjectDetection

#page Configuration
st.set_page_config(
    page_title='VPR',
    page_icon=':earth_africa:',
    layout='wide',
)
#hiding Streamlit Logo
hide_streamlit_style = """
        <style>
        MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

''' Define Path '''
if 'win' in sys.platform:
    path = r"C:\Users\HP\OneDrive\Desktop\CDAC-PRO\VPR\streamlit-ui"
else:
    path = '/home/'+ getpass.getuser() +'/VPR'


cdac_logo = Image.open(r"C:\Users\HP\OneDrive\Desktop\CDAC-PRO\VPR\streamlit-ui\Config\images\cdaclogo.png")
