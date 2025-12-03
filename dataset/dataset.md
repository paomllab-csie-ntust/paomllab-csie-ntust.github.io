# Dataset 資料結構規劃

## 專案架構說明

本專案採用前後端分離的混合架構：
- **前端部署**：GitHub Pages（純靜態 HTML/CSS/JS）
- **後端管理**：本地 Flask Admin（僅在本地運行）
- **資料同步**：透過 JSON 文件進行資料交換

## 工作流程

```
本地 Flask Admin → 編輯資料 → 儲存為 JSON → Push to GitHub → 前端讀取 JSON 渲染頁面
```

---

## 資料結構設計

> **注意**：教授基本資訊、研究領域、教學歷史等不常更動的內容直接寫在 HTML 中，不需要透過 JSON 管理。
>
> 以下僅針對**經常更新**的資料進行 JSON 化管理。

---

### 1. 出版物 (`publications.json`)

```json
{
  "publications": [
    {
      "id": "j13_2025",
      "type": "journal",
      "authors": ["Hanjuan Huang", "Hsing-Kuo Pao"],
      "title": "A unified noise and watermark removal from information bottleneck-based modeling",
      "venue": "Neural Networks",
      "volume": "181",
      "pages": "106853",
      "year": 2025,
      "highlight_author": "Hsing-Kuo Pao"
    },
    {
      "id": "c45_2024",
      "type": "conference",
      "authors": ["John Doe", "Hsing-Kuo Pao"],
      "title": "Deep Learning for Security Applications",
      "venue": "IEEE Conference on Computer Vision",
      "pages": "123-130",
      "year": 2024,
      "highlight_author": "Hsing-Kuo Pao"
    }
  ]
}
```

**欄位說明**：
- `id`: 唯一識別碼（格式：類型縮寫 + 編號 + 年份）
- `type`: 類型（journal/conference/book/dissertation）
- `authors`: 作者列表
- `title`: 標題
- `venue`: 發表場所（期刊名稱或會議名稱）
- `volume`: 卷號（僅 journal）
- `pages`: 頁碼
- `year`: 年份
- `highlight_author`: 需要加粗顯示的作者

---

### 2. 實驗室成員 (`members.json`)

```json
{
  "contact_person": {
    "name": "林品臻",
    "email": "M11415054@mail.ntust.edu.tw",
    "photo": "asset/member/林品臻.jpg"
  },
  "lab_info": {
    "room": "RB304-3",
    "phone": "02-2733-3141 ext. 7298"
  },
  "members": [
    {
      "id": "m001",
      "name": "Ting-Feng Ho",
      "name_zh": "何霆鋒",
      "degree": "MS",
      "year": 2024,
      "photo": "asset/member/Ting-Feng Ho.png",
      "status": "active"
    },
    {
      "id": "m002",
      "name": "莊恩妮",
      "degree": "MS",
      "year": 2024,
      "photo": "asset/member/莊恩妮.jpg",
      "status": "active"
    },
    {
      "id": "m003",
      "name": "鄭孟恒",
      "degree": "MS",
      "year": 2024,
      "photo": "asset/member/pp.png",
      "status": "active"
    }
  ]
}
```

**欄位說明**：
- `id`: 成員唯一識別碼
- `name`: 英文姓名
- `name_zh`: 中文姓名（選填）
- `degree`: 學位（MS/PhD）
- `year`: 入學年份
- `photo`: 照片路徑
- `status`: 狀態（active/alumni/graduated）

---

### 3. 活動資訊 (`events.json`)

```json
{
  "events": [
    {
      "id": "e001",
      "title": "Team Lunch - NTU Eco House",
      "date": "2025-01-17",
      "date_display": "2025 Jan 17",
      "photo": "asset/event/Team Lunch_20250117.png",
      "description": "",
      "category": "team_activity"
    },
    {
      "id": "e002",
      "title": "Hanjuan PhD Oral Defense",
      "date": "2025-01-15",
      "date_display": "2025 Jan 15",
      "photo": "asset/event/hanjuan0115.png",
      "description": "",
      "category": "academic"
    },
    {
      "id": "e003",
      "title": "Team Lunch - Eatogether",
      "date": "2025-01-14",
      "date_display": "2025 Jan 14",
      "photo": "asset/event/Team Lunch_20250114.jpg",
      "description": "",
      "category": "team_activity"
    }
  ]
}
```

**欄位說明**：
- `id`: 活動唯一識別碼
- `title`: 活動標題
- `date`: 日期（ISO 格式，用於排序）
- `date_display`: 顯示用日期格式
- `photo`: 照片路徑
- `description`: 活動描述（選填）
- `category`: 分類（team_activity/academic/conference/workshop）

---

## 資料檔案清單

```
dataset/
├── dataset.md              # 本文件（資料結構說明）
├── publications.json       # 出版物（經常更新）
├── members.json            # 實驗室成員（經常更新）
└── events.json             # 活動資訊（經常更新）
```

**不需要 JSON 管理的內容**（直接寫在 HTML）：
- 教授基本資訊（姓名、學歷、聯絡方式等）
- 研究領域詳細資訊
- 教學歷史

---

## 前端整合方式

### JavaScript 讀取範例

```javascript
// 讀取成員資料
fetch('dataset/members.json')
  .then(response => response.json())
  .then(data => {
    renderMembers(data.members);
  });

// 讀取活動資料
fetch('dataset/events.json')
  .then(response => response.json())
  .then(data => {
    renderEvents(data.events);
  });
```

---

## Flask Admin 功能規劃

### 主要功能模組

1. **Dashboard**：總覽統計（出版物數量、成員數量、活動數量）
2. **Publications Management**：出版物管理（CRUD）
3. **Members Management**：成員管理（CRUD + 照片上傳）
4. **Events Management**：活動管理（CRUD + 照片上傳）
5. **File Upload**：統一的檔案上傳介面
6. **JSON Export**：一鍵匯出所有 JSON 文件
7. **Preview**：預覽前端效果

---

## 注意事項

1. **照片命名規範**：
   - 成員照片：`asset/member/[姓名].jpg`
   - 活動照片：`asset/event/[活動名稱]_[日期].jpg`
   - 使用英文或中文皆可，但避免特殊字元

2. **JSON 編碼**：
   - 使用 UTF-8 編碼
   - 確保中文字元正確顯示

3. **資料驗證**：
   - 必填欄位檢查
   - 日期格式驗證
   - Email 格式驗證
   - 照片檔案存在性檢查

4. **版本控制**：
   - JSON 文件納入 Git 版本控制
   - 照片文件也需要 commit
   - 建議使用有意義的 commit message

5. **備份策略**：
   - 定期備份 dataset 目錄
   - 重要更新前先備份

---

## 下一步

1. ✅ 創建 dataset 目錄
2. ✅ 撰寫資料結構文檔（僅包含常更新的資料）
3. ⬜ 創建初始 JSON 文件（從現有 HTML 提取資料）
   - publications.json
   - members.json
   - events.json
4. ⬜ 建立 Flask Admin 應用
5. ⬜ 實作 CRUD 功能（出版物、成員、活動）
6. ⬜ 實作檔案上傳功能（成員照片、活動照片）
7. ⬜ 修改前端 HTML 以讀取 JSON（僅修改動態部分）
8. ⬜ 測試完整流程

