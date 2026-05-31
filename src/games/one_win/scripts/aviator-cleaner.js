(function () {
    class Cleaner {
        constructor() {
            this.iframe = document.evaluate("//iframe[contains(@src, 'spribelaunch.com/aviator')]", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue
            this.contentDocument = this.iframe ? this.iframe.contentDocument : document

            if (!this.contentDocument.body) {
                window.Scraper.exitWithMessage('Aviator frame not found. Please make sure you are on the Aviator game page.')
            }

            this.RemoveOtherBetsPanel()
            this.RemoveChat()
            this.RemoveSecondBetPanel()
            this.DisableAnimations()
            this.RemoveAirstrip()
            this.RemoveBetCounting()
            this.RemoveOneWinSidebar()
            this.RemoveOneWinNav()
            this.RemoveOneWinFooter()
        }

        RemoveOtherBetsPanel() {
            this.querySelector('app-bets-widget')?.remove()
            this.querySelector('app-bets-widget .bets-block')?.remove()
            this.querySelector('.bets-widget-container')?.remove()
        }

        RemoveChat() {
            this.querySelector('.chat-bar.ng-star-inserted')?.remove()
            const gamePlay = this.querySelector('.game-play');
            if (gamePlay) {
                gamePlay.style.setProperty('width', '100%', 'important');
            }
        }

        RemoveSecondBetPanel() {
            this.querySelector('app-bet-control.double-bet.ng-star-inserted')?.remove()
        }

        RemoveBetCounting() {
            this.querySelector('app-active-players-widget')?.remove()
        }

        RemoveOneWinSidebar() {
            document.querySelector('.common-layout_sleave-V7jCK.variant-1_sleave-Qr2MW')?.remove()
            document.querySelector('.common-layout_sheet-V7jCK')?.remove()
            document.querySelector('.common-layout_space-V7jCK')?.remove()
        }

        RemoveOneWinNav() {
            document.querySelector('nav.segment-control_root-ehnrM.segment-control_variant-1-ehnrM')?.remove()
        }

        RemoveOneWinFooter() {
            document.querySelector('.footer-container_root-Xk572')?.remove()
        }

        StartConsoleCleaning() {
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

        RemoveAirstrip() {
            this.querySelector('.play-board-wrapper')?.remove()
        }

        DisableAnimations() {
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

    window.Cleaner = new Cleaner()
})()