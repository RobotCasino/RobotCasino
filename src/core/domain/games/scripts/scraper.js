(function() {
    class Scraper {
        playing(message = null) {
            if (message != null) {
                console.log(`[PLAYING] ${message}`)
            } else {
                console.log('[PLAYING]')
            }
        }

        observing(message = null) {
            if (message != null) {
                console.log(`[OBSERVING] ${message}`)
            } else {
                console.log('[OBSERVING]')
            }
        }

        waiting(message = null) {
            if (message != null) {
                console.log(`[WAITING] ${message}`)
            } else {
                console.log('[WAITING]')
            }
        }

        log(message) {
            console.log(`[LOG] ${message}`)
        }

        exit() {
            console.log('[EXIT]')
        }

        exitWithMessage(message) {
            console.log(`[EXIT] ${message}`)
        }
    }

    window.Scraper = new Scraper()
})()