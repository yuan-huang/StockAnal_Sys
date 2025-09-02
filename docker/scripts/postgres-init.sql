-- 创建应用用户
CREATE USER app_user WITH PASSWORD 'tradingagents123';

-- 创建示例表结构
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS stocks (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    exchange VARCHAR(50),
    sector VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS trades (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    stock_id INTEGER REFERENCES stocks(id) ON DELETE CASCADE,
    trade_type VARCHAR(10) CHECK (trade_type IN ('BUY', 'SELL')),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    price DECIMAL(10, 2) NOT NULL CHECK (price > 0),
    trade_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 创建索引
CREATE INDEX idx_trades_user_id ON trades(user_id);
CREATE INDEX idx_trades_stock_id ON trades(stock_id);
CREATE INDEX idx_trades_trade_time ON trades(trade_time DESC);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_stocks_symbol ON stocks(symbol);

-- 给应用用户授权
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO app_user;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO app_user;

-- 插入示例数据
INSERT INTO stocks (symbol, name, exchange, sector) VALUES 
    ('AAPL', 'Apple Inc.', 'NASDAQ', 'Technology'),
    ('GOOGL', 'Alphabet Inc.', 'NASDAQ', 'Technology'),
    ('MSFT', 'Microsoft Corporation', 'NASDAQ', 'Technology'),
    ('TSLA', 'Tesla, Inc.', 'NASDAQ', 'Automotive')
ON CONFLICT (symbol) DO NOTHING;

COMMENT ON TABLE users IS '用户表';
COMMENT ON TABLE stocks IS '股票信息表';  
COMMENT ON TABLE trades IS '交易记录表';

SELECT 'PostgreSQL initialization completed successfully!' as message;