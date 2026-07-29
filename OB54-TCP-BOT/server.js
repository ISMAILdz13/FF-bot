const express = require('express');
const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');
const app = express();
const PORT = 8080;

// Global variables for process management
let botProcess = null;
let isRunning = false;
let outputBuffer = [];
const MAX_OUTPUT_LINES = 1000;

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Serve static files
app.use(express.static(__dirname));

// WebSocket setup for real-time console output
const http = require('http');
const server = http.createServer(app);
const { Server } = require('socket.io');
const io = new Server(server);

// Socket.IO connection
io.on('connection', (socket) => {
    console.log('Client connected via WebSocket');
    
    // Send current status
    socket.emit('status', { isRunning });
    
    // Send existing output buffer
    if (outputBuffer.length > 0) {
        socket.emit('console_output', { data: outputBuffer.join('\n') });
    }
    
    socket.on('disconnect', () => {
        console.log('Client disconnected');
    });
});

// Helper function to add console output
function addConsoleOutput(text) {
    const timestamp = new Date().toLocaleTimeString();
    const output = `[${timestamp}] ${text}`;
    
    outputBuffer.push(output);
    
    // Keep buffer size manageable
    if (outputBuffer.length > MAX_OUTPUT_LINES) {
        outputBuffer = outputBuffer.slice(-MAX_OUTPUT_LINES);
    }
    
    // Broadcast to all connected clients
    io.emit('console_output', { data: output });
}

// Start the bot process
function startBot() {
    if (isRunning) {
        addConsoleOutput('Bot is already running!');
        return false;
    }
    
    try {
        const pythonPath = 'python3'; // or 'python' depending on your system
        const scriptPath = path.join(__dirname, 'main.py');
        
        addConsoleOutput('Starting bot...');
        
        // Spawn the Python process
        botProcess = spawn(pythonPath, [scriptPath], {
            cwd: __dirname,
            stdio: ['pipe', 'pipe', 'pipe']
        });
        
        isRunning = true;
        
        // Handle stdout
        botProcess.stdout.on('data', (data) => {
            const output = data.toString().trim();
            if (output) {
                addConsoleOutput(output);
            }
        });
        
        // Handle stderr
        botProcess.stderr.on('data', (data) => {
            const error = data.toString().trim();
            if (error) {
                addConsoleOutput(`ERROR: ${error}`);
            }
        });
        
        // Handle process exit
        botProcess.on('close', (code) => {
            isRunning = false;
            botProcess = null;
            
            if (code === 0) {
                addConsoleOutput('Bot stopped successfully.');
            } else {
                addConsoleOutput(`Bot stopped with exit code: ${code}`);
            }
            
            // Update all clients
            io.emit('status', { isRunning });
        });
        
        botProcess.on('error', (err) => {
            isRunning = false;
            botProcess = null;
            addConsoleOutput(`Failed to start bot: ${err.message}`);
            io.emit('status', { isRunning });
        });
        
        addConsoleOutput('Bot started successfully!');
        io.emit('status', { isRunning });
        return true;
        
    } catch (error) {
        addConsoleOutput(`Error starting bot: ${error.message}`);
        isRunning = false;
        io.emit('status', { isRunning });
        return false;
    }
}

// Stop the bot gracefully
function stopBot() {
    if (!isRunning || !botProcess) {
        addConsoleOutput('Bot is not running!');
        return false;
    }
    
    addConsoleOutput('Stopping bot...');
    
    // Send SIGINT (Ctrl+C) to allow graceful shutdown
    botProcess.kill('SIGINT');
    
    // Force kill after 5 seconds if still running
    setTimeout(() => {
        if (isRunning && botProcess) {
            addConsoleOutput('Force stopping bot...');
            botProcess.kill('SIGKILL');
        }
    }, 5000);
    
    return true;
}

// Force stop immediately
function forceStopBot() {
    if (!isRunning || !botProcess) {
        addConsoleOutput('Bot is not running!');
        return false;
    }
    
    addConsoleOutput('Force stopping bot immediately...');
    botProcess.kill('SIGKILL');
    return true;
}

// Restart the bot
function restartBot() {
    if (isRunning) {
        addConsoleOutput('Restarting bot...');
        stopBot();
        
        // Wait for process to stop, then start again
        setTimeout(() => {
            startBot();
        }, 2000);
    } else {
        addConsoleOutput('Starting bot...');
        startBot();
    }
}

// API Routes
app.get('/', (req, res) => {
    res.redirect('/web.html');
});

// Get bot status
app.get('/api/status', (req, res) => {
    res.json({ 
        is_running: isRunning,
        uptime: isRunning ? 'Running' : 'Stopped'
    });
});

// Start bot
app.post('/api/start', (req, res) => {
    const success = startBot();
    res.json({ 
        status: success ? 'success' : 'error',
        message: success ? 'Bot started' : 'Failed to start bot'
    });
});

// Stop bot
app.post('/api/stop', (req, res) => {
    const success = stopBot();
    res.json({ 
        status: success ? 'success' : 'error',
        message: success ? 'Bot stopping...' : 'Bot is not running'
    });
});

// Restart bot
app.post('/api/restart', (req, res) => {
    restartBot();
    res.json({ 
        status: 'success',
        message: 'Bot restarting...'
    });
});

// Force stop bot
app.post('/api/force-stop', (req, res) => {
    const success = forceStopBot();
    res.json({ 
        status: success ? 'success' : 'error',
        message: success ? 'Bot force stopped' : 'Bot is not running'
    });
});

// Clear console
app.post('/api/clear-console', (req, res) => {
    outputBuffer = [];
    addConsoleOutput('Console cleared.');
    res.json({ 
        status: 'success',
        message: 'Console cleared'
    });
});

// Auto-restart toggle (placeholder - you can implement this)
app.post('/api/auto-restart', (req, res) => {
    res.json({ 
        status: 'success',
        message: 'Auto-restart toggled',
        auto_restart_enabled: true
    });
});

// API to update black_apis.txt
app.post('/api/update-black-apis', (req, res) => {
    try {
        const { uid, password } = req.body;
        
        if (!uid || !password) {
            return res.status(400).json({ 
                success: false, 
                message: 'UID and password are required' 
            });
        }
        
        if (!/^\d+$/.test(uid)) {
            return res.status(400).json({ 
                success: false, 
                message: 'UID must contain only numbers' 
            });
        }
        
        const content = `uid=${uid}\npassword=${password}`;
        const filePath = path.join(__dirname, 'black_apis.txt');
        
        fs.writeFileSync(filePath, content, 'utf8');
        
        addConsoleOutput(`black_apis.txt updated with UID: ${uid}`);
        
        res.json({ 
            success: true, 
            message: 'black_apis.txt updated successfully',
            content: content
        });
        
    } catch (error) {
        res.status(500).json({ 
            success: false, 
            message: `Error: ${error.message}` 
        });
    }
});

// Get current output
app.get('/api/get-output', (req, res) => {
    res.json({
        success: true,
        output: outputBuffer.join('\n')
    });
});

// Start server
server.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
    console.log(`Bot Control Panel: http://localhost:${PORT}/web.html`);
    console.log(`Current bot status: ${isRunning ? 'Running' : 'Stopped'}`);
    
    // Auto-start bot on server start (optional)
    // startBot();
});