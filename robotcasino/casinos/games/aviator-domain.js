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
}

window.AviatorDomain = AviatorDomain;fdsfaasdfsdaf