# llm-code-review-action
A container GitHub Action to review a pull request by Bedrock based AI models.

## Pre-requisites
User needs to set up AWS Access Key, AWS Secret Key, AWS Session Token first

## Inputs

- `githubToken`: The GitHub token to access the GitHub API.
- `githubRepository`: The GitHub repository to post a review comment.
- `githubPullRequestNumber`: The GitHub pull request number to post a review comment.
- `gitCommitHash`: The git commit hash to post a review comment.
- `pullRequestDiff`: The diff of the pull request to generate a review comment.
- `pullRequestDiffChunkSize`: The chunk size of the diff of the pull request to generate a review comment.
- `temperature`: The temperature to generate a review comment.
- `topP`: The top_p to generate a review comment.
- `topK`: The top_k to generate a review comment.
- `maxNewTokens`: The max_tokens to generate a review comment.
- `logLevel`: The log level to print logs.


## Example usage
Here is an example to use the Action to review a pull request of the repository.
The actual file is located at [`.github/workflows/test.yml`](.github/workflows/test.yml).


```yaml
name: "Test Code Review"

on:
  pull_request:
    paths-ignore:
      - "*.md"
      - "LICENSE"

jobs:
  review:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
    steps:
      - uses: actions/checkout@v3
      - name: "Get diff of the pull request"
        id: get_diff
        shell: bash
        env:
          PULL_REQUEST_HEAD_REF: "${{ github.event.pull_request.head.ref }}"
        run: |-
          git fetch origin "${{ env.PULL_REQUEST_HEAD_REF }}:${{ env.PULL_REQUEST_HEAD_REF }}"
          git checkout "${{ env.PULL_REQUEST_HEAD_REF }}"
          git diff "origin/${{ env.PULL_REQUEST_HEAD_REF }}" > "diff.txt"
          # shellcheck disable=SC2086
          echo "diff=$(cat "diff.txt")" >> $GITHUB_ENV
      - uses: digitalneedstech/LLM-Code-Review@1.0.1
        name: "AI Code Review"
        id: code-review
        with:
          githubToken: ${{ secrets.GITHUB_TOKEN }}
          githubRepository: ${{ github.repository }}
          githubPullRequestNumber: ${{ github.event.pull_request.number }}
          gitCommitHash: ${{ github.event.pull_request.head.sha }}
          temperature: "0.2"
          maxNewTokens: "250"
          topK: "50"
          topP: "0.95"
          pullRequestDiff: |-
            ${{ steps.get_diff.outputs.pull_request_diff }}
          pullRequestChunkSize: "3500"
          logLevel: "DEBUG"
```
