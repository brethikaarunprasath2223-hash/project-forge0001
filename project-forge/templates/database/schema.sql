-- Project Forge Database Schema
-- Works on SQLite (dev) and MySQL (production, minor type tweaks noted in comments)

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,       -- MySQL: INT AUTO_INCREMENT
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT NOT NULL,
    college_name TEXT NOT NULL,
    department TEXT NOT NULL,
    year TEXT NOT NULL,                          -- '1st','2nd','3rd','4th'
    password_hash TEXT NOT NULL,
    dark_mode INTEGER DEFAULT 0,
    tutorial_seen INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    idea_text TEXT NOT NULL,
    title TEXT,
    abstract TEXT,
    problem_statement TEXT,
    objectives TEXT,             -- JSON array as text
    features TEXT,               -- JSON array as text
    advantages TEXT,             -- JSON array as text
    disadvantages TEXT,          -- JSON array as text
    similar_projects TEXT,       -- JSON array as text
    suggested_improvements TEXT, -- JSON array as text
    future_scope TEXT,           -- JSON array as text
    tech_stack TEXT,             -- JSON object as text
    roadmap TEXT,                -- JSON array as text
    estimated_cost TEXT,
    estimated_duration TEXT,
    difficulty_level TEXT,
    required_software TEXT,      -- JSON array as text
    required_hardware TEXT,      -- JSON array as text
    domain TEXT,
    status TEXT DEFAULT 'generated',   -- generated / saved / in_progress / completed
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS mentors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    title TEXT,
    skills TEXT,                 -- JSON array as text
    bio TEXT,
    email TEXT,
    rating REAL DEFAULT 4.5,
    availability TEXT DEFAULT 'Available'
);

CREATE TABLE IF NOT EXISTS mentor_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    mentor_id INTEGER NOT NULL,
    project_id INTEGER,
    message TEXT,
    status TEXT DEFAULT 'pending',  -- pending / accepted / declined
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES users(id),
    FOREIGN KEY (mentor_id) REFERENCES mentors(id)
);

CREATE TABLE IF NOT EXISTS feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    message TEXT NOT NULL,
    rating INTEGER DEFAULT 5,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS user_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    project_id INTEGER NOT NULL,
    stage TEXT DEFAULT 'idea_submitted',  -- idea_submitted / planning / development / testing / completed
    progress_percent INTEGER DEFAULT 10,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (project_id) REFERENCES projects(id)
);
