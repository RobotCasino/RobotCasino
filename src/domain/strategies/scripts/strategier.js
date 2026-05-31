(function () {
    class Strategier {
        static verify() {
            this.Scraper = window.Scraper;
            this.Playground = window.Playground;
            this.Util = window.Util;

            if (!this.Scraper) {
                return { success: false, reason: 'Scraper not found' };
            }

            if (!this.Playground) {
                return { success: false, reason: 'Playground not found' };
            }

            if (!this.Util) {
                return { success: false, reason: 'Util not found' };
            }

            return { success: true };
        }
    }

    window.Strategier = Strategier;
})()