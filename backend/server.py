from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def generate_vigenere_table():
    ascii_chars = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return [ascii_chars[i:] + ascii_chars[:i] for i in range(len(ascii_chars))]

def vigenere_encrypt(message, key):
    ascii_chars = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    table = generate_vigenere_table()
    encrypted_message = ""
    key_index = 0

    for char in message:
        if char in ascii_chars:
            msg_idx = ascii_chars.index(char)
            key_char = key[key_index % len(key)]
            key_idx = ascii_chars.index(key_char)
            encrypted_message += table[key_idx][msg_idx]
            key_index += 1
        else:
            encrypted_message += char  # leave non-ASCII chars unchanged

    return encrypted_message

def vigenere_decrypt(encrypted_message, key):
    ascii_chars = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    table = generate_vigenere_table()
    decrypted_message = ""
    key_index = 0

    for char in encrypted_message:
        if char in ascii_chars:
            key_char = key[key_index % len(key)]
            key_idx = ascii_chars.index(key_char)
            row = table[key_idx]
            msg_idx = row.index(char)
            decrypted_message += ascii_chars[msg_idx]
            key_index += 1
        else:
            decrypted_message += char  # leave non-ASCII chars unchanged

    return decrypted_message

@app.route('/encrypt', methods=['POST'])
def encrypt():
    start_time = datetime.now()
    data = request.get_json()
    message = data.get('message', '')
    key = data.get('key', '')
    
    if not message or not key:
        return jsonify({'error': 'Message and key cannot be empty'}), 400
    
    # Check for invalid key characters
    ascii_chars = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    invalid_chars = [c for c in key if c not in ascii_chars]
    if invalid_chars:
        return jsonify({
            'error': f'Key contains invalid characters: {", ".join(invalid_chars)}',
            'invalid_chars': invalid_chars
        }), 400
    
    encrypted_msg = vigenere_encrypt(message, key)
    
    return jsonify({
        'encrypted_message': encrypted_msg,
        'original_length': len(message),
        'key_length': len(key),
        'process_time': str(datetime.now() - start_time)
    })

@app.route('/decrypt', methods=['POST'])
def decrypt():
    start_time = datetime.now()
    data = request.get_json()
    encrypted_message = data.get('message', '')
    key = data.get('key', '')
    
    if not encrypted_message or not key:
        return jsonify({'error': 'Encrypted message and key cannot be empty'}), 400
    
    # Check for invalid key characters
    ascii_chars = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    invalid_chars = [c for c in key if c not in ascii_chars]
    if invalid_chars:
        return jsonify({
            'error': f'Key contains invalid characters: {", ".join(invalid_chars)}',
            'invalid_chars': invalid_chars
        }), 400
    
    decrypted_msg = vigenere_decrypt(encrypted_message, key)
    
    return jsonify({
        'decrypted_message': decrypted_msg,
        'original_length': len(encrypted_message),
        'key_length': len(key),
        'process_time': str(datetime.now() - start_time)
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)