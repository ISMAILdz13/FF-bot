"""JavaScript Upload Module

Handles client-side file upload, validation, and result rendering.
Injected into templates for interactive functionality.

Note: This is a server-side comment block. The actual JS is in static/js/upload.js
"""

// This file is included in templates via:
// <script src="{{ url_for('static', filename='js/upload.js') }}"></script>
// 
// Provides:
// - uploadFile()
// - handleFileSelect()
// - resetUpload()
// - showError(message)
// - showSuccess(message)
// - copyToClipboard()
