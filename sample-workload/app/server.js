const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(helmet());
app.use(cors());
app.use(morgan('combined'));
app.use(express.json());

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    service: 'sample-ecommerce-app',
    version: '1.0.0'
  });
});

// Metrics endpoint for cost optimization monitoring
app.get('/metrics', (req, res) => {
  const metrics = {
    cpu_usage: Math.random() * 0.8 + 0.1, // Simulate 10-90% CPU usage
    memory_usage: Math.random() * 0.7 + 0.2, // Simulate 20-90% memory usage
    request_count: Math.floor(Math.random() * 1000) + 100,
    response_time: Math.random() * 200 + 50, // 50-250ms
    error_rate: Math.random() * 0.05, // 0-5% error rate
    timestamp: new Date().toISOString()
  };
  
  res.json(metrics);
});

// Sample e-commerce endpoints
app.get('/api/products', (req, res) => {
  const products = [
    {
      id: 1,
      name: 'Sample Product 1',
      price: 29.99,
      category: 'electronics',
      stock: Math.floor(Math.random() * 100) + 10
    },
    {
      id: 2,
      name: 'Sample Product 2',
      price: 49.99,
      category: 'clothing',
      stock: Math.floor(Math.random() * 50) + 5
    },
    {
      id: 3,
      name: 'Sample Product 3',
      price: 19.99,
      category: 'books',
      stock: Math.floor(Math.random() * 200) + 20
    }
  ];
  
  // Simulate processing time
  setTimeout(() => {
    res.json(products);
  }, Math.random() * 100 + 50);
});

app.get('/api/products/:id', (req, res) => {
  const productId = parseInt(req.params.id);
  
  const product = {
    id: productId,
    name: `Sample Product ${productId}`,
    price: Math.floor(Math.random() * 100) + 10,
    category: ['electronics', 'clothing', 'books'][Math.floor(Math.random() * 3)],
    stock: Math.floor(Math.random() * 100) + 10,
    description: 'This is a sample product for cost optimization testing.'
  };
  
  setTimeout(() => {
    res.json(product);
  }, Math.random() * 50 + 25);
});

app.post('/api/orders', (req, res) => {
  const order = {
    id: Math.floor(Math.random() * 10000),
    products: req.body.products || [],
    total: req.body.total || 0,
    status: 'pending',
    created_at: new Date().toISOString()
  };
  
  // Simulate order processing
  setTimeout(() => {
    res.status(201).json(order);
  }, Math.random() * 200 + 100);
});

app.get('/api/orders/:id', (req, res) => {
  const orderId = parseInt(req.params.id);
  
  const order = {
    id: orderId,
    products: [
      { id: 1, name: 'Sample Product 1', quantity: 2, price: 29.99 }
    ],
    total: 59.98,
    status: 'completed',
    created_at: new Date().toISOString()
  };
  
  setTimeout(() => {
    res.json(order);
  }, Math.random() * 100 + 50);
});

// Load testing endpoint
app.get('/api/load-test', (req, res) => {
  const duration = parseInt(req.query.duration) || 5000; // 5 seconds default
  const intensity = parseInt(req.query.intensity) || 50; // CPU intensity 0-100
  
  const startTime = Date.now();
  
  // Simulate CPU-intensive work
  const simulateWork = () => {
    let result = 0;
    for (let i = 0; i < intensity * 1000; i++) {
      result += Math.sqrt(i);
    }
    return result;
  };
  
  const interval = setInterval(() => {
    simulateWork();
    
    if (Date.now() - startTime >= duration) {
      clearInterval(interval);
      res.json({
        message: 'Load test completed',
        duration: duration,
        intensity: intensity,
        result: 'success'
      });
    }
  }, 100);
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({
    error: 'Something went wrong!',
    message: err.message
  });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({
    error: 'Not found',
    message: 'The requested resource was not found'
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`Sample e-commerce app listening on port ${PORT}`);
  console.log(`Health check available at http://localhost:${PORT}/health`);
  console.log(`Metrics available at http://localhost:${PORT}/metrics`);
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('SIGTERM received, shutting down gracefully');
  process.exit(0);
});

process.on('SIGINT', () => {
  console.log('SIGINT received, shutting down gracefully');
  process.exit(0);
}); 