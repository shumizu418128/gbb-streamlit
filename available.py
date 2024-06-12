import requests
from datetime import datetime, timedelta

years = [2024, 2023]


def get_last_updated():
    # GitHubリポジトリの情報
    owner = "shumizu418128"
    repo = "gbb-streamlit"

    # GitHub API URL
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"

    # APIリクエストを送信してコミット情報を取得
    response = requests.get(url)
    commits = response.json()

    # 最終コミットの日付を取得
    if response.status_code == 200 and len(commits) > 0:
        last_commit_date = commits[0]['commit']['committer']['date']
        last_updated = datetime.strptime(last_commit_date, "%Y-%m-%dT%H:%M:%SZ")

        # 日本時間に変換
        last_updated += timedelta(hours=9)

        last_updated_str = last_updated.strftime("%Y-%m-%d %H:%M:%S") + " JST"

    else:
        last_updated_str = "取得エラー"

    return last_updated_str
