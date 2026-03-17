// Language codes to names mapping
const languageNames = {
    'ru': { en: 'Russian', native: 'Русский' },
    'en': { en: 'English', native: 'English' },
    'fr': { en: 'French', native: 'Français' },
    'de': { en: 'German', native: 'Deutsch' },
    'es': { en: 'Spanish', native: 'Español' },
    'it': { en: 'Italian', native: 'Italiano' },
    'pt': { en: 'Portuguese', native: 'Português' },
    'ja': { en: 'Japanese', native: '日本語' },
    'zh': { en: 'Chinese', native: '中文' },
    'ar': { en: 'Arabic', native: 'العربية' }
};

// Author signature in different languages
const authorSignatures = {
    'ru': '— Илья Пригожин',
    'en': '— Ilya Prigogine',
    'fr': '— Ilya Prigogine',
    'de': '— Ilya Prigogine',
    'es': '— Ilya Prigogine',
    'it': '— Ilya Prigogine',
    'pt': '— Ilya Prigogine',
    'ja': '— イリヤ・プリゴジン',
    'zh': '— 伊利亚·普里戈津',
    'ar': '— إيليا بريغوجين'
};

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
        'pt': 'pt',
        'ja': 'ja',
        'zh': 'zh',
        'ar': 'ar'
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
        document.getElementById('attributeRussian').textContent = authorSignatures['ru'] || '— Илья Пригожин';
        document.getElementById('russianTitle').textContent = quote.gist_ru || quote.gist;

        // English
        document.getElementById('quoteEnglish').textContent = quote.english;
        document.getElementById('attributeEnglish').textContent = authorSignatures['en'] || '— Ilya Prigogine';
        document.getElementById('englishTitle').textContent = quote.gist_en || quote.gist;

        // Custom language
        document.getElementById('quoteCustom').textContent = quote[thirdLang];
        document.getElementById('attributeCustom').textContent = authorSignatures[thirdLang] || '— Ilya Prigogine';
        const gistKey = `gist_${thirdLang}`;
        document.getElementById('customTitle').textContent = quote[gistKey] || quote.gist;
    } catch (error) {
        console.error('Error loading quote:', error);
        document.getElementById('quoteRussian').textContent = 'Error loading quote';
    }
}

// Start the app when DOM is ready
document.addEventListener('DOMContentLoaded', init);
