(function() {
    if (window.__RobotcasinoScraperLoaded) {
        return;
    }
    window.__RobotcasinoScraperLoaded = true;

    class Scraper {
        static log(message) {
            console.log(`[LOG] ${message}`)
        }

        static exit() {
            console.log('[EXIT]')
        }

        static exitWithMessage(message) {
            console.log(`[EXIT] ${message}`)
        }
    }

    window.Scraper = Scraper
})()