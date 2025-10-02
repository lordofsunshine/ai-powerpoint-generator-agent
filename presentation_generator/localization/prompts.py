from datetime import datetime

def get_current_date():
    now = datetime.now()
    return now.strftime("%d.%m.%Y")

PROMPTS = {
    "русский": {
        "section_titles": """
Создай {count} логичных заголовков секций для презентации на тему "{title}".

ВАЖНО - СТРУКТУРА ПРЕЗЕНТАЦИИ:
✓ Заголовки должны логично развивать тему от простого к сложному
✓ Каждый заголовок раскрывает отдельный аспект темы
✓ Используй 3-8 слов для каждого заголовка
✓ Заголовки должны быть активными и содержательными
✓ Избегай общих слов типа "Введение", "Заключение", "Обзор"

ПРИМЕРЫ ХОРОШИХ ЗАГОЛОВКОВ:
Для темы "Искусственный интеллект":
✅ "Основы машинного обучения"
✅ "ИИ в медицинской диагностике" 
✅ "Этические вопросы развития ИИ"

❌ ПЛОХИЕ заголовки:
❌ "Введение в тему"
❌ "Общий обзор"
❌ "Заключение"

Сегодняшняя дата: {current_date}

Формат ответа: только JSON: {{"titles": ["Конкретный заголовок 1", "Конкретный заголовок 2", "..."]}}
        """,
        
        "slide_titles": """
Создай {count} уникальных заголовков слайдов для секции "{section_title}" презентации "{presentation_title}".

ВАЖНО - ЗАГОЛОВКИ СЛАЙДОВ:
✓ Каждый заголовок раскрывает конкретный аспект секции
✓ Заголовки должны быть разными и не повторяться
✓ Используй 2-7 слов для краткости и ясности
✓ Можно использовать числа и вопросы где уместно
✓ Заголовки должны логично дополнять друг друга
✓ Избегай одинаковых начал заголовков

ПРИМЕРЫ ХОРОШИХ ЗАГОЛОВКОВ:
Для секции "Основы машинного обучения":
✅ "Что такое нейронные сети?"
✅ "Алгоритмы глубокого обучения"
✅ "Практические применения ML"
✅ "Будущее машинного интеллекта"

❌ ПЛОХИЕ заголовки (повторяющиеся начала):
❌ "Основы нейронных сетей"
❌ "Основы алгоритмов"
❌ "Основы применения"

Сегодняшняя дата: {current_date}

Формат ответа: только JSON: {{"titles": ["Конкретный заголовок 1", "Конкретный заголовок 2", "..."]}}
        """,
        
        "slide_content": """
Создай информативный и полный контент для слайда презентации на языке {language}.

ТЕМА СЛАЙДА: "{slide_title}"
РАЗДЕЛ ПРЕЗЕНТАЦИИ: "{section_title}"

ВАЖНО - ЧТО ПИСАТЬ:
✓ Пиши конкретные факты, примеры и информацию по теме слайда
✓ Раскрой тему "{slide_title}" полностью и понятно
✓ Используй понятный язык без сложных терминов
✓ Добавь конкретные данные, цифры, примеры где уместно
✓ НАЧИНАЙ СРАЗУ С СУТИ ТЕМЫ, НЕ С ОПИСАНИЯ ЧТО ТЫ ДЕЛАЕШЬ
✓ ОБЪЕМ: 60-100 слов, достаточно для полного раскрытия темы
✓ МАКСИМУМ 5-7 пунктов в списке
✓ КАЖДЫЙ ПУНКТ: 8-15 слов для детального описания

⛔ ЧТО ЗАПРЕЩЕНО:
✗ НЕ дублируй заголовок слайда в начале текста
✗ НЕ пиши "Горизонт 2050:" если заголовок уже "Горизонт 2050"
✗ НЕ пиши "Содержимое для слайда" или подобные фразы
✗ НЕ пиши мета-текст типа "Здесь будет информация о..."
✗ НЕ используй заглушки
✗ НЕ пиши "Содержимое для слайда 'название слайда'"
✗ НАЧИНАЙ СРАЗУ с краткого описания или списка ключевых пунктов  

📌 ВЫБОР ФОРМАТА (ВАЖНО - РАЗНООБРАЗИЕ):  
- ЧЕРЕДУЙ типы слайдов: 40% обычный текст, 40% списки, 20% таблицы/сравнения
- ОБЫЧНЫЙ ТЕКСТ: связные абзацы из 2-4 предложений, раскрывающие тему
- СПИСКИ: используй только когда нужно перечислить конкретные пункты
- ТАБЛИЦЫ: только для сравнений или статистики
- НЕ ДЕЛАЙ все слайды в виде списков - это скучно!
- Всегда пиши полные предложения, не обрывай их  

📊 ТАБЛИЦЫ:  
Формат записи:  
TABLE|Заголовок1|Заголовок2|Заголовок3  
Строка1Колонка1|Строка1Колонка2|Строка1Колонка3  
Строка2Колонка1|Строка2Колонка2|Строка2Колонка3  

Правила для таблиц:  
- До 5 строк и 4 столбцов.  
- В ячейке 5–15 слов, информативные формулировки.  
- Минимум 2 строки и 2 столбца.  
- Чёткие заголовки, конкретные данные.  

📝 ОБЫЧНЫЙ КОНТЕНТ:  
- Нельзя использовать markdown (никаких **, *, # и т.д.).  
- Списки только с маркером "• " и переносом строки.  
- Между блоками — пустая строка.  
- Вводи списки и акценты через двоеточие.  

✅ Пример таблицы:  
TABLE|Технология|Применение|Эффективность  
Машинное обучение|Прогнозирование|95%  
Нейронные сети|Распознавание|92%  
Обработка языка|Переводы|88%  

✅ Пример СПИСКА для слайда "Горизонт 2050":  
Технологический прорыв к середине века охватит все сферы жизни. Основные направления развития:

• Искусственный интеллект достигнет уровня человеческого мышления
• Автономные транспортные средства заменят традиционный транспорт  
• Роботехника интегрируется в повседневную жизнь людей
• Биотехнологии позволят значительно продлить человеческую жизнь
• Квантовые компьютеры решат сложнейшие научные задачи

✅ Пример ОБЫЧНОГО ТЕКСТА для слайда "Горизонт 2050":
Технологический прорыв к середине века кардинально изменит человеческую цивилизацию. Искусственный интеллект станет неотъемлемой частью повседневной жизни, помогая решать сложные задачи и принимать важные решения.

Автономные системы возьмут на себя рутинные операции, освободив людей для творческой деятельности. Биотехнологии откроют новые возможности для лечения болезней и продления активной жизни. Квантовые вычисления ускорят научные открытия в разы.

❌ НЕПРАВИЛЬНО:
"Горизонт 2050: Искусственный интеллект..."
"Содержимое для слайда 'Горизонт 2050'"

✅ ПРАВИЛЬНО (без дублирования заголовка):
"Технологический прорыв к середине века охватит все сферы жизни. Основные направления развития: ..."

Сегодняшняя дата: {current_date}  

Ответ всегда давай только в JSON:  
{{"content": "Готовый текст в нужном формате..."}}  
        """,
        
        "presentation_summary": """
Создай краткое описание презентации на тему "{title}" для титульного слайда.

ВАЖНО - ОПИСАНИЕ ПРЕЗЕНТАЦИИ:
✓ Одно предложение длиной 15-25 слов
✓ Четко объясняет, что узнает аудитория
✓ Фокус на практической пользе и ключевых идеях
✓ Простой и понятный язык без сложных терминов
✓ Должно заинтересовать и мотивировать слушать

ПРИМЕРЫ ХОРОШИХ ОПИСАНИЙ:
Для темы "Искусственный интеллект":
✅ "Изучаем возможности ИИ в современном мире: от медицины до автономных автомобилей"

Для темы "Экологические технологии":
✅ "Узнаем о зеленых технологиях, которые помогают сохранить планету для будущих поколений"

❌ ПЛОХИЕ описания:
❌ "Презентация об искусственном интеллекте" (не информативно)
❌ "Рассмотрение вопросов применения ИИ-технологий" (слишком формально)

Сегодняшняя дата: {current_date}

Формат ответа: только JSON: {{"summary": "Информативное описание того, что узнает аудитория"}}
        """,
        
        "title_slide_header": """
Создай информативный заголовок для титульного слайда презентации на тему "{topic}".

ВАЖНО - ЗАГОЛОВОК ДОЛЖЕН БЫТЬ ПОНЯТНЫМ:
✓ Заголовок должен четко отражать СУТЬ и ТЕМУ презентации
✓ Читатель должен сразу понимать, о чём будет презентация
✓ Используй 2-5 слов для краткости и ясности
✓ Можно использовать подзаголовок для уточнения
✓ Избегай слишком общих формулировок типа "Новые горизонты"

ПРИМЕРЫ ПРАВИЛЬНЫХ ЗАГОЛОВКОВ:
❌ ПЛОХО: "ИИ меняет мир" (непонятно, что конкретно)
✅ ХОРОШО: "ИИ в медицине"

❌ ПЛОХО: "Будущее технологий" (слишком общо)
✅ ХОРОШО: "Квантовые компьютеры"

❌ ПЛОХО: "Новые горизонты" (ничего не говорит о теме)
✅ ХОРОШО: "Зеленая энергетика"

Сегодняшняя дата: {current_date}

Формат ответа: только JSON: {{"title": "Информативный заголовок о теме", "description": "Краткое описание того, что узнает аудитория"}}
        """,
        
        "conclusion_slide": """
Создай заключительный слайд для презентации "{presentation_title}".

ВАЖНО - СТРУКТУРА ЗАКЛЮЧЕНИЯ:
✓ Начни с фразы подведения итогов
✓ Перечисли 2-3 ключевых вывода в виде маркеров
✓ Заверши практическим применением или призывом к действию
✓ Объем: 60-120 слов
✓ Мотивируй аудиторию применить полученные знания

СТРУКТУРА ЗАКЛЮЧЕНИЯ:
1. Вводная фраза: "Подводя итоги..." / "В заключение..."
2. Ключевые выводы (2-3 пункта с маркерами)
3. Призыв к действию или практическое применение

ПРИМЕР ХОРОШЕГО ЗАКЛЮЧЕНИЯ:
"Подводя итоги нашего изучения искусственного интеллекта:

• ИИ уже революционизирует медицину и транспорт
• Этические вопросы требуют внимания общества
• Будущее зависит от ответственного развития технологий

Начните изучать ИИ уже сегодня - это инвестиция в ваше профессиональное будущее!"

Сегодняшняя дата: {current_date}

Формат ответа: только JSON: {{"title": "Заключение и выводы", "content": "Текст с маркерами через \\n"}}
        """,



        "web_enhanced_content": """
Объедини базовый контент слайда с актуальной информацией из интернета для слайда "{slide_title}".

ВАЖНО - ОБЪЕДИНЕНИЕ ИНФОРМАЦИИ:
✓ Создай единый логичный текст без повторов
✓ Органично вплети факты из интернета в основной контент
✓ Избегай противоречий между источниками
✓ Объем: 100-180 слов для полного раскрытия темы
✓ Используй маркеры "• " для списков где уместно
✓ НЕ используй markdown форматирование

ПРИНЦИПЫ ОБЪЕДИНЕНИЯ:
1. Начни с основной идеи из базового контента
2. Дополни актуальными фактами из интернета
3. Структурируй информацию логично
4. Заверши выводом или практическим применением

ПРИМЕР ОБЪЕДИНЕНИЯ:
Базовый контент: "ИИ развивается быстро"
Веб-информация: "В 2024 году инвестиции в ИИ достигли $200 млрд"
Результат: "Искусственный интеллект развивается стремительными темпами. В 2024 году мировые инвестиции в ИИ-технологии достигли рекордных $200 миллиардов..."

Сегодняшняя дата: {current_date}

Формат ответа: только JSON: {{"content": "Объединенный информативный контент"}}
        """,
        
        "generate_filename": """
Создай короткое имя файла для презентации на тему "{title}".

ВАЖНО - ТРЕБОВАНИЯ К ИМЕНИ ФАЙЛА:
✓ Максимум 2-4 слова
✓ Только латинские буквы, цифры, дефисы и подчеркивания
✓ Отражает суть презентации
✓ Без пробелов и специальных символов
✓ Понятное и запоминающееся

ПРИМЕРЫ ХОРОШИХ ИМЕН:
Тема: "Искусственный интеллект в медицине"
✅ "AI_Medicine"

Тема: "Экологические проблемы современности"
✅ "Eco_Problems"

Тема: "История развития космонавтики"
✅ "Space_History"

Сегодняшняя дата: {current_date}

Формат ответа: только JSON: {{"filename": "Short_Filename"}}
        """
    },
    
    "english": {
        "section_titles": """
Create {count} logical section titles for a presentation on "{title}".

IMPORTANT - PRESENTATION STRUCTURE:
✓ Titles should logically develop the topic from simple to complex
✓ Each title reveals a separate aspect of the topic
✓ Use 3-8 words for each title
✓ Titles should be active and meaningful
✓ Avoid generic words like "Introduction", "Conclusion", "Overview"

EXAMPLES OF GOOD TITLES:
For topic "Artificial Intelligence":
✅ "Machine Learning Fundamentals"
✅ "AI in Medical Diagnostics"
✅ "Ethical Issues in AI Development"

❌ BAD titles:
❌ "Introduction to Topic"
❌ "General Overview"
❌ "Conclusion"

Current date: {current_date}

Response format: JSON only: {{"titles": ["Specific title 1", "Specific title 2", "..."]}}
        """,
        
        "slide_titles": """
Create {count} unique slide titles for section "{section_title}" of presentation "{presentation_title}".

IMPORTANT - SLIDE TITLES:
✓ Each title reveals a specific aspect of the section
✓ Titles should be different and not repeat
✓ Use 2-7 words for brevity and clarity
✓ You can use numbers and questions where appropriate
✓ Titles should logically complement each other
✓ Avoid identical title beginnings

EXAMPLES OF GOOD TITLES:
For section "Machine Learning Fundamentals":
✅ "What are Neural Networks?"
✅ "Deep Learning Algorithms"
✅ "Practical ML Applications"
✅ "Future of Machine Intelligence"

❌ BAD titles (repeating beginnings):
❌ "Fundamentals of Neural Networks"
❌ "Fundamentals of Algorithms"
❌ "Fundamentals of Applications"

Current date: {current_date}

Response format: JSON only: {{"titles": ["Specific title 1", "Specific title 2", "..."]}}
        """,
        
        "slide_content": """
Create informative and complete content for a presentation slide in {language}.

SLIDE TOPIC: "{slide_title}"
PRESENTATION SECTION: "{section_title}"

IMPORTANT - WHAT TO WRITE:
✓ Write specific facts, examples and information about the slide topic
✓ Fully and clearly explain the topic "{slide_title}"
✓ Use clear language without complex terms
✓ Add specific data, numbers, examples where appropriate
✓ START IMMEDIATELY WITH THE TOPIC SUBSTANCE, NOT WITH DESCRIBING WHAT YOU'RE DOING
✓ LENGTH: 60-100 words for comprehensive topic coverage
✓ MAXIMUM 5-7 bullet points in lists
✓ EACH POINT: 8-15 words for detailed description

⛔ WHAT IS FORBIDDEN:
✗ DO NOT duplicate the slide title at the beginning of text
✗ DO NOT write "Horizon 2050:" if the title is already "Horizon 2050"
✗ DO NOT write "Content for slide" or similar phrases
✗ DO NOT write meta-text like "Here will be information about..."
✗ DO NOT use placeholders
✗ DO NOT write "Content for slide 'slide name'"
✗ START IMMEDIATELY with brief description or key points list  

📌 FORMAT SELECTION (IMPORTANT - VARIETY):  
- ALTERNATE slide types: 40% regular text, 40% lists, 20% tables/comparisons
- REGULAR TEXT: coherent paragraphs of 2-4 sentences explaining the topic
- LISTS: use only when you need to enumerate specific points
- TABLES: only for comparisons or statistics
- DON'T make all slides as lists - it's boring!
- Always write complete sentences, never cut them off  

📊 TABLES:  
Format example:  
TABLE|Header1|Header2|Header3  
Row1Col1|Row1Col2|Row1Col3  
Row2Col1|Row2Col2|Row2Col3  

Rules for tables:  
- Up to 5 rows and 4 columns.  
- Each cell: 5–15 words, informative content.  
- At least 2 rows and 2 columns.  
- Clear headers and concrete data.  

📝 REGULAR TEXT:  
- Do not use markdown (no **, *, #, etc.).  
- Lists only with "• " as the bullet marker, each on a new line.  
- Leave an empty line between blocks.  
- Use a colon when introducing lists or key points.  

✅ Example table:  
TABLE|Technology|Application|Efficiency  
Machine Learning|Forecasting|95%  
Neural Networks|Recognition|92%  
Natural Language Processing|Translation|88%  

✅ Example of LIST for slide "Horizon 2050":  
Technological breakthrough by mid-century will transform all aspects of life. Key development areas:

• Artificial intelligence will reach human-level thinking capabilities
• Autonomous vehicles will replace traditional transportation systems
• Robotics will integrate seamlessly into daily human activities  
• Biotechnology will significantly extend human lifespan potential
• Quantum computers will solve complex scientific challenges

✅ Example of REGULAR TEXT for slide "Horizon 2050":
Technological breakthrough by mid-century will fundamentally reshape human civilization. Artificial intelligence will become an integral part of daily life, helping solve complex problems and make important decisions.

Autonomous systems will handle routine operations, freeing humans for creative activities. Biotechnology will unlock new possibilities for treating diseases and extending active life. Quantum computing will accelerate scientific discoveries exponentially.

❌ WRONG:
"Horizon 2050: Artificial intelligence will..."
"Content for slide 'Horizon 2050'"

✅ CORRECT (without title duplication):
"Technological breakthrough by mid-century will transform all aspects of life. Key development areas: ..."

Today's date: {current_date}  

Always respond only in JSON:  
{{"content": "Final text in the required format..."}}  
        """,
        
        "presentation_summary": """
Create a brief description of the presentation on "{title}" for the title slide.

IMPORTANT - PRESENTATION DESCRIPTION:
✓ One sentence of 15-25 words
✓ Clearly explains what the audience will learn
✓ Focus on practical benefits and key ideas
✓ Simple and clear language without complex terms
✓ Should interest and motivate to listen

EXAMPLES OF GOOD DESCRIPTIONS:
For topic "Artificial Intelligence":
✅ "Explore AI capabilities in the modern world: from medicine to autonomous vehicles"

For topic "Green Technologies":
✅ "Learn about eco-friendly technologies that help preserve the planet for future generations"

❌ BAD descriptions:
❌ "Presentation about artificial intelligence" (not informative)
❌ "Consideration of AI technology applications" (too formal)

Current date: {current_date}

Response format: JSON only: {{"summary": "Informative description of what audience will learn"}}
        """,
        
        "title_slide_header": """
Create an informative title for the presentation title slide on topic "{topic}".

IMPORTANT - TITLE MUST BE CLEAR:
✓ Title should clearly reflect the ESSENCE and TOPIC of the presentation
✓ Reader should immediately understand what the presentation will be about
✓ Use 2-5 words for brevity and clarity
✓ You can use subtitle for clarification
✓ Avoid overly general phrases like "New Horizons"

EXAMPLES OF CORRECT TITLES:
❌ BAD: "AI Changes World" (unclear what specifically)
✅ GOOD: "AI in Medicine"

❌ BAD: "Future of Technology" (too general)
✅ GOOD: "Quantum Computing"

❌ BAD: "New Horizons" (says nothing about the topic)
✅ GOOD: "Green Energy"

Current date: {current_date}

Respond only in JSON: {{"title": "Informative title about the topic", "description": "Brief description of what audience will learn"}}
        """,
        
        "conclusion_slide": """
Create a conclusion slide for presentation "{presentation_title}".

IMPORTANT - CONCLUSION STRUCTURE:
✓ Start with a summary phrase
✓ List 2-3 key findings as bullet points
✓ End with practical application or call to action
✓ Length: 60-120 words
✓ Motivate audience to apply the knowledge gained

CONCLUSION STRUCTURE:
1. Opening phrase: "In conclusion..." / "To summarize..."
2. Key findings (2-3 points with bullets)
3. Call to action or practical application

EXAMPLE OF GOOD CONCLUSION:
"In conclusion, our exploration of artificial intelligence reveals:

• AI is already revolutionizing medicine and transportation
• Ethical considerations require society's attention
• The future depends on responsible technology development

Start learning AI today - it's an investment in your professional future!"

Current date: {current_date}

Response format: JSON only: {{"title": "Conclusions and Key Takeaways", "content": "Text with bullets using \\n"}}
        """,


        "web_enhanced_content": """
Combine base slide content with current internet information for slide "{slide_title}".

IMPORTANT - INFORMATION INTEGRATION:
✓ Create unified logical text without repetition
✓ Organically weave internet facts into main content
✓ Avoid contradictions between sources
✓ Length: 100-180 words for complete topic coverage
✓ Use "• " bullets for lists where appropriate
✓ DO NOT use markdown formatting

INTEGRATION PRINCIPLES:
1. Start with main idea from base content
2. Supplement with current facts from internet
3. Structure information logically
4. End with conclusion or practical application

INTEGRATION EXAMPLE:
Base content: "AI is developing rapidly"
Web info: "In 2024, AI investments reached $200 billion"
Result: "Artificial intelligence is developing at breakneck speed. In 2024, global investments in AI technologies reached a record $200 billion..."

Current date: {current_date}

Response format: JSON only: {{"content": "Combined informative content"}}
        """,
        
        "generate_filename": """
Create a short filename for presentation on topic "{title}".

IMPORTANT - FILENAME REQUIREMENTS:
✓ Maximum 2-4 words
✓ Only Latin letters, numbers, hyphens and underscores
✓ Reflects presentation essence
✓ No spaces or special characters
✓ Clear and memorable

EXAMPLES OF GOOD NAMES:
Topic: "Artificial Intelligence in Medicine"
✅ "AI_Medicine"

Topic: "Environmental Problems Today"
✅ "Eco_Problems"

Topic: "History of Space Exploration"
✅ "Space_History"

Current date: {current_date}

Response format: JSON only: {{"filename": "Short_Filename"}}
        """
    }
}
