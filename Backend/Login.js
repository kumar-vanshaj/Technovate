// auth-server.js
const express = require('express');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const path = require('path');
const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser');

const app = express();
const PORT = process.env.PORT || 3000;
const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key'; // Use environment variable in production

// Middleware
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

// Mock user database (in a real app, use MongoDB, MySQL, etc.)
const users = [
  {
    id: 1,
    email: 'user@example.com',
    // Hashed version of 'password123'
    password: '$2b$10$EXyMXZpGpXGoiUgSDpXQUOsszSQntNnXNgTZcF51IOZh3NLImEqRy',
    name: 'John Doe'
  }
];

// Middleware to verify JWT token
const authenticateToken = (req, res, next) => {
  // Get token from cookies or Authorization header
  const token = req.cookies.token || req.headers.authorization?.split(' ')[1];
  
  if (!token) return res.status(401).json({ message: 'Authentication required' });

  jwt.verify(token, JWT_SECRET, (err, user) => {
    if (err) return res.status(403).json({ message: 'Invalid or expired token' });
    req.user = user;
    next();
  });
};

// Routes

// Serve login page
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Login endpoint
app.post('/api/login', async (req, res) => {
  const { email, password } = req.body;
  
  // Input validation
  if (!email || !password) {
    return res.status(400).json({ message: 'Email and password are required' });
  }
  
  // Find user
  const user = users.find(u => u.email === email);
  
  if (!user) {
    // Use vague message for security
    return res.status(401).json({ message: 'Invalid credentials' });
  }
  
  try {
    // Compare passwords
    const passwordMatch = await bcrypt.compare(password, user.password);
    
    if (!passwordMatch) {
      return res.status(401).json({ message: 'Invalid credentials' });
    }
    
    // Create JWT token
    const token = jwt.sign(
      { 
        userId: user.id, 
        email: user.email,
        name: user.name
      }, 
      JWT_SECRET, 
      { expiresIn: '1h' }
    );
    
    // Set token as cookie
    res.cookie('token', token, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production', // Only use secure in production
      maxAge: 3600000 // 1 hour
    });
    
    // Return success with user info (excluding password)
    const { password: _, ...userWithoutPassword } = user;
    res.json({ 
      success: true, 
      message: 'Login successful',
      user: userWithoutPassword,
      token // Consider if you want to return the token in the response
    });
    
  } catch (error) {
    console.error('Login error:', error);
    res.status(500).json({ message: 'Server error during authentication' });
  }
});

// Logout endpoint
app.post('/api/logout', (req, res) => {
  res.clearCookie('token');
  res.json({ success: true, message: 'Logout successful' });
});

// Example protected route
app.get('/api/profile', authenticateToken, (req, res) => {
  // Return user info from token
  res.json({ user: req.user });
});

// Registration endpoint (for future implementation)
app.post('/api/register', async (req, res) => {
  const { email, password, name } = req.body;
  
  // Input validation
  if (!email || !password || !name) {
    return res.status(400).json({ message: 'All fields are required' });
  }
  
  // Check if user already exists
  if (users.find(u => u.email === email)) {
    return res.status(409).json({ message: 'User already exists' });
  }
  
  try {
    // Hash password
    const salt = await bcrypt.genSalt(10);
    const hashedPassword = await bcrypt.hash(password, salt);
    
    // In a real app, save to database
    const newUser = {
      id: users.length + 1,
      email,
      password: hashedPassword,
      name
    };
    
    // Add to mock database
    users.push(newUser);
    
    res.status(201).json({ 
      success: true, 
      message: 'User registered successfully' 
    });
    
  } catch (error) {
    console.error('Registration error:', error);
    res.status(500).json({ message: 'Server error during registration' });
  }
});

// Handle 404
app.use((req, res) => {
  res.status(404).json({ message: 'Route not found' });
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ message: 'Something went wrong!' });
});

// Start the server
app.listen(PORT, () => {
  console.log(Auth server running on port ${PORT});
});
