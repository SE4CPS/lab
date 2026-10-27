// simple module to expose the light-value generator
function generateLux() {
    // same logic as the placeholder in index.html
    return Math.floor(Math.random() * 1000);
}

module.exports = { generateLux };
