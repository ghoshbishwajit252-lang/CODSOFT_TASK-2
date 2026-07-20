from flask import Flask, render_template, request, jsonify, session
import json
import os
from datetime import datetime
import uuid

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# File to store contacts
CONTACTS_FILE = 'contacts.json'

def load_contacts():
    """Load contacts from JSON file"""
    if os.path.exists(CONTACTS_FILE):
        with open(CONTACTS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_contacts(contacts):
    """Save contacts to JSON file"""
    with open(CONTACTS_FILE, 'w') as f:
        json.dump(contacts, f, indent=2)

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    """Get all contacts"""
    contacts = load_contacts()
    return jsonify(contacts)

@app.route('/api/contacts', methods=['POST'])
def add_contact():
    """Add a new contact"""
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
    """Update an existing contact"""
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
    """Delete a contact"""
    contacts = load_contacts()
    contacts = [c for c in contacts if c['id'] != contact_id]
    save_contacts(contacts)
    return jsonify({'message': 'Contact deleted'}), 200

@app.route('/api/contacts/search', methods=['GET'])
def search_contacts():
    """Search contacts by name or phone"""
    query = request.args.get('q', '').lower()
    contacts = load_contacts()
    
    results = [
        c for c in contacts 
        if query in c['name'].lower() or query in c['phone']
    ]
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))