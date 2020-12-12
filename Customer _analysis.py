import pandas as pd
from datetime import datetime
import numpy as np

pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)

data = pd.read_excel(r"C:\Users\cj\Desktop\RFM\RFM实战数据.xlsx")

# 计算RFM值
grouped = data.groupby("买家昵称",as_index=False).agg({"实付金额": np.sum, "购买数量": np.sum,'付款日期':np.max}) 
grouped = grouped.rename(columns={"实付金额": "M消费总额", "购买数量": "F消费频率","付款日期": "最近消费日期"})
grouped['R消费间距'] = (datetime.today() - grouped['最近消费日期']).dt.days
del grouped['最近消费日期']

# 对RFM评分
grouped['M得分'] = pd.cut(grouped['M消费总额'],bins=[0,100,200,300,400,800],labels=[1,2,3,4,5])
grouped['F得分'] = pd.cut(grouped['F消费频率'],bins=[0,3,5,7,9,15],labels=[1,2,3,4,5])
grouped['R得分'] = pd.cut(grouped['R消费间距'],bins=[0,60,120,180,270,365],labels=[5,4,3,2,1])
grouped['RFM总分'] = grouped.loc[:,['M得分','F得分','R得分']].apply(lambda x: x.sum(), axis=1)

# 对RFM定性
grouped['M得分'] = pd.to_numeric(grouped['M得分'], errors='coerce',downcast='integer').fillna(0) # 
grouped['F得分'] = pd.to_numeric(grouped['F得分'], errors='coerce',downcast='integer').fillna(0)
grouped['R得分'] = pd.to_numeric(grouped['R得分'], errors='coerce',downcast='integer').fillna(0)
M_mean = grouped['M得分'].mean()
F_mean = grouped['F得分'].mean()
R_mean = grouped['R得分'].mean()
grouped['M类型'] = grouped['M得分'].apply(lambda x: str(x).replace(str(x),"高") if x>M_mean else "低")
grouped['F类型'] = grouped['F得分'].apply(lambda x: str(x).replace(str(x),"高") if x>F_mean else "低")
grouped['R类型'] = grouped['R得分'].apply(lambda x: str(x).replace(str(x),"高") if x>R_mean else "低")
grouped['客户分类'] = (grouped['M类型'].str.cat(grouped['F类型'])).str.cat(grouped['R类型'])
for index,row in grouped.iterrows():
    if row['客户分类'] == '高高高':
        grouped.loc[index,'客户分类'] = '高价值客户'
    elif row['客户分类'] == '低高高':
       grouped.loc[index,'客户分类'] = '重点保持客户'
    elif row['客户分类'] == '高低高':
        grouped.loc[index,'客户分类'] = '重点发展客户'
    elif row['客户分类'] == '低低高':
        grouped.loc[index,'客户分类'] = '重点挽留客户'
    elif row['客户分类'] == '高高低':
        grouped.loc[index,'客户分类'] = '一般价值客户'
    elif row['客户分类'] == '低高低':
        grouped.loc[index,'客户分类'] = '一般保持客户'
    elif row['客户分类'] == '高低低':
        grouped.loc[index,'客户分类'] = '一般发展客户'
    else:
        grouped.loc[index,'客户分类'] = '潜在客户'

print(grouped)

