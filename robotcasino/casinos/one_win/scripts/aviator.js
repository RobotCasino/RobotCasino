(function() {
    const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            if (mutation.type === 'childList' || mutation.type === 'characterData') {
                const text = scoresDiv.textContent || scoresDiv.innerText;
                
                if (checkPattern(text)) {
                    betButton.click();
                    console.log('Bet button clicked via observer');
                }
            }
        });
    });
    
    observer.observe(scoresDiv, {
        childList: true,
        subtree: true,
        characterData: true
    });
})();