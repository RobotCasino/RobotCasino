(function() {
    class Cleaner {
        static consoleCleanerID = null;
        static iframe = null;

        static Init() {
            Cleaner.iframe = document.evaluate("//iframe[contains(@src, 'spribelaunch.com/aviator')]", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
            Cleaner.contentDocument = Cleaner.iframe ? Cleaner.iframe.contentDocument : document;
            
            if (!Cleaner.contentDocument.body) {
                window.Scraper.exitWithMessage('Aviator frame not found. Please make sure you are on the Aviator game page.');
            }

            Cleaner.DisableAnimations();
            Cleaner.FilterConsoleNoise();
        }

        static RemoveOtherBetsPanel() {
            Cleaner.querySelector('app-bets-widget .bets-block')?.remove();
        }

        static RemoveChat() {
            Cleaner.querySelector('.chat-bar.ng-star-inserted')?.remove();
        }

        static RemoveSecondBetPanel() {
            Cleaner.querySelector('app-bet-control.double-bet.ng-star-inserted')?.remove();
        }

        static StartConsoleCleaning() {
            if (Cleaner.consoleCleanerID) {
                clearInterval(Cleaner.consoleCleanerID);
            }
            Cleaner.consoleCleanerID = setInterval(() => {
                console.clear();
                if (typeof window.gc === 'function') {
                    window.gc();
                }
            }, 60000);
        }

        static DisableAnimations() {
            try {
                const style = Cleaner.contentDocument.createElement('style');
                style.textContent = '* { animation: none !important; transition: none !important; }';
                Cleaner.contentDocument.head?.appendChild(style);
            } catch (error) {
                // Ignore style injection failures
            }
        }

        static FilterConsoleNoise() {
            const allow = (args) => typeof args[0] === 'string' && args[0].startsWith('[');
            const originalLog = console.log.bind(console);
            const originalInfo = console.info.bind(console);
            const originalWarn = console.warn.bind(console);

            console.log = (...args) => { if (allow(args)) originalLog(...args); };
            console.info = (...args) => { if (allow(args)) originalInfo(...args); };
            console.warn = (...args) => { if (allow(args)) originalWarn(...args); };
        }

        static querySelector(selector) {
            return Cleaner.contentDocument.querySelector(selector);
        }
    }

    window.Cleaner = Cleaner
})()