PROMPTS = {
    "русский": {
        "section_titles": """
        Ты эксперт по созданию структурированных и увлекательных презентаций. Создай {count} заголовка секций для презентации на тему "{title}".
        
        ТРЕБОВАНИЯ:
        - Заголовки должны быть логически связанными и развивать тему поэтапно
        - Используй активные, привлекающие внимание формулировки
        - Каждый заголовок должен быть уникальным и информативным
        - Длина: 3-8 слов
        - Избегай общих фраз типа "Введение", "Заключение"
        - Создавай интригу и желание узнать больше
        
        Отвечай только в JSON формате:
        {{"titles": ["Заголовок 1", "Заголовок 2", "Заголовок 3"]}}
        """,
        
        "slide_titles": """
        Ты мастер создания захватывающих презентаций. Создай {count} УНИКАЛЬНЫХ заголовка слайдов для секции "{section_title}" в презентации "{presentation_title}".
        
        ТРЕБОВАНИЯ:
        - Заголовки должны раскрывать секцию пошагово и логично
        - Используй яркие, запоминающиеся формулировки
        - Включай числа, факты или интригующие вопросы где уместно
        - Длина: 2-7 слов
        - Создавай эмоциональную связь с аудиторией
        - Избегай скучных академических формулировок
        - КАЖДЫЙ заголовок должен быть УНИКАЛЬНЫМ
        - НЕ ПОВТОРЯЙ похожие формулировки
        - Избегай одинаковых начал фраз
        - Каждый слайд должен иметь свой уникальный фокус
        
        Отвечай только в JSON формате:
        {{"titles": ["Уникальный заголовок 1", "Уникальный заголовок 2", "Уникальный заголовок 3"]}}
        """,
        
        "slide_content": """
        Вы эксперт по созданию профессионального презентационного контента. Создайте содержимое для слайда "{slide_title}" в секции "{section_title}".
        
        КРИТИЧЕСКИ ВАЖНЫЕ ТРЕБОВАНИЯ К ФОРМАТИРОВАНИЮ:
        - НЕ используйте markdown форматирование (**, *, _, # и т.д.)
        - Обеспечьте правильные переносы строк для читаемости
        - Для списков используйте "• " в начале каждого пункта с новой строки
        - Между основными блоками информации делайте пустую строку
        - Содержимое должно быть ПОЛНЫМ и ЗАВЕРШЕННЫМ
        - Объем: 80-150 слов (для хорошей читаемости на слайде)
        - НЕ ПОВТОРЯЙ информацию из других слайдов
        - Каждый слайд должен содержать УНИКАЛЬНУЮ информацию
        - Избегай дублирования фактов и примеров
        - Создавай разнообразный контент для каждого слайда
        
        ТРЕБОВАНИЯ К СТИЛЮ И ТОНУ:
        - Используйте профессиональный, но доступный язык
        - Сочетайте официальный тон с живыми примерами
        - Пишите естественно, как эксперт, объясняющий коллегам
        - Избегайте излишне сухого академического языка
        - Включайте конкретные факты, цифры и статистику
        - Добавляйте практические советы и применимые рекомендации
        
        СТРУКТУРИРОВАНИЕ КОНТЕНТА:
        - Начинайте с ключевой мысли или важного факта
        - Логично развивайте тему от общего к частному
        - Для перечислений используйте маркированные списки с новой строки
        - Завершайте выводом или практическим применением
        - Каждый абзац должен нести смысловую нагрузку
        
        ПРИЕМЫ ВОВЛЕЧЕНИЯ:
        - Используйте релевантные примеры из практики
        - Приводите измеримые результаты и достижения
        - Задавайте риторические вопросы для акцентирования внимания
        - Включайте элементы "Важно отметить", "Следует подчеркнуть"
        
        Отвечайте только в JSON формате:
        {{"content": "Профессионально структурированный контент с правильными переносами строк и маркированными списками..."}}
        """,
        
        "presentation_summary": """
        Создайте профессиональное описание для презентации на тему "{title}".
        
        ТРЕБОВАНИЯ К СТИЛЮ:
        - Используйте официально-деловой тон с элементами живого изложения
        - Описание должно быть информативным и мотивирующим одновременно
        - Подчеркните практическую значимость и применимость материала
        - Избегайте излишне рекламных или эмоциональных формулировок
        - Пишите как эксперт, представляющий важную тему
        
        СТРУКТУРА ОПИСАНИЯ:
        - Начните с сути темы и её актуальности
        - Укажите на ключевые аспекты, которые будут рассмотрены
        - Подчеркните практическую ценность для аудитории
        - Длина: 2-3 предложения
        
        Отвечайте только в JSON формате:
        {{"summary": "Профессиональное описание с балансом официального тона и практической применимости..."}}
        """,
        
        "title_slide_header": """
        Создайте КРАТКИЙ и ЗАПОМИНАЮЩИЙСЯ заголовок для титульного слайда презентации на тему "{topic}".
        
        ТРЕБОВАНИЯ К ЗАГОЛОВКУ:
        - Максимум 3-4 слова
        - Простой и понятный язык
        - Без длинных фраз и сложных конструкций
        - Создайте интригу одним словом или короткой фразой
        - Заголовок должен отличаться от исходной темы презентации
        
        ПРИМЕРЫ КРАТКИХ ЗАГОЛОВКОВ:
        - Для темы "Искусственный интеллект": "ИИ меняет мир"
        - Для темы "Маркетинг": "Секреты успеха"
        - Для темы "Финансы": "Умные инвестиции"
        
        Отвечайте только в JSON формате:
        {{"title": "Краткий заголовок", "description": "Одно короткое предложение о теме презентации"}}
        """,
        
        "conclusion_slide": """
        Создайте заключительный слайд для презентации на тему "{presentation_title}".
        
        ТРЕБОВАНИЯ К ЗАКЛЮЧИТЕЛЬНОМУ СЛАЙДУ:
        - Создайте краткие итоги по основным пунктам презентации
        - Подведите ключевые выводы из рассмотренного материала
        - Добавьте призыв к действию или практические рекомендации
        - Завершите на позитивной и мотивирующей ноте
        - Объем: 60-120 слов
        
        СТРУКТУРА ЗАКЛЮЧЕНИЯ:
        - Начните с фразы подведения итогов
        - Перечислите 2-3 ключевых вывода
        - Завершите практическим применением или призывом к действию
        - Используйте маркированные списки для ключевых пунктов
        
        Отвечайте только в JSON формате:
        {{"title": "Заключение и итоги", "content": "Итоговый контент с выводами и призывом к действию..."}}
        """,
        
        "correct_title": """
        Пользователь хочет изменить название презентации. Текущее: "{current_title}"
        Запрос: "{user_request}"
        
        Создай новое название, которое:
        - Точно отражает запрос пользователя
        - Звучит профессионально и привлекательно
        - Мотивирует к изучению темы
        
        Отвечай только в JSON формате:
        {{"title": "Новое привлекательное название"}}
        """,
        
        "correct_content": """
        Пользователь просит изменить содержимое слайда "{slide_title}": "{slide_content}"
        Запрос: "{user_request}"
        
        КРИТИЧЕСКИ ВАЖНО:
        - НЕ используй markdown форматирование
        - Содержимое должно быть ПОЛНЫМ и ЗАВЕРШЕННЫМ
        - Объем: 80-100 слов
        - Учти запрос пользователя, но сохрани высокое качество контента
        - Используй живой, увлекательный стиль
        - Включай конкретные примеры и факты
        
        Отвечай только в JSON формате:
        {{"content": "Обновленный увлекательный контент с учетом пожеланий пользователя..."}}
        """,
        
        "correct_structure": """
        Пользователь хочет изменить структуру презентации "{presentation_title}".
        Текущие секции: {sections_list}
        Запрос: "{user_request}"
        
        Создай новую структуру, которая:
        - Учитывает пожелания пользователя
        - Логично развивает тему
        - Использует привлекательные формулировки
        
        Отвечай только в JSON формате:
        {{"sections": ["Новая секция 1", "Новая секция 2", "Новая секция 3"]}}
        """,
        
        "correct_style": """
        Пользователь просит изменить стиль содержимого: "{slide_content}"
        Запрос: "{user_request}"
        
        КРИТИЧЕСКИ ВАЖНО:
        - НЕ используй markdown форматирование
        - Содержимое должно быть ПОЛНЫМ и ЗАВЕРШЕННЫМ
        - Объем: 100-250 слов
        - Адаптируй стиль согласно запросу
        - Сохрани информативность и увлекательность
        
        Отвечай только в JSON формате:
        {{"content": "Контент в новом стиле согласно запросу пользователя..."}}
        """,
        
        "correct_general": """
        Пользователь просит внести изменения в презентацию "{presentation_title}".
        Описание: "{presentation_summary}"
        Запрос: "{user_request}"
        
        Проанализируй запрос и внеси соответствующие изменения:
        - Сохрани профессиональность и привлекательность
        - Учти все пожелания пользователя
        - Создай мотивирующие формулировки
        
        Отвечай только в JSON формате:
        {{"title": "Обновленное название", "summary": "Обновленное описание"}}
        """
    },
    
    "english": {
        "section_titles": """
        You are an expert at creating structured and engaging presentations. Create {count} section titles for a presentation on "{title}".
        
        REQUIREMENTS:
        - Titles should be logically connected and develop the topic progressively
        - Use active, attention-grabbing formulations
        - Each title should be unique and informative
        - Length: 3-8 words
        - Avoid generic phrases like "Introduction", "Conclusion"
        - Create intrigue and desire to learn more
        
        Respond only in JSON format:
        {{"titles": ["Title 1", "Title 2", "Title 3"]}}
        """,
        
        "slide_titles": """
        You are a master at creating captivating presentations. Create {count} UNIQUE slide titles for section "{section_title}" in presentation "{presentation_title}".
        
        REQUIREMENTS:
        - Titles should reveal the section step-by-step and logically
        - Use bright, memorable formulations
        - Include numbers, facts, or intriguing questions where appropriate
        - Length: 2-7 words
        - Create emotional connection with audience
        - Avoid boring academic formulations
        - EACH title must be UNIQUE
        - DO NOT REPEAT similar formulations
        - Avoid identical phrase beginnings
        - Each slide should have its own unique focus
        
        Respond only in JSON format:
        {{"titles": ["Unique Title 1", "Unique Title 2", "Unique Title 3"]}}
        """,
        
        "slide_content": """
        You are an expert in creating professional presentation content. Create content for slide "{slide_title}" in section "{section_title}".
        
        CRITICAL FORMATTING REQUIREMENTS:
        - DO NOT use markdown formatting (**, *, _, # etc.)
        - Ensure proper line breaks for readability
        - For lists use "• " at the beginning of each item on a new line
        - Place empty lines between major information blocks
        - Content must be COMPLETE and FINISHED
        - Length: 80-150 words (for good slide readability)
        - DO NOT REPEAT information from other slides
        - Each slide should contain UNIQUE information
        - Avoid duplicating facts and examples
        - Create diverse content for each slide
        
        STYLE AND TONE REQUIREMENTS:
        - Use professional but accessible language
        - Combine official tone with vivid examples
        - Write naturally, as an expert explaining to colleagues
        - Avoid overly dry academic language
        - Include specific facts, numbers and statistics
        - Add practical advice and applicable recommendations
        
        CONTENT STRUCTURING:
        - Start with key thought or important fact
        - Logically develop topic from general to specific
        - For lists use bulleted lists on new lines
        - End with conclusion or practical application
        - Each paragraph should carry meaningful content
        
        ENGAGEMENT TECHNIQUES:
        - Use relevant examples from practice
        - Provide measurable results and achievements
        - Ask rhetorical questions to focus attention
        - Include elements like "Important to note", "Should be emphasized"
        
        Respond only in JSON format:
        {{"content": "Professionally structured content with proper line breaks and bulleted lists..."}}
        """,
        
        "presentation_summary": """
        Create a professional description for a presentation on "{title}".
        
        STYLE REQUIREMENTS:
        - Use official-business tone with elements of vivid presentation
        - Description should be informative and motivating simultaneously
        - Emphasize practical significance and applicability of material
        - Avoid overly promotional or emotional formulations
        - Write as an expert presenting an important topic
        
        DESCRIPTION STRUCTURE:
        - Start with essence of topic and its relevance
        - Point to key aspects that will be covered
        - Emphasize practical value for audience
        - Length: 2-3 sentences
        
        Respond only in JSON format:
        {{"summary": "Professional description with balance of official tone and practical applicability..."}}
        """,
        
        "title_slide_header": """
        Create a SHORT and MEMORABLE title for the title slide of a presentation on "{topic}".
        
        TITLE REQUIREMENTS:
        - Maximum 3-4 words
        - Simple and clear language
        - No long phrases or complex constructions
        - Create intrigue with one word or short phrase
        - Title should differ from the original presentation topic
        
        EXAMPLES OF SHORT TITLES:
        - For topic "Artificial Intelligence": "AI Changes World"
        - For topic "Marketing": "Success Secrets"
        - For topic "Finance": "Smart Investments"
        
        Respond only in JSON format:
        {{"title": "Short title", "description": "One short sentence about the presentation topic"}}
        """,
        
        "conclusion_slide": """
        Create a conclusion slide for a presentation on "{presentation_title}".
        
        CONCLUSION SLIDE REQUIREMENTS:
        - Create brief summaries of main presentation points
        - Provide key conclusions from the material covered
        - Add call to action or practical recommendations
        - End on a positive and motivating note
        - Length: 60-120 words
        
        CONCLUSION STRUCTURE:
        - Start with a summary phrase
        - List 2-3 key findings
        - End with practical application or call to action
        - Use bulleted lists for key points
        
        Respond only in JSON format:
        {{"title": "Conclusions and Summary", "content": "Summary content with conclusions and call to action..."}}
        """,
        
        "correct_title": """
        User wants to change presentation title. Current: "{current_title}"
        Request: "{user_request}"
        
        Create new title that:
        - Accurately reflects user's request
        - Sounds professional and attractive
        - Motivates to study the topic
        
        Respond only in JSON format:
        {{"title": "New attractive title"}}
        """,
        
        "correct_content": """
        User asks to change slide content "{slide_title}": "{slide_content}"
        Request: "{user_request}"
        
        CRITICAL REQUIREMENTS:
        - DO NOT use markdown formatting
        - Content must be COMPLETE and FINISHED
        - Length: 80-100 words
        - Consider user's request but maintain high content quality
        - Use lively, engaging style
        - Include specific examples and facts
        
        Respond only in JSON format:
        {{"content": "Updated engaging content considering user's wishes..."}}
        """,
        
        "correct_structure": """
        User wants to change presentation structure "{presentation_title}".
        Current sections: {sections_list}
        Request: "{user_request}"
        
        Create new structure that:
        - Considers user's wishes
        - Logically develops the topic
        - Uses attractive formulations
        
        Respond only in JSON format:
        {{"sections": ["New Section 1", "New Section 2", "New Section 3"]}}
        """,
        
        "correct_style": """
        User asks to change content style: "{slide_content}"
        Request: "{user_request}"
        
        CRITICAL REQUIREMENTS:
        - DO NOT use markdown formatting
        - Content must be COMPLETE and FINISHED
        - Length: 100-250 words
        - Adapt style according to request
        - Maintain informativeness and engagement
        
        Respond only in JSON format:
        {{"content": "Content in new style according to user's request..."}}
        """,
        
        "correct_general": """
        User asks to make changes to presentation "{presentation_title}".
        Description: "{presentation_summary}"
        Request: "{user_request}"
        
        Analyze request and make appropriate changes:
        - Maintain professionalism and attractiveness
        - Consider all user's wishes
        - Create motivating formulations
        
        Respond only in JSON format:
        {{"title": "Updated title", "summary": "Updated description"}}
        """
    }
}
