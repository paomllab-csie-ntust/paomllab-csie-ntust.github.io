# Catalog Navigation 工作原理分析

## 📋 概述

這是一個**側邊導航目錄系統**，用於在教授個人頁面中快速跳轉到不同的區塊（Research、Experience、Publications、Others）。

---

## 🏗️ HTML 結構

### 完整結構
```html
<div class="col-3 col-md-12">
  <div class="row mt-md-3">
    <!-- 圓形圖示按鈕 -->
    <div class="col-12 col-md-auto d-flex justify-content-center pr-md-1 pr-lg-3">
      <a class="list-group-item list-group-item-action rounded-circle catalogIco active" 
         href="#Experience"
         id="ExperienceBtn"></a>
    </div>
    <!-- 文字標籤 -->
    <div class="col-12 col-md centerVertically text-md-start px-0">
      Experience
    </div>
  </div>
</div>
```

### 結構分解

#### 1. **外層容器** `<div class="col-3 col-md-12">`
- **手機版** (`col-3`)：佔 1/4 寬度（4 個按鈕橫排）
- **平板/桌面版** (`col-md-12`)：佔全寬（按鈕垂直排列）

#### 2. **內層 Row** `<div class="row mt-md-3">`
- `mt-md-3`：在中型螢幕以上增加上方間距

#### 3. **圓形按鈕容器** `<div class="col-12 col-md-auto d-flex justify-content-center pr-md-1 pr-lg-3">`
- `col-12`：手機版佔全寬（圖示在上）
- `col-md-auto`：平板/桌面版自動寬度
- `d-flex justify-content-center`：內容水平置中
- `pr-md-1 pr-lg-3`：右側 padding（平板 1，桌面 3）

#### 4. **圓形按鈕** `<a class="list-group-item list-group-item-action rounded-circle catalogIco active">`
- `list-group-item`：Bootstrap 列表項目樣式
- `list-group-item-action`：可點擊的互動效果（hover 變色）
- `rounded-circle`：圓形外觀
- `catalogIco`：自訂樣式（設定寬高 50px）
- `active`：當前啟用狀態（藍色背景）
- `href="#Experience"`：錨點連結，點擊跳轉到 `id="Experience"` 的區塊
- `id="ExperienceBtn"`：唯一識別碼（可用於 JavaScript 控制）

#### 5. **文字標籤容器** `<div class="col-12 col-md centerVertically text-md-start px-0">`
- `col-12`：手機版佔全寬（文字在下）
- `col-md`：平板/桌面版自動寬度
- `centerVertically`：自訂樣式，垂直置中
- `text-md-start`：平板/桌面版文字靠左
- `px-0`：左右 padding 為 0

---

## 🎨 CSS 樣式

### 1. **catalogIco** (style.css)
```css
.catalogIco {
    width: 50px;
    height: 50px;
}
```
- 設定圓形按鈕的固定尺寸

### 2. **catalog-out** (sticky 容器)
```css
#catalog-out {
  top: 50px;  /* 手機版：距離頂部 50px */
}

@media (min-width: 768px) {
  #catalog-out {
    top: 0px;  /* 平板/桌面版：距離頂部 0px */
  }
}
```

### 3. **catalog** (sticky 內容)
```css
@media (min-width: 768px) {
  #catalog {
    top: 100px;  /* 平板/桌面版：距離頂部 100px */
  }
}
```

### 4. **centerVertically** (垂直置中)
```css
.centerVertically {
  display: flex;
  flex-direction: column;
  justify-content: center;
}
```

---

## 🔄 工作原理

### 1. **錨點跳轉**
- 點擊按鈕 → 瀏覽器跳轉到對應的 `#Experience` 錨點
- 頁面中必須有 `<div id="Experience">` 或類似的元素

### 2. **Sticky 定位**
- `sticky-top` class 讓導航目錄在滾動時固定在頂部
- 手機版：固定在距離頂部 50px 的位置
- 桌面版：固定在距離頂部 100px 的位置

### 3. **Active 狀態**
- `active` class 讓當前按鈕顯示藍色背景
- 需要 JavaScript 動態切換（目前 HTML 中是靜態設定）

### 4. **響應式佈局**

#### 手機版 (< 768px)
```
┌─────────────────────────┐
│ [●] [●] [●] [●]        │  ← 4 個圓形按鈕橫排
│  R   E   P   O          │  ← 文字在按鈕下方
└─────────────────────────┘
```

#### 平板/桌面版 (≥ 768px)
```
┌──────────────┐
│ [●] Research │
│              │
│ [●] Experience │
│              │
│ [●] Publications │
│              │
│ [●] Others   │
└──────────────┘
```

---

## 📝 完整的 4 個按鈕

1. **Research Area** - `#ResearchBtn` → `#Research`
2. **Experience** - `#ExperienceBtn` → `#Experience` (預設 active)
3. **Publications** - `#PublicationsBtn` → `#Publications`
4. **Others** - `#OthersBtn` → `#Others`

---

## 🎯 關鍵特性

✅ **響應式設計**：手機橫排，桌面直排  
✅ **Sticky 定位**：滾動時固定在頂部  
✅ **錨點導航**：快速跳轉到頁面區塊  
✅ **視覺回饋**：active 狀態顯示當前位置  
✅ **Bootstrap 整合**：使用 list-group 樣式  

---

## 💡 改進建議

如果需要動態切換 active 狀態，可以加入 JavaScript：

```javascript
// 監聽滾動事件，自動切換 active 狀態
$(window).on('scroll', function() {
  var scrollPos = $(document).scrollTop();
  
  $('.catalogIco').each(function() {
    var currLink = $(this);
    var refElement = $(currLink.attr("href"));
    
    if (refElement.position().top <= scrollPos && 
        refElement.position().top + refElement.height() > scrollPos) {
      $('.catalogIco').removeClass("active");
      currLink.addClass("active");
    }
  });
});
```

