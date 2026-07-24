CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    college_name TEXT,
    department TEXT,
    year TEXT,
    password_hash TEXT NOT NULL,
    dark_mode INTEGER DEFAULT 0,
    tutorial_seen INTEGER DEFAULT 0
);
CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,

    idea_text TEXT,
    title TEXT,
    abstract TEXT,
    problem_statement TEXT,
    objectives TEXT,
    features TEXT,
    advantages TEXT,
    disadvantages TEXT,
    similar_projects TEXT,
    suggested_improvements TEXT,
    future_scope TEXT,

    tech_stack TEXT,
    roadmap TEXT,

    estimated_cost TEXT,
    estimated_duration TEXT,
    difficulty_level TEXT,

    required_software TEXT,
    required_hardware TEXT,

    domain TEXT,
    status TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    message TEXT,
    rating INTEGER
);
CREATE TABLE IF NOT EXISTS user_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    project_id INTEGER,
    stage TEXT,
    progress_percent INTEGER DEFAULT 0,
    completed INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);