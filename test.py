import requests
import json


def fetch_pull_review(github_token: str, github_repo: str, pull_request_number: int):
    """Create a comment to a pull request"""
    headers = {
        "Accept": "Accept: application/vnd.github+json",
        "authorization": f"Bearer {github_token}"
    }
    url = f"https://api.github.com/repos/{github_repo}/pulls/{pull_request_number}"
    response = requests.get(url, headers=headers)
    print(response.json())
    return response.json()


def add_comment_pull_review(github_token: str, github_repo: str, pull_request_number: int, body, line: int, path: str,
                            comment_body: str):
    headers = {
        "Accept": "Accept: application/vnd.github+json",
        "authorization": f"Bearer {github_token}"
    }
    data = {
        "body": body,
        "event": "REQUEST_CHANGES",
        "comments": [
            {
                "line": line,
                "path": path,
                "body": comment_body
            }
        ]
    }
    url = f"https://api.github.com/repos/{github_repo}/pulls/{pull_request_number}/reviews"
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response


if __name__ == '__main__':
    '''
    fetch_pull_review(
        github_token="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",
        pull_request_number=1,
        github_repo="digitalneedstech/code-review-action")
    '''
    add_comment_pull_review(
        github_token="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",
        pull_request_number=1,
        github_repo="piyushbhatia891/code-review-action",
        comment_body="Please add more information here, and fix this typo.",
        body="This is PR review body",
        line=12,
        path="app.py")
