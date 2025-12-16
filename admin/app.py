#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flask Admin Application for Managing Laboratory Website Data
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, send_from_directory
import json
import os
from datetime import datetime
from werkzeug.utils import secure_filename
import requests
from bs4 import BeautifulSoup
import re

# 配置
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(BASE_DIR, 'dataset')
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'asset')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# 創建 Flask 應用，設定靜態文件路徑指向上層目錄
app = Flask(__name__,
            static_folder=BASE_DIR,
            static_url_path='/static')
app.secret_key = 'your-secret-key-change-this-in-production'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# ==================== Helper Functions ====================

def load_json(filename):
    """載入 JSON 文件"""
    filepath = os.path.join(DATASET_DIR, filename)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        return None

def save_json(filename, data):
    """儲存 JSON 文件"""
    filepath = os.path.join(DATASET_DIR, filename)
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Error saving {filename}: {e}")
        return False

def allowed_file(filename):
    """檢查文件類型是否允許"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ==================== Routes ====================

@app.route('/asset/<path:subpath>')
def serve_asset(subpath):
    """提供靜態資源文件"""
    asset_dir = os.path.join(BASE_DIR, 'asset')
    return send_from_directory(asset_dir, subpath)

@app.route('/')
def index():
    """Dashboard 首頁"""
    publications = load_json('publications.json')
    members = load_json('members.json')
    events = load_json('events.json')

    stats = {
        'publications': len(publications.get('publications', [])) if publications else 0,
        'members': len(members.get('members', [])) if members else 0,
        'events': len(events.get('events', [])) if events else 0,
        'graduated': sum(1 for m in members.get('members', []) if m.get('status') == 'graduated') if members else 0,
    }

    return render_template('dashboard.html', stats=stats)

# ==================== Publications ====================

@app.route('/publications')
def publications():
    """出版物管理頁面"""
    data = load_json('publications.json')
    return render_template('publications.html', publications=data.get('publications', []) if data else [])

@app.route('/api/publications', methods=['GET'])
def get_publications():
    """獲取所有出版物"""
    data = load_json('publications.json')
    return jsonify(data)

@app.route('/api/publications', methods=['POST'])
def add_publication():
    """新增出版物"""
    data = load_json('publications.json')
    new_pub = request.json

    # 生成新 ID (手動新增使用 z 開頭)
    existing_ids = [p['id'] for p in data['publications']]
    pub_type = new_pub.get('type', 'journal')

    # 根據類型決定 ID 前綴
    if pub_type == 'journal':
        prefix = 'jz'
    elif pub_type == 'conference':
        prefix = 'cz'
    elif pub_type == 'book':
        prefix = 'bz'
    else:
        prefix = 'jz'  # 預設

    # 找到該前綴的最大編號
    max_num = 0
    for id_str in existing_ids:
        if id_str.startswith(prefix):
            try:
                num = int(id_str[2:])  # 跳過前兩個字元 (例如 'jz')
                max_num = max(max_num, num)
            except ValueError:
                continue

    new_pub['id'] = f"{prefix}{max_num + 1}"

    data['publications'].append(new_pub)

    if save_json('publications.json', data):
        return jsonify({'success': True, 'publication': new_pub})
    return jsonify({'success': False, 'error': 'Failed to save'}), 500

@app.route('/api/publications/<pub_id>', methods=['PUT'])
def update_publication(pub_id):
    """更新出版物"""
    data = load_json('publications.json')
    updated_pub = request.json
    
    for i, pub in enumerate(data['publications']):
        if pub['id'] == pub_id:
            data['publications'][i] = updated_pub
            if save_json('publications.json', data):
                return jsonify({'success': True, 'publication': updated_pub})
            return jsonify({'success': False, 'error': 'Failed to save'}), 500
    
    return jsonify({'success': False, 'error': 'Publication not found'}), 404

@app.route('/api/publications/<pub_id>', methods=['DELETE'])
def delete_publication(pub_id):
    """刪除出版物"""
    data = load_json('publications.json')

    data['publications'] = [p for p in data['publications'] if p['id'] != pub_id]

    if save_json('publications.json', data):
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'Failed to save'}), 500

@app.route('/api/publications/reorder', methods=['POST'])
def reorder_publications():
    """重新排序出版物"""
    data = load_json('publications.json')
    new_order = request.json.get('order', [])

    if not new_order:
        return jsonify({'success': False, 'error': 'No order provided'}), 400

    # 建立 ID 到出版物的映射
    pub_map = {pub['id']: pub for pub in data['publications']}

    # 根據新順序重新排列
    reordered_pubs = []
    for pub_id in new_order:
        if pub_id in pub_map:
            reordered_pubs.append(pub_map[pub_id])

    # 添加任何不在新順序中的出版物（以防萬一）
    for pub in data['publications']:
        if pub['id'] not in new_order:
            reordered_pubs.append(pub)

    data['publications'] = reordered_pubs

    if save_json('publications.json', data):
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'Failed to save'}), 500

def crawl_dblp(existing_pubs=None):
    """從 DBLP 爬取出版物資料

    Args:
        existing_pubs: 現有的出版物列表，用於檢查是否需要進入 conference 連結
    """
    url = "https://dblp.org/pid/p/HsingKuoKennethPao.html"

    # 建立現有資料的映射（ID -> publication）
    existing_map = {}
    if existing_pubs:
        existing_map = {pub['id']: pub for pub in existing_pubs}

    try:
        # 發送請求
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        # 解析 HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        publications = []

        # 找到所有的出版物項目
        entries = soup.find_all('li', class_='entry')

        for entry in entries:
            # 找到 ID (nr div)
            nr_div = entry.find('div', class_='nr')
            if not nr_div:
                continue

            # 提取 ID
            id_match = re.search(r'\[(j\d+|c\d+)\]', nr_div.text)
            if not id_match:
                continue

            pub_id = id_match.group(1)

            # 只處理 journal (j) 和 conference (c)
            if not (pub_id.startswith('j') or pub_id.startswith('c')):
                continue

            # 確定類型
            pub_type = 'journal' if pub_id.startswith('j') else 'conference'

            # 找到標題
            title_tag = entry.find('span', class_='title')
            if not title_tag:
                continue
            title = title_tag.text.strip()

            # 找到作者
            authors_list = []
            for author in entry.find_all('span', itemprop='author'):
                author_name = author.find('span', itemprop='name')
                if author_name:
                    authors_list.append(author_name.text.strip())
            authors = ', '.join(authors_list)

            # 獲取完整的文字內容來提取 venue, volume, pages, year
            # DBLP 的格式通常是：Title. Venue Volume: Pages (Year)
            entry_text = entry.get_text(separator=' ', strip=True)

            # 初始化變數
            venue = ''
            year = 0
            volume = ''
            pages = ''
            location = ''
            date = ''

            # 提取年份（通常在括號中）
            year_match = re.search(r'\((\d{4})\)', entry_text)
            if year_match:
                year = int(year_match.group(1))

            if pub_type == 'journal':
                # Journal 格式: Title. Venue Volume: Pages (Year)
                # 例如: Interpretable deep model pruning. Neurocomputing 647: 130485 (2025)

                # 嘗試匹配 "Venue Volume: Pages (Year)" 格式
                # 在標題後面找到 venue 資訊
                title_end = entry_text.find(title) + len(title)
                if title_end > 0:
                    remaining_text = entry_text[title_end:].strip()
                    # 移除開頭的句點
                    if remaining_text.startswith('.'):
                        remaining_text = remaining_text[1:].strip()

                    # 匹配格式: Venue Volume : Pages ( Year )
                    # 注意：DBLP 的文字中可能有額外的空格
                    # 例如: Neurocomputing 647 : 130485 ( 2025 )
                    # 或: IEEE Trans. ... 2 ( 3 ) : 162-175 ( 2010 )

                    # 先嘗試匹配帶 issue 的格式: Venue Volume ( Issue ) : Pages ( Year )
                    venue_match = re.match(r'([^0-9]+?)\s+(\d+)\s*\(\s*\d+\s*\)\s*:\s*([0-9\-]+)\s*\(\s*(\d{4})\s*\)', remaining_text)
                    if venue_match:
                        venue = venue_match.group(1).strip()
                        volume = venue_match.group(2).strip()
                        pages = venue_match.group(3).strip()
                        year = int(venue_match.group(4))
                    else:
                        # 嘗試匹配簡單格式: Venue Volume : Pages ( Year )
                        venue_match = re.match(r'([^0-9]+?)\s+(\d+)\s*:\s*([0-9\-]+)\s*\(\s*(\d{4})\s*\)', remaining_text)
                        if venue_match:
                            venue = venue_match.group(1).strip()
                            volume = venue_match.group(2).strip()
                            pages = venue_match.group(3).strip()
                            year = int(venue_match.group(4))
                        else:
                            # 嘗試只匹配 venue 和 year（沒有 volume 和 pages）
                            venue_match2 = re.match(r'([^(]+?)\s*\(\s*(\d{4})\s*\)', remaining_text)
                            if venue_match2:
                                venue_text = venue_match2.group(1).strip()
                                year = int(venue_match2.group(2))
                                # 嘗試從 venue_text 中分離 venue, volume, pages
                                # 格式可能是: "Venue Volume: Pages"
                                parts_match = re.match(r'([^0-9]+?)\s+(\d+)\s*:\s*([0-9\-]+)', venue_text)
                                if parts_match:
                                    venue = parts_match.group(1).strip()
                                    volume = parts_match.group(2).strip()
                                    pages = parts_match.group(3).strip()
                                else:
                                    venue = venue_text

            elif pub_type == 'conference':
                # Conference 格式: Title. Venue Year: Pages
                # 例如: Reconsider Time Series Analysis. IEEE Big Data 2024: 1558-1565

                # 先從主頁面提取基本資訊
                title_end = entry_text.find(title) + len(title)
                if title_end > 0:
                    remaining_text = entry_text[title_end:].strip()
                    # 移除開頭的句點
                    if remaining_text.startswith('.'):
                        remaining_text = remaining_text[1:].strip()

                    # 匹配格式: Venue Year : Pages
                    # 注意：DBLP 的文字中可能有額外的空格
                    venue_match = re.match(r'(.+?)\s+(\d{4})\s*:\s*([0-9\-]+)', remaining_text)
                    if venue_match:
                        venue = venue_match.group(1).strip()
                        year = int(venue_match.group(2))
                        pages = venue_match.group(3).strip()
                    else:
                        # 嘗試只匹配 venue 和 year（沒有 pages）
                        venue_match2 = re.match(r'(.+?)\s+(\d{4})', remaining_text)
                        if venue_match2:
                            venue = venue_match2.group(1).strip()
                            year = int(venue_match2.group(2))

                # 檢查是否需要進入 conference 連結
                # 只有在現有資料沒有 location 時才進入
                should_fetch_details = True
                if pub_id in existing_map:
                    existing_pub = existing_map[pub_id]
                    if existing_pub.get('location') and existing_pub.get('location') != '':
                        # 已有 location，不需要再抓取
                        should_fetch_details = False
                        # 使用現有的 location 和 date
                        location = existing_pub.get('location', '')
                        date = existing_pub.get('date', '')

                # 嘗試進入 conference 連結抓取完整資訊
                if should_fetch_details:
                    try:
                        # 找到 conference 的連結
                        conf_link = entry.find('a', href=re.compile(r'/db/conf/'))
                        if conf_link and conf_link.get('href'):
                            href = conf_link['href']
                            # 檢查是否已經是完整 URL
                            if href.startswith('http'):
                                conf_url = href
                            else:
                                conf_url = 'https://dblp.org' + href
                            # 移除錨點（#xxx）
                            conf_url = conf_url.split('#')[0]

                            # 發送請求到 conference 頁面
                            conf_response = requests.get(conf_url, timeout=10)
                            if conf_response.status_code == 200:
                                conf_soup = BeautifulSoup(conf_response.text, 'html.parser')

                                # 找到 h1 標籤，格式: "46th EMBC 2024: Orlando, FL, USA"
                                h1 = conf_soup.find('h1')
                                if h1:
                                    h1_text = h1.get_text(strip=True)
                                    # 解析格式: "完整會議名稱: 地點"
                                    h1_match = re.match(r'(.+?):\s*(.+)', h1_text)
                                    if h1_match:
                                        full_venue = h1_match.group(1).strip()
                                        location = h1_match.group(2).strip()

                                        # 從完整會議名稱中提取日期資訊（如果有的話）
                                        # 例如: "46th EMBC 2024" -> venue = "46th Annual International Conference of the IEEE Engineering in Medicine and Biology Society (EMBC 2024)"
                                        # 我們需要從頁面中找到完整的會議名稱

                                        # 找到完整的會議名稱（通常在 cite 標籤中）
                                        cite = conf_soup.find('cite', class_='data')
                                        if cite:
                                            # 找到 itemprop="name" 的標籤
                                            full_name_tag = cite.find('span', itemprop='name')
                                            if full_name_tag:
                                                # 這是完整的會議名稱，例如 "46th Annual International Conference of the IEEE Engineering in Medicine and Biology Society, EMBC 2024, Orlando, FL, USA, July 15-19, 2024"
                                                full_name = full_name_tag.get_text(strip=True)

                                                # 解析日期（通常在最後）
                                                # 格式: "Month Day-Day, Year" 或 "Month Day, Year"
                                                date_match = re.search(r'([A-Z][a-z]+\s+\d+(?:-\d+)?,\s+\d{4})', full_name)
                                                if date_match:
                                                    date = date_match.group(1)

                                                # 更新 venue 為完整名稱（移除地點和日期部分）
                                                # 例如: "46th Annual International Conference of the IEEE Engineering in Medicine and Biology Society, EMBC 2024"
                                                venue_parts = full_name.split(',')
                                                if len(venue_parts) >= 2:
                                                    # 取前兩部分作為 venue
                                                    venue = ', '.join(venue_parts[:2]).strip()

                                        # 如果還沒找到日期，嘗試在整個頁面中搜尋
                                        if not date:
                                            page_text = conf_soup.get_text()
                                            date_match = re.search(r'((?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d+(?:-\d+)?,\s+\d{4})', page_text)
                                            if date_match:
                                                date = date_match.group(1)
                    except Exception as e:
                        print(f"Warning: Failed to fetch conference details for {pub_id}: {e}")

            # 建立出版物物件
            pub = {
                'id': pub_id,
                'type': pub_type,
                'authors': authors,
                'title': title,
                'venue': venue,
                'year': year,
                'highlight_author': 'Hsing-Kuo Pao'
            }

            # 根據類型添加額外欄位
            if pub_type == 'journal':
                pub['volume'] = volume
                pub['pages'] = pages
            elif pub_type == 'conference':
                pub['location'] = location
                pub['date'] = date

            publications.append(pub)

        return publications

    except Exception as e:
        print(f"Error crawling DBLP: {e}")
        raise

@app.route('/api/publications/crawl', methods=['POST'])
def crawl_publications():
    """爬取 DBLP 出版物"""
    try:
        # 載入現有資料
        data = load_json('publications.json')
        if not data:
            data = {'publications': []}

        # 爬取資料（傳入現有資料以避免重複抓取）
        crawled_pubs = crawl_dblp(existing_pubs=data['publications'])

        # 建立 ID 到索引的映射
        existing_map = {pub['id']: i for i, pub in enumerate(data['publications'])}

        # 統計
        added = 0
        updated = 0
        skipped = 0

        # 處理爬取的資料
        for pub in crawled_pubs:
            if pub['id'] in existing_map:
                # 已存在的資料
                idx = existing_map[pub['id']]
                existing_pub = data['publications'][idx]

                # 檢查是否需要更新（針對 conference 沒有 location 的情況）
                if pub['type'] == 'conference':
                    needs_update = False

                    # 只有在現有資料沒有 location 時才更新
                    if not existing_pub.get('location') or existing_pub.get('location') == '':
                        if pub.get('location'):
                            needs_update = True

                    if needs_update:
                        # 更新資料
                        data['publications'][idx] = pub
                        updated += 1
                    else:
                        skipped += 1
                else:
                    skipped += 1
            else:
                # 新資料，插入到最前面
                data['publications'].insert(0, pub)
                added += 1

        # 儲存
        if save_json('publications.json', data):
            return jsonify({
                'success': True,
                'added': added,
                'updated': updated,
                'skipped': skipped,
                'total': len(crawled_pubs)
            })
        else:
            return jsonify({'success': False, 'error': 'Failed to save data'}), 500

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/publications/sort', methods=['POST'])
def sort_publications():
    """重新排序出版物
    排序規則：
    1. 手動新增的（jz, cz, bz 開頭）在最上面
    2. 然後按 ID 從大到小排序
    """
    try:
        # 載入現有資料
        data = load_json('publications.json')
        if not data or 'publications' not in data:
            return jsonify({'success': False, 'error': 'No data found'}), 404

        publications = data['publications']

        # 分類出版物
        manual_pubs = []  # 手動新增的 (jz, cz, bz)
        auto_pubs = []    # 爬蟲的 (j, c)

        for pub in publications:
            pub_id = pub.get('id', '')
            # 檢查是否為手動新增（兩個字母開頭，第二個是 z）
            if len(pub_id) >= 2 and pub_id[1] == 'z':
                manual_pubs.append(pub)
            else:
                auto_pubs.append(pub)

        # 排序函數：提取 ID 中的數字部分
        def extract_number(pub):
            pub_id = pub.get('id', '')
            # 移除前綴字母，提取數字
            match = re.search(r'\d+', pub_id)
            if match:
                return int(match.group())
            return 0

        # 手動新增的按 ID 從大到小排序
        manual_pubs.sort(key=extract_number, reverse=True)

        # 爬蟲的按 ID 從大到小排序
        auto_pubs.sort(key=extract_number, reverse=True)

        # 合併：手動新增的在前，爬蟲的在後
        sorted_pubs = manual_pubs + auto_pubs

        # 更新資料
        data['publications'] = sorted_pubs

        # 儲存
        if save_json('publications.json', data):
            return jsonify({'success': True, 'total': len(sorted_pubs)})
        else:
            return jsonify({'success': False, 'error': 'Failed to save data'}), 500

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== Members ====================

@app.route('/members')
def members():
    """成員管理頁面"""
    data = load_json('members.json')
    return render_template('members.html',
                         members=data.get('members', []) if data else [],
                         contact_person=data.get('contact_person', {}) if data else {},
                         lab_info=data.get('lab_info', {}) if data else {})

@app.route('/api/members', methods=['GET'])
def get_members():
    """獲取所有成員"""
    data = load_json('members.json')
    return jsonify(data)

@app.route('/api/members', methods=['POST'])
def add_member():
    """新增成員"""
    data = load_json('members.json')
    new_member = request.json

    # 生成新 ID
    existing_ids = [m['id'] for m in data['members']]
    max_num = max([int(id[1:]) for id in existing_ids], default=0)
    new_member['id'] = f"m{max_num + 1:03d}"

    # 找到同年份的第一個成員的位置
    new_year = new_member['year']
    insert_index = None

    for i, member in enumerate(data['members']):
        if member['year'] == new_year:
            insert_index = i
            break

    # 如果找到同年份的成員，插入到該位置；否則加到最後
    if insert_index is not None:
        data['members'].insert(insert_index, new_member)
    else:
        data['members'].append(new_member)

    if save_json('members.json', data):
        return jsonify({'success': True, 'member': new_member})
    return jsonify({'success': False, 'error': 'Failed to save'}), 500

@app.route('/api/members/<member_id>', methods=['PUT'])
def update_member(member_id):
    """更新成員"""
    data = load_json('members.json')
    updated_member = request.json

    for i, member in enumerate(data['members']):
        if member['id'] == member_id:
            data['members'][i] = updated_member
            if save_json('members.json', data):
                return jsonify({'success': True, 'member': updated_member})
            return jsonify({'success': False, 'error': 'Failed to save'}), 500

    return jsonify({'success': False, 'error': 'Member not found'}), 404

@app.route('/api/members/<member_id>', methods=['DELETE'])
def delete_member(member_id):
    """刪除成員"""
    data = load_json('members.json')

    data['members'] = [m for m in data['members'] if m['id'] != member_id]

    if save_json('members.json', data):
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'Failed to save'}), 500

@app.route('/api/contact-person', methods=['PUT'])
def update_contact_person():
    """更新 Contact Person"""
    data = load_json('members.json')
    member_id = request.json.get('member_id')

    # 找到選中的成員
    selected_member = None
    for member in data['members']:
        if member['id'] == member_id:
            selected_member = member
            break

    if not selected_member:
        return jsonify({'success': False, 'error': 'Member not found'}), 404

    # 更新 contact_person
    data['contact_person'] = {
        'name': selected_member['name'],
        'email': selected_member.get('email', ''),
        'photo': selected_member['photo']
    }

    if save_json('members.json', data):
        return jsonify({'success': True, 'contact_person': data['contact_person']})
    return jsonify({'success': False, 'error': 'Failed to save'}), 500

# ==================== Events ====================

@app.route('/events')
def events():
    """活動管理頁面"""
    data = load_json('events.json')
    return render_template('events.html', events=data.get('events', []) if data else [])

@app.route('/api/events', methods=['GET'])
def get_events():
    """獲取所有活動"""
    data = load_json('events.json')
    return jsonify(data)

@app.route('/api/events', methods=['POST'])
def add_event():
    """新增活動"""
    data = load_json('events.json')
    new_event = request.json

    # 生成新 ID
    existing_ids = [e['id'] for e in data['events']]
    max_num = max([int(id[1:]) for id in existing_ids], default=0)
    new_event['id'] = f"e{max_num + 1:03d}"

    data['events'].append(new_event)

    if save_json('events.json', data):
        return jsonify({'success': True, 'event': new_event})
    return jsonify({'success': False, 'error': 'Failed to save'}), 500

@app.route('/api/events/<event_id>', methods=['PUT'])
def update_event(event_id):
    """更新活動"""
    data = load_json('events.json')
    updated_event = request.json

    for i, event in enumerate(data['events']):
        if event['id'] == event_id:
            data['events'][i] = updated_event
            if save_json('events.json', data):
                return jsonify({'success': True, 'event': updated_event})
            return jsonify({'success': False, 'error': 'Failed to save'}), 500

    return jsonify({'success': False, 'error': 'Event not found'}), 404

@app.route('/api/events/<event_id>', methods=['DELETE'])
def delete_event(event_id):
    """刪除活動"""
    data = load_json('events.json')

    data['events'] = [e for e in data['events'] if e['id'] != event_id]

    if save_json('events.json', data):
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'Failed to save'}), 500

# ==================== File Upload ====================

@app.route('/upload', methods=['POST'])
def upload_file():
    """上傳文件"""
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file part'}), 400

    file = request.files['file']
    upload_type = request.form.get('type', 'member')  # member, event, general

    if file.filename == '':
        return jsonify({'success': False, 'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        # 根據類型決定儲存路徑
        if upload_type == 'member':
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], 'member', filename)
        elif upload_type == 'event':
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], 'event', filename)
        else:
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], 'general', filename)

        file.save(save_path)

        # 返回相對路徑
        relative_path = f"asset/{upload_type}/{filename}"
        return jsonify({'success': True, 'path': relative_path})

    return jsonify({'success': False, 'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')

