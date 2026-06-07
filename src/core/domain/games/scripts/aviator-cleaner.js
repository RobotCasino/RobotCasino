(function () {
    class GameCleaner {
        start() {
            this.iframe = document.evaluate("//iframe[contains(@src, 'spribelaunch.com/aviator')]", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue
            this.contentDocument = this.iframe.contentDocument

            if (!this.contentDocument.body) {
                window.Scraper.exitWithMessage('Aviator frame not found. Please make sure you are on the Aviator game page.')
            }

            this.removeOtherBetsPanel()
            this.removeChat()
            this.removeSecondBetPanel()
            this.disableAnimations()
            this.removeAirstrip()
            this.removeBetCounting()
        }

        removeOtherBetsPanel() {
            this.querySelector('app-bets-widget')?.remove()
            this.querySelector('app-bets-widget .bets-block')?.remove()
            this.querySelector('.bets-widget-container')?.remove()
        }

        removeChat() {
            this.querySelector('.chat-bar.ng-star-inserted')?.remove()

            const gamePlay = this.querySelector('.game-play');
            const mainContaier = this.querySelector('.main-container');

            if (gamePlay) {
                gamePlay.style.setProperty('width', '100%', 'important');
            }

            if (mainContaier) {
                mainContaier.style.setProperty('width', '100%', 'important');
            }
        }

        removeSecondBetPanel() {
            this.querySelector('app-bet-control.double-bet.ng-star-inserted')?.remove()
        }

        removeBetCounting() {
            this.querySelector('app-active-players-widget')?.remove()
        }

        startConsoleCleaning() {
            if (this.consoleCleanerID) {
                clearInterval(this.consoleCleanerID)
            }
            this.consoleCleanerID = setInterval(() => {
                console.clear()
                if (typeof window.gc === 'function') {
                    window.gc()
                }
            }, 60000)
        }

        removeAirstrip() {
            this.querySelector('.play-board-wrapper')?.remove()
        }

        disableAnimations() {
            try {
                const style = this.contentDocument.createElement('style');
                style.textContent = '* { animation: none !important; transition: none !important; }';
                this.contentDocument.head?.appendChild(style);
            } catch (error) {

            }
        }

        querySelector(selector) {
            return this.contentDocument.querySelector(selector);
        }
    }

    window.GameCleaner = new GameCleaner()
})()