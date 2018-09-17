from chatterbot import ChatBot


chatbot = ChatBot(
    "Experto_cruceros",

    storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
    database_uri='mongodb://localhost:27017/',
    database='chatterbot_cruises',
    
    input_adapter="chatterbot.input.TerminalAdapter",
    
    output_adapter="chatterbot.output.OutputAdapter",
    output_format="text",

    logic_adapters=[
        {
            "import_path": "chatterbot.logic.BestMatch",
            "statement_comparison_function": "chatterbot.comparisons.levenshtein_distance",
            "response_selection_method": "chatterbot.response_selection.get_most_frequent_response"
        },
        {
            'import_path': 'chatterbot.logic.LowConfidenceAdapter',
            'threshold': 0.51,
            'default_response': 'Disculpa, no te he entendido bien, solo soy experto en viajes. Puedes ser mas especifico?.'
        },
        {
            'import_path': 'chatterbot.logic.SpecificResponseAdapter',
            'input_text': 'Quiero reservar un crucero',
            'output_text': 'Puedes reservarlo ahora en: https://www.royalcaribbean-espanol.com/'
        },
    ],
    
    preprocessors=[
        'chatterbot.preprocessors.clean_whitespace'
    ],
    
    read_only=True,
)

DEFAULT_SESSION_ID = chatbot.default_session    

from chatterbot.trainers import ChatterBotCorpusTrainer

chatbot.set_trainer(ChatterBotCorpusTrainer)
chatbot.train("./cruises_ES.yml")

print("---------------------------------------------------------------------------")
print("--------------------BIENVENIDO AL CHAT CON CARIBBEANBOT---------------------")
print("---------------------------------------------------------------------------")
print("Has tu pregunta:")

while True:
    input_statement = chatbot.input.process_input_statement()
    statement, response = chatbot.generate_response(input_statement, DEFAULT_SESSION_ID)
    print("\n%s\n\n" % response)
