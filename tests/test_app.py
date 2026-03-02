def test_root_redirects_to_static(client):
    # Arrange
    url = "/"

    # Act
    response = client.get(url, follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"].endswith("/static/index.html")


def test_get_activities_returns_data(client):
    # Arrange
    url = "/activities"

    # Act
    response = client.get(url)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_successful_signup_and_unregister(client):
    # Arrange
    activity = "Chess Club"
    email = "sam@mergington.edu"
    signup_url = f"/activities/{activity}/signup"
    unregister_url = f"/activities/{activity}/unregister"

    # Act - signup
    r1 = client.post(signup_url, params={"email": email})

    # Assert - signup succeeded
    assert r1.status_code == 200
    assert "Signed up" in r1.json()["message"]

    # Act - unregister
    r2 = client.delete(unregister_url, params={"email": email})

    # Assert - unregister succeeded
    assert r2.status_code == 200
    assert "Unregistered" in r2.json()["message"]


def test_signup_nonexistent_activity(client):
    # Arrange
    url = "/activities/NoSuchActivity/signup"
    email = "nobody@mergington.edu"

    # Act
    response = client.post(url, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_duplicate_signup_returns_400(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"  # already signed up in initial data
    url = f"/activities/{activity}/signup"

    # Act
    response = client.post(url, params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_nonexistent_activity(client):
    # Arrange
    url = "/activities/NoSuchActivity/unregister"
    email = "none@mergington.edu"

    # Act
    response = client.delete(url, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_missing_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "ghost@mergington.edu"
    url = f"/activities/{activity}/unregister"

    # Act
    response = client.delete(url, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in activity"
