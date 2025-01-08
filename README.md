# Dating App Matchmaking Algorithm Assignment

## Requirements

### Technical Stack
- Python 3.8+
- FastAPI
- Additional libraries of your choice (please document them)

### Project Structure
```
matchmaking/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   └── matching/
│       ├── __init__.py
│       └── algorithm.py
│
├── mock_data/
│   └── users.json
│
├── requirements.txt
└── README.md
```

### Data Model
Each user profile contains the following information:
```python
{
    "id": str,
    "name": str,
    "age": int,
    "gender": str,
    "interested_in": str,
    "location": str,
    "hobbies": List[str],
    "interests": List[str],
    "occupation": str,
    "education_level": str,
    "personality_traits": List[str]
}
```

### API Endpoints
Implement the following endpoints:
- `POST /api/v1/match`: Generate matches for a given user
- `GET /api/v1/compatibility/{user_id1}/{user_id2}`: Get compatibility score for two users


## Getting Started
1. Clone this template
2. Install dependencies: `pip install -r requirements.txt`
3. Start server: `uvicorn app.main:app --reload`

## Mock Data
Sample user data is provided in `mock_data/users.json`. Use this data to test your implementation.

## API Testing Guide in Postman

### Base URL
```
http://localhost:8000
```

### Test Cases

#### 1. Health Check
- **Request**:
  - Method: GET
  - URL: `/`
  - No headers required
- **Expected Response**:
```json
{
    "message": "Welcome to the Dating App Matchmaking API"
}
```

#### 2. Generate Matches for a User
- **Request**:
  - Method: POST
  - URL: `/api/v1/match/user1`
  - No body required
- **Expected Response**:
```json
[
    {
        "user_id": "user4",
        "name": "Emily Parker",
        "compatibility_score": 0.85,
        "common_interests": ["travel", "technology"],
        "common_hobbies": ["hiking", "photography"]
    },
    {
        "user_id": "user2",
        "name": "Sarah Chen",
        "compatibility_score": 0.72,
        "common_interests": ["travel"],
        "common_hobbies": ["cooking"]
    }
]
```

#### 3. Check Compatibility Between Two Users
- **Request**:
  - Method: GET
  - URL: `/api/v1/compatibility/user1/user2`
  - No body required
- **Expected Response**:
```json
{
    "user1_id": "user1",
    "user2_id": "user2",
    "compatibility_score": 0.72
}
```

### Test Scenarios

1. **Valid Match Generation**
   - Use existing user IDs (user1, user2, user3, user4, user5)
   - Verify that matches are sorted by compatibility score
   - Check that gender preferences are respected
   - Verify common interests and hobbies are correct

2. **Invalid User IDs**
   - Test with non-existent user ID: `/api/v1/match/user999`
   - Expected: 404 Not Found response
   ```json
   {
       "detail": "User not found"
   }
   ```
