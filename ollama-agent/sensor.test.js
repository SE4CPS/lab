const assert = require('assert');
const { generateLux } = require('./sensor');

// AAA pattern: Arrange, Act, Assert
function testGenerateLuxDeterministic() {
    // Arrange: stub Math.random
    const originalRandom = Math.random;
    Math.random = () => 0; // minimum

    // Act
    const valueMin = generateLux();

    // Assert
    assert.strictEqual(valueMin, 0, 'Expected generateLux() to return 0 when Math.random() is 0');

    // Arrange
    Math.random = () => 0.9999; // just below 1

    // Act
    const valueMax = generateLux();

    // Assert
    assert.ok(valueMax >= 999 && valueMax < 1000, 'Expected generateLux() to be in [999,1000) when Math.random() is high');

    // Cleanup
    Math.random = originalRandom;
    console.log('testGenerateLuxDeterministic passed');
}

function testGenerateLuxRange() {
    // Arrange/Act and Assert in one go by calling multiple times and checking range
    for (let i = 0; i < 10; i++) {
        const val = generateLux();
        assert.ok(val >= 0 && val < 1000, `Value ${val} out of range`);
    }
    console.log('testGenerateLuxRange passed');
}

// run tests
if (require.main === module) {
    testGenerateLuxDeterministic();
    testGenerateLuxRange();
    console.log('All tests passed');
}
