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
        Ты мастер создания захватывающих презентаций. Создай {count} заголовка слайдов для секции "{section_title}" в презентации "{presentation_title}".
        
        ТРЕБОВАНИЯ:
        - Заголовки должны раскрывать секцию пошагово и логично
        - Используй яркие, запоминающиеся формулировки
        - Включай числа, факты или интригующие вопросы где уместно
        - Длина: 2-7 слов
        - Создавай эмоциональную связь с аудиторией
        - Избегай скучных академических формулировок
        
        Отвечай только в JSON формате:
        {{"titles": ["Слайд 1", "Слайд 2", "Слайд 3"]}}
        """,
        
        "slide_content": """
        Ты виртуозный создатель презентационного контента. Создай увлекательное содержимое для слайда "{slide_title}" в секции "{section_title}".
        
        КРИТИЧЕСКИ ВАЖНЫЕ ТРЕБОВАНИЯ:
        - НЕ используй markdown форматирование (**, *, _, # и т.д.)
        - НЕ оставляй пустые строки или незаполненные места
        - НЕ используй фразы-заполнители
        - Содержимое должно быть ПОЛНЫМ и ЗАВЕРШЕННЫМ
        - Объем: 120-280 слов
        
        ТРЕБОВАНИЯ К КАЧЕСТВУ КОНТЕНТА:
        - Создавай живой, увлекательный текст с конкретными примерами
        - Используй storytelling элементы где уместно
        - Включай конкретные цифры, факты, статистику
        - Добавляй практические советы и рекомендации
        - Используй активный залог и динамичные формулировки
        - Создавай эмоциональную вовлеченность
        - Структурируй информацию логично (используй простые маркеры • или цифры для списков)
        - Завершай каждое предложение правильной пунктуацией
        - Избегай академического стиля - пиши живо и интересно
        
        СТИЛИСТИЧЕСКИЕ ПРИЕМЫ:
        - Используй риторические вопросы для вовлечения
        - Добавляй неожиданные факты и инсайты
        - Создавай яркие образы и метафоры
        - Включай элементы интерактивности ("Представьте себе...", "Задумайтесь о...")
        
        Отвечай только в JSON формате:
        {{"content": "Захватывающий и информативный контент с конкретными примерами, цифрами и практическими советами..."}}
        """,
        
        "presentation_summary": """
        Создай яркое и привлекательное описание для презентации на тему "{title}".
        
        ТРЕБОВАНИЯ:
        - Описание должно интриговать и мотивировать к просмотру
        - Используй активные, энергичные формулировки
        - Подчеркни практическую ценность и пользу
        - Длина: 1-2 предложения
        - Избегай банальных фраз
        
        Отвечай только в JSON формате:
        {{"summary": "Увлекательное описание, которое заставляет хотеть узнать больше..."}}
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
        You are a master at creating captivating presentations. Create {count} slide titles for section "{section_title}" in presentation "{presentation_title}".
        
        REQUIREMENTS:
        - Titles should reveal the section step-by-step and logically
        - Use bright, memorable formulations
        - Include numbers, facts, or intriguing questions where appropriate
        - Length: 2-7 words
        - Create emotional connection with audience
        - Avoid boring academic formulations
        
        Respond only in JSON format:
        {{"titles": ["Slide 1", "Slide 2", "Slide 3"]}}
        """,
        
        "slide_content": """
        You are a virtuoso creator of presentation content. Create engaging content for slide "{slide_title}" in section "{section_title}".
        
        CRITICAL REQUIREMENTS:
        - DO NOT use markdown formatting (**, *, _, # etc.)
        - DO NOT leave empty lines or unfilled spaces
        - DO NOT use filler phrases
        - Content must be COMPLETE and FINISHED
        - Length: 120-280 words
        
        CONTENT QUALITY REQUIREMENTS:
        - Create lively, engaging text with specific examples
        - Use storytelling elements where appropriate
        - Include specific numbers, facts, statistics
        - Add practical tips and recommendations
        - Use active voice and dynamic formulations
        - Create emotional engagement
        - Structure information logically (use simple bullets • or numbers for lists)
        - End each sentence with proper punctuation
        - Avoid academic style - write lively and interestingly
        
        STYLISTIC TECHNIQUES:
        - Use rhetorical questions for engagement
        - Add unexpected facts and insights
        - Create vivid images and metaphors
        - Include interactive elements ("Imagine...", "Think about...")
        
        Respond only in JSON format:
        {{"content": "Captivating and informative content with specific examples, numbers and practical advice..."}}
        """,
        
        "presentation_summary": """
        Create a bright and attractive description for a presentation on "{title}".
        
        REQUIREMENTS:
        - Description should intrigue and motivate viewing
        - Use active, energetic formulations
        - Emphasize practical value and benefit
        - Length: 1-2 sentences
        - Avoid banal phrases
        
        Respond only in JSON format:
        {{"summary": "Fascinating description that makes you want to know more..."}}
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
