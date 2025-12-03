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
    
    # 生成新 ID
    existing_ids = [p['id'] for p in data['publications']]
    pub_type = new_pub.get('type', 'j')
    max_num = max([int(id[1:]) for id in existing_ids if id.startswith(pub_type[0])], default=0)
    new_pub['id'] = f"{pub_type[0]}{max_num + 1}"
    
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

