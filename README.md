![Version](https://img.shields.io/badge/Version-1.0.1-green)
![Maintenance](https://img.shields.io/badge/Maintenance-Yes-green)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/rahfianugerah/sch-bot/blob/main/LICENSE)
![JavaScript](https://img.shields.io/badge/Javascript-%23323330.svg?&logo=javascript&logoColor=%23F7DF1E)
![NodeJS](https://img.shields.io/badge/Node.js-6DA55F?&logo=node.js&logoColor=white)
![Yaml](https://img.shields.io/badge/Made_with-Yaml-blue.svg)
![Github Action](https://img.shields.io/badge/GitHub_Workflows-%23121011.svg?&logo=github&logoColor=white)

<div align="center">
  <img src="img/bot.png" height=150 width=150>
  <h3>
    SC-Bot
  </h3>
  <p>
    An awesome bot that will maintain your github contribution history
  </p>
</div>

## Project Overview
<p align="justify">
  The Scheduled Commit Bot is an advanced automation tool designed to help developers keep their GitHub repositories consistently active and engaging. By utilizing GitHub Actions, this bot automates the process of generating and pushing commits at random intervals within a user-defined date range.
</p>

<div align="center">
  <img src="https://github.com/user-attachments/assets/0b5df6aa-ad46-4b1f-a541-3d91c1e0fe62" height=150/>
</div>

## About Node.js
<p align="justify">
  Node.js is a popular, open-source, server-side runtime environment that allows developers to execute JavaScript code outside of a web browser. It is built on the V8 JavaScript engine, which is the same engine that powers Google Chrome, making it fast and efficient.
</p>

## Node.js Key Features
- Event-Driven Architecture:
Node.js operates on a non-blocking, event-driven architecture, which means it can handle multiple requests simultaneously. This makes it ideal for building scalable and high-performance applications, such as real-time chat applications, online games, and live streaming.

- Single-Threaded but Highly Scalable:
While Node.js uses a single thread for handling requests, it can manage many concurrent connections efficiently through its event loop mechanism. This allows Node.js to scale easily and handle a large number of simultaneous users without requiring significant resources.

- Non-Blocking I/O:
Node.js uses non-blocking I/O operations, which means it can perform multiple tasks simultaneously without waiting for one to complete before starting another. This is particularly useful for I/O-heavy applications like data streaming, file system interactions, and network communication.

- Cross-Platform:
Node.js is cross-platform, meaning it can run on various operating systems, including Windows, macOS, and Linux. This flexibility allows developers to build and deploy applications on different environments without compatibility issues.

## Disclaimer </b>
<p align="justify">
  Scheduled Commit Bot is designed to automate the process of creating commits to GitHub repositories. While this bot can be useful for maintaining a history of active commits, users should be aware of the potential and limitations associated with its use. This bot is intended for educational and experimental purposes. It should not be used to artificially inflate repository activity or misrepresent project progress.
</p> 

## Installation
- Clone this repository
```
git clone https://github.com/rahfianugerah/sc-bot
```
- Enter a date range & commit(s)
```javascript
//Example Usage startCommitBot(startDate, endDate, commits)
startCommitBot('2024-06-6', '2024-06-23', 18);
```
- Run the app
```
npm start
```

## Bot Script (Github Actions)
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

## Time Default

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


## License

[MIT](https://github.com/rahfianugerah/sch-bot/blob/main/LICENSE)

## Project Author
- GitHub: [@rahfianugerah](https://www.github.com/rahfianugerah)
