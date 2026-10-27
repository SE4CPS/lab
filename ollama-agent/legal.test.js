const assert = require('assert');
const fs = require('fs');

// Simple tests to ensure basic legal/compliance artifacts are present

function testLicenseFileExists() {
    // Arrange
    const path = './LICENSE';

    // Act
    const exists = fs.existsSync(path);

    // Assert
    assert.ok(exists, 'A LICENSE file should be present in the repository');
    console.log('testLicenseFileExists passed');
}

function testReadmeContainsPrivacy() {
    // Arrange
    const md = fs.readFileSync('README.md', 'utf8');

    // Act & Assert
    assert.ok(md.toLowerCase().includes('privacy'), 'README should mention privacy or data policy');
    console.log('testReadmeContainsPrivacy passed');
}

if (require.main === module) {
    testLicenseFileExists();
    testReadmeContainsPrivacy();
    console.log('Legal requirement tests completed');
}
