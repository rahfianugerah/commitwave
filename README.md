![Version](https://img.shields.io/badge/Version-1.0.0-green)
![Maintenance](https://img.shields.io/badge/Maintenance-Yes-green)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/rahfianugerah/scheduled-commit-bot/blob/main/LICENSE)
![Yaml](https://img.shields.io/badge/Made_with-Yaml-blue.svg)
![Github Action](https://img.shields.io/badge/GitHub_Workflows-%23121011.svg?&logo=github&logoColor=white)

<div align="center">
  <img src="https://github.com/rahfianugerah/scheduled-commit-bot/blob/main/img/newbot.png" height=150 width=150>
  <h3>
    Scheduled Commit Bot
  </h3>
  <p>
    An awesome bot that will maintain your github contribution history
  </p>
</div>

## Project Overview
<p align="justify">
  Scheduled Commit Bot is an automated tool designed to help developers maintain an active commit history on their GitHub repositories. Utilizing GitHub Actions, the bot generates and pushes random commits 1-2 times daily.
</p>

### 🤖 Bot Script:
```yml
name: Scheduled Commit Bot

on:
  schedule:
    - cron: '0 0 * * *'
    
jobs:
  commit:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v2

      - name: Set up Git
        run: |
          git config --global user.name 'username'
          git config --global user.email 'youremail@email.com'

      - name: Random number generation
        id: random
        # Generates a random number between 1 to 2
        run: echo "::set-output name=random_number::$(shuf -i 1-2 -n 1)" 

      - name: Make commits
        run: |
          for ((i=0; i<${{ steps.random.outputs.random_number }}; i++)); do
            echo "$(date)" >> commit.txt
            git add commit.txt
            git commit -m "Automated Commit at $(date)"
          done
          git push

```

⚠️ <b> Disclaimer: </b>

<p align="justify">
  Scheduled Commit Bot is designed to automate the process of creating commits to GitHub repositories. While this bot can be useful for maintaining a history of active commits, users should be aware of the potential and limitations associated with its use. This bot is intended for educational and experimental purposes. It should not be used to artificially inflate repository activity or misrepresent project progress.
</p> 


## Time Default

Runs at midnight every day (00:00 UTC) | Generate random commit (1 or 2)
```yml
on:
  schedule:
    - cron: '0 0 * * *'
```

Runs at 6 hours a day | Generate random 1 - 2 commit for every 6 hours (MAX 8)
```yml
on:
  schedule:
    - cron: '0 */6 * * *'
```


