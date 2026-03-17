#!/usr/bin/env python3
"""
HTTP server for the Prigogine quotes app with API endpoint
"""
import http.server
import socketserver
import os
import json
import random
from pathlib import Path
from urllib.parse import urlparse

PORT = 8000

# Prigogine quotes with gists and translations
QUOTES = [
    {
        "gist": "Time Transforms Life",
        "gist_ru": "Время преобразует жизнь",
        "gist_en": "Time Transforms Life",
        "gist_fr": "Le temps transforme la vie",
        "gist_de": "Zeit transformiert das Leben",
        "gist_es": "El tiempo transforma la vida",
        "russian": "Время и опыт - те факторы, которые преобразуют жизнь. Мы не просто наблюдаем течение времени; мы участвуем в нём, и через это участие наша жизнь приобретает новые смыслы и направления.",
        "english": "Time and experience are the factors that transform life. We do not merely observe the passage of time; we participate in it, and through this participation our lives acquire new meanings and directions.",
        "fr": "Le temps et l'expérience sont les facteurs qui transforment la vie. Nous ne faisons pas que observer le passage du temps; nous y participons, et par cette participation nos vies acquièrent de nouveaux sens et directions.",
        "de": "Zeit und Erfahrung sind die Faktoren, die das Leben verändern. Wir beobachten nicht nur den Ablauf der Zeit; wir nehmen an ihr teil, und durch diese Teilnahme erhalten unsere Leben neue Bedeutungen und Richtungen.",
        "es": "El tiempo y la experiencia son los factores que transforman la vida. No simplemente observamos el paso del tiempo; participamos en él, y a través de esta participación nuestras vidas adquieren nuevos significados y direcciones.",
    },
    {
        "gist": "Vanguard Rooted Past",
        "gist_ru": "Авангард с корнями в прошлом",
        "gist_en": "Vanguard Rooted Past",
        "gist_fr": "L'avant-garde enracinée dans le passé",
        "gist_de": "Avantgarde in der Vergangenheit verwurzelt",
        "gist_es": "Vanguardia enraizada en el pasado",
        "russian": "Мы находимся в авангарде времени, но с корнями в прошлом. Это парадокс нашего существования: мы стремимся вперёд, но не можем отрицать того, что нас сформировало. Только понимая историю, мы можем истинно понимать будущее.",
        "english": "We are at the vanguard of time, but rooted in the past. This is the paradox of our existence: we strive forward, yet cannot deny what has shaped us. Only by understanding history can we truly understand the future.",
        "fr": "Nous sommes à l'avant-garde du temps, mais enracinés dans le passé. C'est le paradoxe de notre existence: nous avançons, mais ne pouvons nier ce qui nous a formés. Ce n'est qu'en comprenant l'histoire que nous pouvons vraiment comprendre l'avenir.",
        "de": "Wir sind an der Spitze der Zeit, aber in der Vergangenheit verwurzelt. Das ist das Paradoxon unserer Existenz: Wir streben vorwärts, können aber nicht leugnen, was uns geprägt hat. Nur durch das Verständnis der Geschichte können wir die Zukunft wirklich verstehen.",
        "es": "Estamos en la vanguardia del tiempo, pero enraizados en el pasado. Esta es la paradoja de nuestra existencia: avanzamos, pero no podemos negar lo que nos ha formado. Solo comprendiendo la historia podemos verdaderamente comprender el futuro.",
    },
    {
        "gist": "Chaos Creates Order",
        "gist_ru": "Хаос создаёт порядок",
        "gist_en": "Chaos Creates Order",
        "gist_fr": "Le chaos crée l'ordre",
        "gist_de": "Chaos schafft Ordnung",
        "gist_es": "El caos crea orden",
        "russian": "Хаос - это не противоположность порядку, а его источник. В самых хаотичных системах рождается новый порядок, новые структуры, новая сложность. И наоборот, идеальный порядок неизбежно порождает расстройство. Это вечный танец творчества во Вселенной.",
        "english": "Chaos is not the opposite of order, but its source. In the most chaotic systems new order is born, new structures, new complexity. Conversely, perfect order inevitably generates disorder. This is the eternal dance of creativity in the Universe.",
        "fr": "Le chaos n'est pas l'opposé de l'ordre, mais sa source. Dans les systèmes les plus chaotiques naît un nouvel ordre, de nouvelles structures, une nouvelle complexité. Inversement, l'ordre parfait génère inévitablement le désordre. C'est la danse éternelle de la créativité dans l'univers.",
        "de": "Chaos ist nicht das Gegenteil von Ordnung, sondern ihre Quelle. In den chaotischsten Systemen entsteht neue Ordnung, neue Strukturen, neue Komplexität. Umgekehrt erzeugt perfekte Ordnung unvermeidlich Störung. Dies ist der ewige Tanz der Kreativität im Universum.",
        "es": "El caos no es lo opuesto del orden, sino su fuente. En los sistemas más caóticos nace un nuevo orden, nuevas estructuras, nueva complejidad. Inversamente, el orden perfecto genera inevitablemente desorden. Este es el baile eterno de la creatividad en el Universo.",
    },
    {
        "gist": "Irreversible Time Meaning",
        "gist_ru": "Необратимое время даёт смысл",
        "gist_en": "Irreversible Time Meaning",
        "gist_fr": "Le temps irréversible donne du sens",
        "gist_de": "Irreversible Zeit gibt Bedeutung",
        "gist_es": "El tiempo irreversible da significado",
        "russian": "В необратимом времени мы обретаем смысл. Если бы время было обратимым, все события были бы равноправны, и жизнь потеряла бы направление и значение. Именно необратимость времени создаёт историю, создаёт выбор, создаёт ответственность, создаёт смысл нашего существования.",
        "english": "In irreversible time, we find meaning. If time were reversible, all events would be equivalent, and life would lose direction and significance. It is precisely the irreversibility of time that creates history, creates choice, creates responsibility, creates the meaning of our existence.",
        "fr": "Dans le temps irréversible, nous trouvons du sens. Si le temps était réversible, tous les événements seraient équivalents, et la vie perdrait sa direction et son importance. C'est précisément l'irréversibilité du temps qui crée l'histoire, crée le choix, crée la responsabilité, crée le sens de notre existence.",
        "de": "In irreversibler Zeit finden wir Bedeutung. Wenn die Zeit umkehrbar wäre, würden alle Ereignisse gleichberechtigt sein, und das Leben würde seine Richtung und Bedeutung verlieren. Es ist gerade die Irreversibilität der Zeit, die die Geschichte schafft, die Wahl schafft, Verantwortung schafft, die Bedeutung unserer Existenz schafft.",
        "es": "En el tiempo irreversible, encontramos significado. Si el tiempo fuera reversible, todos los eventos serían equivalentes, y la vida perdería dirección e importancia. Es precisamente la irreversibilidad del tiempo la que crea la historia, crea la elección, crea la responsabilidad, crea el significado de nuestra existencia.",
    },
    {
        "gist": "Nature Dialogue Universe",
        "gist_ru": "Природа как диалог с универсумом",
        "gist_en": "Nature Dialogue Universe",
        "gist_fr": "La nature est un dialogue avec l'univers",
        "gist_de": "Natur ist ein Dialog mit dem Universum",
        "gist_es": "La naturaleza es un diálogo con el universo",
        "russian": "Природа - это диалог между человеком и универсумом. Мы не отделены от природы, наблюдая её со стороны. Мы являемся частью природы, и наше участие в её эволюции столь же значимо, как и эволюция самой природы. Человек и космос говорят друг с другом через язык физики.",
        "english": "Nature is a dialogue between man and the universe. We are not separated from nature, observing it from the side. We are part of nature, and our participation in its evolution is as significant as the evolution of nature itself. Human and cosmos communicate with each other through the language of physics.",
        "fr": "La nature est un dialogue entre l'homme et l'univers. Nous ne sommes pas séparés de la nature, l'observant de loin. Nous faisons partie de la nature, et notre participation à son évolution est aussi significative que l'évolution de la nature elle-même. L'humain et le cosmos communiquent l'un avec l'autre par le langage de la physique.",
        "de": "Die Natur ist ein Dialog zwischen dem Menschen und dem Universum. Wir sind nicht von der Natur getrennt und beobachten sie von außen. Wir sind ein Teil der Natur, und unsere Teilnahme an ihrer Evolution ist genauso bedeutsam wie die Evolution der Natur selbst. Mensch und Kosmos kommunizieren durch die Sprache der Physik miteinander.",
        "es": "La naturaleza es un diálogo entre el hombre y el universo. No estamos separados de la naturaleza, observándola desde afuera. Somos parte de la naturaleza, y nuestra participación en su evolución es tan significativa como la evolución de la naturaleza misma. El humano y el cosmos se comunican entre sí a través del lenguaje de la física.",
    },
    {
        "gist": "Entropy Is Creativity",
        "gist_ru": "Энтропия - это творчество",
        "gist_en": "Entropy Is Creativity",
        "gist_fr": "L'entropie est la créativité",
        "gist_de": "Entropie ist Kreativität",
        "gist_es": "La entropía es creatividad",
        "russian": "Энтропия - это не просто беспорядок, это творчество. Классическая механика рассматривала энтропию как упадок, как смерть упорядоченных систем. Но современная физика показывает, что энтропия - это движущая сила эволюции, источник разнообразия, источник жизни. Творчество Вселенной скрыто в увеличении энтропии.",
        "english": "Entropy is not merely disorder; it is creativity. Classical mechanics viewed entropy as decline, as the death of ordered systems. But modern physics shows that entropy is the driving force of evolution, the source of diversity, the source of life. The Universe's creativity is hidden in the increase of entropy.",
        "fr": "L'entropie n'est pas seulement le désordre ; c'est la créativité. La mécanique classique considérait l'entropie comme un déclin, comme la mort des systèmes ordonnés. Mais la physique moderne montre que l'entropie est la force motrice de l'évolution, la source de la diversité, la source de la vie. La créativité de l'univers est cachée dans l'augmentation de l'entropie.",
        "de": "Entropie ist nicht nur Unordnung; es ist Kreativität. Die klassische Mechanik betrachtete die Entropie als Niedergang, als den Tod geordneter Systeme. Aber die moderne Physik zeigt, dass Entropie die treibende Kraft der Evolution ist, die Quelle der Vielfalt, die Quelle des Lebens. Die Kreativität des Universums ist in der Zunahme der Entropie verborgen.",
        "es": "La entropía no es solo desorden; es creatividad. La mecánica clásica veía la entropía como decadencia, como la muerte de sistemas ordenados. Pero la física moderna muestra que la entropía es la fuerza impulsora de la evolución, la fuente de la diversidad, la fuente de la vida. La creatividad del Universo se esconde en el aumento de la entropía.",
    },
    {
        "gist": "World Grows Complex",
        "gist_ru": "Мир растёт в сложности",
        "gist_en": "World Grows Complex",
        "gist_fr": "Le monde grandit en complexité",
        "gist_de": "Die Welt wächst in Komplexität",
        "gist_es": "El mundo crece en complejidad",
        "russian": "Мир усложняется, становится более интересным и более непредсказуемым. Это не деградация, а творческая эволюция. Каждый день Вселенная находит новые способы организовать материю, создать новые формы жизни, новые мысли. Сложность - это не проблема, а кульминация творчества природы.",
        "english": "The world becomes more complex, more interesting, and more unpredictable. This is not degradation, but creative evolution. Every day the Universe finds new ways to organize matter, create new forms of life, new thoughts. Complexity is not a problem, but the culmination of nature's creativity.",
        "fr": "Le monde devient plus complexe, plus intéressant et plus imprévisible. Ce n'est pas une dégradation, mais une évolution créative. Chaque jour, l'univers trouve de nouvelles façons d'organiser la matière, de créer de nouvelles formes de vie, de nouvelles pensées. La complexité n'est pas un problème, mais l'aboutissement de la créativité de la nature.",
        "de": "Die Welt wird komplexer, interessanter und unvorhersehbarer. Dies ist keine Verschlechterung, sondern kreative Evolution. Jeden Tag findet das Universum neue Wege, um Materie zu organisieren, neue Lebensformen zu schaffen, neue Gedanken. Komplexität ist nicht ein Problem, sondern der Höhepunkt der Kreativität der Natur.",
        "es": "El mundo se vuelve más complejo, más interesante e impredecible. Esto no es degradación, sino evolución creativa. Cada día el Universo encuentra nuevas formas de organizar la materia, crear nuevas formas de vida, nuevos pensamientos. La complejidad no es un problema, sino la culminación de la creatividad de la naturaleza.",
    },
    {
        "gist": "Future Through Us",
        "gist_ru": "Будущее развивается через нас",
        "gist_en": "Future Through Us",
        "gist_fr": "L'avenir se développe à travers nous",
        "gist_de": "Die Zukunft entwickelt sich durch uns",
        "gist_es": "El futuro se desarrolla a través de nosotros",
        "russian": "Будущее не определено, оно развивается через нас. Это фундаментальный принцип: мы не пассивные свидетели истории, мы её творцы. Каждое наше решение, каждое действие влияет на развитие будущего. Вселенная через нас решает, какой путь ей избрать. Мы несём ответственность за будущее.",
        "english": "The future is not determined; it evolves through us. This is a fundamental principle: we are not passive witnesses to history, we are its creators. Every decision we make, every action we take influences the development of the future. The Universe through us decides which path to take. We bear the responsibility for the future.",
        "fr": "L'avenir n'est pas déterminé ; il évolue à travers nous. C'est un principe fondamental: nous ne sommes pas des observateurs passifs de l'histoire, nous en sommes les créateurs. Chaque décision que nous prenons, chaque action que nous posons influence le développement de l'avenir. L'univers à travers nous décide quel chemin prendre. Nous portons la responsabilité de l'avenir.",
        "de": "Die Zukunft ist nicht bestimmt; sie entwickelt sich durch uns. Dies ist ein grundlegendes Prinzip: Wir sind nicht passive Beobachter der Geschichte, wir sind ihre Schöpfer. Jede Entscheidung, die wir treffen, jede Aktion, die wir ergreifen, beeinflusst die Entwicklung der Zukunft. Das Universum entscheidet durch uns, welchen Weg es einschlagen soll. Wir tragen die Verantwortung für die Zukunft.",
        "es": "El futuro no está determinado; evoluciona a través de nosotros. Este es un principio fundamental: no somos observadores pasivos de la historia, somos sus creadores. Cada decisión que tomamos, cada acción que realizamos influye en el desarrollo del futuro. El Universo a través de nosotros decide qué camino tomar. Somos responsables del futuro.",
    },
]

class QuoteHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)

        if parsed_path.path == '/api/quote':
            quote = random.choice(QUOTES)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(quote).encode())
        else:
            super().do_GET()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def start_server():
    os.chdir(Path(__file__).parent)

    with socketserver.TCPServer(("", PORT), QuoteHandler) as httpd:
        url = f"http://localhost:{PORT}"
        print(f"\n✨ Prigogine Quotes App is running!")
        print(f"📍 Open your browser: {url}")
        print(f"🛑 Press Ctrl+C to stop the server\n")

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n✋ Server stopped.")

if __name__ == "__main__":
    start_server()
