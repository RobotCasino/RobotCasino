(function () {
    class Provider {
        constructor() {
            this.Scraper = null
            this.Playground = null
            this.Util = null
            this.Domain = null
            this.GameCleaner = null
            this.CasinoCleaner = null
        }

        retrieve() {
            this.Scraper = window.Scraper || null
            this.Playground = window.Playground || null
            this.Util = window.Util || null
            this.Domain = window.Domain || null
            this.GameCleaner = window.GameCleaner || null
            this.CasinoCleaner = window.CasinoCleaner || null

            return {
                success: !!this.Scraper && !!this.Playground && !!this.Util && !!this.Domain && !!this.GameCleaner && !!this.CasinoCleaner,
            }
        }

        verify() {
            const res = this.retrieve()

            if (!this.Scraper) {
                return { success: false, reason: 'Scraper not found' }
            }

            if (!this.Playground) {
                return { success: false, reason: 'Playground not found' }
            }

            if (!this.Util) {
                return { success: false, reason: 'Util not found' }
            }

            if (!this.GameCleaner) {
                return { success: false, reason: 'GameCleaner not found' }
            }

            if (!this.CasinoCleaner) {
                return { success: false, reason: 'CasinoCleaner not found' }
            }

            return { success: true }
        }
    }

    window.Provider = new Provider()
})()
