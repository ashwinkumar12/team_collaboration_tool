from flask import Flask, render_template
import datetime
import random
import os

app = Flask(__name__)

def get_mock_data():
    """Return mocked data for the dashboard"""
    # Generate next 7 days
    today = datetime.date(2026, 5, 2)
    days = []
    for i in range(7):
        current_date = today + datetime.timedelta(days=i)
        # format like 2/5/26
        formatted_date = f"{current_date.day}/{current_date.month}/{current_date.strftime('%y')}"
        days.append(formatted_date)
        
    team_members = [
        {
            "id": "member-1",
            "name": "Ashwin",
            "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=Ashwin&backgroundColor=b6e3f4",
            "load_score": 75,
            "mood_emoji": "⚡",
            "status_summary": "4 Meetings, 2 High Priority Tasks",
            "on_leave": False,
            "context_tags": "Payment API, Architecture",
            "tasks": [
                {"id": 1, "title": "Refactor Payment API", "date": days[0], "status": "In Progress", "complexity": 4, "description": "Rewrite the payment processing logic."},
                {"id": 2, "title": "API Docs", "date": days[0], "status": "To Do", "complexity": 2, "description": "Update swagger docs."},
                {"id": 3, "title": "Code Review", "date": days[0], "status": "To Do", "complexity": 1, "description": "Review PRs for the backend."},
                {"id": 4, "title": "Write Integration Tests", "date": days[1], "status": "To Do", "complexity": 3, "description": "Tests for the new payment endpoints."}
            ]
        },
        {
            "id": "member-2",
            "name": "Lokesh",
            "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=Lokesh&backgroundColor=ffdfbf",
            "load_score": 90,
            "mood_emoji": "🔥",
            "status_summary": "6 Meetings, 5 High Priority Tasks",
            "on_leave": False,
            "context_tags": "Database, CI/CD",
            "tasks": [
                {"id": 5, "title": "Database Migration", "date": days[0], "status": "In Progress", "complexity": 5, "description": "Migrate users table to PostgreSQL."},
                {"id": 6, "title": "Setup CI/CD", "date": days[0], "status": "To Do", "complexity": 3, "description": "Configure GitHub Actions."},
                {"id": 7, "title": "Fix Auth Bug", "date": days[1], "status": "To Do", "complexity": 4, "description": "Session token expiration issue."},
                {"id": 8, "title": "Standup", "date": days[1], "status": "Completed", "complexity": 1, "description": "Daily sync."}
            ]
        },
        {
            "id": "member-3",
            "name": "Aarthi",
            "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=Aarthi&backgroundColor=c0aede",
            "load_score": 0,
            "mood_emoji": "🌴",
            "status_summary": "On Leave (Out of Office)",
            "on_leave": True,
            "context_tags": "UI/UX, Frontend",
            "tasks": []
        },
        {
            "id": "member-4",
            "name": "David",
            "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=David&backgroundColor=ffc0cb",
            "load_score": 30,
            "mood_emoji": "☕",
            "status_summary": "1 Meeting, Code Review",
            "on_leave": False,
            "context_tags": "Security, Auth",
            "tasks": [
                {"id": 10, "title": "Security Audit", "date": days[0], "status": "In Progress", "complexity": 3, "description": "Review auth flows."}
            ]
        },
        {
            "id": "member-5",
            "name": "Elena",
            "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=Elena&backgroundColor=d8bfd8",
            "load_score": 50,
            "mood_emoji": "🚀",
            "status_summary": "Sprint Planning",
            "on_leave": False,
            "context_tags": "Product, Analytics",
            "tasks": [
                {"id": 11, "title": "Define KPIs", "date": days[1], "status": "To Do", "complexity": 2, "description": "Define Q3 metrics."}
            ]
        }
    ]
    
    return {"team_members": team_members, "days": days}

@app.route('/')
def index():
    data = get_mock_data()
    return render_template('index.html', 
                           team_members=data["team_members"], 
                           days=data["days"],
                           current_time=datetime.datetime.now().strftime("%b %d, %Y | %I:%M %p IST"))

if __name__ == '__main__':
    # Cloud Run expects the app to listen on the port defined by the PORT environment variable.
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=False, host='0.0.0.0', port=port)
