// Detect browser/system language
function getDetectedLanguage() {
    const browserLang = (navigator.language || navigator.userLanguage || 'en').toLowerCase().split('-')[0];

    // If English or Russian, default to French
    if (browserLang === 'en' || browserLang === 'ru') {
        return 'fr';
    }

    // Map common languages to available languages
    const langMap = {
        'de': 'de',
        'es': 'es',
        'fr': 'fr',
        'it': 'it',
        'pt': 'pt'
    };

    return langMap[browserLang] || 'fr';
}

// Initialize app
function init() {
    const detectedLang = getDetectedLanguage();
    const thirdLanguageSelect = document.getElementById('thirdLanguage');
    thirdLanguageSelect.value = detectedLang;

    displayQuote();

    document.getElementById('newQuoteBtn').addEventListener('click', displayQuote);
    thirdLanguageSelect.addEventListener('change', displayQuote);
}

// Display quote from API
async function displayQuote() {
    try {
        const response = await fetch('/api/quote');
        if (!response.ok) throw new Error('Failed to fetch quote');

        const quote = await response.json();
        const thirdLang = document.getElementById('thirdLanguage').value;

        // Russian
        document.getElementById('quoteRussian').textContent = quote.russian;
        document.getElementById('attributeRussian').textContent = '— Ilya Prigogine';

        // English
        document.getElementById('quoteEnglish').textContent = quote.english;
        document.getElementById('attributeEnglish').textContent = '— Ilya Prigogine';

        // Custom language
        document.getElementById('quoteCustom').textContent = quote[thirdLang];
        document.getElementById('attributeCustom').textContent = '— Ilya Prigogine';

        // Update titles with quote gist
        document.getElementById('russianTitle').textContent = quote.gist;
        document.getElementById('englishTitle').textContent = quote.gist;
        document.getElementById('customTitle').textContent = quote.gist;
    } catch (error) {
        console.error('Error loading quote:', error);
        document.getElementById('quoteRussian').textContent = 'Error loading quote';
    }
}

// Start the app when DOM is ready
document.addEventListener('DOMContentLoaded', init);
