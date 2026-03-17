// Prigogine quotes in multiple languages
const quotes = [
    {
        russian: "Время и опыт - те факторы, которые преобразуют жизнь.",
        english: "Time and experience are the factors that transform life.",
        fr: "Le temps et l'expérience sont les facteurs qui transforment la vie.",
        de: "Zeit und Erfahrung sind die Faktoren, die das Leben verändern.",
        es: "El tiempo y la experiencia son los factores que transforman la vida.",
        it: "Il tempo e l'esperienza sono i fattori che trasformano la vita.",
        pt: "O tempo e a experiência são os fatores que transformam a vida.",
        ja: "時間と経験は人生を変える要因です。",
        zh: "时间和经验是改变生活的因素。",
        ar: "الوقت والخبرة هما العاملان اللذان يغيران الحياة."
    },
    {
        russian: "Мы находимся в авангарде времени, но с корнями в прошлом.",
        english: "We are at the vanguard of time, but rooted in the past.",
        fr: "Nous sommes à l'avant-garde du temps, mais enracinés dans le passé.",
        de: "Wir sind an der Spitze der Zeit, aber in der Vergangenheit verwurzelt.",
        es: "Estamos en la vanguardia del tiempo, pero enraizados en el pasado.",
        it: "Siamo all'avanguardia del tempo, ma radicati nel passato.",
        pt: "Estamos na vanguarda do tempo, mas enraizados no passado.",
        ja: "私たちは時代の先端にいますが、過去に根ざしています。",
        zh: "我们走在时代的最前沿，但根植于过去。",
        ar: "نحن في طليعة الوقت، لكننا متجذرون في الماضي."
    },
    {
        russian: "Хаос - это источник порядка, и порядок производит хаос.",
        english: "Chaos is the source of order, and order produces chaos.",
        fr: "Le chaos est la source de l'ordre, et l'ordre produit le chaos.",
        de: "Chaos ist die Quelle der Ordnung, und Ordnung erzeugt Chaos.",
        es: "El caos es la fuente del orden, y el orden produce caos.",
        it: "Il caos è la fonte dell'ordine, e l'ordine produce caos.",
        pt: "O caos é a fonte da ordem, e a ordem produz caos.",
        ja: "カオスは秩序の源であり、秩序はカオスを生み出します。",
        zh: "混沌是秩序的源头，秩序产生混沌。",
        ar: "الفوضى هي مصدر النظام، والنظام ينتج الفوضى."
    },
    {
        russian: "В необратимом времени мы обретаем смысл.",
        english: "In irreversible time, we find meaning.",
        fr: "Dans le temps irréversible, nous trouvons du sens.",
        de: "In irreversibler Zeit finden wir Sinn.",
        es: "En el tiempo irreversible, encontramos significado.",
        it: "Nel tempo irreversibile, troviamo significato.",
        pt: "No tempo irreversível, encontramos significado.",
        ja: "不可逆的な時間の中に、私たちは意味を見つけます。",
        zh: "在不可逆的时间中，我们发现了意义。",
        ar: "في الوقت غير القابل للعودة، نجد المعنى."
    },
    {
        russian: "Природа - это диалог между человеком и универсумом.",
        english: "Nature is a dialogue between man and the universe.",
        fr: "La nature est un dialogue entre l'homme et l'univers.",
        de: "Die Natur ist ein Dialog zwischen dem Menschen und dem Universum.",
        es: "La naturaleza es un diálogo entre el hombre y el universo.",
        it: "La natura è un dialogo tra l'uomo e l'universo.",
        pt: "A natureza é um diálogo entre o homem e o universo.",
        ja: "自然は人間と宇宙の間の対話です。",
        zh: "自然是人与宇宙之间的对话。",
        ar: "الطبيعة هي حوار بين الإنسان والكون."
    },
    {
        russian: "Энтропия - это не просто беспорядок, это творчество.",
        english: "Entropy is not merely disorder; it is creativity.",
        fr: "L'entropie n'est pas seulement le désordre ; c'est la créativité.",
        de: "Entropie ist nicht nur Unordnung; es ist Kreativität.",
        es: "La entropía no es solo desorden; es creatividad.",
        it: "L'entropia non è solo disordine; è creatività.",
        pt: "A entropia não é apenas desordem; é criatividade.",
        ja: "エントロピーは単なる無秩序ではなく、創造性です。",
        zh: "熵不仅仅是混乱，它是创造力。",
        ar: "الإنتروبيا ليست مجرد فوضى؛ إنها الإبداع."
    },
    {
        russian: "Мир усложняется, становится более интересным и более непредсказуемым.",
        english: "The world becomes more complex, more interesting, and more unpredictable.",
        fr: "Le monde devient plus complexe, plus intéressant et plus imprévisible.",
        de: "Die Welt wird komplexer, interessanter und unvorhersehbarer.",
        es: "El mundo se vuelve más complejo, más interesante e impredecible.",
        it: "Il mondo diventa più complesso, più interessante e più imprevedibile.",
        pt: "O mundo fica mais complexo, mais interessante e mais imprevisível.",
        ja: "世界はより複雑になり、より興味深く、より予測不可能になります。",
        zh: "世界变得更加复杂、更加有趣、更加不可预测。",
        ar: "يصبح العالم أكثر تعقيداً وأكثر إثارة للاهتمام وأقل قابلية للتنبؤ."
    },
    {
        russian: "Будущее не определено, оно развивается через нас.",
        english: "The future is not determined; it evolves through us.",
        fr: "L'avenir n'est pas déterminé ; il évolue à travers nous.",
        de: "Die Zukunft ist nicht bestimmt; sie entwickelt sich durch uns.",
        es: "El futuro no está determinado; evoluciona a través de nosotros.",
        it: "Il futuro non è determinato; si evolve attraverso di noi.",
        pt: "O futuro não é determinado; evolui através de nós.",
        ja: "未来は決まっていません。それは私たちを通じて進化します。",
        zh: "未来不是决定的，它通过我们发展。",
        ar: "المستقبل ليس محدداً؛ فهو يتطور من خلالنا."
    }
];

// Language display names
const languageNames = {
    'fr': 'French (Français)',
    'de': 'German (Deutsch)',
    'es': 'Spanish (Español)',
    'it': 'Italian (Italiano)',
    'pt': 'Portuguese (Português)',
    'ja': 'Japanese (日本語)',
    'zh': 'Chinese (中文)',
    'ar': 'Arabic (العربية)'
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

// Display random quote
function displayQuote() {
    const randomIndex = Math.floor(Math.random() * quotes.length);
    const quote = quotes[randomIndex];
    const thirdLang = document.getElementById('thirdLanguage').value;

    // Russian
    document.getElementById('quoteRussian').textContent = quote.russian;
    document.getElementById('attributeRussian').textContent = '— Ilya Prigogine';

    // English
    document.getElementById('quoteEnglish').textContent = quote.english;
    document.getElementById('attributeEnglish').textContent = '— Ilya Prigogine';

    // Custom language
    const customQuoteKey = thirdLang;
    document.getElementById('quoteCustom').textContent = quote[customQuoteKey];
    document.getElementById('attributeCustom').textContent = '— Ilya Prigogine';

    // Update custom language title
    document.getElementById('customLanguageName').textContent = languageNames[thirdLang];
}

// Start the app when DOM is ready
document.addEventListener('DOMContentLoaded', init);
