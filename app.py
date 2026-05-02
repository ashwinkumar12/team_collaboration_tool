from flask import Flask, render_template

app = Flask(__name__)

def sync_with_google_services():
    """Mock integration point for Google Services"""
    print("[LOG] Syncing with Google Services...")
    print("[LOG] - Fetching events from Google Calendar API...")
    print("[LOG] - Extracting standup transcripts from Google Meet...")
    print("[LOG] Sync complete.")

def get_mock_data():
    """Return mocked data for the dashboard"""
    team_members = [
        {
            "name": "Alice",
            "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=Alice&backgroundColor=b6e3f4",
            "load_score": 85,
            "mood_emoji": "🔥",
            "current_status": "Deep work"
        },
        {
            "name": "Bob",
            "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=Bob&backgroundColor=ffdfbf",
            "load_score": 40,
            "mood_emoji": "☕",
            "current_status": "Reviewing PRs"
        },
        {
            "name": "Charlie",
            "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=Charlie&backgroundColor=c0aede",
            "load_score": 60,
            "mood_emoji": "🚀",
            "current_status": "Planning sprint"
        }
    ]
    
    sticky_notes = [
        {"id": 1, "user": "Alice", "content": "Finish the API integration for the payment gateway.", "type": "task", "bucket_date": "Monday", "linked_user": None},
        {"id": 2, "user": "Bob", "content": "Can someone help me debug the Redis cache latency?", "type": "help", "bucket_date": "Tuesday", "linked_user": "Alice"},
        {"id": 3, "user": "Charlie", "content": "Completed the onboarding flow, moving to analytics.", "type": "standup", "bucket_date": "Monday", "linked_user": None},
        {"id": 4, "user": "Alice", "content": "Update docs for the new API endpoints.", "type": "task", "bucket_date": "Wednesday", "linked_user": None},
        {"id": 5, "user": "Charlie", "content": "I'm stuck on the CI/CD pipeline issue in staging.", "type": "help", "bucket_date": "Thursday", "linked_user": "Bob"},
        {"id": 6, "user": "Bob", "content": "Reviewed Alice's PR, looks good. Starting on the metrics dashboard.", "type": "standup", "bucket_date": "Friday", "linked_user": None},
        {"id": 7, "user": "Alice", "content": "Research new auth providers.", "type": "task", "bucket_date": "Friday", "linked_user": None},
    ]
    
    return {"team_members": team_members, "sticky_notes": sticky_notes}

@app.route('/')
def index():
    sync_with_google_services()
    data = get_mock_data()
    return render_template('index.html', 
                           team_members=data["team_members"], 
                           sticky_notes=data["sticky_notes"],
                           days=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])

if __name__ == '__main__':
    app.run(debug=True)
