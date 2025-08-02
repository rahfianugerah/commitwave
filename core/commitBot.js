// commitBot.js
const path = require('path');
const { formatDate, getRandomDate } = require('../utils/dateUtils');
const { gitAdd, gitCommit, gitPush } = require('./gitOperations');
const { logCommit, writeTempFile, dataDir } = require('../utils/fileUtils');

const LOG_PATH = path.join(dataDir, 'commit.txt');
const TEMP_FILE_PATH = path.join(dataDir, 'temp.txt');

/**
 * Recursively makes commits with random dates.
 */
function makeCommit(n, startDate, endDate) {
  if (n <= 0) {
    try {
      const pushResult = gitPush();
      console.log("Commit Wave: All commits are done. Pushed to remote successfully.");
    } catch (error) {
      console.error("Commit Wave: Error pushing to remote:", error.message);
    }
    return;
  }

  const randomDate = getRandomDate(startDate, endDate);
  const formattedDate = formatDate(randomDate);

  // Log the commit date and update the temporary file.
  logCommit(LOG_PATH, formattedDate);
  writeTempFile(TEMP_FILE_PATH, formattedDate);

  try {
    gitAdd(TEMP_FILE_PATH);
    gitCommit(formattedDate, formattedDate);
    console.log(`Commit Wave: Committed with date: ${formattedDate}`);
  } catch (error) {
    console.error("Commit Wave: Error during commit:", error.message);
  }

  // Recur for the next commit.
  makeCommit(n - 1, startDate, endDate);
}

/**
 * Starts the commit bot by converting the provided string dates
 * into Date objects and beginning the commit process.
 */

function startCommitBot(startDateStr, endDateStr, numberOfCommits) {
  const startDate = new Date(startDateStr);
  const endDate = new Date(endDateStr);
  console.log(`Commit Wave: Starting commits between ${startDate.toDateString()} and ${endDate.toDateString()}...`);
  makeCommit(numberOfCommits, startDate, endDate);
}

module.exports = { startCommitBot };
