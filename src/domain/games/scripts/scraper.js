(function() {
    class Scraper {
        static playing(message = null) {
            if (message != null) {
                console.log(`[PLAYING] ${message}`)
            } else {
                console.log('[PLAYING]')
            }
        }

        static observing(message = null) {
            if (message != null) {
                console.log(`[OBSERVING] ${message}`)
            } else {
                console.log('[OBSERVING]')
            }
        }

        static waiting(message = null) {
            if (message != null) {
                console.log(`[WAITING] ${message}`)
            } else {
                console.log('[WAITING]')
            }
        }

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