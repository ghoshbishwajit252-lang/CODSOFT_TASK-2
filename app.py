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
    <html>
    <head>
        <title>Contact Book</title>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            body { font-family: Arial; background: linear-gradient(135deg, #667eea, #764ba2); min-height: 100vh; padding: 20px; margin: 0; }
            .container { max-width: 1200px; margin: 0 auto; background: white; border-radius: 20px; padding: 30px; }
            h1 { color: #333; display: flex; align-items: center; gap: 10px; }
            h1 i { color: #667eea; }
            .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; flex-wrap: wrap; }
            .btn { padding: 12px 24px; border: none; border-radius: 10px; font-size: 1rem; cursor: pointer; }
            .btn-primary { background: #667eea; color: white; }
            .btn-primary:hover { background: #5a67d8; }
            .btn-danger { background: #fc8181; color: white; }
            .btn-danger:hover { background: #f56565; }
            .search-box { display: flex; gap: 10px; flex-wrap: wrap; }
            .search-box input { padding: 12px 20px; border: 2px solid #e0e0e0; border-radius: 10px; font-size: 1rem; width: 250px; }
            .contacts-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; margin-top: 20px; }
            .contact-card { background: #f7fafc; border-radius: 15px; padding: 20px; }
            .contact-card .name { font-size: 1.25rem; font-weight: 600; color: #2d3748; }
            .contact-card .detail { display: flex; align-items: center; gap: 10px; color: #4a5568; margin: 8px 0; }
            .contact-card .detail i { width: 20px; color: #667eea; }
            .contact-card .actions { margin-top: 15px; display: flex; gap: 10px; }
            .contact-card .actions .btn { padding: 8px 16px; font-size: 0.9rem; }
            .modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); justify-content: center; align-items: center; z-index: 1000; }
            .modal.active { display: flex; }
            .modal-content { background: white; padding: 40px; border-radius: 20px; width: 90%; max-width: 500px; }
            .form-group { margin-bottom: 20px; }
            .form-group label { display: block; margin-bottom: 8px; font-weight: 600; }
            .form-group input { width: 100%; padding: 12px; border: 2px solid #e0e0e0; border-radius: 10px; font-size: 1rem; }
            .form-actions { display: flex; gap: 10px; margin-top: 20px; }
            .empty-state { text-align: center; padding: 60px 20px; color: #a0aec0; }
            .toast { position: fixed; bottom: 30px; right: 30px; background: #48bb78; color: white; padding: 15px 25px; border-radius: 10px; display: none; }
            .toast.show { display: block; }
            .toast.error { background: #fc8181; }
            @media (max-width: 768px) { .header { flex-direction: column; gap: 15px; } .search-box input { width: 100%; } .contacts-grid { grid-template-columns: 1fr; } }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1><i class="fas fa-address-book"></i> Contact Book</h1>
                <div class="search-box">
                    <input type="text" id="searchInput" placeholder="Search contacts..." oninput="searchContacts()">
                    <button class="btn btn-primary" onclick="openAddModal()"><i class="fas fa-plus"></i> Add Contact</button>
                </div>
            </div>
            <div class="contacts-grid" id="contactsGrid"></div>
        </div>

        <div class="modal" id="contactModal">
            <div class="modal-content">
                <h2 id="modalTitle">Add Contact</h2>
                <form id="contactForm" onsubmit="saveContact(event)">
                    <input type="hidden" id="contactId">
                    <div class="form-group"><label>Name *</label><input type="text" id="name" required></div>
                    <div class="form-group"><label>Phone *</label><input type="tel" id="phone" required></div>
                    <div class="form-group"><label>Email</label><input type="email" id="email"></div>
                    <div class="form-group"><label>Address</label><input type="text" id="address"></div>
                    <div class="form-actions">
                        <button type="submit" class="btn btn-primary"><i class="fas fa-save"></i> Save</button>
                        <button type="button" class="btn btn-secondary" onclick="closeModal()">Cancel</button>
                    </div>
                </form>
            </div>
        </div>

        <div class="toast" id="toast"></div>

        <script>
        let contacts = [];
        let editingId = null;
        document.addEventListener('DOMContentLoaded', loadContacts);

        async function loadContacts() {
            try {
                const response = await fetch('/api/contacts');
                contacts = await response.json();
                renderContacts(contacts);
            } catch (error) {
                showToast('Error loading contacts', 'error');
            }
        }

        function renderContacts(contactsList) {
            const grid = document.getElementById('contactsGrid');
            if (contactsList.length === 0) {
                grid.innerHTML = '<div class="empty-state"><i class="fas fa-address-book" style="font-size:4rem"></i><h3>No contacts found</h3><button class="btn btn-primary" onclick="openAddModal()">Add Contact</button></div>';
                return;
            }
            grid.innerHTML = contactsList.map(contact => `
                <div class="contact-card">
                    <div class="name">${contact.name}</div>
                    <div class="detail"><i class="fas fa-phone"></i> ${contact.phone}</div>
                    ${contact.email ? `<div class="detail"><i class="fas fa-envelope"></i> ${contact.email}</div>` : ''}
                    ${contact.address ? `<div class="detail"><i class="fas fa-map-marker-alt"></i> ${contact.address}</div>` : ''}
                    <div class="actions">
                        <button class="btn btn-primary" onclick="editContact('${contact.id}')"><i class="fas fa-edit"></i> Edit</button>
                        <button class="btn btn-danger" onclick="deleteContact('${contact.id}')"><i class="fas fa-trash"></i> Delete</button>
                    </div>
                </div>
            `).join('');
        }

        async function searchContacts() {
            const query = document.getElementById('searchInput').value.trim();
            if (!query) { renderContacts(contacts); return; }
            try {
                const response = await fetch(`/api/contacts/search?q=${encodeURIComponent(query)}`);
                const results = await response.json();
                renderContacts(results);
            } catch (error) {
                showToast('Error searching contacts', 'error');
            }
        }

        function openAddModal() {
            editingId = null;
            document.getElementById('modalTitle').textContent = 'Add Contact';
            document.getElementById('contactForm').reset();
            document.getElementById('contactId').value = '';
            document.getElementById('contactModal').classList.add('active');
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
            document.getElementById('contactModal').classList.add('active');
        }

        async function saveContact(event) {
            event.preventDefault();
            const id = document.getElementById('contactId').value;
            const data = {
                name: document.getElementById('name').value,
                phone: document.getElementById('phone').value,
                email: document.getElementById('email').value,
                address: document.getElementById('address').value
            };
            try {
                let response;
                if (id) {
                    response = await fetch(`/api/contacts/${id}`, {
                        method: 'PUT',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(data)
                    });
                } else {
                    response = await fetch('/api/contacts', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(data)
                    });
                }
                if (response.ok) {
                    closeModal();
                    await loadContacts();
                    showToast(id ? 'Contact updated!' : 'Contact added!');
                } else {
                    showToast('Error saving contact', 'error');
                }
            } catch (error) {
                showToast('Error saving contact', 'error');
            }
        }

        async function deleteContact(id) {
            if (!confirm('Delete this contact?')) return;
            try {
                const response = await fetch(`/api/contacts/${id}`, { method: 'DELETE' });
                if (response.ok) {
                    await loadContacts();
                    showToast('Contact deleted!');
                } else {
                    showToast('Error deleting contact', 'error');
                }
            } catch (error) {
                showToast('Error deleting contact', 'error');
            }
        }

        function closeModal() {
            document.getElementById('contactModal').classList.remove('active');
        }

        function showToast(message, type = 'success') {
            const toast = document.getElementById('toast');
            toast.textContent = message;
            toast.className = 'toast show';
            if (type === 'error') toast.classList.add('error');
            setTimeout(() => toast.classList.remove('show'), 3000);
        }

        document.getElementById('contactModal').addEventListener('click', function(e) {
            if (e.target === this) closeModal();
        });
        </script>
    </body>
    </html>
    '''

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
            contact.update(data)
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
    app.run(host='0.0.0.0', port=port, debug=True)
