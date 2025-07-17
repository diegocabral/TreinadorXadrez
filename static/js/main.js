// Chess Analyzer Main JavaScript

// Global variables
let analysisEngine = null;

// Initialize application
document.addEventListener('DOMContentLoaded', function() {
    console.log('Chess Analyzer initialized');
    
    // Auto-dismiss alerts after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            if (alert.classList.contains('alert-dismissible')) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        });
    }, 5000);
});

// Utility functions
function formatTime(timestamp) {
    const date = new Date(timestamp);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// Chess utility functions
function fenToPieces(fen) {
    const pieces = {
        'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚', 'p': '♟',
        'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔', 'P': '♙'
    };
    
    const board = fen.split(' ')[0];
    const rows = board.split('/');
    const result = [];
    
    for (let row of rows) {
        const currentRow = [];
        for (let char of row) {
            if (isNaN(char)) {
                currentRow.push(pieces[char] || '');
            } else {
                for (let i = 0; i < parseInt(char); i++) {
                    currentRow.push('');
                }
            }
        }
        result.push(currentRow);
    }
    
    return result;
}

function isLightSquare(row, col) {
    return (row + col) % 2 === 0;
}

// API helper functions
async function makeApiRequest(url, options = {}) {
    try {
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API request failed:', error);
        showNotification('Request failed: ' + error.message, 'danger');
        throw error;
    }
}

// File handling utilities
function validatePgnFile(file) {
    if (!file) return false;
    
    const maxSize = 16 * 1024 * 1024; // 16MB
    if (file.size > maxSize) {
        showNotification('File is too large. Maximum size is 16MB.', 'warning');
        return false;
    }
    
    const allowedTypes = ['.pgn', 'text/plain', 'application/octet-stream'];
    const fileName = file.name.toLowerCase();
    
    if (!fileName.endsWith('.pgn')) {
        showNotification('Please select a valid PGN file.', 'warning');
        return false;
    }
    
    return true;
}

// Export functions for use in other scripts
window.ChessAnalyzer = {
    formatTime,
    showNotification,
    fenToPieces,
    isLightSquare,
    makeApiRequest,
    validatePgnFile
};