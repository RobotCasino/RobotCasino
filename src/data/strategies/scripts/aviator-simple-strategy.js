(function () 
{
    class Strategy {
        constructor() {
            this.Provider = window.Provider

            const { success, reason } = this.Provider.verify()
            
            if (!success) {
                return this.kill(`Strategy verification failed: ${reason}`)
            }

            this.Scraper = this.Provider.Scraper
            this.Playground = this.Provider.Playground
            this.Util = this.Provider.Util

            this.Scraper.log('Strategy initialized successfully')
        }

        start() {
            this.Util.observe(this.Playground.payoutsBlock, (node, mutation) => {
                window.Scraper.log(`New payout: ${node.textContent}`)
            })
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

    window.Strategy = strategy

    strategy.start()
})();


