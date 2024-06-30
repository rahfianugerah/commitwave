# Github Bot Commit

```yml
name: Scheduled Commit Bot

on:
  schedule:
    - cron: '0 */6 * * *'
    
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

