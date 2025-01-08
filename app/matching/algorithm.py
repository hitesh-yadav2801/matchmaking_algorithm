from typing import List, Dict
from ..models import MatchResult
import math

def calculate_matches(user: Dict, all_users: List[Dict]) -> List[MatchResult]:
    """
    Calculate and return matches for a given user.
    
    Parameters:
    - user: Dict containing user information
    - all_users: List of all users in the system
    
    Returns:
    - List of MatchResult objects sorted by compatibility score
    """
    matches = []
    
    for potential_match in all_users:
        # Skip if it's the same user
        if user['id'] == potential_match['id']:
            continue
            
        # Calculate compatibility score
        score = get_compatibility_score(user, potential_match)
        
        # Only include matches with non-zero compatibility
        if score > 0:
            # Calculate common interests and hobbies
            common_interests = list(set(user['interests']) & set(potential_match['interests']))
            common_hobbies = list(set(user['hobbies']) & set(potential_match['hobbies']))
            
            # Create match result
            match = MatchResult(
                user_id=potential_match['id'],
                name=potential_match['name'],
                compatibility_score=score,
                common_interests=common_interests,
                common_hobbies=common_hobbies
            )
            matches.append(match)
    
    # Sort matches by compatibility score in descending order
    matches.sort(key=lambda x: x.compatibility_score, reverse=True)
    return matches

def get_compatibility_score(user1: Dict, user2: Dict) -> float:
    """
    Calculate compatibility score between two users.
    
    Parameters:
    - user1: Dict containing first user's information
    - user2: Dict containing second user's information
    
    Returns:
    - Float representing compatibility score (0-1)
    """
    # Check gender preference compatibility
    if not _check_gender_preference_match(user1, user2):
        return 0.0
    
    # Initialize base score
    base_score = 1.0
    
    # Calculate individual component scores
    scores = {
        'interests': _calculate_interest_score(user1['interests'], user2['interests']),
        'hobbies': _calculate_hobby_score(user1['hobbies'], user2['hobbies']),
        'education': _calculate_education_compatibility(user1['education_level'], user2['education_level']),
        'personality': _calculate_personality_compatibility(user1['personality_traits'], user2['personality_traits']),
        'location': _calculate_location_compatibility(user1['location'], user2['location']),
        'age': _calculate_age_compatibility(user1['age'], user2['age'])
    }

    # Get distance between locations
    distance = get_distance(user1['location'], user2['location'])
    
    # Define weights for different factors
    weights = {
        'interests': 0.25,  
        'hobbies': 0.15,    
        'education': 0.10,
        'personality': 0.15,
        'location': 0.25,
        'age': 0.10
    }
    if 20 < distance <= 30:
        weights['interests'] = 0.30  # +0.05
        weights['hobbies'] = 0.20    # +0.05
        weights['location'] = 0.15    # -0.10
    elif 30 < distance <= 40:
        weights['interests'] = 0.29  # +0.04
        weights['hobbies'] = 0.19    # +0.04
        weights['location'] = 0.17    # -0.08
    elif 40 < distance <= 50:
        weights['interests'] = 0.28  # +0.3
        weights['hobbies'] = 0.18    # +0.03
        weights['location'] = 0.19     # -0.06

    print(weights)

    # print(scores)
    
    # Exponential boost for high similarity in key areas
    boost_factor = 1.0
    if scores['interests'] > 0.7 and scores['hobbies'] > 0.7:
        boost_factor = 1.2
    
    # Calculate weighted score with boost
    final_score = sum(scores[k] * weights[k] for k in weights.keys()) * boost_factor
    
    # Normalize score 
    final_score = min(1.0, final_score)
    print('Final score:', final_score)
    # print('Boost factor:', boost_factor)
    
    return round(final_score, 2)

def _calculate_interest_score(interests1: List[str], interests2: List[str]) -> float:
    """Calculate enhanced interest similarity score."""
    # Find common and total interests
    common = set(interests1) & set(interests2)
    total = set(interests1) | set(interests2)
    
    # Return 0 if both have no interests interests
    if not total:
        return 0.0
    

    # Calculate the base score
    base_score = len(common) / len(total)

    
    if base_score >= 0.8:
        return 1.0  # Full score/perfect match
    elif base_score >= 0.6:
        return 0.8  # High similarity
    elif base_score >= 0.4:
        return 0.6  # Moderate similarity
    elif base_score >= 0.2:
        return 0.4  # Low similarity
    else:
        return 0.2  # Very low similarity

def _calculate_hobby_score(hobbies1: List[str], hobbies2: List[str]) -> float:
    """Calculate enhanced hobby similarity score."""
    common = set(hobbies1) & set(hobbies2)
    total = set(hobbies1) | set(hobbies2)
    
    if not total:
        return 0.0
        
    # Enhanced scoring for specific high-value hobbies
    # Can be changed according to mass data or other factors
    high_value_hobbies = {'photography', 'hiking', 'cooking'}
    common_high_value = len(common & high_value_hobbies)
    
    base_score = len(common) / len(total)
    bonus = 0.2 * (common_high_value / len(high_value_hobbies))
    
    return min(1.0, base_score + bonus)

def _calculate_age_compatibility(age1: int, age2: int) -> float:
    """Calculate age compatibility score."""
    age_diff = abs(age1 - age2)
    if age_diff <= 2:
        return 1.0
    elif age_diff <= 5:
        return 0.8
    elif age_diff <= 10:
        return 0.6
    return 0.4

def _check_gender_preference_match(user1: Dict, user2: Dict) -> bool:
    """Check if users match each other's gender preferences."""
    return (user1['interested_in'] == user2['gender'] and 
            user2['interested_in'] == user1['gender'])

def _calculate_education_compatibility(edu1: str, edu2: str) -> float:
    """Calculate compatibility score based on education levels."""
    education_levels = {
        'Bachelors': 1,
        'Masters': 2,
        'PhD': 3
    }
    
    level1 = education_levels.get(edu1, 0)
    level2 = education_levels.get(edu2, 0)
    
    # If both are near in the education level better the match
    if level1 == level2:
        return 1.0
    elif abs(level1 - level2) == 1:
        return 0.8
    return 0.6

def _calculate_location_compatibility(loc1: str, loc2: str) -> float:
    """Calculate compatibility score based on location."""
    if loc1 == loc2:
        return 1.0
    
    # Nearby cities(Will be calculated based vicinity of the cities in real time. For sake of algorithm dummy data is used)
    distance = get_distance(loc1, loc2)
    
 
    # print("Distance between", loc1, "and", loc2, ":", distance)
    # Score based on distance
    if distance <= 20:
        return 1.0  # High compatibility
    elif distance <= 30:
        return 0.8  # Moderate compatibility
    elif distance <= 50:
        return 0.6  # Lower compatibility
    elif distance <= 100:
        return 0.4  # Very low compatibility or far apart
    elif distance <= 150:
        return 0.2  # Very Very low compatibility or far apart
    else:
        return 0.0  # No compatibility in case of far distance
    

def _calculate_personality_compatibility(traits1: List[str], traits2: List[str]) -> float:
    """Calculate personality compatibility score."""
    common_traits = set(traits1) & set(traits2)
    total_traits = set(traits1) | set(traits2)
    
    # Complementary traits(Let's assume these are traits are found after so much of data analysis)
    complementary_pairs = {
        'creative': {'analytical'},
        'outgoing': {'independent'},
        'ambitious': {'empathetic'}
    }
    
    # Count complementary traits
    complementary_count = sum(1 for t1 in traits1 for t2 in traits2 
                            if t2 in complementary_pairs.get(t1, set()))
    
    base_score = len(common_traits) / len(total_traits) if total_traits else 0
    complementary_bonus = 0.2 * (complementary_count / len(traits1))
    
    return min(1.0, base_score + complementary_bonus)


def get_distance(location1: str, location2: str) -> int:
    """Get the distance between two locations."""
    distances = {
        ('New York', 'Boston'): 10,   
        ('Boston', 'New York'): 16,
        ('Boston', 'Chicago'): 30,
        ('San Francisco', 'Seattle'): 51,
        ('Seattle', 'San Francisco'): 63,
        ('New York', 'Seattle'): 20,
        ('New York', 'San Francisco'): 80,
        ('San Francisco', 'New York'): 100    
    }
    return distances.get((location1, location2), 1000)