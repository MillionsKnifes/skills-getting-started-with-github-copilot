from fastapi.testclient import TestClient

def test_root_redirect(client: TestClient):
    """Test that the root path returns the static index.html"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.url.path == "/static/index.html"  # Verify we got the index page

def test_get_activities(client: TestClient):
    """Test getting the list of activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    
    # Check that we have the expected activities
    assert "Chess Club" in data
    assert "Programming Class" in data
    
    # Check activity structure
    chess_club = data["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    
    # Validate participants data type
    assert isinstance(chess_club["participants"], list)

def test_signup_new_participant(client: TestClient):
    """Test signing up a new participant for an activity"""
    activity_name = "Chess Club"
    email = "test@mergington.edu"
    
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    
    # Verify the participant was added
    activities = client.get("/activities").json()
    assert email in activities[activity_name]["participants"]

def test_signup_duplicate_participant(client: TestClient):
    """Test that signing up a duplicate participant returns an error"""
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # This email is already in the participants list
    
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

def test_signup_nonexistent_activity(client: TestClient):
    """Test that signing up for a non-existent activity returns an error"""
    activity_name = "NonexistentClub"
    email = "test@mergington.edu"
    
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

def test_unregister_participant(client: TestClient):
    """Test unregistering a participant from an activity"""
    # First, sign up a new participant
    activity_name = "Chess Club"
    email = "tounregister@mergington.edu"
    client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # Then unregister them
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
    
    # Verify the participant was removed
    activities = client.get("/activities").json()
    assert email not in activities[activity_name]["participants"]

def test_unregister_nonexistent_participant(client: TestClient):
    """Test that unregistering a non-existent participant returns an error"""
    activity_name = "Chess Club"
    email = "nonexistent@mergington.edu"
    
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"]