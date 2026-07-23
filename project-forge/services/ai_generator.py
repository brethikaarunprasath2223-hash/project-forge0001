"""
services/ai_generator.py
--------------------------
This module turns a raw student idea (free text) into a full, structured
project plan: title, abstract, tech stack, roadmap, cost/duration estimate,
and more.

HOW IT WORKS (current implementation):
It uses keyword-based domain detection + templated generation, so the app
works completely offline with zero API keys — good for local dev, demos,
and Replit hosting where an external LLM key may not be configured.

HOW TO UPGRADE TO REAL LLM GENERATION:
Swap the body of `generate_project()` to call the Anthropic API instead
(https://docs.claude.com). Keep the same return shape (a dict with the
keys listed at the bottom of this file) so nothing else in the app needs
to change. Example:

    import anthropic
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        messages=[{"role": "user", "content": PROMPT}],
    )
    # then parse response into the same dict shape used below
"""

import re
import random

# ---------------------------------------------------------------------------
# Domain detection: keyword -> domain profile
# ---------------------------------------------------------------------------
DOMAINS = {
    "ai_ml": {
        "keywords": ["ai", "machine learning", "ml", "attendance", "face recognition",
                     "prediction", "recommendation", "chatbot", "nlp", "detect", "classify",
                     "deep learning", "neural", "computer vision", "image recognition"],
        "frontend": ["React.js", "HTML5", "CSS3", "Chart.js (for analytics dashboards)"],
        "backend": ["Python (Flask)", "REST API"],
        "database": ["MySQL", "SQLite (dev)"],
        "languages": ["Python", "JavaScript"],
        "ai_models": ["Scikit-learn / TensorFlow model", "OpenCV (if vision-based)", "Pretrained transformer (if NLP-based)"],
        "software": ["Python 3.10+", "VS Code", "Jupyter Notebook", "MySQL Workbench", "Git"],
        "hardware": ["Laptop with 8GB+ RAM", "Webcam (if vision-based)", "GPU recommended for training (optional)"],
    },
    "web": {
        "keywords": ["website", "web app", "e-commerce", "portal", "platform", "booking",
                     "management system", "dashboard", "blog", "social media", "marketplace"],
        "frontend": ["React.js", "HTML5", "CSS3", "Bootstrap/Tailwind CSS"],
        "backend": ["Python (Flask) or Node.js (Express)", "REST API"],
        "database": ["MySQL", "SQLite (dev)"],
        "languages": ["Python or JavaScript", "HTML/CSS"],
        "ai_models": ["Not required (add later for smart search/recommendations)"],
        "software": ["VS Code", "Node.js / Python", "MySQL Workbench", "Postman", "Git"],
        "hardware": ["Laptop with 4GB+ RAM", "Internet connection"],
    },
    "mobile": {
        "keywords": ["app", "mobile", "android", "ios", "flutter"],
        "frontend": ["Flutter or React Native", "Material Design components"],
        "backend": ["Python (Flask) REST API or Firebase Functions"],
        "database": ["Firebase Firestore", "MySQL (if custom backend)"],
        "languages": ["Dart or Kotlin/Swift", "Python (for backend)"],
        "ai_models": ["Optional: TensorFlow Lite for on-device ML"],
        "software": ["Android Studio", "Flutter SDK", "VS Code", "Firebase Console"],
        "hardware": ["Laptop with 8GB+ RAM", "Android device for testing"],
    },
    "iot": {
        "keywords": ["iot", "sensor", "arduino", "raspberry pi", "smart home", "embedded",
                     "automation", "hardware"],
        "frontend": ["React.js or Flutter (mobile control app)"],
        "backend": ["Python (Flask)", "MQTT broker"],
        "database": ["MySQL", "InfluxDB (for sensor time-series data)"],
        "languages": ["Python", "C/C++ (microcontroller firmware)"],
        "ai_models": ["Optional: anomaly detection on sensor data"],
        "software": ["Arduino IDE", "VS Code", "MySQL Workbench", "MQTT client (e.g. MQTT Explorer)"],
        "hardware": ["Arduino/Raspberry Pi board", "Relevant sensors", "Jumper wires, breadboard", "Wi-Fi module"],
    },
    "general": {
        "keywords": [],
        "frontend": ["HTML5", "CSS3", "JavaScript"],
        "backend": ["Python (Flask)", "REST API"],
        "database": ["MySQL", "SQLite (dev)"],
        "languages": ["Python", "JavaScript"],
        "ai_models": ["Not required"],
        "software": ["VS Code", "Python 3.10+", "MySQL Workbench", "Git"],
        "hardware": ["Laptop with 4GB+ RAM"],
    },
}


def detect_domain(idea_text):
    text = idea_text.lower()
    scores = {}
    for domain, profile in DOMAINS.items():
        if domain == "general":
            continue
        score = sum(1 for kw in profile["keywords"] if kw in text)
        if score > 0:
            scores[domain] = score
    if not scores:
        return "general"
    return max(scores, key=scores.get)


def extract_subject(idea_text):
    """Pulls a short human-readable subject phrase out of the idea text for titling."""
    text = idea_text.strip()
    text = re.sub(r"^(i want to build|i want to make|i wanna build|build|create|make|develop)\s+(an?|the)?\s*",
                   "", text, flags=re.IGNORECASE)
    text = text.rstrip(".!")
    words = text.split()
    subject = " ".join(words[:8]) if len(words) > 8 else text
    subject = subject.strip()
    if not subject:
        return "Smart Student Project"
    # Capitalize first word but preserve the rest as-is so acronyms like AI/IoT aren't mangled
    return subject[0].upper() + subject[1:]


def title_case(s):
    small = {"a", "an", "the", "of", "for", "and", "in", "on", "to", "with"}
    acronyms = {"ai": "AI", "iot": "IoT", "ml": "ML", "nlp": "NLP", "ui": "UI", "ux": "UX",
                "api": "API", "sql": "SQL", "gps": "GPS", "qr": "QR", "erp": "ERP", "lms": "LMS"}
    words = s.split()
    result = []
    for i, w in enumerate(words):
        lw = w.lower().strip(".,")
        if lw in acronyms:
            result.append(acronyms[lw])
        elif lw in small and i != 0:
            result.append(lw)
        else:
            result.append(w.capitalize())
    return " ".join(result)


def generate_project(idea_text):
    """
    Main entry point. Takes raw idea text, returns a dict with every field
    the Project Idea Submission spec requires.
    """
    domain_key = detect_domain(idea_text)
    profile = DOMAINS[domain_key]
    subject = extract_subject(idea_text)

    domain_labels = {
        "ai_ml": "AI / Machine Learning",
        "web": "Web Application",
        "mobile": "Mobile Application",
        "iot": "IoT / Embedded System",
        "general": "Software Application",
    }
    domain_label = domain_labels[domain_key]

    title = title_case(f"{subject} — {domain_label} System") if len(subject) < 40 else title_case(subject)

    abstract = (
        f"This project proposes the design and development of \"{title}\", a {domain_label.lower()} "
        f"solution aimed at addressing the problem of {subject.lower()}. The system leverages modern "
        f"software engineering practices to deliver an efficient, scalable, and user-friendly solution "
        f"for college students and institutions. The proposed system automates manual processes, reduces "
        f"human error, and provides real-time insights through an intuitive interface, making it suitable "
        f"for academic submission and potential real-world deployment."
    )

    problem_statement = (
        f"Traditional approaches to {subject.lower()} are often manual, time-consuming, error-prone, and "
        f"lack real-time visibility. Existing solutions may be expensive, difficult to scale, or not "
        f"tailored to the specific needs of students and institutions. There is a clear need for an "
        f"affordable, automated, and easy-to-use system that solves this problem effectively."
    )

    objectives = [
        f"To design and develop a functional prototype of {subject.lower()}.",
        "To automate manual processes and reduce human effort and error.",
        "To provide a simple, intuitive interface accessible to non-technical users.",
        "To ensure the system is scalable, secure, and maintainable.",
        "To evaluate the system's performance against existing/traditional methods.",
    ]

    features = [
        "User authentication and role-based access control",
        "Clean, responsive dashboard for real-time monitoring",
        f"Core functionality: automated handling of {subject.lower()}",
        "Data storage and retrieval via a relational database",
        "Notifications/alerts for important events",
        "Exportable reports (PDF/CSV)",
        "Admin panel for management and analytics",
    ]

    advantages = [
        "Reduces manual effort and human error significantly",
        "Provides real-time data and faster decision-making",
        "Cost-effective compared to commercial alternatives",
        "Scalable architecture that can grow with institutional needs",
        "Improves overall efficiency and user experience",
    ]

    disadvantages = [
        "Requires initial setup and internet/hardware dependency",
        "Accuracy may depend on data quality and training data (if AI-based)",
        "Ongoing maintenance needed for updates and security patches",
        "Learning curve for first-time users/administrators",
    ]

    similar_projects = [
        f"Commercial {domain_label} platforms with similar core functionality (e.g. enterprise SaaS tools)",
        f"Open-source GitHub repositories tackling {subject.lower()} at a smaller scale",
        "Existing college-built final year projects on related themes (useful for comparison, not copying)",
    ]

    suggested_improvements = [
        "Add AI-powered analytics/recommendations for smarter insights",
        "Integrate cloud deployment for anywhere-access",
        "Add multi-language support for wider accessibility",
        "Introduce automated testing (unit + integration tests) for reliability",
        "Add role-based dashboards (student/faculty/admin) for better UX",
    ]

    future_scope = [
        "Integrate with institutional ERP/LMS systems",
        "Add predictive analytics using historical data",
        "Build a companion mobile app (Flutter/React Native)",
        "Scale to multi-college / multi-tenant architecture",
        "Explore monetization or open-source community contribution",
    ]

    tech_stack = {
        "frontend": profile["frontend"],
        "backend": profile["backend"],
        "database": profile["database"],
        "languages": profile["languages"],
        "ai_models": profile["ai_models"],
    }

    roadmap = [
        {"phase": "Week 1-2: Planning & Research", "detail": "Requirement gathering, literature survey, finalize tech stack and system design (ER diagram, architecture diagram)."},
        {"phase": "Week 3-4: Database & Backend Setup", "detail": "Design database schema, set up Flask project structure, build core REST APIs."},
        {"phase": "Week 5-6: Frontend Development", "detail": "Build UI screens, connect to backend APIs, implement authentication."},
        {"phase": "Week 7", "detail": "Implement core feature logic" + (" and integrate AI/ML model." if domain_key == "ai_ml" else ".")},
        {"phase": "Week 8", "detail": "Testing (unit, integration, user testing), bug fixing."},
        {"phase": "Week 9", "detail": "Documentation, PPT preparation, and final deployment."},
        {"phase": "Week 10", "detail": "Final review, demo rehearsal, and project submission."},
    ]

    difficulty_pool = {
        "ai_ml": "Advanced",
        "iot": "Advanced",
        "mobile": "Intermediate",
        "web": "Intermediate",
        "general": "Beginner-Intermediate",
    }
    cost_pool = {
        "ai_ml": "₹2,000 – ₹6,000 (cloud GPU credits optional, mostly free-tier feasible)",
        "iot": "₹3,000 – ₹8,000 (hardware components: sensors, boards, wiring)",
        "mobile": "₹0 – ₹2,000 (mostly free tools; optional Play Store fee ₹1,900 one-time)",
        "web": "₹0 – ₹2,000 (mostly free/open-source tools; optional hosting)",
        "general": "₹0 – ₹1,500",
    }

    return {
        "domain": domain_label,
        "title": title,
        "abstract": abstract,
        "problem_statement": problem_statement,
        "objectives": objectives,
        "features": features,
        "advantages": advantages,
        "disadvantages": disadvantages,
        "similar_projects": similar_projects,
        "suggested_improvements": suggested_improvements,
        "future_scope": future_scope,
        "tech_stack": tech_stack,
        "roadmap": roadmap,
        "estimated_cost": cost_pool[domain_key],
        "estimated_duration": "8 – 10 weeks (part-time, alongside coursework)",
        "difficulty_level": difficulty_pool[domain_key],
        "required_software": profile["software"],
        "required_hardware": profile["hardware"],
    }


def generate_dev_guide(project_dict):
    """
    Builds the beginner-friendly step-by-step development guide shown
    below every generated project.
    """
    domain = project_dict["domain"]
    steps = [
        {
            "title": "1. Install the required software",
            "content": (
                "Install these tools before writing any code:\n"
                + "\n".join(f"  • {s}" for s in project_dict["required_software"])
                + "\n\nTip: Download Python from python.org, VS Code from code.visualstudio.com, "
                  "and MySQL Community Server from mysql.com. Verify installation by running "
                  "`python --version` and `mysql --version` in your terminal."
            ),
        },
        {
            "title": "2. Learn the core languages",
            "content": (
                "Focus your learning on: " + ", ".join(project_dict["tech_stack"]["languages"]) + ".\n"
                "Spend 1-2 weeks on free resources (W3Schools, freeCodeCamp, official docs) before coding. "
                "You don't need to master everything — learn just enough to build, then learn more as you go."
            ),
        },
        {
            "title": "3. Set up the folder structure",
            "content": (
                "Create this structure for a clean, maintainable Flask project:\n"
                "  project-name/\n"
                "  ├── app.py\n"
                "  ├── requirements.txt\n"
                "  ├── templates/   (HTML files)\n"
                "  ├── static/      (CSS, JS, images)\n"
                "  ├── models/      (database models)\n"
                "  ├── routes/      (route blueprints)\n"
                "  └── database/    (schema + db connection)"
            ),
        },
        {
            "title": "4. Set up the database",
            "content": (
                "Install " + " / ".join(project_dict["tech_stack"]["database"]) + ". "
                "Design your tables based on the entities in your project (e.g. Users, Records, Logs). "
                "Start with SQLite locally (zero config), then migrate to MySQL for production by "
                "exporting your schema and importing it via MySQL Workbench."
            ),
        },
        {
            "title": "5. Build the backend (Flask)",
            "content": (
                "Create Flask routes for each core feature (e.g. /api/submit, /api/list). "
                "Use Flask-CORS if your frontend runs separately. Test every route using Postman "
                "before connecting it to the frontend — this isolates bugs early."
            ),
        },
        {
            "title": "6. Build the frontend",
            "content": (
                "Use " + " / ".join(project_dict["tech_stack"]["frontend"]) + " to build your UI. "
                "Start with static HTML pages, then connect them to your Flask backend using fetch() "
                "calls to your API endpoints. Keep the design simple first — polish later."
            ),
        },
        {
            "title": "7. Add AI/ML (if applicable)",
            "content": (
                ("Train a simple model using Scikit-learn or use a pretrained model to save time. "
                 "Wrap it in a Flask route that accepts input and returns predictions as JSON.")
                if "ai" in domain.lower() else
                "Not required for this project — you can skip this step, or add smart features later "
                "as a future enhancement (e.g. simple recommendation logic)."
            ),
        },
        {
            "title": "8. Testing",
            "content": (
                "Test each feature manually as you build it. Before submission, run through the full "
                "user flow at least 3 times as a first-time user would, and fix any broken links, "
                "missing validations, or crashes. Ask a classmate to test it — fresh eyes catch bugs fast."
            ),
        },
        {
            "title": "9. Deployment",
            "content": (
                "For a free, simple deployment: use Replit, Render, or PythonAnywhere for the Flask "
                "backend. Set environment variables for any secrets. Make sure `debug=False` in "
                "production and that your requirements.txt is up to date (`pip freeze > requirements.txt`)."
            ),
        },
    ]
    return steps
