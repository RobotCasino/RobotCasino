(function () {
    class Provider {
        constructor() {
            this.Scraper = null
            this.Playground = null
            this.Util = null
        }

        retrieve() {
            this.Scraper = window.Scraper || null
            this.Playground = window.Playground || null
            this.Util = window.Util || null

            return {
                success: !!this.Scraper && !!this.Playground && !!this.Util,
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

            return { success: true }
        }
    }

    window.Provider = new Provider()
})()
