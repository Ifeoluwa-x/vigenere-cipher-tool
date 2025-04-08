import React, { useState, useEffect } from 'react';
import './App.css';

const VigenereCipher = () => {
  const [message, setMessage] = useState('');
  const [key, setKey] = useState('');
  const [encrypted, setEncrypted] = useState('');
  const [decrypted, setDecrypted] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [mode, setMode] = useState('encrypt'); // 'encrypt' or 'decrypt'
  const [error, setError] = useState('');
  const [processTime, setProcessTime] = useState(null);

  useEffect(() => {
    let interval;
    if (isLoading) {
      interval = setInterval(() => {
        setProgress(prev => {
          if (prev >= 100) {
            clearInterval(interval);
            return 100;
          }
          return prev + Math.floor(Math.random() * 10) + 5;
        });
      }, 200);
    }
    return () => clearInterval(interval);
  }, [isLoading]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setProgress(0);
    setError('');
    setProcessTime(null);
    const startTime = new Date();

    try {
      const endpoint = mode === 'encrypt' ? '/encrypt' : '/decrypt';
      const response = await fetch(`https://vigenere-cipher-tool.onrender.com${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message, key }),
      });

      if (!response.ok) {
        throw new Error(await response.text());
      }

      const data = await response.json();
      if (mode === 'encrypt') {
        setEncrypted(data.encrypted_message);
        setDecrypted('');
      } else {
        setDecrypted(data.decrypted_message);
        setEncrypted('');
      }
      
      const endTime = new Date();
      setProcessTime({
        start: startTime.toLocaleString(),
        end: endTime.toLocaleString(),
        duration: `${endTime - startTime}ms`
      });
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text)
      .then(() => {
        alert('Copied to clipboard!');
      })
      .catch(err => {
        console.error('Failed to copy: ', err);
      });
  };

  const toggleMode = () => {
    setMode(mode === 'encrypt' ? 'decrypt' : 'encrypt');
    setEncrypted('');
    setDecrypted('');
    setError('');
  };

  return (
    <div className="cyber-terminal">
      <div className="scanlines"></div>
      <div className="terminal-header">
        <div className="terminal-dots">
          <div className="dot dot-red"></div>
          <div className="dot dot-yellow"></div>
          <div className="dot dot-green"></div>
        </div>
        <div>VIGENÈRE TERMINAL v3.56.0</div>
        <div className="terminal-dots" style={{ visibility: 'hidden' }}>
          <div className="dot"></div>
          <div className="dot"></div>
          <div className="dot"></div>
        </div>
      </div>
      
      <h1>NEON VIGENÈRE {mode.toUpperCase()}</h1>
      
      <div className="mode-toggle">
        <button 
          onClick={toggleMode}
          className={`toggle-btn ${mode === 'encrypt' ? 'active' : ''}`}
        >
          ENCRYPT
        </button>
        <button 
          onClick={toggleMode}
          className={`toggle-btn ${mode === 'decrypt' ? 'active' : ''}`}
        >
          DECRYPT
        </button>
      </div>
      
      <form onSubmit={handleSubmit}>
        <div className="input-group">
          <label htmlFor="message">
            {mode === 'encrypt' ? 'MESSAGE TO ENCRYPT:' : 'MESSAGE TO DECRYPT:'}
          </label>
          <textarea 
            id="message" 
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            required 
            placeholder={mode === 'encrypt' 
              ? "Enter your classified message here..." 
              : "Enter your encrypted message here..."}
          />
        </div>
        <div className="input-group">
          <label htmlFor="key">VIGENÈRE CIPHER KEY:</label>
          <input 
            type="text" 
            id="key" 
            value={key}
            onChange={(e) => setKey(e.target.value)}
            required 
            placeholder="Enter your encryption key (letters and numbers only)"
          />
        </div>
        
        {isLoading && (
          <div className="progress-container">
            <div className="progress-bar" style={{ width: `${progress}%` }}>
              <span className="progress-text">{progress}%</span>
            </div>
          </div>
        )}
        
        <button type="submit" className="cyber-button" disabled={isLoading}>
          {isLoading 
            ? `${mode === 'encrypt' ? 'ENCRYPTING' : 'DECRYPTING'}...` 
            : `INITIATE ${mode === 'encrypt' ? 'ENCRYPTION' : 'DECRYPTION'} SEQUENCE`}
        </button>
      </form>
      
      {error && <div className="error-message">{error}</div>}
      
      {(encrypted || decrypted) && (
        <div id="result">
          <h3>{mode === 'encrypt' ? 'ENCRYPTION COMPLETE:' : 'DECRYPTION COMPLETE:'}</h3>
          
          <div className="process-info">
            <p><strong>Original Length:</strong> {message.length} characters</p>
            <p><strong>Key Length:</strong> {key.length} characters</p>
            {processTime && (
              <>
                <p><strong>Process Started:</strong> {processTime.start}</p>
                <p><strong>Process Completed:</strong> {processTime.end}</p>
                <p><strong>Processing Time:</strong> {processTime.duration}</p>
              </>
            )}
          </div>
          
          <div className="warning-message">
            <span className="warning-icon">⚠️</span>
            WARNING: Without the exact key, this message cannot be {mode === 'encrypt' ? 'decrypted' : 'verified'}!
          </div>
          
          <div className="output-container">
            <p className="output-label">
              {mode === 'encrypt' ? 'ENCRYPTED MESSAGE:' : 'DECRYPTED MESSAGE:'}
            </p>
            <div id="outputContent" className="output-content">
              {mode === 'encrypt' ? encrypted : decrypted}
            </div>
            <button 
              className="copy-btn" 
              onClick={() => copyToClipboard(mode === 'encrypt' ? encrypted : decrypted)}
            >
              COPY TO CLIPBOARD
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default VigenereCipher;