(function () {
    class Cleaner {
        static consoleCleanerID = null;
        static iframe = null;

        static Init() {
            Cleaner.iframe = document.evaluate("//iframe[contains(@src, 'spribelaunch.com/aviator')]", document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue
            Cleaner.contentDocument = Cleaner.iframe ? Cleaner.iframe.contentDocument : document

            if (!Cleaner.contentDocument.body) {
                window.Scraper.exitWithMessage('Aviator frame not found. Please make sure you are on the Aviator game page.')
            }

            Cleaner.RemoveOtherBetsPanel()
            Cleaner.RemoveChat()
            Cleaner.RemoveSecondBetPanel()
            Cleaner.DisableAnimations()
            Cleaner.RemoveAirstrip()
            Cleaner.RemoveBetCounting()
            Cleaner.RemoveOneWinSidebar()
            Cleaner.RemoveOneWinNav()
            Cleaner.RemoveOneWinFooter()
        }

        static RemoveOtherBetsPanel() {
            Cleaner.querySelector('app-bets-widget')?.remove()
            Cleaner.querySelector('app-bets-widget .bets-block')?.remove()
            Cleaner.querySelector('.bets-widget-container')?.remove()
        }

        static RemoveChat() {
            Cleaner.querySelector('.chat-bar.ng-star-inserted')?.remove()
            const gamePlay = Cleaner.querySelector('.game-play');
            if (gamePlay) {
                gamePlay.style.setProperty('width', '100%', 'important');
            }
        }

        static RemoveSecondBetPanel() {
            Cleaner.querySelector('app-bet-control.double-bet.ng-star-inserted')?.remove()
        }

        static RemoveBetCounting() {
            Cleaner.querySelector('app-active-players-widget')?.remove()
        }

        static RemoveOneWinSidebar() {
            document.querySelector('.common-layout_sleave-V7jCK.variant-1_sleave-Qr2MW')?.remove()
            document.querySelector('.common-layout_sheet-V7jCK')?.remove()
            document.querySelector('.common-layout_space-V7jCK')?.remove()
        }

        static RemoveOneWinNav() {
            document.querySelector('nav.segment-control_root-ehnrM.segment-control_variant-1-ehnrM')?.remove()
        }

        static RemoveOneWinFooter() {
            document.querySelector('.footer-container_root-Xk572')?.remove()
        }

        static StartConsoleCleaning() {
            if (Cleaner.consoleCleanerID) {
                clearInterval(Cleaner.consoleCleanerID)
            }
            Cleaner.consoleCleanerID = setInterval(() => {
                console.clear()
                if (typeof window.gc === 'function') {
                    window.gc()
                }
            }, 60000)
        }

        static RemoveAirstrip() {
            Cleaner.querySelector('.play-board-wrapper')?.remove()
        }

        static DisableAnimations() {
            try {
                const style = Cleaner.contentDocument.createElement('style');
                style.textContent = '* { animation: none !important; transition: none !important; }';
                Cleaner.contentDocument.head?.appendChild(style);
            } catch (error) {

            }
        }

        static querySelector(selector) {
            return Cleaner.contentDocument.querySelector(selector);
        }
    }

    window.Cleaner = Cleaner
})()