#!/usr/bin/env python
# coding: utf-8

# In[12]:


import requests
from pyquery import PyQuery as pq


# In[18]:


#輸入代碼查天氣 輸入錯誤的可以重新輸入
for i in range(1):
    place = input("請輸入代碼: 臺北市:0 、 新北市:1 、 桃園市:2 、 臺中市:3 、 臺南市:4 、 高雄市:5 ")
    if place>="6":
        while True:
            print("輸入錯誤，請重新輸入")  
            place = input("請輸入代碼: 臺北市:0 、 新北市:1 、 桃園市:2 、 臺中市:3 、 臺南市:4 、 高雄市:5 ")
            if place<="5":
                break
    if place == "0":
        place1 = "taipei-city/05007a30"
        place2 = "臺北市"
    if place == "1":
        place1 = "new-taipei-city/a9b31e48"
        place2 = "新北市"
    if place == "2":
        place1 = "taoyuan-city/bb3d980d"
        place2 = "桃園市"
    if place == "3":
        place1 = "taichung-city/b020373f"
        place2 = "臺中市"
    if place == "4":
        place1 = "tainan-city/b3acb34b"
        place2 = "臺南市"
    if place == "5":
        place1= "kaohsiung-city/d68d7466"
        place2 = "高雄市"
    else:
        pass
if int(place)<=5:
    print("以下是"+"\""+place2+"\""+"今日氣象及未來十日氣象預報:")
else:
    pass

# 取得欲查詢地區的網址
res = requests.get("https://air-quality.com/place/taiwan/"+place1+"?lang=en&standard=aqi_us")
doc = pq(res.text)
#今日最高溫 用在下面當日各種氣象資料的程式碼中
todayMaxTemp = doc("div.daily-forecast-scroll>div>div:nth-child(1)>.temp_c > span:nth-child(1)").text()
#今日最低溫
todayMinTemp = doc("div.daily-forecast-scroll>div>div:nth-child(1)>.temp_c > span:nth-child(3)").text()
#最低溫的值
todayMinTempValue = int(todayMinTemp.replace("°",""))
#最高溫的值
todayMaxTempValue = int(todayMaxTemp.replace("°",""))

#當日天氣 todayweather1用在下面當日各種氣象資料的程式碼中
todayweather=doc("body > div.container > div.detail-main > div.forecast-box > div.main-block-content >                     div.daily-forecast-scroll > div > div:nth-child(1) > div.icon").attr.style
if todayweather[48:-12] == 'rain':
    todayweather1="雨天"
elif todayweather[48:-12] == 'chancerain':
    todayweather1="短暫雨"
elif todayweather[48:-12] == 'cloudy':
    todayweather1="陰天"
elif todayweather[48:-12] == 'mostlycloudy':
    todayweather1="多雲時晴"
elif todayweather[48:-12] == 'partlycloudy':
    todayweather1="晴時多雲"
elif todayweather[48:-12] == 'clear':
    todayweather1="晴天"
else:
    todayweather1="陰天"
# todayweather1

#當日AQI todayAQI2用在下面當日各種氣象資料的程式碼中 AQI可能兩個以上 求平均
todayAQI1 = 0
todayAQI = doc("body > div.container > div.detail-main > div.site-box > div.main-block-content > a > div.value-wrap").text()
todayAQI1 = todayAQI.split(" ")
num = todayAQI1.count("AQI")
sum=0
for i in range(num):
    if "AQI" in todayAQI1:
        todayAQI1.remove("AQI")
    else:
        pass
    sum=sum+int(todayAQI1[i])
    todayAQI2=int(sum/num)
# todayAQI2

#當日所有天氣資料 跟建議
todayDataList = []
doc.make_links_absolute(base_url=res.url)
itemDict1={}
itemDict1["氣溫"] = doc(".weather-item .temperature").text()
itemDict1["天氣"] = todayweather1
itemDict1["濕度"] = doc(".weather-item .humidity").text()
itemDict1["UV指數"] = doc(".weather-item .uv").text()
itemDict1["AQI指數"] = todayAQI2
itemDict1["PM2.5指數"] = doc("body > div.container > div.detail-main > div.reading-box > div.pollutants > div:nth-child(2) >                                 div.value").text()+'μg/m³'
#空品建議
if int(todayAQI2)<=50:
    todaySuggest = "空氣品質良好，適合進行戶外運動"
elif int(todayAQI2)<=100:
    todaySuggest = "空氣品質可接受，適合外出走走"
elif int(todayAQI2)<=150:
    todaySuggest = "空氣品質不佳，若出門請戴口罩"
elif int(todayAQI2)<=200:
    todaySuggest = "空氣品質堪慮，避免長時間待在室外"
elif int(todayAQI2)<=300:
    todaySuggest = "空氣品質很糟，避免出門且關閉門窗"
else:
    todaySuggest = "霧霾來襲，請戴上防毒面具"
#溫度建議

if todayMinTempValue <=10:     # 如果最低溫小於10度 提醒
    todaySuggest1 = "寒流來襲，低溫只有"+todayMinTemp[0:2]+"度，請做好保暖措施"
elif todayMinTempValue <=20:     # 如果最低溫小於20度 提醒
    todaySuggest1 = "氣溫寒冷，低溫只有"+todayMinTemp[0:2]+"度，請多添加衣物"
elif todayMinTempValue <=30:     # 如果最低溫小於20度 提醒
    todaySuggest1 = "氣溫涼爽，低溫有"+todayMinTemp[0:2]+"度，請帶件薄外套"
elif todayMaxTempValue <=35:     # 如果最高溫大於35度 提醒
    todaySuggest1 = "氣溫炎熱，低溫高達"+todayMaxTemp[0:2]+"度，注意室內外溫差"
else:
    todaySuggest1 ="熱浪來襲，低溫竟高達"+todayMaxTemp[0:2]+"度，多補充水分避免中暑"
# 天氣建議
if todayweather1 == "雨天":
    todaySuggest2 = "出門請攜帶雨具，行車請保持安全距離"
elif todayweather1 == "短暫雨":
    todaySuggest2 = "帶把傘以防萬一"
elif todayweather1 == "晴天":
    todaySuggest2 = "請做好防曬措施"
elif todayweather1 == "多雲時晴":
    todaySuggest2 = "天氣穩定，沒甚麼需要特別注意的"
elif todayweather1 == "晴時多雲":
    todaySuggest2 = "天氣穩定，沒甚麼需要特別注意的"
elif todaySuggest1 == "陰天":
    todaySuggest2 = "天氣穩定，沒甚麼需要特別注意的"
else:
    todaySuggest2 = "天氣穩定，沒甚麼需要特別注意的"
itemDict1["天氣小提醒:"] = "\n"+todaySuggest +";"+"\n"+todaySuggest1+";"+"\n"+todaySuggest2
todayDataList.append(itemDict1)

#直接印出今日天氣概況
print("今日天氣概況:")
for k,v in todayDataList[0].items():
    print(k,v)
    
# 取得未來十日的日期、溫度、氣象資料
weekDataList = []
for eachitem in doc(".daily-forecast>.forecast-item").items():
    itemDict={}
    itemDict["日期"] = eachitem(".date").text()
    itemDict["溫度"] = eachitem(".temp_c").text()  
    weekweather = eachitem(".icon").attr("style")  #取得style的資料
    # 把icon style中的英文天氣轉變為中文
    if weekweather == "background-image:url(css/images/weather/weather_rain_light.png);": 
        weekweather1 = "雨天"
    elif weekweather == "background-image:url(css/images/weather/weather_chancerain_light.png);":
        weekweather1 = "短暫雨"
    elif weekweather == "background-image:url(css/images/weather/weather_cloudy_light.png);":
        weekweather1 = "陰天"
    elif weekweather == "background-image:url(css/images/weather/weather_mostlycloudy_light.png);":
        weekweather1 = "多雲時晴"
    elif weekweather == "background-image:url(css/images/weather/weather_partlycloudy_light.png);":
        weekweather1 = "晴時多雲"
    elif weekweather == "background-image:url(css/images/weather/weather_clear_light.png);":   
        weekweather1 = "晴天"
    else:
        weekweather1 = "陰天"
    itemDict["天氣"] = weekweather1
    weekDataList.append(itemDict)

print("\n"+"未來十日氣象預報:")
# print(weekDataList)

#印出十日資料
for n in range(len(weekDataList)):
    # print(str(n+1))
    print()
    for k,v in weekDataList[n].items():
        print("{}:{}".format(k,v), end=" ")


# In[ ]:


# this is the latest version updated on 20190509
### note: todayMinTemp[0:2] changed to todayMinTemp.replace("°","") => prevent error when temp. value has only 1 digit
### note: todaysuggest2 added an else statement to prevent undefined


# In[ ]:


# 存圖片用的
# image_url = "https://air-quality.com/css/images/weather/weather_rain_light.png"
# r = requests.get(image_url)
# with open("icon.png",'wb') as f:
#     f.write(r.content)   


# In[ ]:


# # 抓各縣市分頁網址 因為各縣市網址除了城市名稱外還有一段8個英數組成的固定代碼
# doc.make_links_absolute(base_url=res.url) 
# for eachitem in doc("body > div.container > div.detail-main > div.site-box > div.main-block-content > a").items():
#     print(eachitem.attr("href"))
#     cityRes = requests.get(eachitem.attr("href"))
#     cityDoc = pq(cityRes.text)


# In[ ]:




