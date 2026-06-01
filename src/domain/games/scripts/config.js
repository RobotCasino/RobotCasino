(function() {

    class Config {

        constructor() {
            this.isTesting = {IS_TESTING} ?? null

            if (this.isTestingMode()) {
                this.fakeAmount = {FAKE_AMOUNT} ?? null

                this.getFakeAmount = () => this.fakeAmount
            }

            this.stopLoss = {STOP_LOSS} ?? null

            this.stopLossTries = {STOP_LOSS_TRIES} ?? null

            this.autoCashout = {AUTO_CASHOUT} ?? null
        }

        isTestingMode() {
            return this.isTesting ?? false
        }

        getStopLoss() {
            return this.stopLoss
        }

        getStopLossTries() {
            return this.stopLossTries
        }
        
        getAutoCashout() {
            return this.autoCashout
        }
    }
    
    window.Config = new Config()
})()