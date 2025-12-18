# 網站安裝說明

由github下載之後,使用`npm install`安裝相關套件
此專案由Open Source的OpenWebUI拉下來做調整
包含Python的後端與Svelte的前端
前後端分開啟動方式請參考如下URL:
https://docs.openwebui.com/getting-started/advanced-topics/development


## 開發時的設定

### Stop 1:
Ollama的安裝
```
docker run -d \
  --name ollama \
  --gpus all \
  -p 11434:11434 \
  -v ollama:/root/.ollama \
  ollama/ollama
```

### Step 2:
啟動後端:
進入backend Folder
```
cd backend
```

設定開發時用的URL,允許後端可以傳送資料的URL在此行
再將此行附加到dev.sh檔案內
```
export CORS_ALLOW_ORIGIN="http://localhost:5173;http://localhost:8080;http://10.204.16.67:5173"
```

另一個地方可以設定在./backend/open_webui/config.py,調整其中的CORS_ALLOW_ORIGIN內容
```
CORS_ALLOW_ORIGIN = os.environ.get("CORS_ALLOW_ORIGIN", "http://localhost:5173;http://127.0.0.1:5173;http://10.204.16.67:5173").split(";")
```

安裝後端服務伺服器
```
sudo pip install uvicorn
```

安裝python3.11並確認使用3.11
```
sudo apt install python3.11 python3.11-venv
python3.11 -m venv venv
source venv/bin/activate
python --version
```

安裝相關套件
```
pip install -r requirements.txt -U
```


啟動後端服務
```
sh dev.sh
```
之後開啟Browser輸入網址,會有後端的SwggerAPI文件網頁
http://localhost:8080/docs

### Step 3:
啟動前端:
node版本要大於22.10.0
於專案根目錄下安裝套件
```
npm install
```

開啟vite.config.ts,加入如下設定
```
server: {
    watch: {
        ignored: [
            '**/venv/**',
            '**/backend/venv/**',
            '**/.venv/**'
        ]
    }
}
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



## 完成版本目標後的注意事項

### Step 1:
配合CI/CD,新進版號需要修改CHANGELOG.md
版本與日期格式要如之前格式
```
## [0.4.13] - 2025-12-15

### Added 

- **RAG flow UI**
```
package.json版本也可配合新版做調整
```
{
    "name": "open-webui",
	"version": "0.4.13",
    ...
}
```
git remote branch要新增branch
例如`dev_frontend_0.4.13`
push後再發PR merge到dev版本內

### Step 2:
執行run.sh整合前後端產生docker image

### Step 3:
因為這是前後端整合的專案
特別要注意github push時要先建立一個新的branch
例如dev_frontend_0.4.12再推上去
之後再整併到dev版本

### Note:
如果要清除之前的所有設定可以刪除db檔案
```
/backend/data/webui.db
```
連接local的ollama服務時,如果用docker
localhost 要改為 host.docker.internal

