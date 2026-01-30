import requests

BASE_URL = "http://127.0.0.1:8000/api"
UPLOAD_URL = f"{BASE_URL}/upload/"
LOGIN_URL = f"{BASE_URL}/token/"
HISTORY_URL = f"{BASE_URL}/history/"

def login(username, password):
    """
    Authenticates the user and returns a token.
    """
    try:
        response = requests.post(LOGIN_URL, json={"username": username, "password": password})
        if response.status_code == 200:
            return response.json().get("token")
        else:
            raise Exception("Invalid credentials")
    except requests.RequestException as e:
        raise Exception(f"Connection error: {e}")

def get_history(token):
    """
    Fetches the upload history.
    """
    headers = {"Authorization": f"Token {token}"}
    try:
        response = requests.get(HISTORY_URL, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        # Don't crash on history fetch fail, just return empty
        print(f"Failed to fetch history: {e}") 
        return []

def upload_csv(file_path, token):
    """
    Uploads a CSV file to the backend API.
    """
    if not token:
        raise ValueError("Token is missing")

    try:
        with open(file_path, "rb") as f:
            files = {"file": f}
            headers = {
                "Authorization": f"Token {token}"
            }
            response = requests.post(UPLOAD_URL, files=files, headers=headers)
        
        if response.status_code != 200:
            try:
                error_msg = response.json().get('error', 'Unknown Error')
            except:
                error_msg = response.text
            raise Exception(f"Server Error: {error_msg}")

        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Network or API Error: {str(e)}")
    except ValueError as e:
        raise Exception(f"Invalid Response: {str(e)}")
    except Exception as e:
        raise Exception(f"Upload Failed: {str(e)}")

def generate_report(token, dataset_id=None):
    """
    Requests a PDF report from the backend.
    Returns binary content.
    """
    url = f"{BASE_URL}/generate-report/"
    headers = {"Authorization": f"Token {token}"}
    data = {}
    if dataset_id:
        data["dataset_id"] = dataset_id
    
    try:
        response = requests.post(url, headers=headers, json=data, stream=True)
        if response.status_code == 200:
            return response.content
        else:
            try:
                err = response.json().get('error', 'Unknown Error')
            except:
                err = response.text
            raise Exception(f"Failed to generate report: {err}")
    except Exception as e:
        raise Exception(f"Network Error: {str(e)}")
