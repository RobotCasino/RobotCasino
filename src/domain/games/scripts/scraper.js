(function() {
    class Scraper {
        static _exitEndpoint() {
            return 'http://127.0.0.1:8081/exit'
        }

        static _sendExit(message) {
            const payload = JSON.stringify({ message })
            let sent = false

            try {
                if (navigator.sendBeacon) {
                    const blob = new Blob([payload], { type: 'application/json' })
                    sent = navigator.sendBeacon(Scraper._exitEndpoint(), blob)
                }
            } catch (error) {
                sent = false
            }

            if (!sent) {
                fetch(Scraper._exitEndpoint(), {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: payload,
                    keepalive: true,
                }).catch(() => {})
            }
        }

        static log(message) {
            console.log(`[LOG] ${message}`)
        }

        static exit() {
            Scraper._sendExit(null)
        }

        static exitWithMessage(message) {
            Scraper._sendExit(message)
        }
    }

    window.Scraper = Scraper
})()