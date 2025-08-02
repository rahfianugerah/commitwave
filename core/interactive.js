const readline = require('readline');
const { startCommitBot } = require('./commitBot');

// ASCII art printed to the console at startup
const asciiArt = `
 ██████╗ ██████╗ ███╗   ███╗███╗   ███╗██╗████████╗    ██╗    ██╗ █████╗ ██╗   ██╗███████╗
██╔════╝██╔═══██╗████╗ ████║████╗ ████║██║╚══██╔══╝    ██║    ██║██╔══██╗██║   ██║██╔════╝
██║     ██║   ██║██╔████╔██║██╔████╔██║██║   ██║       ██║ █╗ ██║███████║██║   ██║█████╗  
██║     ██║   ██║██║╚██╔╝██║██║╚██╔╝██║██║   ██║       ██║███╗██║██╔══██║╚██╗ ██╔╝██╔══╝  
╚██████╗╚██████╔╝██║ ╚═╝ ██║██║ ╚═╝ ██║██║   ██║       ╚███╔███╔╝██║  ██║ ╚████╔╝ ███████╗
 ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝     ╚═╝╚═╝   ╚═╝        ╚══╝╚══╝ ╚═╝  ╚═╝  ╚═══╝  ╚══════╝
`;

console.log(asciiArt);

/**
 * Returns a Promise that resolves after a specified time.
 * @param {number} ms - Milliseconds to sleep.
 */
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Simulates a typing effect when printing text to the console.
 * The function now accepts a header that is animated along with the message.
 *
 * @param {string} text - The text to print.
 * @param {number} [maxLength=95] - Maximum characters per line before wrapping.
 * @param {string} [header="Commit Wave: "] - The header to print before the text.
 */
async function typeLikeTyping(text, maxLength = 95, header = "Commit Wave: ") {
  // Print the header as part of the animation.
  process.stdout.write(header);
  let charCount = header.length;

  for (const char of text) {
    process.stdout.write(char);
    await sleep(Math.random() * (40 - 20) + 20); // Random delay between 20 and 40 ms
    charCount++;

    // Insert a new line with indentation if maxLength is reached and the character is a space.
    if (charCount >= maxLength && char === " ") {
      process.stdout.write("\n" + " ".repeat(header.length));
      charCount = 0;
    }
  }
  process.stdout.write("\n");
}

/**
 * Asks a question using the typing effect for the prompt, then waits for user input.
 *
 * @param {object} rl - Readline interface instance.
 * @param {string} question - The question to ask.
 * @param {string} [header="Commit Wave: "] - The header for the animated prompt.
 * @returns {Promise<string>} - Resolves with the user's input.
 */
function askQuestion(rl, question, header = "Commit Wave: ") {
  return new Promise(resolve => {
    typeLikeTyping(question, 95, header).then(() => {
      rl.question("", answer => resolve(answer));
    });
  });
}

/**
 * Initiates the interactive commit bot with animated prompts.
 */
async function startInteractive() {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  // Animate the welcome message
  await typeLikeTyping("Hello! I am your commit bot.", 95, "Commit Wave: ");

  // Use the animated typing effect for all prompts
  const startDateStr = await askQuestion(rl, "Please enter the start date (YYYY-MM-DD): ");
  const endDateStr = await askQuestion(rl, "Please enter the end date (YYYY-MM-DD): ");
  const numCommitsStr = await askQuestion(rl, "How many commits would you like to make? ");

  const numCommits = parseInt(numCommitsStr, 10);
  if (isNaN(numCommits) || numCommits <= 0) {
    await typeLikeTyping("Please enter a valid positive number for commits.", 95, "Commit Wave: ");
    rl.close();
    return;
  }

  await typeLikeTyping(`Great! I will make ${numCommits} commits from ${startDateStr} to ${endDateStr}.`, 95, "Commit Wave: ");
  startCommitBot(startDateStr, endDateStr, numCommits);
  rl.close();
}

module.exports = { startInteractive };
