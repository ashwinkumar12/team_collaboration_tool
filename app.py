from flask import Flask, render_template
import datetime

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
            "name": "Ashwin",
            "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=Ashwin&backgroundColor=b6e3f4",
            "load_score": 75,
            "mood_emoji": "⚡",
            "status_summary": "4 Meetings, 2 High Priority Tasks",
            "tasks": [
                {"id": 1, "title": "Refactor Payment API", "date": days[0], "status": "In Progress", "complexity": 4, "description": "Rewrite the payment processing logic."},
                {"id": 2, "title": "API Docs", "date": days[0], "status": "To Do", "complexity": 2, "description": "Update swagger docs."},
                {"id": 3, "title": "Code Review", "date": days[0], "status": "To Do", "complexity": 1, "description": "Review PRs for the backend."},
                {"id": 4, "title": "Write Integration Tests", "date": days[1], "status": "To Do", "complexity": 3, "description": "Tests for the new payment endpoints."}
            ]
        },
        {
            "name": "Lokesh",
            "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=Lokesh&backgroundColor=ffdfbf",
            "load_score": 90,
            "mood_emoji": "🔥",
            "status_summary": "6 Meetings, 5 High Priority Tasks",
            "tasks": [
                {"id": 5, "title": "Database Migration", "date": days[0], "status": "In Progress", "complexity": 5, "description": "Migrate users table to PostgreSQL."},
                {"id": 6, "title": "Setup CI/CD", "date": days[0], "status": "To Do", "complexity": 3, "description": "Configure GitHub Actions."},
                {"id": 7, "title": "Fix Auth Bug", "date": days[1], "status": "To Do", "complexity": 4, "description": "Session token expiration issue."},
                {"id": 8, "title": "Standup", "date": days[1], "status": "Completed", "complexity": 1, "description": "Daily sync."}
            ]
        },
        {
            "name": "Aarthi",
            "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=Aarthi&backgroundColor=c0aede",
            "load_score": 40,
            "mood_emoji": "✨",
            "status_summary": "2 Meetings, 1 High Priority Task",
            "tasks": [
                {"id": 9, "title": "UI Mockups", "date": days[2], "status": "In Progress", "complexity": 2, "description": "Design new dashboard components."}
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
    app.run(debug=True)
