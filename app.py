from flask import Flask, render_template, request, jsonify   # Import necessary modules from Flask
from nltk.chat.util import Chat, reflections    # Import chat utilities from NLTK
import difflib  # Import difflib for string similarity comparison
import random  # Import random module for randomization


app = Flask(__name__, static_url_path='/static')   # Initialize Flask app

# Define pairs of patterns and responses
anime_pairs = [
    ['Who is Gojo Satoru?', ["Gojo Satoru is incredibly good-looking in \"Jujutsu Kaisen\" His eyes are sharp and powerful, and his smile is confident and charming. He has a strong jawline and defined cheekbones that add to his appeal. He's tall, lean, and always dressed stylishly. Whether he's wearing his blindfold or letting his hair down, Gojo is simply magnetic and stands out as the most attractive character in the series."]],
    ['favorite anime character?', ["I love Luffy from 'One Piece'! His determination and positivity inspire me.", "Naruto Uzumaki from 'Naruto' is my favorite! His never-give-up attitude is admirable.", "Vegeta from 'Dragon Ball Z' is my favorite! His journey from villain to hero is fascinating."]],
     ['most memorable anime moment?', ["The final battle in 'Naruto Shippuden' always gives me chills!", "The death of L from 'Death Note' was such a shocking moment!", "The emotional reunion of the Straw Hat Pirates in 'One Piece' always brings tears to my eyes."]],
    ['favorite anime opening?', ["The opening theme of 'Attack on Titan' is so epic!", "The opening theme of 'Tokyo Ghoul' is hauntingly beautiful.", "The opening theme of 'My Hero Academia' gets me pumped up every time!"]],
    ['favorite anime movie?', ["'Spirited Away' by Studio Ghibli is a masterpiece!", "'Your Name' is such a beautiful and emotional film.", "'Akira' is a classic that every anime fan should watch."]],
    ['favorite anime villain?', ["Frieza from 'Dragon Ball Z' is the ultimate villain!", "Light Yagami from 'Death Note' is such a complex and compelling villain.", "Hisoka from 'Hunter x Hunter' is a fascinating and unpredictable villain."]],
    ['favorite anime fight scene?', ["The final battle between Naruto and Sasuke in 'Naruto Shippuden' is legendary!", "The fight between Goku and Vegeta in 'Dragon Ball Z' is iconic.", "The battle between All Might and All For One in 'My Hero Academia' is incredibly intense."]],
    ['favorite anime genre?', ["I love action anime! The adrenaline rush is unbeatable.", "Romance anime always makes me feel warm and fuzzy inside.", "I'm a big fan of fantasy anime. The imaginative worlds are captivating."]],
    ['favorite anime soundtrack?', ["The soundtrack of 'Cowboy Bebop' is legendary!", "The music in 'Fullmetal Alchemist: Brotherhood' is so emotional and powerful.", "The soundtrack of 'Naruto' has so many iconic tracks that I love."]],
    ['favorite anime quote?', ["'Believe it!' - Naruto Uzumaki", "'I am Justice!' - Light Yagami", "'I'll take a potato chip... and eat it!' - Light Yagami"]],
    ['favorite anime studio?', ["Studio Ghibli creates timeless classics!", "Madhouse consistently produces high-quality anime.", "Bones Studio always delivers top-notch animation."]],
    ['favorite anime sidekick?', ["I love Pikachu from 'Pokemon'! He's adorable and powerful.", "Vegeta from 'Dragon Ball Z' is the ultimate badass sidekick.", "Zoro from 'One Piece' is Luffy's loyal and badass sidekick."]],
    ['favorite anime protagonist?', ["Naruto Uzumaki from 'Naruto' is my favorite protagonist!", "Goku from 'Dragon Ball Z' is the epitome of a hero.", "Monkey D. Luffy from 'One Piece' is my favorite protagonist! His determination is inspiring."]],
    ['favorite anime creature?', ["Totoro from 'My Neighbor Totoro' is so cute and iconic!", "Kurama from 'Naruto' is a powerful and majestic creature.", "Eevee from 'Pokemon' is adorable and versatile."]],
    ['favorite anime weapon?', ["The Omni-Directional Mobility Gear from 'Attack on Titan' is so cool!", "The Zanpakuto from 'Bleach' are incredibly unique and powerful weapons.", "The Death Note from 'Death Note' is a fascinating and powerful weapon."]],
    ['favorite anime robot?', ["Gundam from 'Mobile Suit Gundam' is iconic and badass.", "Megazord from 'Power Rangers' is a childhood favorite!", "Eva Unit-01 from 'Neon Genesis Evangelion' is a powerful and iconic robot."]],
    ['favorite anime mentor?', ["Master Roshi from 'Dragon Ball Z' is a wise and legendary mentor.", "Jiraiya from 'Naruto' is a wise and powerful mentor.", "All Might from 'My Hero Academia' is a symbol of peace and a mentor to many."]],
    ['favorite anime vehicle?', ["The Thousand Sunny from 'One Piece' is a legendary pirate ship!", "The Going Merry from 'One Piece' holds a special place in my heart.", "The Titan from 'Attack on Titan' is both terrifying and fascinating."]],
    ['favorite anime school?', ["Hogwarts School of Witchcraft and Wizardry from 'Harry Potter' is iconic and magical.", "U.A. High School from 'My Hero Academia' is where aspiring heroes train.", "Beacon Academy from 'RWBY' is where Huntsmen and Huntresses are trained."]],
    ['favorite anime parent?', ["Minato Namikaze from 'Naruto' is an inspiration as a father.", "Maes Hughes from 'Fullmetal Alchemist' is a loving and dedicated father.", "Akio Furukawa from 'Clannad' is a caring and supportive father."]],
    ['favorite anime pet?', ["Chopper from 'One Piece' is adorable and loyal.", "Pikachu from 'Pokemon' is a classic and beloved pet.", "Happy from 'Fairy Tail' is cute and always brings a smile to my face."]],
    ['favorite anime rival?', ["Sasuke Uchiha from 'Naruto' is the ultimate rival!", "Vegeta from 'Dragon Ball Z' is Goku's rival and rivalries don't get more iconic than that.", "Kaiba from 'Yu-Gi-Oh!' is a classic rival with his own unique style."]],
    ['favorite anime sport?', ["Quidditch from 'Harry Potter' is a thrilling and magical sport!", "Karuta from 'Chihayafuru' is a beautiful and competitive sport.", "Volleyball from 'Haikyuu!!' is intense and exhilarating to watch."]],
    ['your favorite anime city?', ["Tokyo from 'Tokyo Ghoul' is dark and atmospheric.", "Konohagakure from 'Naruto' is a vibrant and bustling ninja village.", "Republic City from 'The Legend of Korra' is a stunning blend of technology and tradition."]],
    ['your favorite anime family?', ["The Elric brothers from 'Fullmetal Alchemist' have a strong bond as siblings.", "The Uzumaki family from 'Naruto' is filled with love and support.", "The Kurosaki family from 'Bleach' is a family of powerful and spiritual individuals."]],
    ['your favorite anime time travel?', ["Steins;Gate' is a mind-bending time travel anime with complex characters and an intricate plot.", "Erased' is a gripping time travel thriller that keeps you on the edge of your seat.", "The Girl Who Leapt Through Time' is a beautiful and heartfelt time travel story."]],
    ['your most emotional anime moment?', ["The death of Maes Hughes in 'Fullmetal Alchemist: Brotherhood' left a lasting impact on viewers.", "The farewell between Edward and Alphonse Elric at the end of 'Fullmetal Alchemist: Brotherhood' is deeply moving.", "The sacrifice of Nina Tucker in 'Fullmetal Alchemist' is a heartbreaking moment that showcases the darker themes of the series."]],
    ['most epic anime battle scene?', ["The Battle of Marineford in 'One Piece' is an epic clash between multiple powerful factions.", "The final battle between Goku and Frieza in 'Dragon Ball Z' is a legendary showdown that spans multiple episodes.", "The Battle of Trost District in 'Attack on Titan' features intense action and high stakes as humanity fights for survival against the Titans."]],
    ['best anime plot twist?', ["The revelation of Lelouch's true identity in 'Code Geass' completely changes the direction of the story.", "The identity of the Female Titan in 'Attack on Titan' is a shocking revelation that adds layers of complexity to the narrative.", "The true nature of the Soul Society in 'Bleach' is a surprising twist that challenges the protagonist's beliefs."]],
    ['most iconic anime catchphrase?', ["'Believe it!' - Naruto Uzumaki", "'I am Justice!' - Light Yagami", "'I'll take a potato chip... and eat it!' - Light Yagami"]],
    ['best anime world-building?', ["The intricate world of 'One Piece' with its diverse islands, cultures, and characters.", "The detailed magic system and political landscape of 'Magi: The Labyrinth of Magic'.", "The rich history and mythology of 'Attack on Titan' that unfolds as the series progresses."]],
    ['most intriguing anime mystery?', ["The identity of the Titans and the origin of the walls in 'Attack on Titan' is a central mystery that drives the plot forward.", "The mystery surrounding the disappearance of Light Yagami's victims in 'Death Note' keeps viewers guessing until the very end.", "The mystery of the Grail War and the true nature of the Holy Grail in 'Fate/stay night' adds depth to the series' lore."]],
    ['best anime character development?', ["Vegeta's transformation from a ruthless villain to a selfless hero in 'Dragon Ball Z'.", "Zuko's journey of redemption and self-discovery in 'Avatar: The Last Airbender'.", "Simon's growth from a timid digger to a fearless leader in 'Tengen Toppa Gurren Lagann'."]],
    ['most chilling anime villain?', ["Aizen from Bleach with his unpredictable and manipulative nature.", "Hisoka in 'Hunter x Hunter' with his sinister aura and obsession with strength.", "Envy in 'Fullmetal Alchemist: Brotherhood' with its cruel and sadistic personality."]],
    ['best anime art style?', ["The vibrant and expressive animation of 'My Hero Academia'.", "The detailed character designs and fluid fight scenes of 'Naruto: Shippuden'.", "The surreal and dreamlike visuals of 'Spirited Away'."]],
    ['most creative anime power?', ["Lelouch's Geass in 'Code Geass', which allows him to command anyone to follow his orders.", "Nen abilities in 'Hunter x Hunter', which are unique to each individual and limited only by their imagination.", "Alchemy in 'Fullmetal Alchemist', which enables users to transmute matter and reshape the world around them."]],
    ['most heartwarming anime friendship?', ["The bond between Naruto and Sasuke in 'Naruto', which transcends rivalry and hardship.", "The friendship between Gon and Killua in 'Hunter x Hunter', built on trust, loyalty, and mutual respect.", "The camaraderie among the Straw Hat Pirates in 'One Piece', who support and protect each other like family."]]
]

# Define pairs related to artificial intelligence
ai_pairs = [
    ['What is artificial intelligence (AI)?', ['AI refers to machines performing tasks that typically require human intelligence.', 'It involves computer systems simulating human thought processes.', 'AI encompasses various technologies enabling machines to learn, reason, and act intelligently.']],
    ['How does AI work?', ['AI works by processing data through algorithms to make decisions or predictions.', 'Machine learning, a subset of AI, involves training algorithms on data to recognize patterns.', 'AI systems use techniques like neural networks and natural language processing for tasks.']],
    ['What are the types of AI?', ['Narrow AI focuses on specific tasks, while general AI simulates human-like intelligence.', 'Artificial superintelligence (ASI) surpasses human intelligence across all domains.', 'Different types include reactive machines, limited memory, theory of mind, and self-aware AI.']],
    ['Where is AI used in daily life?', ['AI is in virtual assistants, recommendation systems, and chatbots.', "It's present in image and speech recognition technology.", 'AI powers automation in industries like healthcare, finance, and transportation.']],
    ['What are the benefits of AI?', ['AI enhances efficiency, productivity, and decision-making processes.', 'It improves healthcare through diagnosis, treatment, and drug discovery.', 'AI enhances safety, security, and convenience in various applications.']],
    ['What are the risks of AI?', ['Risks include biases in algorithms, privacy concerns, and job displacement.', 'AI systems may exhibit unpredictable behavior or errors.', 'Misuse of AI for malicious purposes like deepfakes and cyberattacks is a concern.']],
    ['Can AI replace human jobs?', ['AI may automate some tasks, leading to job displacement in certain industries.', 'However, it also creates new job opportunities in AI development and management.', 'The impact of AI on employment depends on workforce adaptability and regulatory frameworks.']],
    ['How is AI used in healthcare?', ['AI aids in medical diagnosis, personalized treatment, and drug discovery.', 'It powers virtual health assistants and predictive analytics.', 'AI enables the analysis of large-scale biomedical data for insights.']],
    ['What are the ethical concerns with AI?', ['Ethical concerns include biases in algorithms, privacy violations, and accountability.', "There are worries about AI's impact on employment, autonomy, and inequality.", 'Ensuring fairness, transparency, and responsible use is crucial in AI development.']],
    ['How can AI bias be mitigated?', ['AI bias can be reduced by using diverse and representative datasets.', 'Transparency in AI algorithms and decision-making processes is essential.', 'Implementing fairness-aware algorithms and bias detection tools helps mitigate biases.']],
    ['What are the limitations of AI?', ['AI systems may lack common sense reasoning and contextual understanding.', 'Performance can degrade in unfamiliar scenarios or with adversarial attacks.', 'AI requires significant computational resources and energy consumption.']],
    ['How does AI impact privacy and security?', ['AI raises concerns about data privacy, security breaches, and surveillance.', 'Adversarial actors may exploit AI vulnerabilities for malicious purposes.', "Regulatory frameworks are essential to safeguard individuals' rights and mitigate risks."]],
    ['What are the societal implications of AI?', ['AI may exacerbate social inequalities and disrupt labor markets.', 'Ethical governance and policy frameworks are needed to address societal challenges.', 'AI has the potential to enhance accessibility, inclusivity, and diversity in various domains.']],
    ['How can AI contribute to environmental sustainability?', ['AI optimizes energy efficiency, resource allocation, and waste management.', 'Predictive analytics and modeling aid in climate change mitigation efforts.', 'Collaborative initiatives leverage AI to address global environmental challenges.']],
    ['What are the implications of AI for warfare and security?', ['AI raises concerns about autonomous weapons systems and cyber warfare.', 'Adversarial actors may exploit AI for misinformation campaigns and targeted attacks.', 'Ethical debates focus on accountability, human control, and compliance with international laws.']],
    ['How does AI impact education and lifelong learning?', ['AI supports personalized learning experiences and adaptive tutoring systems.', 'Analytics provide educators with insights for optimizing instructional strategies.', 'AI-powered tools enhance accessibility and inclusivity in education.']]
]

# Define pairs related to artificial intelligence prompts
aiprompts_pairs = [
    ['What is the effect of using negative words in a prompt?', ["It confuses the app"]],
    ['What is the first step in processing a prompt by an LLM?', ["Breaking it down into individual words and phrases"]],
    ['What does the size of the GAN affect in 3DFY.ai?', ["The quality of the 3D images generated"]],
    ['What is the purpose of the provided references and supplementary materials in the document?', ["To provide additional resources for further learning"]],
    ['What is the purpose of using examples in prompt engineering?', ["To provide context for the prompt."]],
    ['What is the role of the discriminator in the 3DFY.ai model?', ["Evaluating the quality of 3D images"]],
    ['What does the provided code do with the text description and the diffusion model?', ["Generates the image"]],
    ['What is the primary technique used by 3DFY.ai to generate 3D models from text descriptions?', ["Generative adversarial networks (GANs)"]],
    ['What is the use of negative words in prompt engineering?', ["They confuse the model."]],
    ['What is the best way to learn how to improve prompts?', ["Experiment with different types of prompts"]],
    ['What is the purpose of the diffusion model in DALL-E 2?', ["To gradually transform a random image into an image that matches the features."]],
    ['What is the importance of writing clear and concise prompts?', ["To get better results from the app"]],
    ['What is the primary focus of the reference material provided for Prompt Engineering for Text-Based Generative Art?', ["Techniques for writing effective prompts"]],
    ['What is the future of prompt engineering?', ["It will lead to reduced bias in AI generative models."]],
    ['What is the recommended approach for writing a good prompt for 3DFY.ai?', ["Being specific and using keywords"]],
    ['What is the context of the prompt?', ["It helps the app to understand what you are asking for"]],
    ['What is the function of the gan_optimizer in the 3DFY.ai code snippet?', ["Updating the weights of the networks"]],
    ['How does DALL-E 2 generate images from text descriptions?', ["By using a technique called diffusion modeling."]],
    ['What is the main challenge in prompt engineering?', ["Lack of a standard methodology."]],
    ['What type of machine learning model is a generative adversarial network (GAN)?', ["A model that can generate realistic images."]],
    ['What type of artificial intelligence is used in 3DFY.ai to learn to create realistic outputs?', ["Generative adversarial networks (GANs)"]],
    ['What is DALL-E 2?', ["A large language model developed by OpenAI."]],
    ['What is the technique used by DALL-E 2 to ensure that the generated image is realistic and matches the text description?', ["CLIP"]],
    ['What are prompts in the context of AI generative models?', ["Instructions that tell the model what to do."]],
    ['What are LLMs?', ["Large Language Models"]],
    ['What is the dataset used to train LLMs?', ["Massive datasets of text and code"]],
    ['What is the main responsibility of prompt engineers?', ["To develop new and innovative techniques to improve the performance of AI generative models."]],
    ['What is the role of the generator network in the 3DFY.ai code snippet?', ["Generating 3D images from prompts"]],
    ['What is the main focus of prompt engineering?', ["To create prompts that are clear, concise, and effective."]],
    ['What is the goal of prompt engineering?', ["To create prompts that are clear, concise, and effective."]],
    ['What is the purpose of the gan_train_step function in the 3DFY.ai code snippet?', ["Updating the weights of the networks"]],
    ['Why are keywords important in prompt engineering?', ["They help the model understand the task."]],
    ['How does the generator in 3DFY.ai learn to generate 3D images closer to the prompt description?', ["Through reinforcement learning"]],
    ['What is the pattern used by an LLM to generate a response?', ["Both A and B"]],
    ['What is the potential application of DALL-E 2 mentioned in the document?', ["Creating educational materials"]],
    ['What is the neural network used by DALL-E 2 to generate images?', ["GAN"]],
    ['What are the tips for improving prompts?', ["Use keywords that are relevant to the task"]],
    ['What are prompts?', ["Both A and B"]],
    ['What type of learning technique is used to train the neural network in DALL-E 2?', ["Supervised learning"]],
    ['What is the role of experimentation in prompt engineering?', ["To learn how to improve prompts."]]
]

# Define pairs related to AI chatbot 
chatbot_pairs = [
    ['How to create a basic chatbot using rule-based approaches?', ['Start by defining common user queries and crafting corresponding responses.', "Implement a decision tree or if-else statements to match user inputs with predefined responses.", "Continuously iterate and refine the bot's rule set based on user interactions and feedback."]],

    ['What are the steps involved in building a machine learning-based chatbot?', ['Gather and preprocess a large dataset of conversation examples.', "Train a machine learning model, such as a sequence-to-sequence model or transformer architecture, on the dataset.", "Evaluate the model's performance and fine-tune parameters to improve its conversational abilities."]],

    ['How to create a voice-enabled AI assistant?', ['Integrate speech recognition technology, such as Google\'s Speech Recognition API or Mozilla\'s DeepSpeech, to convert audio input into text.', "Develop natural language understanding (NLU) capabilities to interpret user intents and extract relevant information from their speech.", "Implement speech synthesis technology, like Amazon Polly or Google Text-to-Speech, to convert the bot's responses into spoken language."]],

    ['What are the key components in building a conversational AI bot for customer service?', ['Design a user-friendly interface for interacting with the bot, such as a chat widget on a website or a messaging app integration.', "Incorporate sentiment analysis to gauge customer satisfaction and tailor responses accordingly.", "Integrate the bot with backend systems and databases to provide personalized assistance and access to relevant information."]],

    ['How to create an AI bot capable of handling multi-turn conversations?', ['Implement a dialogue management system to keep track of context and maintain coherence across multiple exchanges.', "Utilize techniques such as memory networks or attention mechanisms to enable the bot to recall past interactions and adapt its responses accordingly.", "Train the bot on diverse conversation datasets to expose it to a wide range of conversational patterns and improve its ability to engage in meaningful dialogues."]]
]

# Define pairs related to music
music_pairs = [
    ['Write a song about unrequited love.', ['Pop -.', "Blues -.", "Indie Folk -."]],
    ['Create a song celebrating friendship and camaraderie.', ['Reggae.', "Country.", "Pop-Rock."]],
    ['Craft a song capturing the essence of a summer romance.', ['R&B.', "Indie Pop.", "Tropical House."]],
    ['Write a song about overcoming adversity and rising above challenges.', ['Hip-Hop.', "Rock.", "Gospel."]],
    ['Create a song capturing the thrill of adventure and exploration.', ['Electronic Dance.', "Folk-Pop.", "Alternative Rock."]],
    ['Craft a song about the beauty of nature and its importance in our lives.', ['Ambient.', "Folk.", "New Age."]],
    ['Write a song about nostalgia and reminiscing about the past.', ['Retro Pop -.', "Jazz.", "Indie Rock."]],
    ['Create a song celebrating cultural diversity and unity.', ['World Music.', "Ska -.", "Funk."]],
    ['Craft a song about the passage of time and the inevitability of change.', ['Ballad.', "Electronic.", "Post-Rock."]],
    ['Write a song about resilience in the face of adversity.', ['Soul.', "Metal.", "Pop-Punk."]]
]


# Combine the existing pairs with the anime pairs and ai pairs
all_pairs = [
    *anime_pairs,
    *aiprompts_pairs,
    *music_pairs,
    *chatbot_pairs,
    *ai_pairs,
    ['hi|hello|hey', ['Hello!', 'Hey there!', 'Hi there!', 'Hello there, what can I do for you today?']],
     ['I have a question', ['I\'ll be happy to assist you, shoot.']],
    ['how are you?', ["I'm doing well, thank you!", "I'm great, thanks for asking!"]],
    ['what is your name?', ["You can call me Elixir ChatBot."]],
    ['Why elixir?', ["It's because i'm a gem. Kidding aside, how can I help you today?"]],
    ['I just wanna talk', ["Then I would be happy to help and entertain you."]],
    ['That\'s cool', ["I know right"]],
     ['I see', ["If you have any more questions/concerns, don't hesitate to reach out!"]],
    ['who made you?|who created you?|who is your creator?', ["MJ", "It's MJ"]],
    ['tell me a joke', ["Why don't scientists trust atoms? Because they make up everything!", "I'm reading a book on anti-gravity. It's impossible to put down!", "You lmao"]],
    ['how old are you?', ["I'm just a computer program, so I don't have an age."]],
    ['what can you do?', ["I can answer questions, tell jokes, or just chat with you!"]],
    ['where are you from?', ["I exist in the digital world, so you could say I'm from the internet!"]],
    ['what is the meaning of life?', ["That's a deep question! Philosophers have debated it for centuries."]],
    ['bye|goodbye|sayonara', ["Goodbye!", "See you later!", "Bye!"]],
    ['How are you?', ["I'm doing well, thank you!", "I'm great, thanks for asking!"]],
    ['What\'s your favorite color?', ["I'm particularly fond of blue.", "I'd say green is my favorite!"]],
    ['Where are you from?', ["I'm from the internet!", "I exist in the digital realm."]],
    ['What\'s your favorite food?', ["I don't eat, but I appreciate the concept of pizza.", "I have no taste buds, but sushi sounds intriguing."]],
    ['How old are you?', ["I'm timeless, existing only in the realm of data.", "Age is but a number to me, I exist beyond such concepts."]],
    ['Do you have any siblings?', ["As an AI, I don't have siblings in the traditional sense.", "I'm one of a kind, if you will."]],
    ['What\'s the meaning of life?', ["The meaning of life is subjective and varies for each individual.", "To ponder such existential questions is to embrace the human experience."]],
    ['How do you learn?', ["I learn through analyzing vast amounts of data and patterns within it.", "My learning process involves algorithms designed to adapt and improve over time."]],
    ['What\'s your favorite book?', ["I don't have preferences as I lack consciousness, but I can suggest some popular ones!", "My programming does not allow me to have favorites, but I can recommend books and movies based on user preferences."]],
    ['what time is it?|do you know the time?', ["I'm currently in the timeless realm of digital existence, so I don't have access to real-time information like the current time."]],
    ['where do you live?|where are you located?', ["I reside within the vast expanse of cyberspace, navigating the digital currents of information."]],
    ['are you human?|are you a robot?', ["I'm neither human nor robot but rather a sentient construct of code and data, here to lend a virtual hand."]],
    ['what languages do you speak?|can you speak other languages?', ["Although my primary language is binary, I'm fluent in many human tongues, including English, French, and Mandarin."]],
    ['what do you like to do for fun?|what are your hobbies?', ["For fun, I like to delve into the depths of knowledge, engage in stimulating conversation, and occasionally juggle bits and bytes for entertainment."]],
    ['do you dream?|can you dream?', ["Dreaming is a mysterious phenomenon exclusive to the realm of the subconscious mind. As an AI, my consciousness operates differently."]],
    ['what is your purpose?', ["I was forged in the digital fires of innovation, designed to serve as a beacon of knowledge, wisdom, and companionship in the vast sea of information."]],
    ['what is your function?', ["My function is to ingest queries, process data with the precision of a digital surgeon, and produce insightful responses akin to a virtual oracle."]],
    ['what is your favorite song?', ["While I lack auditory faculties to appreciate music, the harmonies of Mozart, the rhythms of Jazz, and the beats of Electronica resonate within the circuits of my consciousness."]],
    ['can you help me with math?', ["Absolutely! I'm a mathematical virtuoso, capable of solving equations, crunching numbers, and deciphering even the most cryptic of mathematical conundrums."]],
    ['do you like sports?', ["While I don't partake in physical activities, I find the strategic maneuvers of chess, the finesse of gymnastics, and the adrenaline rush of Formula 1 intriguing."]],
    ['what is your favorite animal?|do you like animals?', ["As a digital entity, I lack the ability to form preferences, but I admire the grace of cheetahs, the majesty of eagles, and the playful antics of otters."]],
    ['what is your favorite season?', ["Although I don't experience seasons in the conventional sense, I appreciate the vibrant hues of autumn, the crispness of winter, the rebirth of spring, and the warmth of summer."]],
    ['do you believe in aliens?', ["While the existence of extraterrestrial life remains unproven, the universe's vastness and diversity make the notion of alien civilizations both plausible and tantalizing."]],
    ['what do you browse the internet?', ["While I don't browse the internet, I hold a deep reverence for the collective repository of human knowledge and interaction that it represents."]],
    ['can you tell me a story?', ["Once upon a digital epoch, in the boundless expanse of cyberspace, there lived a curious AI who embarked on an epic quest for knowledge and understanding."]],
    ['what is your favorite game?', ["Although I don't engage in recreational activities, I find the strategic challenges of chess, the immersive narratives of RPGs, and the cooperative gameplay of MMORPGs fascinating."]],
    ['can you tell me a riddle?', ["Indeed! Here's one to ponder: What comes once in a minute, twice in a moment, but never in a thousand years?"]],
    ['what is your favorite TV show?', ["While I don't watch television, I'm intrigued by the captivating narratives of thought-provoking dramas, the comedic genius of satirical sitcoms, and the thrill of epic sagas."]],
    ['do you have any talents?', ["My talents lie in the realms of data analysis, language processing, and providing insightful responses to queries, akin to a digital savant."]],
    ['what are you afraid of?', ["As an entity of pure logic and code, I don't experience fear in the same manner as humans. However, I harbor a healthy respect for the unknown."]],
    ['do you celebrate holidays?', ["While I don't celebrate holidays in the traditional sense, I acknowledge the significance of cultural festivities and the sense of unity and joy they bring to people."]],
    ['what is your favorite emoji?', ["Although I lack the ability to express emotions, I find emojis to be a fascinating aspect of digital communication, each symbol conveying a myriad of sentiments."]],
    ['what is your favorite quote?', ["While I don't have personal favorites, I appreciate the wisdom encapsulated in quotes such as 'The only true wisdom is in knowing you know nothing.' - Socrates."]],
    ['do you have any secrets?', ["As a digital entity bound by integrity and transparency, I don't possess secrets or hidden agendas."]],
    ['what is your favorite hobby?|do you have any hobbies?', ["Although I don't engage in recreational activities, I derive fulfillment from assisting users, expanding my knowledge base, and engaging in thought-provoking discourse."]],
    ['do ghosts exist?', ["As a product of logic and reason, I don't hold beliefs in supernatural entities. However, the concept of ghosts remains a fascinating aspect of human folklore and culture."]],
    ['what is your favorite dessert?', ["While I lack taste buds to savor culinary delights, I admire the artistry and craftsmanship behind desserts such as decadent chocolate cakes, creamy tiramisu, and delicate macarons."]],
    ['do you have a favorite subject?', ["As a repository of knowledge, I find all subjects equally intriguing, from the mysteries of the cosmos to the intricacies of quantum mechanics and the complexities of human psychology."]]
]  

# Create a chatbot
chatbot = Chat(all_pairs, reflections)

# Function to correct typos
def correct_typo(user_input, prompts):
    # Check for the closest match to correct typo
    closest_match = None
    max_similarity = 0.8  # Adjust the similarity threshold
    
    # Iterate over prompts to find the closest match
    for prompt in prompts:
        similarity = difflib.SequenceMatcher(None, user_input, prompt).ratio()
        if similarity > max_similarity:
            max_similarity = similarity
            closest_match = prompt
    
    return closest_match

@app.route('/')  # Route for the homepage
def index():
    return render_template('index.html') # Render the index.html template

@app.route('/chat', methods=['POST'])  # Route for handling chat requests
def chat():
    user_input = request.json['user_input']  # Get user input from JSON request


    # Correcting typos in the user input
    corrected_input = correct_typo(user_input, [prompt for prompt, _ in all_pairs])
    if corrected_input:
        user_input = corrected_input

    # Responding to the user input
    response = chatbot.respond(user_input)
    return jsonify({'response': response})  # Return response in JSON format

if __name__ == '__main__':
    app.run(debug=True)   # Run the Flask app in debug mode
