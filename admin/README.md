# Laboratory Website Admin Panel

這是一個基於 Flask 的本地管理系統，用於管理實驗室網站的資料（Publications、Members、Events）。

## 功能特色

- ✅ **Publications 管理**：新增、編輯、刪除研究出版物（Journal、Conference、Book、Dissertation）
- ✅ **Members 管理**：管理實驗室成員資訊、照片、畢業狀態
- ✅ **Events 管理**：管理實驗室活動、上傳活動照片
- ✅ **檔案上傳**：支援照片上傳（成員照片、活動照片）
- ✅ **即時預覽**：可直接查看前端網站效果
- ✅ **JSON 匯出**：所有資料自動儲存為 JSON 格式

## 安裝與啟動

### 1. 安裝依賴

```bash
cd /mnt/e/project/newPao
pip3 install -r admin/requirements.txt
```

### 2. 啟動 Admin 應用

```bash
python3 admin/app.py
```

應用會在 `http://localhost:5000` 啟動。

### 3. 啟動前端網站（用於預覽）

在另一個終端機中：

```bash
cd /mnt/e/project/newPao
python3 -m http.server 3000
```

前端網站會在 `http://localhost:3000` 啟動。

## 使用方式

### Dashboard（首頁）

- 顯示資料統計（Publications、Members、Events 數量）
- 提供快速導航到各個管理頁面
- 顯示 Git 操作指令

### Publications 管理

**Tab 分頁功能**：
- **全部**：顯示所有類型的出版物（僅供查看，不支援拖曳）
- **Journal**：只顯示 Journal 類型，包含 Volume、Pages 欄位
- **Conference**：只顯示 Conference 類型，包含 Location 欄位
- **Book**：只顯示 Book 類型，包含 Publisher 欄位

**新增出版物**：
1. 點擊「新增 Publication」按鈕
2. 選擇類型（Journal、Conference、Book、Dissertation）
3. 填寫必要欄位：
   - 作者（用 `, ` 或 ` and ` 分隔）
   - 標題
   - Venue
   - 年份
   - 高亮作者（預設為 H.-K. Pao）
4. 根據類型填寫額外欄位：
   - **Journal**：Volume、Pages
   - **Conference**：Location、Date
   - **Book**：Editors、Publisher
5. 點擊「儲存」

**拖曳排序功能**：
- Journal、Conference、Book Tab 支援拖曳排序
- 點擊並按住最左側的 ⋮⋮ 圖示
- 拖曳到想要的位置
- 放開滑鼠後會自動儲存並重新載入頁面
- 重新載入後會自動回到拖曳前的 Tab
- ⚠️ 「全部」Tab 不支援拖曳，避免不同類型交錯

### Members 管理

1. 點擊「新增 Member」按鈕
2. 填寫必要欄位：
   - 英文姓名（必填）
   - 中文姓名（選填）
   - 學位（MS/PhD）
   - 年份
   - 狀態（在學中/已畢業）
3. 上傳照片（選填，預設使用 `pp.png`）
4. 點擊「儲存」

**篩選功能**：
- 可按年份篩選
- 可按狀態篩選（在學中/已畢業）

### Events 管理

1. 點擊「新增 Event」按鈕
2. 填寫必要欄位：
   - 標題
   - 日期（YYYY-MM-DD 格式）
   - 顯示日期（例如：2024/01/15）
   - 描述（選填）
   - 分類（選填）
3. 上傳活動照片（必填）
4. 點擊「儲存」

## 資料結構

所有資料儲存在 `/dataset` 目錄下：

- `publications.json` - 出版物資料
- `members.json` - 成員資料
- `events.json` - 活動資料

## 照片管理

照片儲存在 `/asset` 目錄下：

- `/asset/member/` - 成員照片
- `/asset/event/` - 活動照片
- `/asset/general/` - 其他照片

支援格式：JPG, PNG, GIF（最大 16MB）

## 部署到 GitHub Pages

完成資料更新後，使用以下指令將變更推送到 GitHub：

```bash
cd /mnt/e/project/newPao
git add dataset/*.json asset/
git commit -m "Update data: [描述你的更新]"
git push origin main
```

GitHub Pages 會自動更新網站內容。

## 注意事項

⚠️ **安全性**：此管理系統僅供本地使用，請勿部署到公開網路。

⚠️ **備份**：建議定期備份 `dataset/` 目錄下的 JSON 文件。

⚠️ **照片命名**：建議使用有意義的檔名（例如：成員姓名、活動日期）。

## 技術架構

- **後端**：Flask 3.0.0
- **前端**：Bootstrap 5.3.3 + jQuery 3.6.4
- **資料格式**：JSON
- **檔案上傳**：Werkzeug secure_filename

## 疑難排解

### 問題：無法啟動 Flask 應用

**解決方案**：
```bash
pip3 install --upgrade Flask Werkzeug
```

### 問題：照片上傳失敗

**解決方案**：
- 檢查檔案大小是否超過 16MB
- 檢查檔案格式是否為 JPG、PNG 或 GIF
- 確認 `/asset/member/` 和 `/asset/event/` 目錄存在且有寫入權限

### 問題：JSON 儲存失敗

**解決方案**：
- 檢查 `/dataset/` 目錄是否有寫入權限
- 確認 JSON 文件格式正確（可使用 `python3 -m json.tool dataset/publications.json` 驗證）

## 聯絡資訊

如有問題，請聯絡實驗室管理員。

