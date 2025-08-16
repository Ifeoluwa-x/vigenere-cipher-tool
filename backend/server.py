from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import string

app = Flask(__name__)
CORS(app)

# Define our full character set (95 printable ASCII characters)
ascii_chars = ' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~'

def generate_vigenere_table():
    return [ascii_chars[i:] + ascii_chars[:i] for i in range(len(ascii_chars))]

def vigenere_encrypt(message, key):
    table = generate_vigenere_table()
    encrypted_message = []
    key_index = 0
    
    for char in message:
        if char in ascii_chars:
            # Find positions in our character set
            msg_idx = ascii_chars.index(char)
            key_char = key[key_index % len(key)]
            key_idx = ascii_chars.index(key_char)
            # Get encrypted character
            encrypted_char = table[key_idx][msg_idx]
            encrypted_message.append(encrypted_char)
            key_index += 1
        else:
            # Leave unknown characters as-is
            encrypted_message.append(char)
    
    return ''.join(encrypted_message)

def vigenere_decrypt(encrypted_message, key):
    table = generate_vigenere_table()
    decrypted_message = []
    key_index = 0
    
    for char in encrypted_message:
        if char in ascii_chars:
            key_char = key[key_index % len(key)]
            key_idx = ascii_chars.index(key_char)
            row = table[key_idx]
            msg_idx = row.index(char)
            decrypted_char = ascii_chars[msg_idx]
            decrypted_message.append(decrypted_char)
            key_index += 1
        else:
            decrypted_message.append(char)
    
    return ''.join(decrypted_message)

@app.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.get_json()
    message = data.get('message', '')
    key = data.get('key', '')
    
    if not message or not key:
        return jsonify({'error': 'Message and key cannot be empty'}), 400
    
    # Validate key characters
    invalid_chars = [c for c in key if c not in ascii_chars]
    if invalid_chars:
        return jsonify({
            'error': f'Key contains invalid characters: {invalid_chars}',
            'invalid_chars': invalid_chars
        }), 400
    
    encrypted_msg = vigenere_encrypt(message, key)
    
    return jsonify({
        'encrypted_message': encrypted_msg,
        'original_length': len(message),
        'key_length': len(key)
    })

@app.route('/decrypt', methods=['POST'])
def decrypt():
    data = request.get_json()
    encrypted_message = data.get('message', '')
    key = data.get('key', '')
    
    if not encrypted_message or not key:
        return jsonify({'error': 'Encrypted message and key cannot be empty'}), 400
    
    # Validate key characters
    invalid_chars = [c for c in key if c not in ascii_chars]
    if invalid_chars:
        return jsonify({
            'error': f'Key contains invalid characters: {invalid_chars}',
            'invalid_chars': invalid_chars
        }), 400
    
    decrypted_msg = vigenere_decrypt(encrypted_message, key)
    
    return jsonify({
        'decrypted_message': decrypted_msg,
        'original_length': len(encrypted_message),
        'key_length': len(key)
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)