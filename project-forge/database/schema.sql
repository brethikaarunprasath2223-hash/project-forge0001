DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS projects;
DROP TABLE IF EXISTS mentors;
DROP TABLE IF EXISTS mentor_requests;
DROP TABLE IF EXISTS feedback;
DROP TABLE IF EXISTS user_progress;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    college_name TEXT,
    department TEXT,
    year TEXT,
    password_hash TEXT NOT NULL,
    dark_mode INTEGER DEFAULT 0,
    tutorial_seen INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE projects (
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

CREATE TABLE mentors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    title TEXT,
    email TEXT,
    skills TEXT,
    bio TEXT,
    rating REAL
);

CREATE TABLE mentor_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    mentor_id INTEGER,
    project_id INTEGER,
    message TEXT,
    status TEXT DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    message TEXT,
    rating INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    project_id INTEGER,
    stage TEXT,
    progress_percent INTEGER,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);