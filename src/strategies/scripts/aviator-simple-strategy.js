(function () 
{
    class Strategy {

        constructor() {
            this.Strategier = window.Strategier

            const { success, reason } = this.Strategier.verify()
            
            if (!success) {
                return this.kill(`Strategy verification failed: ${reason}`)
            }

            this.Scraper = window.Scraper
            this.Playground = window.Playground
        }

        start() {

        }

        kill(message = null) {
            this.Scraper = this.Scraper ?? { exit: () => console.log('[EXIT]'), exitWithMessage: (msg) => console.log(`[EXIT] ${msg}`) }

            if (message != null) {
                return this.Scraper.exitWithMessage(message)
            }

            return this.Scraper.exit()
        }

    }

    const strategy = new Strategy()

    strategy.start()
})();


