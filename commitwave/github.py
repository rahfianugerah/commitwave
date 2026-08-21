"""GitHub REST and GraphQL calls over the standard library.

Every function takes an explicit token. Two badges act as two different accounts, and
a shared client object would hide which account is speaking at the call site.
"""

from __future__ import annotations

import base64
import json
import time
import urllib.error
import urllib.parse
import urllib.request

API = "https://api.github.com"
GRAPHQL = f"{API}/graphql"
API_VERSION = "2022-11-28"
USER_AGENT = "commitwave/3.0.0"
MAX_RETRIES = 5


class GitHubError(RuntimeError):
    """A GitHub request failed. Carries the status and GitHub's own message, never a header."""

    def __init__(self, status: int, message: str) -> None:
        super().__init__(f"GitHub returned {status}: {message}")
        self.status = status
        self.message = message


def rest(method: str, path: str, token: str, body: dict | None = None) -> dict:
    return _request(method, f"{API}{path}", token, body)


def graphql(query: str, variables: dict, token: str) -> dict:
    """Run a GraphQL operation. GraphQL answers 200 on failure, so errors are checked here."""
    payload = _request("POST", GRAPHQL, token, {"query": query, "variables": variables})
    errors = payload.get("errors")
    if errors:
        raise GitHubError(200, "; ".join(item.get("message", "unknown") for item in errors))
    return payload["data"]


def whoami(token: str) -> dict:
    """Return the account the token belongs to."""
    return rest("GET", "/user", token)


def noreply_email(login: str, token: str) -> str:
    """Build the address GitHub attributes to `login` in a Co-authored-by trailer.

    Derived rather than configured. A hand-typed address produces a commit that looks
    co-authored and counts for nothing, and the mistake is invisible until the badge
    fails to arrive.
    """
    user = rest("GET", f"/users/{login}", token)
    return f"{user['id']}+{user['login']}@users.noreply.github.com"


def repository(owner: str, name: str, token: str) -> dict:
    return rest("GET", f"/repos/{owner}/{name}", token)


def branch_sha(owner: str, name: str, branch: str, token: str) -> str:
    return rest("GET", f"/repos/{owner}/{name}/git/ref/heads/{branch}", token)["object"]["sha"]


def create_branch(owner: str, name: str, branch: str, sha: str, token: str) -> None:
    body = {"ref": f"refs/heads/{branch}", "sha": sha}
    rest("POST", f"/repos/{owner}/{name}/git/refs", token, body)


def commit_file(
    owner: str, name: str, branch: str, path: str, text: str, message: str, token: str
) -> None:
    """Create one new file on `branch`. The path must not already exist, so no blob sha."""
    body = {
        "message": message,
        "content": base64.b64encode(text.encode("utf-8")).decode("ascii"),
        "branch": branch,
    }
    rest("PUT", f"/repos/{owner}/{name}/contents/{path}", token, body)


def open_pull(owner: str, name: str, head: str, base: str, title: str, token: str) -> int:
    body = {"title": title, "head": head, "base": base, "body": "Opened by Commit Wave."}
    return rest("POST", f"/repos/{owner}/{name}/pulls", token, body)["number"]


def merge_pull(owner: str, name: str, number: int, title: str, detail: str, token: str) -> str:
    """Squash merge and return the new head sha, so the next branch needs no extra lookup."""
    body = {"merge_method": "squash", "commit_title": title, "commit_message": detail}
    return rest("PUT", f"/repos/{owner}/{name}/pulls/{number}/merge", token, body)["sha"]


def delete_branch(owner: str, name: str, branch: str, token: str) -> None:
    rest("DELETE", f"/repos/{owner}/{name}/git/refs/heads/{branch}", token)


def merged_pull_count(login: str, token: str) -> int:
    """Count the account's merged pull requests through the search index.

    The index lags a merge by seconds to minutes, so a run that just finished can read low.
    """
    query = urllib.parse.quote(f"is:pr is:merged author:{login}")
    return rest("GET", f"/search/issues?q={query}&per_page=1", token)["total_count"]


def accepted_answer_count(login: str, token: str) -> int:
    """Count the account's discussion comments that were marked as the answer."""
    data = graphql(_ANSWER_COUNT, {"login": login}, token)
    return data["user"]["repositoryDiscussionComments"]["totalCount"]


def discussion_target(owner: str, name: str, token: str) -> tuple[str, str]:
    """Return the repository node id and an answerable category id."""
    repo = graphql(_REPOSITORY, {"owner": owner, "name": name}, token)["repository"]
    if not repo["hasDiscussionsEnabled"]:
        raise GitHubError(
            400,
            f"Discussions are off for {owner}/{name}. Turn them on under "
            "Settings, Features, Discussions.",
        )
    for category in repo["discussionCategories"]["nodes"]:
        if category["isAnswerable"]:
            return repo["id"], category["id"]
    raise GitHubError(
        400,
        f"{owner}/{name} has no question and answer category. GitHub exposes no API "
        "to create one, so add an answerable category in the repository settings.",
    )


def create_discussion(repo_id: str, category_id: str, title: str, body: str, token: str) -> str:
    variables = {"repositoryId": repo_id, "categoryId": category_id, "title": title, "body": body}
    return graphql(_CREATE_DISCUSSION, variables, token)["createDiscussion"]["discussion"]["id"]


def add_comment(discussion_id: str, body: str, token: str) -> str:
    """Add a top-level comment. A threaded reply cannot be marked as the answer."""
    variables = {"discussionId": discussion_id, "body": body}
    return graphql(_ADD_COMMENT, variables, token)["addDiscussionComment"]["comment"]["id"]


def mark_answer(comment_id: str, token: str) -> None:
    """Mark a comment as the answer. The token must belong to the discussion author."""
    graphql(_MARK_ANSWER, {"id": comment_id}, token)


def _request(method: str, url: str, token: str, body: dict | None = None) -> dict:
    payload = None if body is None else json.dumps(body).encode("utf-8")
    request = urllib.request.Request(url, data=payload, method=method)
    request.add_header("Authorization", f"Bearer {token}")
    request.add_header("Accept", "application/vnd.github+json")
    request.add_header("X-GitHub-Api-Version", API_VERSION)
    request.add_header("User-Agent", USER_AGENT)
    if payload is not None:
        request.add_header("Content-Type", "application/json")

    for attempt in range(MAX_RETRIES):
        try:
            with urllib.request.urlopen(request) as response:
                text = response.read().decode("utf-8")
            return json.loads(text) if text else {}
        except urllib.error.HTTPError as error:
            if error.code not in (403, 429) or attempt == MAX_RETRIES - 1:
                raise GitHubError(error.code, _message(error)) from error
            time.sleep(_backoff(error, attempt))

    raise GitHubError(429, "Gave up after retrying a rate-limited request")


def _backoff(error: urllib.error.HTTPError, attempt: int) -> float:
    """Wait in GitHub's documented order: retry-after, then the reset time, then a backoff.

    GitHub bans integrations that keep calling while limited, so this is correctness
    rather than politeness. The body text of a secondary limit is not documented, so
    nothing here branches on the message.
    """
    retry_after = (error.headers.get("retry-after") or "").strip()
    if retry_after.isdigit():
        return float(retry_after)

    reset = (error.headers.get("x-ratelimit-reset") or "").strip()
    if error.headers.get("x-ratelimit-remaining") == "0" and reset.isdigit():
        return max(1.0, float(reset) - time.time())

    return 60.0 * (2**attempt)


def _message(error: urllib.error.HTTPError) -> str:
    try:
        return json.loads(error.read().decode("utf-8")).get("message", str(error.reason))
    except (ValueError, OSError):
        return str(error.reason)


_REPOSITORY = """
query($owner: String!, $name: String!) {
  repository(owner: $owner, name: $name) {
    id
    hasDiscussionsEnabled
    discussionCategories(first: 25) {
      nodes { id name isAnswerable }
    }
  }
}
"""

_CREATE_DISCUSSION = """
mutation($repositoryId: ID!, $categoryId: ID!, $title: String!, $body: String!) {
  createDiscussion(input: {
    repositoryId: $repositoryId, categoryId: $categoryId, title: $title, body: $body
  }) { discussion { id url } }
}
"""

_ADD_COMMENT = """
mutation($discussionId: ID!, $body: String!) {
  addDiscussionComment(input: {discussionId: $discussionId, body: $body}) {
    comment { id url }
  }
}
"""

_MARK_ANSWER = """
mutation($id: ID!) {
  markDiscussionCommentAsAnswer(input: {id: $id}) {
    discussion { id isAnswered }
  }
}
"""

_ANSWER_COUNT = """
query($login: String!) {
  user(login: $login) {
    repositoryDiscussionComments(onlyAnswers: true, first: 1) { totalCount }
  }
}
"""
