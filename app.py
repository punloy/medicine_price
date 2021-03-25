from flask import Flask, render_template,url_for,request
import pandas as pd
from IPython.display import HTML
import csv

searchValue = 0
app = Flask(__name__)

def keyDF(searchValue):
    print('-1')        
    korfullDF = pd.read_csv('./static/info/korFull.csv')
    jpnfullDF = pd.read_csv('./static/info/jpnFull.csv')
    print('0')
    jpnfullDF['英文名(處理)']=jpnfullDF['英文名(處理)'].astype(str)
    print('a')
    jpnfullDF = jpnfullDF.drop(columns = ['\ufeff\ufeff\ufeffNo',':Unnamed: 4', 'Unnamed: 5','Unnamed 6', '產品名稱', '需按醫療費用等計算的仿製藥', '原藥', '具有相同劑型/標準的仿製藥的原始藥物','使用期限', '備註', '查詢結果數', '英文名', '成分名1','成分名1(處理)', '成分名2', '成分名2(處理)', '成分名2(再處理)', '成分名3','成分名3(處理)', '成分名3(再處理)'])
    jpnfullDF = jpnfullDF.rename(columns= {"英文名(處理)":"英文名","成分名1(再處理)":"成分英文名"})
    print('b')
    #jpnfullDF.drop_duplicates('產品名稱', keep='first', inplace=True)       #刪除重複項
    print('c')
    korfullDF = korfullDF.drop(columns = ['No','管理途徑', '專業人員/一般人員','出口預防分類', '主要成分代碼', '不可隨機準備', '使用獎勵', '上限', '藥品分類', '薪水', '單價開始日期','單價結束日期', '關鍵字', '查詢結果數', '分析類型', '分析名'])
    print('d')
    #korfullDF.drop_duplicates('\ufeff產品名稱', keep='first', inplace=True) #刪除重複項
    print('1')
    #entry = ''
    # entry = 'Sitaliptin'
    # entry = 'Bromovalerylurea'
    #entry = 'Diflucan Dry Syrup'
    #entry = input()
    entry = str(searchValue)
    tmpjpn = pd.DataFrame()
    tmpkor = pd.DataFrame()
    for i in range(len(jpnfullDF)):
        if entry.lower() in jpnfullDF['英文名'][i].lower():
            #print(jpnfullDF.iloc[i])
            tmpjpn = tmpjpn.append(jpnfullDF.iloc[i])
                
    for i in range(len(korfullDF)):
        if str(entry).lower() in korfullDF['英文名'][i].lower():
            #print(korfullDF.iloc[i])
            tmpkor=tmpkor.append(korfullDF.iloc[i])
    print('2')


    tmpkor = pd.DataFrame(tmpkor,columns=['藥品代碼','產品名稱','英文名','分類號','規格','單位','製造商'])
    tmpkor=tmpkor.reset_index(drop=True)
    #tmpkor.to_csv('result_kr.csv')
    tmpjpn = pd.DataFrame(tmpjpn,columns=['藥品代碼','\ufeff產品名稱','英文名','類別','規格','藥價','製造商', '成分名稱','成分英文名'])        
    tmpjpn=tmpjpn.reset_index(drop=True)
    #tmpjpn.to_csv('result_jp.csv')
    try:
        tmpkor = tmpkor.drop(columns = ['Unnamed: 0'])
        tmpkor.to_csv('result_kr.csv')
        print('tmpkor OK 1')
    except:
        try:
            tmpkor.to_csv('result_kr.csv')
            print('tmpkor OK 2')
        except:
            pass
    try:
        tmpjpn = easyDF.drop(columns = ['Unnamed: 0'])
        easyDF.to_csv('result_jp.csv')
        print('easyDF OK 1')
    except:
        try:
            tmpjpn.to_csv('result_jp.csv')
            print('easyDF OK 2')
        except:
            pass
    print('3')
    fullDF = pd.DataFrame(columns=['韓國產品名稱','日本產品名稱','英文名'])

    if len(tmpkor) != 0:
        fullDF['韓國產品名稱'] = tmpkor['產品名稱'].unique()
    elif len(tmpkor) == 0:
        fullDF['日本產品名稱'] = tmpjpn['\ufeff產品名稱'].unique()
    else:
        fullDF = pd.DataFrame(columns=['韓國產品名稱','日本產品名稱','英文名'])
    fullDF=fullDF.reset_index(drop=True)
    print('4')
    for i in range(len(fullDF)):
        if len(tmpkor) == 0:
            # fullDF['日本產品名稱'][i] = tmpjpn['\ufeff產品名稱'].values[i]
            fullDF['英文名'][i] = tmpjpn['英文名'].values[i]
        elif len(tmpjpn) == 0:
            # fullDF['日本產品名稱'][i] = tmpjpn['\ufeff產品名稱'].values[i]
            fullDF['英文名'][i] = tmpkor['英文名'].values[i]
        elif len(tmpkor) != 0 and len(tmpjpn) != 0:
            fullDF['日本產品名稱'][i] = tmpjpn['\ufeff產品名稱'].values[i]
            fullDF['英文名'][i] = tmpkor['英文名'].values[i]
    print('5')
    try:
        fullDF = fullDF.drop(columns = ['Unnamed: 0'])
        fullDF.to_csv('result_dn.csv')  
        print('fullDF OK 1')
    except:
        try:
            fullDF.to_csv('result_dn.csv')
            print('fullDF OK 2')
        except:
            print(fullDF)
            pass                
    print('6')      
    return searchValue


@app.route('/')
def index():
    return render_template('index.html',howtouse='How to use',htu1='Insert the English  ')

@app.route('/search',methods= ("GET","POST"))
def search():
    return render_template("search.html")

@app.route('/result',methods = ("POST","GET"))
def searchPOST():
    global searchValue
    searchValue = ''
    try:
        searchValue = request.form["search_key"]
        print(searchValue)
        if searchValue != '':
            #searchValue = krDF(searchValue)
            searchValue = keyDF(searchValue)
            return  render_template('search.html',search_key= 'About: '+searchValue,search_result = 'Press the button to see info')
        else:
            return render_template("search.html",search_result = 'Please input keywords!')
    except:
        return render_template("search.html",search_result = 'No releative name')

@app.route('/result_dn',methods= ("POST","GET"))
def result_dn():    
    with open('result_dn.csv',newline='',encoding='utf-8') as infofile:
        info = csv.reader(infofile)
        infoCsv = []
        for idx,row in enumerate(info):
            infoCsv.append(row)
        print(len(infoCsv))
        print(len(infoCsv[0]))
        print(infoCsv[0])
    return render_template('result.html',num= len(infoCsv[0]),len = len(infoCsv), infoCsv = infoCsv)

@app.route('/result_kr',methods= ("POST","GET"))
def result_kr():    
    with open('result_kr.csv',newline='',encoding='utf-8') as infofile:
        info = csv.reader(infofile)
        infoCsv = []
        for idx,row in enumerate(info):
            infoCsv.append(row)
    return render_template('result.html',num= len(infoCsv[0]),len = len(infoCsv), infoCsv = infoCsv)

@app.route('/result_jp',methods= ("POST","GET"))
def result_jp():    
    with open('result_jp.csv',newline='',encoding='utf-8') as infofile:
        info = csv.reader(infofile)
        infoCsv = []
        for idx,row in enumerate(info):
            infoCsv.append(row)
    return render_template('result.html',num= len(infoCsv[0]),len = len(infoCsv), infoCsv = infoCsv)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port='6138',debug = True)