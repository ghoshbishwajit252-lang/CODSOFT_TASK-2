from flask import Flask, request, jsonify, render_template_string
import json
import os
from datetime import datetime
import uuid

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')

CONTACTS_FILE = 'contacts.json'

def load_contacts():
    if os.path.exists(CONTACTS_FILE):
        try:
            with open(CONTACTS_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_contacts(contacts):
    with open(CONTACTS_FILE, 'w') as f:
        json.dump(contacts, f, indent=2)

# --- Main Page (Redesigned) ---
@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        <title>📇 Contact Book Pro</title>
        <!-- Google Fonts & Font Awesome -->
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400;14..32,500;14..32,600;14..32,700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Inter', -apple-system, sans-serif;
                background: #f4f6f9;
                min-height: 100vh;
                display: flex;
                justify-content: center;
                padding: 40px 20px;
            }
            .app-container {
                max-width: 1300px;
                width: 100%;
            }

            /* --- Header --- */
            .app-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 32px;
                flex-wrap: wrap;
                gap: 16px;
            }
            .logo-area {
                display: flex;
                align-items: center;
                gap: 14px;
            }
            .logo-icon {
                width: 48px;
                height: 48px;
                background: linear-gradient(145deg, #6366f1, #8b5cf6);
                border-radius: 16px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 24px;
                color: white;
                box-shadow: 0 8px 20px rgba(99, 102, 241, 0.3);
            }
            .app-title {
                font-size: 28px;
                font-weight: 700;
                color: #1e293b;
                letter-spacing: -0.5px;
            }
            .app-title span { color: #6366f1; }

            .header-actions {
                display: flex;
                gap: 12px;
                flex-wrap: wrap;
            }
            .search-wrapper {
                position: relative;
                display: flex;
                align-items: center;
            }
            .search-wrapper i {
                position: absolute;
                left: 16px;
                color: #94a3b8;
            }
            .search-wrapper input {
                padding: 12px 20px 12px 44px;
                border: 1.5px solid #e2e8f0;
                border-radius: 12px;
                font-size: 0.95rem;
                width: 260px;
                background: white;
                transition: all 0.2s;
                font-family: 'Inter', sans-serif;
            }
            .search-wrapper input:focus {
                outline: none;
                border-color: #6366f1;
                box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.1);
                width: 300px;
            }
            .btn {
                padding: 12px 24px;
                border: none;
                border-radius: 12px;
                font-weight: 600;
                font-size: 0.95rem;
                cursor: pointer;
                transition: all 0.2s;
                display: inline-flex;
                align-items: center;
                gap: 8px;
                font-family: 'Inter', sans-serif;
                text-decoration: none;
            }
            .btn-primary {
                background: linear-gradient(145deg, #6366f1, #8b5cf6);
                color: white;
                box-shadow: 0 4px 14px rgba(99, 102, 241, 0.35);
            }
            .btn-primary:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4);
            }
            .btn-success {
                background: #10b981;
                color: white;
            }
            .btn-success:hover { background: #059669; transform: translateY(-2px); }
            .btn-danger {
                background: #ef4444;
                color: white;
            }
            .btn-danger:hover { background: #dc2626; transform: translateY(-2px); }
            .btn-outline {
                background: transparent;
                color: #475569;
                border: 1.5px solid #e2e8f0;
            }
            .btn-outline:hover { background: #f1f5f9; }

            /* --- Stats --- */
            .stats-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
                gap: 16px;
                margin-bottom: 32px;
            }
            .stat-card {
                background: white;
                padding: 18px 22px;
                border-radius: 16px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.05);
                display: flex;
                align-items: center;
                gap: 14px;
                border: 1px solid #f1f5f9;
            }
            .stat-icon {
                width: 44px;
                height: 44px;
                background: #eef2ff;
                border-radius: 12px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: #6366f1;
                font-size: 18px;
            }
            .stat-info .number { font-size: 22px; font-weight: 700; color: #0f172a; line-height: 1.2; }
            .stat-info .label { font-size: 14px; color: #64748b; }

            /* --- Contact Grid --- */
            .contacts-grid {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                gap: 24px;
            }
            .contact-card {
                background: white;
                border-radius: 20px;
                padding: 24px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
                border: 1px solid #f1f5f9;
                transition: all 0.25s;
            }
            .contact-card:hover {
                transform: translateY(-6px);
                box-shadow: 0 20px 40px -12px rgba(0,0,0,0.15);
                border-color: #e2e8f0;
            }
            .card-header {
                display: flex;
                align-items: center;
                gap: 16px;
                margin-bottom: 16px;
            }
            .avatar {
                width: 56px;
                height: 56px;
                border-radius: 16px;
                background: linear-gradient(145deg, #6366f1, #8b5cf6);
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-weight: 700;
                font-size: 20px;
                flex-shrink: 0;
            }
            .contact-name {
                font-size: 18px;
                font-weight: 700;
                color: #0f172a;
            }
            .detail-row {
                display: flex;
                align-items: center;
                gap: 12px;
                padding: 8px 0;
                color: #475569;
                font-size: 0.95rem;
                border-bottom: 1px solid #f8fafc;
            }
            .detail-row i {
                width: 20px;
                color: #6366f1;
                text-align: center;
            }
            .card-actions {
                display: flex;
                gap: 10px;
                margin-top: 18px;
                padding-top: 16px;
                border-top: 1px solid #f1f5f9;
            }
            .card-actions .btn { flex: 1; justify-content: center; padding: 10px; font-size: 0.85rem; }

            /* --- Empty State --- */
            .empty-state {
                grid-column: 1 / -1;
                text-align: center;
                padding: 80px 20px;
                background: white;
                border-radius: 24px;
                border: 2px dashed #e2e8f0;
            }
            .empty-state i { font-size: 56px; color: #cbd5e1; margin-bottom: 20px; }
            .empty-state h3 { font-size: 24px; color: #1e293b; margin-bottom: 8px; }
            .empty-state p { color: #64748b; margin-bottom: 24px; }

            /* --- Modal (Add/Edit) --- */
            .modal-overlay {
                display: none;
                position: fixed;
                inset: 0;
                background: rgba(15, 23, 42, 0.5);
                backdrop-filter: blur(8px);
                justify-content: center;
                align-items: center;
                z-index: 1000;
                padding: 20px;
                animation: fadeIn 0.2s;
            }
            .modal-overlay.active { display: flex; }
            .modal-box {
                background: white;
                border-radius: 28px;
                max-width: 520px;
                width: 100%;
                padding: 36px 40px;
                box-shadow: 0 50px 100px -20px rgba(0,0,0,0.3);
                animation: slideUp 0.3s ease;
            }
            @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
            @keyframes slideUp { from { transform: translateY(30px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }

            .modal-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 28px;
            }
            .modal-header h2 {
                font-size: 24px;
                font-weight: 700;
                color: #0f172a;
            }
            .modal-close {
                background: none;
                border: none;
                font-size: 24px;
                color: #94a3b8;
                cursor: pointer;
                padding: 4px 8px;
                border-radius: 8px;
                transition: 0.2s;
            }
            .modal-close:hover { background: #f1f5f9; color: #0f172a; }

            .form-group { margin-bottom: 20px; }
            .form-group label {
                display: block;
                font-weight: 600;
                font-size: 0.9rem;
                color: #334155;
                margin-bottom: 6px;
            }
            .form-group label .required { color: #ef4444; margin-left: 4px; }
            .form-group input {
                width: 100%;
                padding: 12px 16px;
                border: 1.5px solid #e2e8f0;
                border-radius: 12px;
                font-size: 1rem;
                transition: 0.2s;
                font-family: 'Inter', sans-serif;
                background: #f8fafc;
            }
            .form-group input:focus {
                outline: none;
                border-color: #6366f1;
                background: white;
                box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.08);
            }
            .form-actions {
                display: flex;
                gap: 12px;
                margin-top: 28px;
            }
            .form-actions .btn { flex: 1; justify-content: center; padding: 14px; }

            /* --- Toast --- */
            .toast-container {
                position: fixed;
                bottom: 30px;
                right: 30px;
                z-index: 2000;
                display: flex;
                flex-direction: column;
                gap: 10px;
            }
            .toast {
                padding: 14px 24px;
                border-radius: 14px;
                color: white;
                font-weight: 500;
                background: #0f172a;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                transform: translateX(400px);
                opacity: 0;
                transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
                display: flex;
                align-items: center;
                gap: 12px;
                font-size: 0.95rem;
            }
            .toast.show { transform: translateX(0); opacity: 1; }
            .toast.success { background: #10b981; }
            .toast.error { background: #ef4444; }

            /* Responsive */
            @media (max-width: 768px) {
                body { padding: 20px 12px; }
                .app-header { flex-direction: column; align-items: stretch; gap: 16px; }
                .search-wrapper input { width: 100%; }
                .search-wrapper input:focus { width: 100%; }
                .header-actions { flex-direction: column; }
                .btn { justify-content: center; }
                .modal-box { padding: 28px 20px; }
                .stats-grid { grid-template-columns: 1fr 1fr; }
            }
            @media (max-width: 480px) {
                .stats-grid { grid-template-columns: 1fr; }
                .contacts-grid { grid-template-columns: 1fr; }
            }
        </style>
    </head>
    <body>
        <div class="app-container">
            <!-- Header -->
            <header class="app-header">
                <div class="logo-area">
                    <div class="logo-icon">📇</div>
                    <div class="app-title">Contact<span>Book</span></div>
                </div>
                <div class="header-actions">
                    <div class="search-wrapper">
                        <i class="fas fa-search"></i>
                        <input type="text" id="searchInput" placeholder="Search contacts..." oninput="searchContacts()">
                    </div>
                    <button class="btn btn-primary" onclick="openAddModal()">
                        <i class="fas fa-plus"></i> Add Contact
                    </button>
                </div>
            </header>

            <!-- Stats -->
            <div class="stats-grid" id="statsBar">
                <div class="stat-card">
                    <div class="stat-icon"><i class="fas fa-users"></i></div>
                    <div class="stat-info"><div class="number" id="totalContacts">0</div><div class="label">Total</div></div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon"><i class="fas fa-phone"></i></div>
                    <div class="stat-info"><div class="number" id="phoneCount">0</div><div class="label">With Phone</div></div>
                </div>
                <div class="stat-card">
                    <div class="stat-icon"><i class="fas fa-envelope"></i></div>
                    <div class="stat-info"><div class="number" id="emailCount">0</div><div class="label">With Email</div></div>
                </div>
            </div>

            <!-- Contacts Grid -->
            <div class="contacts-grid" id="contactsGrid"></div>
        </div>

        <!-- Modal -->
        <div class="modal-overlay" id="contactModal">
            <div class="modal-box">
                <div class="modal-header">
                    <h2 id="modalTitle">Add New Contact</h2>
                    <button class="modal-close" onclick="closeModal()"><i class="fas fa-times"></i></button>
                </div>
                <form id="contactForm" onsubmit="saveContact(event)">
                    <input type="hidden" id="contactId">
                    <div class="form-group">
                        <label>Full Name <span class="required">*</span></label>
                        <input type="text" id="name" required placeholder="e.g. John Doe">
                    </div>
                    <div class="form-group">
                        <label>Phone <span class="required">*</span></label>
                        <input type="tel" id="phone" required placeholder="e.g. +1 234 567 890">
                    </div>
                    <div class="form-group">
                        <label>Email</label>
                        <input type="email" id="email" placeholder="john@example.com">
                    </div>
                    <div class="form-group">
                        <label>Address</label>
                        <input type="text" id="address" placeholder="123 Main St, City">
                    </div>
                    <div class="form-actions">
                        <button type="submit" class="btn btn-success" id="saveBtn">
                            <i class="fas fa-save"></i> <span id="saveBtnText">Save</span>
                        </button>
                        <button type="button" class="btn btn-outline" onclick="closeModal()">Cancel</button>
                    </div>
                </form>
            </div>
        </div>

        <!-- Toast Container -->
        <div class="toast-container" id="toastContainer"></div>

        <script>
            // --- State ---
            let contacts = [];
            let editingId = null;

            // --- Load & Render ---
            document.addEventListener('DOMContentLoaded', loadContacts);

            async function loadContacts() {
                try {
                    const res = await fetch('/api/contacts');
                    contacts = await res.json();
                    renderContacts(contacts);
                    updateStats(contacts);
                } catch { showToast('Error loading contacts', 'error'); }
            }

            function renderContacts(list) {
                const grid = document.getElementById('contactsGrid');
                if (!list.length) {
                    grid.innerHTML = `
                        <div class="empty-state">
                            <i class="fas fa-address-book"></i>
                            <h3>No contacts yet</h3>
                            <p>Start building your contact list</p>
                            <button class="btn btn-primary" onclick="openAddModal()">
                                <i class="fas fa-plus"></i> Add Your First Contact
                            </button>
                        </div>`;
                    return;
                }
                grid.innerHTML = list.map(c => `
                    <div class="contact-card">
                        <div class="card-header">
                            <div class="avatar">${getInitials(c.name)}</div>
                            <div class="contact-name">${escapeHtml(c.name)}</div>
                        </div>
                        <div class="detail-row"><i class="fas fa-phone"></i> ${escapeHtml(c.phone)}</div>
                        ${c.email ? `<div class="detail-row"><i class="fas fa-envelope"></i> ${escapeHtml(c.email)}</div>` : ''}
                        ${c.address ? `<div class="detail-row"><i class="fas fa-map-marker-alt"></i> ${escapeHtml(c.address)}</div>` : ''}
                        <div class="card-actions">
                            <button class="btn btn-primary" onclick="editContact('${c.id}')"><i class="fas fa-edit"></i> Edit</button>
                            <button class="btn btn-danger" onclick="deleteContact('${c.id}')"><i class="fas fa-trash"></i></button>
                        </div>
                    </div>
                `).join('');
            }

            function updateStats(list) {
                document.getElementById('totalContacts').textContent = list.length;
                document.getElementById('phoneCount').textContent = list.filter(c => c.phone).length;
                document.getElementById('emailCount').textContent = list.filter(c => c.email).length;
            }

            // --- Helpers ---
            function getInitials(name) {
                if (!name) return '?';
                const parts = name.trim().split(' ');
                if (parts.length === 1) return parts[0].charAt(0).toUpperCase();
                return (parts[0].charAt(0) + parts[parts.length-1].charAt(0)).toUpperCase();
            }
            function escapeHtml(text) {
                const div = document.createElement('div');
                div.textContent = text;
                return div.innerHTML;
            }

            // --- Search ---
            async function searchContacts() {
                const q = document.getElementById('searchInput').value.trim();
                if (!q) { renderContacts(contacts); updateStats(contacts); return; }
                try {
                    const res = await fetch(`/api/contacts/search?q=${encodeURIComponent(q)}`);
                    const results = await res.json();
                    renderContacts(results);
                    updateStats(results);
                } catch { showToast('Search error', 'error'); }
            }

            // --- Modal ---
            function openAddModal() {
                editingId = null;
                document.getElementById('modalTitle').textContent = 'Add New Contact';
                document.getElementById('contactForm').reset();
                document.getElementById('contactId').value = '';
                document.getElementById('saveBtnText').textContent = 'Save';
                document.getElementById('contactModal').classList.add('active');
                document.body.style.overflow = 'hidden';
                setTimeout(() => document.getElementById('name').focus(), 100);
            }

            function editContact(id) {
                const contact = contacts.find(c => c.id === id);
                if (!contact) return;
                editingId = id;
                document.getElementById('modalTitle').textContent = 'Edit Contact';
                document.getElementById('contactId').value = id;
                document.getElementById('name').value = contact.name;
                document.getElementById('phone').value = contact.phone;
                document.getElementById('email').value = contact.email || '';
                document.getElementById('address').value = contact.address || '';
                document.getElementById('saveBtnText').textContent = 'Update';
                document.getElementById('contactModal').classList.add('active');
                document.body.style.overflow = 'hidden';
                setTimeout(() => document.getElementById('name').focus(), 100);
            }

            function closeModal() {
                document.getElementById('contactModal').classList.remove('active');
                document.body.style.overflow = '';
            }

            // --- Save Contact ---
            async function saveContact(event) {
                event.preventDefault();
                const id = document.getElementById('contactId').value;
                const data = {
                    name: document.getElementById('name').value.trim(),
                    phone: document.getElementById('phone').value.trim(),
                    email: document.getElementById('email').value.trim(),
                    address: document.getElementById('address').value.trim()
                };
                if (!data.name || !data.phone) {
                    showToast('Name and Phone are required', 'error');
                    return;
                }
                try {
                    const url = id ? `/api/contacts/${id}` : '/api/contacts';
                    const method = id ? 'PUT' : 'POST';
                    const res = await fetch(url, {
                        method,
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(data)
                    });
                    if (res.ok) {
                        closeModal();
                        await loadContacts();
                        showToast(id ? 'Contact updated!' : 'Contact added!', 'success');
                    } else {
                        showToast('Error saving contact', 'error');
                    }
                } catch { showToast('Error saving contact', 'error'); }
            }

            // --- Delete ---
            async function deleteContact(id) {
                const contact = contacts.find(c => c.id === id);
                if (!confirm(`Delete "${contact?.name}"?`)) return;
                try {
                    const res = await fetch(`/api/contacts/${id}`, { method: 'DELETE' });
                    if (res.ok) {
                        await loadContacts();
                        showToast('Contact deleted', 'success');
                    } else {
                        showToast('Error deleting contact', 'error');
                    }
                } catch { showToast('Error deleting contact', 'error'); }
            }

            // --- Toast ---
            function showToast(message, type = 'success') {
                const container = document.getElementById('toastContainer');
                const toast = document.createElement('div');
                toast.className = `toast ${type}`;
                toast.innerHTML = `<i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'}"></i> ${message}`;
                container.appendChild(toast);
                requestAnimationFrame(() => toast.classList.add('show'));
                setTimeout(() => {
                    toast.classList.remove('show');
                    setTimeout(() => toast.remove(), 400);
                }, 3000);
            }

            // --- Close modal on outside click & ESC ---
            document.getElementById('contactModal').addEventListener('click', function(e) {
                if (e.target === this) closeModal();
            });
            document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModal(); });
        </script>
    </body>
    </html>
    '''

# --- Edit Page Route (FIXES THE 404 ERROR) ---
@app.route('/edit/<contact_id>')
def edit_contact_page(contact_id):
    """Dedicated edit page with modern UI"""
    return f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        <title>✏️ Edit Contact</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400;14..32,500;14..32,600;14..32,700&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                font-family: 'Inter', -apple-system, sans-serif;
                background: #f4f6f9;
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }}
            .edit-container {{
                background: white;
                border-radius: 28px;
                padding: 40px 44px;
                max-width: 500px;
                width: 100%;
                box-shadow: 0 30px 60px -15px rgba(0,0,0,0.15);
                border: 1px solid #f1f5f9;
            }}
            .edit-header {{
                display: flex;
                align-items: center;
                gap: 16px;
                margin-bottom: 32px;
            }}
            .edit-header i {{
                font-size: 32px;
                color: #6366f1;
                background: #eef2ff;
                padding: 14px;
                border-radius: 16px;
            }}
            .edit-header h1 {{
                font-size: 26px;
                font-weight: 700;
                color: #0f172a;
            }}
            .edit-header h1 span {{ color: #6366f1; }}
            .form-group {{ margin-bottom: 22px; }}
            .form-group label {{
                display: block;
                font-weight: 600;
                font-size: 0.9rem;
                color: #334155;
                margin-bottom: 6px;
            }}
            .form-group label .required {{ color: #ef4444; margin-left: 4px; }}
            .form-group input {{
                width: 100%;
                padding: 12px 16px;
                border: 1.5px solid #e2e8f0;
                border-radius: 12px;
                font-size: 1rem;
                transition: 0.2s;
                font-family: 'Inter', sans-serif;
                background: #f8fafc;
            }}
            .form-group input:focus {{
                outline: none;
                border-color: #6366f1;
                background: white;
                box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.08);
            }}
            .form-actions {{
                display: flex;
                gap: 12px;
                margin-top: 8px;
            }}
            .form-actions .btn {{ flex: 1; justify-content: center; padding: 14px; }}
            .btn {{
                padding: 12px 24px;
                border: none;
                border-radius: 12px;
                font-weight: 600;
                font-size: 0.95rem;
                cursor: pointer;
                transition: all 0.2s;
                display: inline-flex;
                align-items: center;
                gap: 8px;
                font-family: 'Inter', sans-serif;
                text-decoration: none;
                justify-content: center;
            }}
            .btn-success {{
                background: #10b981;
                color: white;
            }}
            .btn-success:hover {{ background: #059669; transform: translateY(-2px); }}
            .btn-outline {{
                background: transparent;
                color: #475569;
                border: 1.5px solid #e2e8f0;
            }}
            .btn-outline:hover {{ background: #f1f5f9; }}
            .loading-state {{
                text-align: center;
                padding: 40px 0;
                color: #64748b;
            }}
            .loading-state i {{ font-size: 32px; margin-bottom: 12px; display: block; }}
            .error-state {{
                text-align: center;
                padding: 40px 0;
                color: #ef4444;
            }}
            .error-state i {{ font-size: 40px; margin-bottom: 12px; display: block; }}
            .hidden {{ display: none; }}
            @media (max-width: 480px) {{
                .edit-container {{ padding: 28px 20px; }}
                .edit-header h1 {{ font-size: 22px; }}
                .form-actions {{ flex-direction: column; }}
            }}
        </style>
    </head>
    <body>
        <div class="edit-container">
            <div class="edit-header">
                <i class="fas fa-pen"></i>
                <h1>Edit <span>Contact</span></h1>
            </div>

            <div id="loading" class="loading-state">
                <i class="fas fa-spinner fa-spin"></i>
                <p>Loading contact...</p>
            </div>

            <div id="error" class="error-state hidden">
                <i class="fas fa-exclamation-circle"></i>
                <p>Contact not found</p>
                <a href="/" class="btn btn-outline" style="margin-top: 16px;">
                    <i class="fas fa-arrow-left"></i> Back to Home
                </a>
            </div>

            <form id="editForm" class="hidden" onsubmit="updateContact(event)">
                <input type="hidden" id="contactId" value="{contact_id}">
                <div class="form-group">
                    <label>Full Name <span class="required">*</span></label>
                    <input type="text" id="name" required placeholder="e.g. John Doe">
                </div>
                <div class="form-group">
                    <label>Phone <span class="required">*</span></label>
                    <input type="tel" id="phone" required placeholder="e.g. +1 234 567 890">
                </div>
                <div class="form-group">
                    <label>Email</label>
                    <input type="email" id="email" placeholder="john@example.com">
                </div>
                <div class="form-group">
                    <label>Address</label>
                    <input type="text" id="address" placeholder="123 Main St, City">
                </div>
                <div class="form-actions">
                    <button type="submit" class="btn btn-success">
                        <i class="fas fa-save"></i> Update Contact
                    </button>
                    <a href="/" class="btn btn-outline">
                        <i class="fas fa-times"></i> Cancel
                    </a>
                </div>
            </form>
        </div>

        <script>
            const contactId = document.getElementById('contactId').value;

            async function loadContact() {{
                try {{
                    const res = await fetch(`/api/contacts/${{contactId}}`);
                    if (!res.ok) throw new Error('Not found');
                    const contact = await res.json();

                    document.getElementById('loading').classList.add('hidden');
                    document.getElementById('editForm').classList.remove('hidden');

                    document.getElementById('name').value = contact.name || '';
                    document.getElementById('phone').value = contact.phone || '';
                    document.getElementById('email').value = contact.email || '';
                    document.getElementById('address').value = contact.address || '';
                }} catch {{
                    document.getElementById('loading').classList.add('hidden');
                    document.getElementById('error').classList.remove('hidden');
                }}
            }}

            async function updateContact(event) {{
                event.preventDefault();
                const data = {{
                    name: document.getElementById('name').value.trim(),
                    phone: document.getElementById('phone').value.trim(),
                    email: document.getElementById('email').value.trim(),
                    address: document.getElementById('address').value.trim()
                }};

                if (!data.name || !data.phone) {{
                    alert('Name and Phone are required.');
                    return;
                }}

                try {{
                    const res = await fetch(`/api/contacts/${{contactId}}`, {{
                        method: 'PUT',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify(data)
                    }});
                    if (res.ok) {{
                        alert('✅ Contact updated successfully!');
                        window.location.href = '/';
                    }} else {{
                        alert('❌ Error updating contact.');
                    }}
                }} catch {{
                    alert('❌ Error updating contact.');
                }}
            }}

            loadContact();
        </script>
    </body>
    </html>
    '''

# --- API Routes ---
@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    return jsonify(load_contacts())

@app.route('/api/contacts', methods=['POST'])
def add_contact():
    data = request.json
    contacts = load_contacts()
    new_contact = {
        'id': str(uuid.uuid4()),
        'name': data.get('name', ''),
        'phone': data.get('phone', ''),
        'email': data.get('email', ''),
        'address': data.get('address', ''),
        'created_at': datetime.now().isoformat()
    }
    contacts.append(new_contact)
    save_contacts(contacts)
    return jsonify(new_contact), 201

@app.route('/api/contacts/<contact_id>', methods=['PUT'])
def update_contact(contact_id):
    data = request.json
    contacts = load_contacts()
    for contact in contacts:
        if contact['id'] == contact_id:
            contact['name'] = data.get('name', contact['name'])
            contact['phone'] = data.get('phone', contact['phone'])
            contact['email'] = data.get('email', contact['email'])
            contact['address'] = data.get('address', contact['address'])
            save_contacts(contacts)
            return jsonify(contact)
    return jsonify({'error': 'Contact not found'}), 404

@app.route('/api/contacts/<contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    contacts = load_contacts()
    contacts = [c for c in contacts if c['id'] != contact_id]
    save_contacts(contacts)
    return jsonify({'message': 'Contact deleted'}), 200

@app.route('/api/contacts/search', methods=['GET'])
def search_contacts():
    query = request.args.get('q', '').lower()
    contacts = load_contacts()
    results = [c for c in contacts if query in c['name'].lower() or query in c['phone']]
    return jsonify(results)

@app.route('/favicon.ico')
def favicon():
    return '', 204

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
