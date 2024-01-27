const { Builder } = require('selenium-webdriver');
const fs = require('fs');
const path = require('path');
const firefox = require('selenium-webdriver/firefox');

const inputFolder = path.join(__dirname, 'input');
const outputFolder = path.join(__dirname, 'output');
const extensionsFolder = path.join(__dirname, 'extensions');

const sleep = (milliseconds) => new Promise(resolve => setTimeout(resolve, milliseconds));

async function captureScreenshot(title, url, screenshotFilename, uniqueId) {
    console.log(`Processing screenshot for ${title} - ${url}`);
    const geckoDriverPath = path.join(__dirname, 'geckodriver', 'geckodriver.exe');

    let driver = null;

    try {
        const firefoxOptions = new firefox.Options();

        firefoxOptions.windowSize({ width: 1920, height: 1080 });

        firefoxOptions.addExtensions(
            path.join(extensionsFolder, 'idcac-pub@guus.ninja.xpi'),
            path.join(extensionsFolder, 'uBlock0@raymondhill.net.xpi'),
            path.join(extensionsFolder, 'jid1-KKzOGWgsW3Ao4Q@jetpack.xpi'),
            path.join(extensionsFolder, '{d10d0bf8-f5b5-c8b4-a8b2-2b9879e08c5d}.xpi')
        );

        driver = await new Builder()
            .forBrowser('firefox')
            .setFirefoxOptions(firefoxOptions)
            .build();

        await driver.manage().setTimeouts({ implicit: 10000, pageLoad: 30000, script: 30000 });

        await driver.get(url);
        await sleep(5000);

        console.log(`Current URL: ${await driver.getCurrentUrl()}`);

        await driver.takeScreenshot().then(screenshot => {
            fs.writeFileSync(screenshotFilename, screenshot, 'base64');
            console.log(`Screenshot captured successfully for ${title} - ${url}`);
        });

    } catch (error) {
        console.error(`Error capturing screenshot for ${title} - ${url}: ${error}`);

    } finally {
        if (driver) {
            try {
                await driver.quit();
                console.log('Driver quit successfully.');

            } catch (quitError) {
                console.error(`Error quitting driver: ${quitError}`);
            }
        }
    }
}

async function processScreenshots() {
    const jsonFile = path.join(inputFolder, 'all.json');
    const jsonData = fs.readFileSync(jsonFile, 'utf-8');
    const data = jsonData.split('\n').map(line => JSON.parse(line.trim()));

    for (let idx = 0; idx < data.length; idx++) {
        const item = data[idx];
        const title = item.title || '';
        const url = item.web_site;
        const screenshot = item.screenshot !== false;

        if (url && screenshot) {
            const uniqueId = `${idx + 1}_${url.replace(/\s/g, '_').replace(/[^\w]/g, '')}`;
            const screenshotFilename = path.join(outputFolder, `${uniqueId}.png`);

            await captureScreenshot(title, url, screenshotFilename, uniqueId);
        }
    }
}

processScreenshots();
