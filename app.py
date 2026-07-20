# Add this with your other routes
@app.route('/edit/<contact_id>')
def edit_contact_page(contact_id):
    """Direct edit page for contacts"""
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Edit Contact</title>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #667eea, #764ba2);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                margin: 0;
                padding: 20px;
            }}
            .container {{
                background: white;
                padding: 40px;
                border-radius: 20px;
                max-width: 500px;
                width: 100%;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            }}
            h2 {{ color: #2d3748; margin-bottom: 25px; text-align: center; }}
            .form-group {{ margin-bottom: 20px; }}
            .form-group label {{ display: block; margin-bottom: 8px; font-weight: 600; color: #4a5568; }}
            .form-group input {{
                width: 100%;
                padding: 12px;
                border: 2px solid #e2e8f0;
                border-radius: 10px;
                font-size: 1rem;
                box-sizing: border-box;
            }}
            .form-group input:focus {{ outline: none; border-color: #667eea; }}
            .btn {{
                padding: 12px 24px;
                border: none;
                border-radius: 10px;
                font-weight: 600;
                cursor: pointer;
                font-size: 1rem;
                width: 100%;
                margin-top: 10px;
            }}
            .btn-primary {{ background: #667eea; color: white; }}
            .btn-primary:hover {{ background: #5a67d8; }}
            .btn-secondary {{ background: #e2e8f0; color: #4a5568; }}
            .btn-secondary:hover {{ background: #cbd5e0; }}
            .loading {{ text-align: center; color: #718096; padding: 20px; }}
            .error {{ color: #fc8181; text-align: center; padding: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2><i class="fas fa-edit" style="color: #667eea;"></i> Edit Contact</h2>
            <div id="loading" class="loading">
                <i class="fas fa-spinner fa-spin"></i> Loading contact...
            </div>
            <div id="error" class="error" style="display:none;">
                <i class="fas fa-exclamation-circle"></i> Contact not found
            </div>
            <form id="editForm" style="display:none;" onsubmit="updateContact(event)">
                <input type="hidden" id="contactId" value="{contact_id}">
                <div class="form-group">
                    <label>Name *</label>
                    <input type="text" id="name" required>
                </div>
                <div class="form-group">
                    <label>Phone *</label>
                    <input type="tel" id="phone" required>
                </div>
                <div class="form-group">
                    <label>Email</label>
                    <input type="email" id="email">
                </div>
                <div class="form-group">
                    <label>Address</label>
                    <input type="text" id="address">
                </div>
                <button type="submit" class="btn btn-primary">
                    <i class="fas fa-save"></i> Update Contact
                </button>
                <button type="button" class="btn btn-secondary" onclick="window.location.href='/'">
                    <i class="fas fa-arrow-left"></i> Back to Contacts
                </button>
            </form>
        </div>

        <script>
            const contactId = document.getElementById('contactId').value;
            
            async function loadContact() {{
                try {{
                    const response = await fetch(`/api/contacts/${{contactId}}`);
                    if (!response.ok) throw new Error('Contact not found');
                    const contact = await response.json();
                    
                    document.getElementById('loading').style.display = 'none';
                    document.getElementById('editForm').style.display = 'block';
                    
                    document.getElementById('name').value = contact.name || '';
                    document.getElementById('phone').value = contact.phone || '';
                    document.getElementById('email').value = contact.email || '';
                    document.getElementById('address').value = contact.address || '';
                }} catch (error) {{
                    document.getElementById('loading').style.display = 'none';
                    document.getElementById('error').style.display = 'block';
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
                    alert('Please fill in all required fields');
                    return;
                }}

                try {{
                    const response = await fetch(`/api/contacts/${{contactId}}`, {{
                        method: 'PUT',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify(data)
                    }});

                    if (response.ok) {{
                        alert('✅ Contact updated successfully!');
                        window.location.href = '/';
                    }} else {{
                        alert('❌ Error updating contact');
                    }}
                }} catch (error) {{
                    alert('❌ Error updating contact');
                }}
            }}

            loadContact();
        </script>
    </body>
    </html>
    '''
