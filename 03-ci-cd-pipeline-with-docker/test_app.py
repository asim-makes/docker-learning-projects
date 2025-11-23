import pytest
import os
from datetime import datetime
from core import app, db
from core.models import ShortUrls
from config import TestingConfig

# Set up the application context for testing
# We override the configuration to use the fast, in-memory SQLite DB
@pytest.fixture(scope='module')
def test_client():
    """Configures the application for testing, returns a test client."""
    # Ensure the app is configured for testing
    app.config.from_object(TestingConfig)
    
    # Use the application context
    with app.app_context():
        # 1. Create all database tables
        db.create_all()
        
        # 2. Get the test client
        testing_client = app.test_client()
        
        # 3. Yield the client for the tests to run
        yield testing_client
        
        # 4. Teardown: Remove the database session and drop all tables
        db.session.remove()
        db.drop_all()

# --- Utility Tests (Unit Tests for supporting functions) ---

def test_generate_short_id():
    """Test the random ID generator function for correct length and characters."""
    from core.routes import generate_short_id
    
    short_id = generate_short_id(10)
    assert len(short_id) == 10
    assert short_id.isalnum() # Check if it contains only letters and digits

# --- Route Integration Tests ---

def test_index_get(test_client):
    """Test that the index page loads successfully (GET request)."""
    response = test_client.get('/')
    assert response.status_code == 200
    # Check for some expected content on the page (e.g., a form element)
    assert b'<form' in response.data

def test_create_short_url_random_id(test_client):
    """Test creation of a new short URL using a randomly generated ID."""
    original_url = 'https://www.google.com/very/long/path/to/search/something'
    
    # 1. POST the data
    response = test_client.post('/', data={
        'url': original_url,
        'custom_id': ''
    }, follow_redirects=True)
    
    assert response.status_code == 200
    
    # 2. Verify link was created in the database
    with app.app_context():
        # Get the latest entry
        new_link = ShortUrls.query.order_by(ShortUrls.id.desc()).first()
        assert new_link is not None
        assert new_link.original_url == original_url
        
        # Check if a short_id was generated (default length 8)
        assert len(new_link.short_id) == 8
        
        # 3. Verify the generated short URL is displayed in the response
        short_url_substring = f'{app.config["SERVER_NAME"]}/{new_link.short_id}' if app.config.get("SERVER_NAME") else new_link.short_id
        assert short_url_substring.encode('utf-8') in response.data

def test_create_short_url_custom_id(test_client):
    """Test creation of a new short URL using a user-defined custom ID."""
    custom_id = 'testcustom'
    original_url = 'https://docs.pytest.org/en/stable/'
    
    # 1. POST the data
    response = test_client.post('/', data={
        'url': original_url,
        'custom_id': custom_id
    }, follow_redirects=True)
    
    assert response.status_code == 200
    
    # 2. Verify link was created with the custom ID
    with app.app_context():
        new_link = ShortUrls.query.filter_by(short_id=custom_id).first()
        assert new_link is not None
        assert new_link.original_url == original_url
        assert new_link.short_id == custom_id

def test_custom_id_conflict_error(test_client):
    """Test that using an already existing custom ID fails."""
    # This test relies on the link created in the previous test ('testcustom')
    custom_id = 'testcustom'
    
    # Attempt to use the same custom ID again
    response = test_client.post('/', data={
        'url': 'http://www.new-url.com',
        'custom_id': custom_id
    }, follow_redirects=True)
    
    assert response.status_code == 200
    
    # Check for the flash message indicating the conflict
    # Flash messages are usually present in the session or response data in test environments
    # Check if the error message is present in the rendered index page
    assert b'Please enter different custom id!' in response.data
    
    # Verify no new entry was added to the DB for this short_id
    with app.app_context():
        count = ShortUrls.query.filter_by(short_id=custom_id).count()
        assert count == 1 # Still only one entry

def test_missing_url_error(test_client):
    """Test that submitting the form without a URL fails with a flash message."""
    response = test_client.post('/', data={
        'url': '', # Empty URL
        'custom_id': 'missing'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    # Check for the flash message indicating the URL is required
    assert b'The URL is required!' in response.data

def test_redirection_success(test_client):
    """Test that visiting a short ID successfully redirects to the original URL."""
    short_id = 'testredir'
    original_url = 'https://www.python.org/'
    
    # 1. Manually add a link to the DB
    with app.app_context():
        link = ShortUrls(original_url=original_url, short_id=short_id, created_at=datetime.now())
        db.session.add(link)
        db.session.commit()
        
    # 2. Attempt to visit the short ID
    response = test_client.get(f'/{short_id}')
    
    # 3. Assert a 302 redirect status code
    assert response.status_code == 302
    
    # 4. Assert the redirection target is correct
    assert response.headers['Location'] == original_url

def test_redirection_invalid_id(test_client):
    """Test that visiting a non-existent short ID redirects to index with an error."""
    invalid_id = 'nonexistent123'
    
    # 1. Attempt to visit the invalid short ID
    response = test_client.get(f'/{invalid_id}', follow_redirects=True) # Follows redirect to /
    
    # 2. Assert the final status code is 200 (the index page)
    assert response.status_code == 200
    
    # 3. Assert the flash message is present
    assert b'Invalid URL' in response.data