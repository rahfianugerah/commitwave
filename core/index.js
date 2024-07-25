const fs = require('fs');
const moment = require('moment');
const simpleGit = require('simple-git');
const LOG_PATH = './data/commit.txt';
const TEMP_FILE_PATH = './data/temp.txt';
const git = simpleGit();

const makeCommit = async (n, startDate, endDate) => {
    if (n === 0) {
        return git.push();
    }

    // Dynamically import the random module
    const { default: random } = await import('random');

    // Generate a random date within the provided range
    const randomTime = random.int(0, endDate.getTime() - startDate.getTime());
    const randomDate = new Date(startDate.getTime() + randomTime);
    const formattedDate = moment(randomDate).format('ddd MMM DD HH:mm:ss UTC YYYY');

    // Log the commit date
    fs.appendFileSync(LOG_PATH, `${formattedDate}\n`);

    // Create a temporary file to make a commit
    fs.writeFileSync(TEMP_FILE_PATH, formattedDate);

    await git.add(TEMP_FILE_PATH);
    await git.commit(formattedDate, { '--date': formattedDate });
    
    // Recur for the next commit
    await makeCommit(n - 1, startDate, endDate);
};

const startCommitBot = async (startDateStr, endDateStr, numberOfCommits) => {
    const startDate = new Date(startDateStr);
    const endDate = new Date(endDateStr);
    await makeCommit(numberOfCommits, startDate, endDate);
};

// Example usage
startCommitBot('2024-01-13', '2024-04-6', 52);