(function() {
    class Domain {
        isBlue(multiplier) {
            return multiplier >= 1 && multiplier < 2
        }

        isPurple(multiplier) {
            return multiplier >= 2 && multiplier < 10
        }

        isPink(multiplier) {
            return multiplier >= 10
        }

        getResult(multiplier, autoWithdrawal) {
            return multiplier < autoWithdrawal ? 'LOST' : 'WON'
        }
    }

    window.Domain = new Domain();
})()