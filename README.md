# 網站安裝說明

由github下載之後,使用`npm install`安裝相關套件
此專案由Open Source的OpenWebUI拉下來做調整
包含Python的後端與Svelte的前端
前後端分開啟動方式請參考如下URL:
https://docs.openwebui.com/getting-started/advanced-topics/development


## 開發時的後端連線設定

### Step 1:
啟動後端:
進入backend Folder
```
cd backend
```

安裝相關套件
```
pip install -r requirements.txt -U
```

設定開發時用的URL,允許後端可以傳送資料的URL在此行
再將此行附加到dev.sh檔案內
```
export CORS_ALLOW_ORIGIN="http://localhost:5173;http://localhost:8080;http://10.204.16.57:5173"
```

另一個地方可以設定在./backend/open_webui/config.py,調整其中的CORS_ALLOW_ORIGIN內容
```
CORS_ALLOW_ORIGIN = os.environ.get("CORS_ALLOW_ORIGIN", "http://localhost:5173;http://127.0.0.1:5173").split(";")
```


啟動後端服務
```
sh dev.sh
```
之後開啟Browser輸入網址,會有後端的SwggerAPI文件網頁
http://localhost:8080/docs

### Step 2:
啟動前端:
於專案根目錄下安裝套件
```
npm install
```
執行啟動command
```
npm run dev
```
開啟Browser網址輸入
```
http://localhost:5173
```
即可開始編輯專案



## 佈署時的後端連線設定
### Step 1:
執行run.sh整合前後端產生docker image

### Step 2:
因為這是前後端整合的專案
特別要注意github push時要先建立一個新的branch
例如dev_frontend_0.4.12再推上去
之後再整併到dev版本


