# 🕵️‍ Recommender
### Centive's Repo Recommendation Engine

This repo contains code for the recommendation engines powering Centive's onboarding/discovery process, namely our:
- Repository Recommendation Engine
- Similar Repo Discovery

## Repository Recommendation
#### `POST /api/recs`
Requires a JSON body for the POST data containing a `token` field representing a user's GitHub access token (with scoped permissions) and a `lf` field representing what the user is looking for in a repo (e.g. Frontend UI related repositories).

Returns an array of 4-8 repositories most relevant to the user. Search criteria is returned based off of user's top 4 most familiar programming languages (measured by a mixture of last 5 created repos and last 5 starred repos). Results are then weighted against relevance between project description and what the user is looking for.

## Similar Repo Discovery
#### `POST /api/similar`
Requires a JSON body for the POST data containing a `token` field representing a user's GitHub access token (with scoped permissions) and a `repo` field representing the target repository to find projects similar to.

Returns an array of similar repositories. Search is conducted based off of top repos with the same topic items as original.

## Setup
### Python
1. Download requirements: `pip install -r requirements.txt`
2. Run the API server: `python api.py`

### Docker
1. `docker run -p 8080:8080 jzhao2k19/centive-recommender:latest`