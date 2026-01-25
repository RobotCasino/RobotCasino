window._invokeFatalError = (message) => {
    if (!window._robotcasinoErrorQueue) {
        window._robotcasinoErrorQueue = [];
    }

    window._robotcasinoErrorQueue.push(message);
    window._robotcasinoIsFatalError = true;
}
