-- Database Schema for Enterprise Deal & Revenue Intelligence Platform

CREATE TABLE IF NOT EXISTS accounts (
    account_id SERIAL PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,
    arr_value DECIMAL(12, 2) NOT NULL,
    health_score INT DEFAULT 100,
    industry VARCHAR(100),
    tier VARCHAR(50) DEFAULT 'Enterprise',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS contacts (
    contact_id SERIAL PRIMARY KEY,
    account_id INT REFERENCES accounts(account_id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    persona VARCHAR(100) NOT NULL, -- 'CTO', 'CFO', 'Procurement', 'Champion'
    email VARCHAR(255) UNIQUE NOT NULL,
    title VARCHAR(150),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS deals (
    deal_id SERIAL PRIMARY KEY,
    account_id INT REFERENCES accounts(account_id) ON DELETE CASCADE,
    deal_name VARCHAR(255) NOT NULL,
    stage VARCHAR(100) NOT NULL, -- 'Discovery', 'Technical Validation', 'Negotiation', 'Closed Won', 'Closed Lost'
    arr_amount DECIMAL(12, 2) NOT NULL,
    owner VARCHAR(100) NOT NULL,
    close_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS call_transcripts (
    transcript_id SERIAL PRIMARY KEY,
    account_id INT REFERENCES accounts(account_id) ON DELETE CASCADE,
    deal_id INT REFERENCES deals(deal_id) ON DELETE SET NULL,
    call_stage VARCHAR(100) NOT NULL, -- 'Discovery', 'Technical Deep-Dive', 'Negotiation'
    transcript_text TEXT NOT NULL,
    objections_raised TEXT[],
    sentiment_score DECIMAL(3, 2) DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS product_feedback (
    feedback_id SERIAL PRIMARY KEY,
    account_id INT REFERENCES accounts(account_id) ON DELETE CASCADE,
    feature_name VARCHAR(255) NOT NULL,
    category VARCHAR(100), -- 'Performance', 'Security', 'Integrations', 'UI/UX'
    arr_weighted_impact DECIMAL(12, 2) DEFAULT 0.0,
    feedback_text TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'Open', -- 'Open', 'In Backlog', 'In Progress', 'Resolved'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
