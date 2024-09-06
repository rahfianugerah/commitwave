![Version](https://img.shields.io/badge/Version-1.0.1-green)
![Maintenance](https://img.shields.io/badge/Maintenance-Yes-green)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/rahfianugerah/sch-bot/blob/main/LICENSE)
![JavaScript](https://img.shields.io/badge/JavaScript-%23323330.svg?&logo=javascript&logoColor=%23F7DF1E)
![NodeJS](https://img.shields.io/badge/Node.js-6DA55F?&logo=node.js&logoColor=white)
![Github Action](https://img.shields.io/badge/GitHub_Action-%23121011.svg?&logo=github&logoColor=white)

<div align="center">
  <img src="img/bot.png" height=150 width=150>
  <h3>
    Commit Wave
  </h3>
  <p>
    An awesome bot that will maintain your github contribution history
  </p>
</div>

#### Project Overview
<p align="justify">
  Commit Wave is an automation tool designed to help developers keep their GitHub contribution history consistently active and engaging. By utilizing GitHub Actions or JavaScript based, this bot automates the process of generating and pushing commits at random intervals [GitHub Action & JavaScript] within a user-defined date range [JavaScript].
</p>

#### Key Features
- Automatic Commit Scheduling: Automatically executes commits.
- Randomized Commit Timing: Commits are made at random times each day to simulate consistent activity without a predictable pattern.
- Date Interval Commit: Commits are spaced out based on a configurable date interval.
- Commit Graph Maintenance: Keeps the GitHub commit graph full and active.
- Simple Configuration: Easy setup with minimal configuration required to start automating commits.

#### Getting Started
<p align="justify">
  
To get started with this project, please refer to the <a href=#installation-guide>Installation Guide</a> and <a href=#usage-instructions>User Instruction</a> in the documentation. For additional information on contributing, please check out the Contributing Guidelines [N/A].
</p>

#### Disclaimer </b>
<p align="justify">
  Commit Wave is designed to automate the process of creating commits to GitHub repositories. While this bot can be useful for maintaining a history of active commits, users should be aware of the potential and limitations associated with its use. This bot is intended for educational and experimental purposes. It should not be used to artificially inflate repository activity or misrepresent project progress [<b>only 1 repository that can contain this bot and you're prohibited to insert this bot to other repository</b>].
</p> 

#### Installation Guide

- Clone this repository
```
git clone https://github.com/rahfianugerah/sc-bot
```

#### Usage Instructions

- Enter a date range and commit(s)
```javascript
//Example Usage startCommitBot(startDate, endDate, commits)
startCommitBot('2024-06-6', '2024-06-23', 18);
```

- Run the app
```
npm start
```

#### Bot Script (Github Actions Script)

<p align="justify">
The Commit Wave project leverages a GitHub Actions script to automate commit operations. This script is configured to run on a schedule, performing 1-2 commits daily at random times. By utilizing GitHub Actions, the script ensures seamless integration with GitHub’s ecosystem, automatically pushing changes to maintain an active commit graph. The script is designed for simplicity and reliability, making it easy to set up and manage automated commits directly within your GitHub repository.
</p>

```yml
name: Bot

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

#### Time Configuration

<p align="justify">
Commit Wave allows you to customize the timing of automated commits through flexible time configuration settings. You can specify the frequency and interval between commits. The tool ensures that commits are made at random times within the defined intervals, maintaining a dynamic and active commit graph. Below are the default example of the time configuration and you a can adjust the timing anytime you like:
</p>

- Runs at midnight every day (00:00 UTC)
```yml
on:
  schedule:
    - cron: '0 0 * * *'
```

- Runs at 6 hours a day
```yml
on:
  schedule:
    - cron: '0 */6 * * *'
```


#### License
<p align="justify">
This project is licensed under the MIT License. This means you are free to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software. The full text of the license is available in the <a href="https://github.com/rahfianugerah/sch-bot/blob/main/LICENSE">LICENSE</a> file. By using this project, you agree to include the license notice and disclaimers in all copies or substantial portions of the Software. For more details on the terms and conditions of the MIT License, please refer to the license file.
</p>

#### Project Author
GitHub: [@rahfianugerah](https://www.github.com/rahfianugerah)
