# -*- coding: utf-8 -*-
"""dashboard_เบาหวาน.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1VyFDf_TIaQMGaIihUhYBM4lcJzw3OR7M
"""

# from google.colab import drive
# drive.mount('/gdrive')
# %cd /gdrive

# from google.colab import drive
# drive.mount('/content/drive')


import pandas as pd
import xml.etree.ElementTree as et
import os
from pathlib import Path
import glob
import streamlit as st 
from matplotlib import pyplot as plt
import streamlit as st
from PIL import Image
# df = pd.read_xml('570-ws-training.xml')

# from pandas.core.construction import (
#     create_series_with_explicit_dtype,
#     extract_array,
#     is_empty_data,
#     sanitize_array,
# )
from pandas.core.construction import is_empty_data
import xml.etree.ElementTree as ET
tree = ET.parse('570-ws-training.xml')
root = tree.getroot()
# taglist = []
# for child in root:
#     #print(child.tag, child.attrib)
#     taglist.append(child.tag)
# #print(taglist)
# dict_attr = dict()
# for i in range(len(root)):
#       dict_list = dict()
#       try:
#           key_list = root[i][0].keys()
#       except (IndexError, ValueError):
#           key_list = ['empty']
#           dict_attr[taglist[i]]={'empty_ts': ['07-12-2021 07:13:07']}

#       #print(taglist[i])
#       for attr in key_list:
#          dict_list[taglist[i]+'_'+attr] = []
#       for event in root[i]:
#          for attr in key_list:
#             dict_list[taglist[i]+'_'+attr].append(event.attrib[attr])
# #            print(event.tag, event.attrib)   
# #            dict_list.append(event.attrib)
#          dict_attr[taglist[i]] =  dict_list
# print("Tag, num_items")
# for i in range(len(root)):
#     print(i, taglist[i], len(dict_attr[taglist[i]]))

path = '570-ws-training.xml'
df = pd.read_xml(path, xpath=".//event")

# ดึงข้อมูลแต่ละ taglist ไปเป็น dataframe
for child in root:
  name = child.tag
  try:
    locals()['{0}'.format(name)] = pd.read_xml(path, xpath = "./"+name+"/event")
    # print(name)
  except (IndexError, ValueError):
    locals()['{0}'.format(name)] = pd.DataFrame({'empty_ts': ['07-12-2021 07:13:07']})
    # print(name)

# """## **Lastest Data**
# # glucose_level

# """

lastest_glu = glucose_level
lastest_glu['ts'] = pd.to_datetime(lastest_glu.ts, format = '%d-%m-%Y %H:%M:%S')
lastest_glu.sort_values(by = ['ts'], ascending = False, inplace = True) 

lastest_glu = lastest_glu.assign(time = pd.cut(lastest_glu.ts.dt.hour,[0,6,12,18,24], labels=['night', 'morning', 'afternoon', 'evening'], right=False, include_lowest=True))
lastest_glu['ts'] = pd.to_datetime(lastest_glu['ts'], format = '%d-%m-%Y %H:%M:%S').dt.strftime('%d-%m-%Y %H:%M:%S')

# glucose_level['date'] = pd.to_datetime(glucose_level.ts, format = '%d-%m-%Y %H:%M:%S').dt.strftime('%d-%m-%Y')
# glucose_level['time'] = pd.to_datetime(glucose_level.ts, format = '%d-%m-%Y %H:%M:%S').dt.strftime('%H:%M:%S')

# print(lastest_glu.iloc[0])


# # **Glucose overview**
# """




# Use the full page instead of a narrow central column
st.set_page_config(layout="wide")

# Space out the maps so the first one is 2x the size of the other three
col1, col2 = st.columns(2)

with col1:
    
    """##### **รายบุคคล**"""

      # col1, col2, col3 = st.columns(3)
    
    #Left Column
    # with col1:
    #ต่อdataframe glucose_level กับ finger_stick
    glu_level = pd.concat([glucose_level, finger_stick],ignore_index=True)
    #แปลง ค่าระดับน้ำตาล เป็น Hypo', 'Low', 'normal', 'High', 'Hyper'
    glu_level['lavel'] = pd.cut(glu_level['value'], bins=[0,54,90,120,220,500], labels=['Hypo', 'Low', 'normal', 'High', 'Hyper'])

    #group Hypo', 'Low', 'normal', 'High', 'Hyper' ว่าแต่ละอันมีกี่ rows
    category_glu = glu_level.groupby(['lavel']).agg({'value': 'count'})

    #คิดเปอร์เซ็นของแต่ละ group
    percentage_lavel_glu = glu_level.lavel.value_counts(normalize=True).mul(100).round(1).astype(str) + '%'

    # Setting size in Chart based on
    # given values
    # sizes = [sum.value.Hypo, sum.value.Low, sum.value.normal, sum.value.High, sum.value.Hyper]
    sizes = [category_glu.value.Hypo, category_glu.value.Low, category_glu.value.normal, category_glu.value.High, category_glu.value.Hyper]
    Hypo = "Hypo : "+ str(category_glu.value.Hypo)
    Low = "Low : "+ str(category_glu.value.Low)
    Normal = "Normal : "+ str(category_glu.value.normal)
    High = "High : "+str(category_glu.value.High)
    Hyper = "Hyper : "+str(category_glu.value.Hyper)

    # Setting labels for items in Chart
    labels = [Hypo, Low, Normal, High, Hyper]

    # colors
    colors = ['#9772FB', '#516BEB', '#21BF73', '#FEB139','#F05454']

    # explosion
    explode = (0.01, 0.01, 0.01, 0.01, 0.01)

    # Pie Chart
    # plt.subplot(1, 3, 1)
    # plt.subplot(3, 1, 1)
    fig4, ax4 = plt.subplots() 
    ax4.pie(sizes, colors=colors,
                autopct='%1.1f%%', pctdistance=0.85,
                explode=explode)

    # draw circle
    centre_circle = plt.Circle((0, 0), 0.50, fc='white')
    fig4 = plt.gcf()

    # Adding Circle in Pie chart
    fig4.gca().add_artist(centre_circle)

    # Adding Title of chart
    # plt.title('ภาพรวมของระดับน้ำตาล')
    # ax4.title(u'ภาพรวมของระดับน้ำตาล',fontname='Tahoma',fontsize=9)
    # Glucose overview
    # Add Legends
    # plt.legend(labels, loc='upper center', bbox_to_anchor=(0.5, -0.05))
    ax4.legend(labels,   loc="center left",bbox_to_anchor=(1, 0, 0.5, 1), title="Legends")

    # Displaying Chart
    # plt.show()

    # with col2:
        # """## **Daily insulin average**
        # bolus คืออินซูลินชนิดออกฤทธิ์เร็ว เช่น ฉีดตอนรับประทานอาหารหรือฉีดเพื่อแก้ไข <br>
        # basal *คืออินซูลินชนิดออกฤทธิ์ช้า* หรือที่เรียกว่าออกฤทธิ์นาน
        # """
    # container.pyplot(fig)

    Date = "16-01-2022"

    basal['ts']   = pd.to_datetime(basal.ts, format = '%d-%m-%Y %H:%M:%S')
    basal['date'] = basal['ts'].dt.date
    basal['ts']   = pd.to_datetime(basal['ts'], format = '%d-%m-%Y %H:%M:%S').dt.strftime('%d-%m-%Y %H:%M:%S')
    basal['date'] = pd.to_datetime(basal['date'], format = '%Y-%m-%d').dt.strftime('%d-%m-%Y')
    basal_date    = basal.loc[basal['date'] == Date]
    mean_basal_daily = basal_date.mean()
    # mean_basal_daily

    bolus = bolus.rename(columns = {'ts_begin':'ts','dose':'value'})
    bolus_df = bolus[["ts", "value"]]

    bolus_df['ts']   = pd.to_datetime(bolus_df.ts, format = '%d-%m-%Y %H:%M:%S')
    bolus_df['date'] = bolus_df['ts'].dt.date
    bolus_df['ts']   = pd.to_datetime(bolus_df['ts'], format = '%d-%m-%Y %H:%M:%S').dt.strftime('%d-%m-%Y %H:%M:%S')
    bolus_df['date'] = pd.to_datetime(bolus_df['date'], format = '%Y-%m-%d').dt.strftime('%d-%m-%Y')
    bolus_date       = bolus_df[bolus_df['date']  == Date]
    mean_bolus_daily = bolus_date.mean()
    # mean_bolus_daily

    #ผลรวม dose
    sum_dose_basal = basal_date.value.sum()
    sum_dose_bolus = bolus_date.value.sum()
    sum_dose = sum_dose_basal+sum_dose_bolus
    sum_dose = round(sum_dose, 2)
    sum_dose_str = str(sum_dose) +'\n units'

    # Setting size in Chart based on
    # given values
    sizes = [sum_dose_bolus , sum_dose_basal]

    # Setting labels for items in Chart
    labels = ['Bolus', 'Basal']

    # colors
    colors = ['#516BEB', '#FEB139']

    #explosion
    explode = (0.01, 0.01)

    # Pie Chart
    # plt.subplot(1, 3, 2)
    # plt.subplot(3, 1, 2)
    fig5, ax5 = plt.subplots() 
    ax5.pie(sizes, colors=colors,
                autopct='%1.1f%%', pctdistance=0.85,
                explode=explode)

    # outside = ax.pie(sizes, radius=1, pctdistance=1-width/2,
    #                  labels=labels,**kwargs)[0]

    # plt.text(0.4, 0.4, sum_dose_str , va = 'center', ha = 'center', backgroundcolor = 'white')

    # draw circle
    centre_circle = plt.Circle((0, 0), 0.50, fc='white')
    fig = plt.gcf()

    # Adding Circle in Pie chart
    fig.gca().add_artist(centre_circle)

    # Adding Title of chart
    # plt.title('เฉลี่ยการฉีดอินซูลินต่อวัน')
    # ax5.title(u'เฉลี่ยการฉีดอินซูลินต่อวัน',fontname='Tahoma',fontsize=9)
    # Daily insulin average
    kwargs = dict(size=10, color='white', va='center', fontweight='bold')
    ax5.text(0, 0, sum_dose_str, ha='center',
                bbox=dict(boxstyle='round', edgecolor='none'),
                **kwargs)

    # plt.text(0, 0, sum_dose_str, ha='center',
    #         bbox=dict(boxstyle='round', facecolor='#9772FB', edgecolor='none'),
    #         **kwargs)
    # Add Legends
    # plt.legend(labels, loc='upper center', bbox_to_anchor=(0.5, -0.05))
    ax5.legend(labels,   loc="center left",bbox_to_anchor=(1, 0, 0.5, 1), title="Legends")

    # container.pyplot(fig)


    # Displaying Chart
    # plt.show()

    ###### Daily meal average

    # with col3:

    meal_df = meal.rename(columns = {'type':'cate'})
    # meal_df = bolus[["cate", "carbs"]]
    # meal_df

    meal_df['ts']   = pd.to_datetime(meal_df.ts, format = '%d-%m-%Y %H:%M:%S')
    meal_df['date'] = meal_df['ts'].dt.date
    meal_df['ts']   = pd.to_datetime(meal_df['ts'], format = '%d-%m-%Y %H:%M:%S').dt.strftime('%d-%m-%Y %H:%M:%S')
    meal_df['date'] = pd.to_datetime(meal_df['date'], format = '%Y-%m-%d').dt.strftime('%d-%m-%Y')
    meal_date    = meal_df.loc[meal_df['date'] == Date]
    mean_meal_daily = meal_date.mean()
    # mean_meal_daily

    carb_sum = meal_date.carbs.sum()
    carb_sum = round(carb_sum)
    carb_sum = str(carb_sum) +'\n cal'

    # carb_sum

    meal_date = meal_date.groupby(['cate']).agg({'carbs': 'mean'})
    meal_date.reset_index(inplace=True)


    # meal_date

    # meal_date

    name_crabs = meal_date.carbs.to_numpy()
    name_cate = meal_date.cate.to_numpy()

    # Setting size in Chart based on
    # given values
    sizes = name_crabs

    # Setting labels for items in Chart
    labels = name_cate

    # colors
    colors = ['#8EA7E9', '#DFFFD8', '#F7C8E0', '#95BDFF','#FFC93C']


    #explosion
    explode = [ 0.01 for i in labels ]


    # Pie Chart
    # plt.subplot(1, 3, 3)
    fig6, ax6 = plt.subplots() 
    ax6.pie(sizes, colors=colors,
                autopct='%1.1f%%', pctdistance=0.85,
                explode=explode)

    # outside = ax.pie(sizes, radius=1, pctdistance=1-width/2,
    #                  labels=labels,**kwargs)[0]

    # plt.text(0.4, 0.4, sum_dose_str , va = 'center', ha = 'center', backgroundcolor = 'white')

    # draw circle
    centre_circle = plt.Circle((0, 0), 0.50, fc='white')
    fig = plt.gcf()

    # Adding Circle in Pie chart
    fig.gca().add_artist(centre_circle)

    # Adding Title of chart
    # b = a.encode("cp874")
    # c = b.decode("cp874")
    # st.write("เฉลี่ยการทานอาหารต่อวัน")
    # ax6.title(u'เฉลี่ยการทานอาหารต่อวัน',fontname='Tahoma',fontsize=9)
    # plt.title(a)
    # Daily meal average

    kwargs = dict(size=10, color='white', va='center', fontweight='bold')
    ax6.text(0, 0, carb_sum, ha='center',
                bbox=dict(boxstyle='round', edgecolor='none'),
                **kwargs)

    # plt.text(0, 0, sum_dose_str, ha='center',
    #         bbox=dict(boxstyle='round', facecolor='#9772FB', edgecolor='none'),
    #         **kwargs)
    # Add Legends
    # plt.legend(labels, loc='upper center', bbox_to_anchor=(0.5, -0.05))
    ax6.legend(labels,   loc="center left",bbox_to_anchor=(1, 0, 0.5, 1), title="Legends")

    # plt.legend(labels,   loc="upper center",bbox_to_anchor=(1, 0, 0.5, 1), title="Legends")

    # Displaying Chart
    # plt.show()
    
    # st.pyplot(fig)
    # plt.plot()
    st.write("ภาพรวมของระดับน้ำตาล")
    st.pyplot(fig4)
    st.write("เฉลี่ยการฉีดอินซูลินต่อวัน")
    st.pyplot(fig5)
    st.write("เฉลี่ยการทานอาหารต่อวัน")
    st.pyplot(fig6)


with col2:
    
    # """##### **แนวโน้มทำนายค่าน้ำตาลในเลือด**"""
    image = Image.open('1678271221085@2x_Tahoma.jpg')
    st.image(image)
######################################################################################################################
###########################################โค้ดเริ่มพี่จิ๊บ แบบภาพรวม#######################################################

import datetime as dt
import io
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt



df_plan = pd.read_csv("dmthai_Feb2023/user_plan_240223_2214.csv")
df_profile = pd.read_csv("dmthai_Feb2023/user_profile_240223_2215.csv",parse_dates={'DOB': ['date_of_birth']},infer_datetime_format=True,dayfirst=True)
df_lastesgrowth = pd.read_csv("dmthai_Feb2023/user_profile_latest_growth_240223_2215.csv")
df_doctorconnect = pd.read_csv("dmthai_Feb2023/doctor_connection_child_240223_2217.csv")
# df_user = pd.read_csv("dmthai_Feb2023/user_240223_2214.csv")
df_alert = pd.read_csv("dmthai_Feb2023/user_alert_240223_2216.csv")
df_log = pd.read_csv("dmthai_Feb2023/user_log_240223_2216.csv",parse_dates={'Date': ['date']},infer_datetime_format=True,dayfirst=True)
#df_log = pd.read_csv("/content/drive/MyDrive/Colab Notebooks/dmthai_Feb2023/user_log_240223_2216.csv")
df_mood = pd.read_csv("dmthai_Feb2023/mood_240223_2218.csv")
df_insulin = pd.read_csv("dmthai_Feb2023/insulin_240223_2219.csv")
df_excer = pd.read_csv("dmthai_Feb2023/exercise_type_240223_2219.csv")
df_carb = pd.read_csv("dmthai_Feb2023/carb_book_240223_2221.csv")
df_bolus = pd.read_csv("dmthai_Feb2023/bolus_list_240223_2217.csv")
df_basal = pd.read_csv("dmthai_Feb2023/basal_list_240223_2218.csv")

df_profile_filter = []
#df_profile_filter = df_profile[df_profile['user_id']==4]
#df_profile_filter = df_profile[~df_profile["user_id"].isin([2, 3,4])]
df_profile_filter = df_profile[~df_profile["user_id"].isin([1,2,	3,	4,5,	8,	11,	14,15,17,	18,19,	20,	21,22,23,25,27,28,	30,	32,	33,	34,	35,	36,	41,	43,	44,	45,	46,	49,	51,	105,	112,	113,	118,	120,	131	,180,	204,	214,	244,	251	,332,	342	,355,	356,	357,	358,	359,	360,	361,	362,	363,	365,	366,	368,	369]
 )] 
print("#row_profile:",len(df_profile_filter.index))
#st.write("จำนวนผู้ใช้งานที่ลงทะเบียน:",len(df_profile_filter.index))
#df_profile_filter.head(10)
numb_gender =df_profile_filter["gender"].value_counts()
print('% of count female:',numb_gender[1]/sum(numb_gender))
print('% of count male:',numb_gender[2]/sum(numb_gender))
#st.write("% of count female:",numb_gender[1]/sum(numb_gender))
#st.write("% of count male:",numb_gender[2]/sum(numb_gender))

#Identify given date as date month and year

# #------age----------------------------------------------------
now = pd.to_datetime('now')
df_profile_filter["age"] = (now - df_profile_filter["DOB"]).astype('<m8[Y]') 

df_profile_filter["bins"] = pd.cut(df_profile_filter["age"],bins=[0,15,25,35,50,100], labels=["0-15","15-25","25-35","35-50","50+"])

#df = df_profile_filter.groupby(['age', 'bins']).size().unstack(fill_value=0)
fig1, ax1 = plt.subplots()
ax1 =  df_profile_filter.groupby('bins').size()
ax1.plot.pie(figsize=(4,4),title='age range')


# #------doctor connect----------------------------------------------------
#print("#row_doctorconnect:",len(df_doctorconnect_filter.index)) #row count of pandas#df_doctorconnect_filter.head(21)
df_doctorconnect_filter = df_doctorconnect[~df_doctorconnect["child_user_id"].isin([1,2,3,4,5,8,11,14,15,17,18,19,20,21,22,23,25,27,28,30,32,33,34,35,36,41,43,44,45,46,49,51,105,112,113,118,120,131,180,204,214,244,251,332,342,355,356,357,358,359,360,361,362,363,365,366,368,369])]
print("% of row_doctorconnect:",len(df_doctorconnect_filter.index)/sum(numb_gender))

df_lastesgrowth_filter = df_lastesgrowth[~df_lastesgrowth["user_profile_id"].isin([1,2,	3,	4,5,	8,	11,	14,15,17,	18,19,	20,	21,22,23,25,27,28,	30,	32,	33,	34,	35,	36,	41,	43,	44,	45,	46,	49,	51,	105,	112,	113,	118,	120,	131	,180,	204,	214,	244,	251	,332,	342	,355,	356,	357,	358,	359,	360,	361,	362,	363,	365,	366,	368,	369])]
#df_lastesgrowth_filter.head(10)
df_plan_filter = df_plan[~df_plan["user_id"].isin([1,2,	3,	4,5,	8,	11,	14,15,17,	18,19,	20,	21,22,23,25,27,28,	30,	32,	33,	34,	35,	36,	41,	43,	44,	45,	46,	49,	51,	105,	112,	113,	118,	120,	131	,180,	204,	214,	244,	251	,332,	342	,355,	356,	357,	358,	359,	360,	361,	362,	363,	365,	366,	368,	369])]
#df_plan_filter.head(10)
# cannot link with user_id for df_user
# just name  for df_insulin /carbbook/ exercise/mood
#df_bolus
#df_basal 
df_alert_filter = df_alert[~df_alert["user_id"].isin([1,2,	3,	4,5,	8,	11,	14,15,17,	18,19,	20,	21,22,23,25,27,28,	30,	32,	33,	34,	35,	36,	41,	43,	44,	45,	46,	49,	51,	105,	112,	113,	118,	120,	131	,180,	204,	214,	244,	251	,332,	342	,355,	356,	357,	358,	359,	360,	361,	362,	363,	365,	366,	368,	369])]

# #------log-------------------------------------------------------------
df_log_filter = df_log[~df_log["user_id"].isin([1,2,	3,	4,5,	8,	11,	14,15,17,	18,19,	20,	21,22,23,25,27,28,	30,	32,	33,	34,	35,	36,	41,	43,	44,	45,	46,	49,	51,	105,	112,	113,	118,	120,	131	,180,	204,	214,	244,	251	,332,	342	,355,	356,	357,	358,	359,	360,	361,	362,	363,	365,	366,	368,	369])]
df_log_filter.groupby('user_id').nth(-1)
df_log_filter.groupby("user_id").mean()
print('#glucose:',df_log_filter["glucose_total"].count())
print('#carb:',df_log_filter["carb_total"].count())
print('#bolus:', df_log_filter["insulin_bolus_actual"].count())
print('#basal:',df_log_filter["insulin_basal_actual"].count())
print('#mood:',df_log_filter["mood"].count())
print('#ketone:',df_log_filter["ketone_level"].count())
print('#exercise:',df_log_filter["exercise"].count())
p1 = df_log_filter["glucose_total"].count()
p2 = df_log_filter["carb_total"].count()
p3 = df_log_filter["insulin_bolus_actual"].count()
p4 = df_log_filter["insulin_basal_actual"].count()
p5 = df_log_filter["mood"].count()
p6 = df_log_filter["ketone_level"].count()
p7 =df_log_filter["exercise"].count()
# st.write('#glucose:',df_log_filter["glucose_total"].count())
# st.write('#carb:',df_log_filter["carb_total"].count())
# st.write('#bolus:', df_log_filter["insulin_bolus_actual"].count())
# st.write('#basal:',df_log_filter["insulin_basal_actual"].count())
# st.write('#mood:',df_log_filter["mood"].count())
# st.write('#ketone:',df_log_filter["ketone_level"].count())
# st.write('#exercise:',df_log_filter["exercise"].count())
#df_log_filter.groupby(['user_id']).mean().plot(kind='pie', y='glucose_total')
# #--------log filtered 3 months-----------------------------------------
mask=[]
mask = df_log_filter[(df_log_filter['Date'] > '2022-12-01') & (df_log_filter['Date'] <= '2023-03-02')]
#mask_id = mask.groupby("user_id")["user_id"].count()
print('active users(3 months):',len(pd.unique(mask['user_id'])),',registered users:',len(df_profile_filter.index)) #percentage of active users last 3 months
# st.write('active users(3 months):',len(pd.unique(mask['user_id'])),',registered users:',len(df_profile_filter.index)) #percentage of active users last 3 months

pp1 = mask["glucose_total"].count()
pp2 = mask["carb_total"].count()
pp3 = mask["insulin_bolus_actual"].count()
pp4 = mask["insulin_basal_actual"].count()
pp5 = mask["mood"].count()
pp6 = mask["ketone_level"].count()
pp7 = mask["exercise"].count()
print('#glucose_Active:',pp1)
print('#carb_Active:',pp2)
print('#bolus_Active:',pp3)
print('#basal_Active:',pp4)
print('#mood_Active:',pp5)
print('#ketone_Active:',pp6)
print('#exercise_Active:',pp7)

# st.write('#glucose_Active:',pp1)
# st.write('#carb_Active:',pp2)
# st.write('#bolus_Active:',pp3)
# st.write('#basal_Active:',pp4)
# st.write('#mood_Active:',pp5)
# st.write('#ketone_Active:',pp6)
# st.write('#exercise_Active:',pp7)

#df_log_filter.groupby(['user_id']).mean().hist(column='glucose_total')
#print('#rows of gluc',mask.groupby("user_id")["glucose_total"].max())
max_gluc = mask.groupby("user_id")["glucose_total"].transform(max)
print(max_gluc.index)
# st.write(max_gluc.index)

min_gluc = mask.groupby("user_id")["glucose_total"].transform(min)
# print(min_gluc.index)
# st.write(max_gluc.index)
# st.write(min_gluc.index)

##################################โค้ดจบพี่จิ๊บ แบบภาพรวม########################################################################
############################################################################################################################

# fig2, ax2 = plt.subplots()
# ax2 =  df_profile_filter.groupby('bins').size()
# ax2.plot.pie(figsize=(4,4),title='age range')
active_user = len(pd.unique(mask['user_id']))
num_user = len(df_profile_filter.index)


label_active_user = "Active_user(last 3 months) : "+str(active_user)
label_num_user = "Total users : "+ str(num_user)
labels = label_active_user, label_num_user
sizes = [active_user, num_user]
explode = (0.1, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

fig2, ax2 = plt.subplots()

ax2.pie(sizes, explode=explode, labels=labels, startangle=90)

##########################################################################################################################
    # - #glucose_Active: """+ str(pp1) +"""
    # - #carb_Active: """+ str(pp2) +"""
    # - #bolus_Active: """+ str(pp3) +"""
    # - #basal_Active: """+ str(pp4) +"""
    # - #mood_Active: """+ str(pp5) +"""
    # - #ketone_Active: """+ str(pp6) +"""
    # - #exercise_Active: """+ str(pp7) +"""

    # List:
glucose_total = df_log_filter["glucose_total"].count()
carb_total = df_log_filter["carb_total"].count()
insulin_bolus_actual = df_log_filter["insulin_bolus_actual"].count()
insulin_basal_actual = df_log_filter["insulin_basal_actual"].count()
mood = df_log_filter["mood"].count()
ketone_level = df_log_filter["ketone_level"].count()
exercise = df_log_filter["exercise"].count()

species = ("glucose", "carb","insulin_bolus", "insulin_basal", "mood", "ketone_level", "exercise")
penguin_means = {
    'Active': (pp1, pp2, pp3, pp4, pp5, pp6, pp7),
    'Total': (glucose_total, carb_total, insulin_bolus_actual, insulin_basal_actual, mood, ketone_level, exercise)
}

x = np.arange(len(species))  # the label locations
width = 0.25  # the width of the bars
multiplier = 0

fig3, ax3 = plt.subplots(layout='constrained')

for attribute, measurement in penguin_means.items():
    offset = width * multiplier
    rects = ax3.bar(x + offset, measurement, width, label=attribute)
    ax3.bar_label(rects, padding=3)
    multiplier += 1

# Add some text for labels, title and custom x-axis tick labels, etc.
ax3.set_ylabel('records')
ax3.set_title('Activity')
ax3.set_xticks(x + width, species)
ax3.legend(loc='upper left')
ax3.set_ylim(0, 10000)


##########################################################################################################################
style = """  <style>
            [data-testid=“stSidebar”][aria-expanded=“true”] > div:first-child {
            width: 500px;
            }
            [data-testid=“stSidebar”][aria-expanded=“false”] > div:first-child {
            width: 500px;
            margin-left: -500px;
            }
             </style>

        """
st.markdown(style, unsafe_allow_html=True)

# st.sidebar.markdown("## **ภาพรวม DMTHAIDIARY**")
# st.sidebar.write("จำนวนผู้ใช้งานที่ลงทะเบียน:",str(len(df_profile_filter.index)))
st.sidebar.markdown("""# ภาพรวม DMTHAIDIARY""")

st.sidebar.subheader("จำนวนผู้ใช้งาน")
col1, col2, col3, col4 = st.sidebar.columns(4)
col2.metric("ชาย", str(round((numb_gender[2]/sum(numb_gender)*100)))+"%", "")
col3.metric("หญิง", str(round((numb_gender[1]/sum(numb_gender)*100)))+"%", "")
col4.metric("เชื่อมระบบแพทย์", str(round((len(df_doctorconnect_filter.index)/sum(numb_gender))*100))+"%", "")
col1.metric("ผู้ที่ลงทะเบียน(คน)",  str(len(df_profile_filter.index)), "")

st.sidebar.pyplot(fig2)
st.sidebar.pyplot(fig1)
st.sidebar.pyplot(fig3)

# - จำนวนผู้ใช้งานที่ลงทะเบียน """+ str(len(df_profile_filter.index)) + """
#     - จำนวนผู้ใช้งาน ชาย """+ str(round((numb_gender[2]/sum(numb_gender)*100))) + """% หญิง """+ str(round((numb_gender[1]/sum(numb_gender)*100)))+"""%""" """
#     - จำนวนการใช้งานเชื่อมระบบแพทย์ """+ str(round((len(df_doctorconnect_filter.index)/sum(numb_gender))*100))+"""%""" """
#     - จำนวนผู้ใช้าน Active (3 เดือนล่าสุด) """+str(len(pd.unique(mask['user_id'])))+""":"""+str(len(df_profile_filter.index))+"""

   # Active List: #max_gluc: """+ str(max_gluc.index) +"""
    # Active List: #min_gluc: """+ str(min_gluc.index) +""" 
    # - #glucose_Active: """+ str(pp1) +"""
    # - #carb_Active: """+ str(pp2) +"""
    # - #bolus_Active: """+ str(pp3) +"""
    # - #basal_Active: """+ str(pp4) +"""
    # - #mood_Active: """+ str(pp5) +"""
    # - #ketone_Active: """+ str(pp6) +"""
    # - #exercise_Active: """+ str(pp7) +"""

    # List:
    # - #glucose: """+ str(df_log_filter["glucose_total"].count()) +"""
    # - #carb: """+ str(df_log_filter["carb_total"].count()) +"""
    # - #bolus: """+ str(df_log_filter["insulin_bolus_actual"].count()) +"""
    # - #basal: """+ str(df_log_filter["insulin_basal_actual"].count()) +"""
    # - #mood: """+ str(df_log_filter["mood"].count()) +"""
    # - #ketone: """+ str(df_log_filter["ketone_level"].count()) +"""
    # - #exercise: """+ str(df_log_filter["exercise"].count()) +"""
# st.sidebar.pyplot(a)

# # Using object notation
# st.sidebar.write("จำนวนผู้ใช้งานที่ลงทะเบียน:",str(len(df_profile_filter.index)))
# st.sidebar.write("% of count female:",round((numb_gender[1]/sum(numb_gender)*100)))
# st.sidebar.write("% of count male:",round((numb_gender[2]/sum(numb_gender)*100)))
# st.sidebar.write("% of row_doctorconnect:",round((len(df_doctorconnect_filter.index)/sum(numb_gender))*100))
# st.write('active users(3 months):',len(pd.unique(mask['user_id'])),',registered users:',len(df_profile_filter.index)) #percentage of active users last 3 months

# st.sidebar.write('#glucose:',df_log_filter["glucose_total"].count())
# st.sidebar.write('#carb:',df_log_filter["carb_total"].count())
# st.sidebar.write('#bolus:', df_log_filter["insulin_bolus_actual"].count())
# st.sidebar.write('#basal:',df_log_filter["insulin_basal_actual"].count())
# st.sidebar.write('#mood:',df_log_filter["mood"].count())
# st.sidebar.write('#ketone:',df_log_filter["ketone_level"].count())
# st.sidebar.write('#exercise:',df_log_filter["exercise"].count())
# st.sidebar.write('#glucose_Active:',pp1)
# st.sidebar.write('#carb_Active:',pp2)
# st.sidebar.write('#bolus_Active:',pp3)
# st.sidebar.write('#basal_Active:',pp4)
# st.sidebar.write('#mood_Active:',pp5)
# st.sidebar.write('#ketone_Active:',pp6)
# st.sidebar.write('#exercise_Active:',pp7)




