class AviatorDomain {
    static isBlue(multiplier) {
        return multiplier >= 1 && multiplier < 2
    }

    static isPurple(multiplier) {
        return multiplier >= 2 && multiplier < 10
    }

    static isPink(multiplier) {
        return multiplier >= 10
    }

    static getColor(multiplier) {
        if (this.isBlue(multiplier)) {
            return 'blue'
        } else if (this.isPurple(multiplier)) {
            return 'purple'
        } else if (this.isPink(multiplier)) {
            return 'pink'
        }
    }
}

window._AviatorDomain = AviatorDomain;