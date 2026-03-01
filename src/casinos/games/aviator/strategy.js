class Strategy {
    constructor() {
        this.onWinCallback = null
        this.onLossCallback = null
    }

    onWin(onWinCallback) {
        this.onWinCallback = onWinCallback
    }

    onLoss(onLossCallback) {
        this.onLossCallback = onLossCallback
    }
}