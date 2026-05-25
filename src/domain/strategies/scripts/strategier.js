(function () {
    class Strategier {
        static verify() {
            this.Scraper = window.Scraper;
            this.Playground = window.Playground;

            if (!this.Scraper) {
                return { success: false, reason: 'Scraper not found' };
            }

            if (!this.Playground) {
                return { success: false, reason: 'Playground not found' };
            }

            return { success: true };
        }
    }

    window.Strategier = Strategier;
})()