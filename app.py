from flask import Flask, request, jsonify
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

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>📇 Contact Book Pro</title>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            body {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
                position: relative;
                overflow-x: hidden;
            }

            /* Animated background particles */
            body::before {
                content: '';
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: 
                    radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
                    radial-gradient(circle at 80% 20%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
                    radial-gradient(circle at 40% 40%, rgba(120, 119, 198, 0.2) 0%, transparent 50%);
                pointer-events: none;
                z-index: 0;
            }

            .container {
                max-width: 1200px;
                margin: 0 auto;
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(20px);
                border-radius: 30px;
                box-shadow: 0 30px 80px rgba(0, 0, 0, 0.3);
                overflow: hidden;
                padding: 40px;
                position: relative;
                z-index: 1;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }

            /* Header */
            .header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 35px;
                flex-wrap: wrap;
                gap: 20px;
            }

            .header-left {
                display: flex;
                align-items: center;
                gap: 15px;
            }

            .logo-icon {
                width: 55px;
                height: 55px;
                background: linear-gradient(135deg, #667eea, #764ba2);
                border-radius: 16px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 28px;
                color: white;
                box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
            }

            h1 {
                font-size: 2.2rem;
                font-weight: 800;
                background: linear-gradient(135deg, #667eea, #764ba2);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                letter-spacing: -0.5px;
            }

            .header-right {
                display: flex;
                gap: 12px;
                flex-wrap: wrap;
            }

            /* Search Box */
            .search-wrapper {
                position: relative;
                display: flex;
                align-items: center;
            }

            .search-wrapper i {
                position: absolute;
                left: 18px;
                color: #a0aec0;
                font-size: 16px;
                pointer-events: none;
            }

            .search-wrapper input {
                padding: 14px 20px 14px 48px;
                border: 2px solid #e2e8f0;
                border-radius: 14px;
                font-size: 1rem;
                width: 280px;
                transition: all 0.3s;
                background: #f7fafc;
                font-family: 'Inter', sans-serif;
            }

            .search-wrapper input:focus {
                outline: none;
                border-color: #667eea;
                background: white;
                box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
                width: 320px;
            }

            .search-wrapper input::placeholder {
                color: #a0aec0;
            }

            /* Buttons */
            .btn {
                padding: 14px 28px;
                border: none;
                border-radius: 14px;
                font-size: 0.95rem;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                display: inline-flex;
                align-items: center;
                gap: 10px;
                font-family: 'Inter', sans-serif;
                text-decoration: none;
            }

            .btn-primary {
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
            }

            .btn-primary:hover {
                transform: translateY(-3px);
                box-shadow: 0 12px 35px rgba(102, 126, 234, 0.5);
            }

            .btn-primary:active {
                transform: translateY(0px);
            }

            .btn-success {
                background: linear-gradient(135deg, #48bb78, #38a169);
                color: white;
                box-shadow: 0 8px 25px rgba(72, 187, 120, 0.4);
            }

            .btn-success:hover {
                transform: translateY(-3px);
                box-shadow: 0 12px 35px rgba(72, 187, 120, 0.5);
            }

            .btn-danger {
                background: linear-gradient(135deg, #fc8181, #f56565);
                color: white;
                box-shadow: 0 8px 25px rgba(252, 129, 129, 0.3);
            }

            .btn-danger:hover {
                transform: translateY(-3px);
                box-shadow: 0 12px 35px rgba(252, 129, 129, 0.4);
            }

            .btn-secondary {
                background: #e2e8f0;
                color: #4a5568;
            }

            .btn-secondary:hover {
                background: #cbd5e0;
                transform: translateY(-2px);
            }

            .btn-sm {
                padding: 10px 18px;
                font-size: 0.85rem;
            }

            /* Stats Bar */
            .stats-bar {
                display: flex;
                gap: 30px;
                padding: 20px 25px;
                background: linear-gradient(135deg, #f7fafc, #edf2f7);
                border-radius: 16px;
                margin-bottom: 30px;
                flex-wrap: wrap;
            }

            .stat-item {
                display: flex;
                align-items: center;
                gap: 12px;
            }

            .stat-item i {
                font-size: 24px;
                color: #667eea;
            }

            .stat-item .stat-info {
                display: flex;
                flex-direction: column;
            }

            .stat-item .stat-number {
                font-size: 1.5rem;
                font-weight: 700;
                color: #2d3748;
                line-height: 1.2;
            }

            .stat-item .stat-label {
                font-size: 0.85rem;
                color: #718096;
            }

            /* Contact Grid */
            .contacts-grid {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
                gap: 24px;
                margin-top: 10px;
            }

            /* Contact Card */
            .contact-card {
                background: white;
                border-radius: 20px;
                padding: 24px;
                transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
                position: relative;
                border: 1px solid #edf2f7;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
            }

            .contact-card:hover {
                transform: translateY(-8px);
                box-shadow: 0 20px 50px rgba(0, 0, 0, 0.1);
                border-color: #667eea;
            }

            .contact-card .card-header {
                display: flex;
                align-items: center;
                gap: 15px;
                margin-bottom: 15px;
            }

            .contact-card .avatar {
                width: 55px;
                height: 55px;
                background: linear-gradient(135deg, #667eea, #764ba2);
                border-radius: 16px;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-weight: 700;
                font-size: 1.3rem;
                flex-shrink: 0;
                box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
            }

            .contact-card .name {
                font-size: 1.2rem;
                font-weight: 700;
                color: #2d3748;
                flex: 1;
            }

            .contact-card .detail {
                display: flex;
                align-items: center;
                gap: 12px;
                color: #4a5568;
                margin: 10px 0;
                padding: 8px 12px;
                border-radius: 10px;
                transition: background 0.2s;
            }

            .contact-card .detail:hover {
                background: #f7fafc;
            }

            .contact-card .detail i {
                width: 22px;
                color: #667eea;
                font-size: 16px;
            }

            .contact-card .detail span {
                word-break: break-word;
            }

            .contact-card .card-actions {
                margin-top: 18px;
                display: flex;
                gap: 10px;
                border-top: 1px solid #edf2f7;
                padding-top: 18px;
            }

            .contact-card .card-actions .btn {
                flex: 1;
                justify-content: center;
            }

            /* Empty State */
            .empty-state {
                text-align: center;
                padding: 80px 20px;
                color: #a0aec0;
                grid-column: 1 / -1;
            }

            .empty-state i {
                font-size: 5rem;
                margin-bottom: 25px;
                background: linear-gradient(135deg, #667eea, #764ba2);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }

            .empty-state h3 {
                font-size: 1.8rem;
                color: #2d3748;
                margin-bottom: 12px;
                -webkit-text-fill-color: #2d3748;
            }

            .empty-state p {
                color: #718096;
                font-size: 1.1rem;
                margin-bottom: 25px;
            }

            /* Modal */
            .modal {
                display: none;
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.6);
                backdrop-filter: blur(10px);
                justify-content: center;
                align-items: center;
                z-index: 1000;
                animation: fadeIn 0.3s ease;
            }

            .modal.active {
                display: flex;
            }

            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }

            .modal-content {
                background: white;
                padding: 45px;
                border-radius: 30px;
                width: 92%;
                max-width: 520px;
                max-height: 90vh;
                overflow-y: auto;
                animation: slideUp 0.4s cubic-bezier(0.4, 0, 0.2, 1);
                box-shadow: 0 50px 100px rgba(0, 0, 0, 0.3);
            }

            @keyframes slideUp {
                from { transform: translateY(40px) scale(0.98); opacity: 0; }
                to { transform: translateY(0) scale(1); opacity: 1; }
            }

            .modal-content .modal-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 28px;
            }

            .modal-content .modal-header h2 {
                font-size: 1.8rem;
                font-weight: 700;
                color: #2d3748;
                background: linear-gradient(135deg, #667eea, #764ba2);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }

            .modal-close {
                width: 40px;
                height: 40px;
                border: none;
                background: #f7fafc;
                border-radius: 12px;
                font-size: 1.2rem;
                cursor: pointer;
                transition: all 0.2s;
                color: #4a5568;
                display: flex;
                align-items: center;
                justify-content: center;
            }

            .modal-close:hover {
                background: #fc8181;
                color: white;
                transform: rotate(90deg);
            }

            .form-group {
                margin-bottom: 22px;
            }

            .form-group label {
                display: block;
                margin-bottom: 8px;
                font-weight: 600;
                color: #4a5568;
                font-size: 0.95rem;
            }

            .form-group label .required {
                color: #fc8181;
                margin-left: 4px;
            }

            .form-group input {
                width: 100%;
                padding: 14px 18px;
                border: 2px solid #e2e8f0;
                border-radius: 14px;
                font-size: 1rem;
                transition: all 0.3s;
                font-family: 'Inter', sans-serif;
                background: #f7fafc;
            }

            .form-group input:focus {
                outline: none;
                border-color: #667eea;
                background: white;
                box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
            }

            .form-group input::placeholder {
                color: #a0aec0;
            }

            .form-actions {
                display: flex;
                gap: 12px;
                margin-top: 30px;
            }

            .form-actions .btn {
                flex: 1;
                justify-content: center;
            }

            /* Toast */
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
                padding: 16px 24px;
                border-radius: 16px;
                color: white;
                font-weight: 500;
                font-family: 'Inter', sans-serif;
                box-shadow: 0 15px 40px rgba(0, 0, 0, 0.2);
                transform: translateX(400px);
                opacity: 0;
                transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
                display: flex;
                align-items: center;
                gap: 12px;
                font-size: 0.95rem;
                min-width: 280px;
            }

            .toast.show {
                transform: translateX(0);
                opacity: 1;
            }

            .toast.success {
                background: linear-gradient(135deg, #48bb78, #38a169);
            }

            .toast.error {
                background: linear-gradient(135deg, #fc8181, #f56565);
            }

            .toast i {
                font-size: 1.2rem;
            }

            /* Loading Spinner */
            .spinner {
                display: inline-block;
                width: 20px;
                height: 20px;
                border: 3px solid rgba(255, 255, 255, 0.3);
                border-radius: 50%;
                border-top-color: white;
                animation: spin 0.8s linear infinite;
            }

            @keyframes spin {
                to { transform: rotate(360deg); }
            }

            /* Scrollbar */
            ::-webkit-scrollbar {
                width: 8px;
            }

            ::-webkit-scrollbar-track {
                background: #f7fafc;
                border-radius: 10px;
            }

            ::-webkit-scrollbar-thumb {
                background: #667eea;
                border-radius: 10px;
            }

            ::-webkit-scrollbar-thumb:hover {
                background: #764ba2;
            }

            /* Responsive */
            @media (max-width: 768px) {
                .container {
                    padding: 20px;
                    border-radius: 20px;
                }

                h1 {
                    font-size: 1.6rem;
                }

                .logo-icon {
                    width: 45px;
                    height: 45px;
                    font-size: 22px;
                }

                .header {
                    flex-direction: column;
                    align-items: stretch;
                    gap: 15px;
                }

                .search-wrapper input {
                    width: 100%;
                }

                .search-wrapper input:focus {
                    width: 100%;
                }

                .header-right {
                    flex-direction: column;
                }

                .stats-bar {
                    flex-direction: column;
                    gap: 15px;
                    padding: 15px 20px;
                }

                .contacts-grid {
                    grid-template-columns: 1fr;
                }

                .modal-content {
                    padding: 28px;
                    width: 95%;
                }

                .form-actions {
                    flex-direction: column;
                }

                .toast {
                    min-width: auto;
                    width: calc(100% - 40px);
                }

                .toast-container {
                    right: 20px;
                    bottom: 20px;
                    left: 20px;
                }
            }

            @media (max-width: 480px) {
                body {
                    padding: 10px;
                }

                .container {
                    padding: 15px;
                }

                h1 {
                    font-size: 1.3rem;
                }

                .contact-card {
                    padding: 18px;
                }
            }

            /* Dark mode support */
            @media (prefers-color-scheme: dark) {
                .container {
                    background: rgba(26, 32, 44, 0.95);
                }

                .contact-card {
                    background: #2d3748;
                    border-color: #4a5568;
                }

                .contact-card .name {
                    color: #e2e8f0;
                }

                .contact-card .detail {
                    color: #cbd5e0;
                }

                .contact-card .detail:hover {
                    background: #4a5568;
                }

                .stats-bar {
                    background: #2d3748;
                }

                .stat-item .stat-number {
                    color: #e2e8f0;
                }

                .stat-item .stat-label {
                    color: #a0aec0;
                }

                .search-wrapper input {
                    background: #2d3748;
                    border-color: #4a5568;
                    color: #e2e8f0;
                }

                .search-wrapper input:focus {
                    background: #2d3748;
                    border-color: #667eea;
                }

                .modal-content {
                    background: #2d3748;
                }

                .modal-content .modal-header h2 {
                    -webkit-text-fill-color: #e2e8f0;
                }

                .form-group label {
                    color: #cbd5e0;
                }

                .form-group input {
                    background: #1a202c;
                    border-color: #4a5568;
                    color: #e2e8f0;
                }

                .form-group input:focus {
                    background: #1a202c;
                }

                .modal-close {
                    background: #4a5568;
                    color: #cbd5e0;
                }

                .modal-close:hover {
                    background: #fc8181;
                    color: white;
                }

                .btn-secondary {
                    background: #4a5568;
                    color: #cbd5e0;
                }

                .btn-secondary:hover {
                    background: #718096;
                }

                .empty-state h3 {
                    -webkit-text-fill-color: #e2e8f0;
                }

                .empty-state p {
                    color: #a0aec0;
                }

                .contact-card .card-actions {
                    border-top-color: #4a5568;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <!-- Header -->
            <div class="header">
                <div class="header-left">
                    <div class="logo-icon">📇</div>
                    <h1>Contact Book</h1>
                </div>
                <div class="header-right">
                    <div class="search-wrapper">
                        <i class="fas fa-search"></i>
                        <input type="text" id="searchInput" placeholder="Search contacts..." oninput="searchContacts()">
                    </div>
                    <button class="btn btn-primary" onclick="openAddModal()">
                        <i class="fas fa-plus"></i> Add Contact
                    </button>
                </div>
            </div>

            <!-- Stats -->
            <div class="stats-bar" id="statsBar">
                <div class="stat-item">
                    <i class="fas fa-users"></i>
                    <div class="stat-info">
                        <span class="stat-number" id="totalContacts">0</span>
                        <span class="stat-label">Total Contacts</span>
                    </div>
                </div>
                <div class="stat-item">
                    <i class="fas fa-phone"></i>
                    <div class="stat-info">
                        <span class="stat-number" id="phoneCount">0</span>
                        <span class="stat-label">With Phone</span>
                    </div>
                </div>
                <div class="stat-item">
                    <i class="fas fa-envelope"></i>
                    <div class="stat-info">
                        <span class="stat-number" id="emailCount">0</span>
                        <span class="stat-label">With Email</span>
                    </div>
                </div>
            </div>

            <!-- Contacts Grid -->
            <div class="contacts-grid" id="contactsGrid"></div>
        </div>

        <!-- Modal -->
        <div class="modal" id="contactModal">
            <div class="modal-content">
                <div class="modal-header">
                    <h2 id="modalTitle">Add New Contact</h2>
                    <button class="modal-close" onclick="closeModal()">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
                <form id="contactForm" onsubmit="saveContact(event)">
                    <input type="hidden" id="contactId">
                    <div class="form-group">
                        <label>Full Name <span class="required">*</span></label>
                        <input type="text" id="name" required placeholder="Enter full name">
                    </div>
                    <div class="form-group">
                        <label>Phone Number <span class="required">*</span></label>
                        <input type="tel" id="phone" required placeholder="Enter phone number">
                    </div>
                    <div class="form-group">
                        <label>Email Address</label>
                        <input type="email" id="email" placeholder="Enter email address">
                    </div>
                    <div class="form-group">
                        <label>Address</label>
                        <input type="text" id="address" placeholder="Enter address">
                    </div>
                    <div class="form-actions">
                        <button type="submit" class="btn btn-success" id="saveBtn">
                            <i class="fas fa-save"></i> <span id="saveBtnText">Save Contact</span>
                        </button>
                        <button type="button" class="btn btn-secondary" onclick="closeModal()">
                            Cancel
                        </button>
                    </div>
                </form>
            </div>
        </div>

        <!-- Toast Container -->
        <div class="toast-container" id="toastContainer"></div>

        <script>
        // State
        let contacts = [];
        let editingId = null;
        let isSubmitting = false;

        // Load contacts on page load
        document.addEventListener('DOMContentLoaded', loadContacts);

        // Load contacts from API
        async function loadContacts() {
            try {
                const response = await fetch('/api/contacts');
                contacts = await response.json();
                renderContacts(contacts);
                updateStats(contacts);
            } catch (error) {
                showToast('Error loading contacts', 'error');
            }
        }

        // Render contacts
        function renderContacts(contactsList) {
            const grid = document.getElementById('contactsGrid');
            
            if (contactsList.length === 0) {
                grid.innerHTML = `
                    <div class="empty-state">
                        <i class="fas fa-address-book"></i>
                        <h3>No Contacts Yet</h3>
                        <p>Start building your contact list by adding your first contact!</p>
                        <button class="btn btn-primary" onclick="openAddModal()">
                            <i class="fas fa-plus"></i> Add Your First Contact
                        </button>
                    </div>
                `;
                return;
            }

            grid.innerHTML = contactsList.map(contact => `
                <div class="contact-card">
                    <div class="card-header">
                        <div class="avatar">${getInitials(contact.name)}</div>
                        <div class="name">${escapeHtml(contact.name)}</div>
                    </div>
                    <div class="detail">
                        <i class="fas fa-phone"></i>
                        <span>${escapeHtml(contact.phone)}</span>
                    </div>
                    ${contact.email ? `
                        <div class="detail">
                            <i class="fas fa-envelope"></i>
                            <span>${escapeHtml(contact.email)}</span>
                        </div>
                    ` : ''}
                    ${contact.address ? `
                        <div class="detail">
                            <i class="fas fa-map-marker-alt"></i>
                            <span>${escapeHtml(contact.address)}</span>
                        </div>
                    ` : ''}
                    <div class="card-actions">
                        <button class="btn btn-primary btn-sm" onclick="editContact('${contact.id}')">
                            <i class="fas fa-edit"></i> Edit
                        </button>
                        <button class="btn btn-danger btn-sm" onclick="deleteContact('${contact.id}')">
                            <i class="fas fa-trash"></i> Delete
                        </button>
                    </div>
                </div>
            `).join('');
        }

        // Update stats
        function updateStats(contactsList) {
            document.getElementById('totalContacts').textContent = contactsList.length;
            document.getElementById('phoneCount').textContent = contactsList.filter(c => c.phone).length;
            document.getElementById('emailCount').textContent = contactsList.filter(c => c.email).length;
        }

        // Get initials for avatar
        function getInitials(name) {
            if (!name) return '?';
            const parts = name.trim().split(' ');
            if (parts.length === 1) return parts[0].charAt(0).toUpperCase();
            return (parts[0].charAt(0) + parts[parts.length - 1].charAt(0)).toUpperCase();
        }

        // Search contacts
        async function searchContacts() {
            const query = document.getElementById('searchInput').value.trim();
            
            if (!query) {
                renderContacts(contacts);
                updateStats(contacts);
                return;
            }

            try {
                const response = await fetch(`/api/contacts/search?q=${encodeURIComponent(query)}`);
                const results = await response.json();
                renderContacts(results);
                updateStats(results);
            } catch (error) {
                showToast('Error searching contacts', 'error');
            }
        }

        // Open add modal
        function openAddModal() {
            editingId = null;
            document.getElementById('modalTitle').textContent = 'Add New Contact';
            document.getElementById('contactForm').reset();
            document.getElementById('contactId').value = '';
            document.getElementById('saveBtnText').textContent = 'Save Contact';
            document.getElementById('contactModal').classList.add('active');
            document.body.style.overflow = 'hidden';
            // Focus on first input
            setTimeout(() => document.getElementById('name').focus(), 100);
        }

        // Edit contact
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
            document.getElementById('saveBtnText').textContent = 'Update Contact';
            document.getElementById('contactModal').classList.add('active');
            document.body.style.overflow = 'hidden';
            setTimeout(() => document.getElementById('name').focus(), 100);
        }

        // Save contact - FIXED FORM SUBMISSION
        async function saveContact(event) {
            event.preventDefault(); // Prevent default form submission
            
            if (isSubmitting) return;
            isSubmitting = true;
            
            const saveBtn = document.getElementById('saveBtn');
            const originalText = saveBtn.innerHTML;
            saveBtn.innerHTML = '<span class="spinner"></span> Saving...';
            saveBtn.disabled = true;

            const id = document.getElementById('contactId').value;
            const data = {
                name: document.getElementById('name').value.trim(),
                phone: document.getElementById('phone').value.trim(),
                email: document.getElementById('email').value.trim(),
                address: document.getElementById('address').value.trim()
            };

            // Validate
            if (!data.name || !data.phone) {
                showToast('Please fill in all required fields', 'error');
                saveBtn.innerHTML = originalText;
                saveBtn.disabled = false;
                isSubmitting = false;
                return;
            }

            try {
                let response;
                let url = '/api/contacts';
                let method = 'POST';
                
                if (id) {
                    url = `/api/contacts/${id}`;
                    method = 'PUT';
                }

                response = await fetch(url, {
                    method: method,
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });

                if (response.ok) {
                    closeModal();
                    await loadContacts();
                    showToast(id ? 'Contact updated successfully! ✨' : 'Contact added successfully! 🎉');
                } else {
                    const error = await response.json();
                    showToast(error.error || 'Error saving contact', 'error');
                }
            } catch (error) {
                showToast('Error saving contact. Please try again.', 'error');
            } finally {
                saveBtn.innerHTML = originalText;
                saveBtn.disabled = false;
                isSubmitting = false;
            }
        }

        // Delete contact
        async function deleteContact(id) {
            const contact = contacts.find(c => c.id === id);
            if (!contact) return;

            if (!confirm(`Are you sure you want to delete "${contact.name}"?`)) return;

            try {
                const response = await fetch(`/api/contacts/${id}`, {
                    method: 'DELETE'
                });

                if (response.ok) {
                    await loadContacts();
                    showToast('Contact deleted successfully! 🗑️');
                } else {
                    showToast('Error deleting contact', 'error');
                }
            } catch (error) {
                showToast('Error deleting contact', 'error');
            }
        }

        // Close modal
        function closeModal() {
            document.getElementById('contactModal').classList.remove('active');
            document.body.style.overflow = '';
            // Reset form state
            const saveBtn = document.getElementById('saveBtn');
            saveBtn.innerHTML = '<i class="fas fa-save"></i> <span id="saveBtnText">Save Contact</span>';
            saveBtn.disabled = false;
            isSubmitting = false;
        }

        // Show toast notification
        function showToast(message, type = 'success') {
            const container = document.getElementById('toastContainer');
            const toast = document.createElement('div');
            const icon = type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle';
            toast.className = `toast ${type}`;
            toast.innerHTML = `<i class="fas ${icon}"></i> ${message}`;
            container.appendChild(toast);

            // Trigger show animation
            setTimeout(() => toast.classList.add('show'), 10);

            // Auto remove after 3.5 seconds
            setTimeout(() => {
                toast.classList.remove('show');
                setTimeout(() => toast.remove(), 400);
            }, 3500);
        }

        // Escape HTML to prevent XSS
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }

        // Close modal on click outside
        document.getElementById('contactModal').addEventListener('click', function(e) {
            if (e.target === this) {
                closeModal();
            }
        });

        // Close modal on escape key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                closeModal();
            }
        });

        // Handle Enter key in search
        document.getElementById('searchInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                searchContacts();
            }
        });
        </script>
    </body>
    </html>
    '''

@app.route('/favicon.ico')
def favicon():
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
             <rect width="100" height="100" rx="15" fill="#667eea"/>
             <text x="50" y="68" font-size="55" text-anchor="middle" fill="white">📇</text>
             </svg>'''
    return svg, 200, {'Content-Type': 'image/svg+xml'}

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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
