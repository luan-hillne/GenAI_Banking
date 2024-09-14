class Model_Settings:
    def __init__(self):
        self.MODEL_TYPE = "ChatOpenAI"
        self.MODEL_NAME = 'gpt-4o-mini-2024-07-18'
        self.MAX_TOKEN = 2048
        self.TEMPERATURE = 0.5
        self.TOP_K = 100
        self.TOP_P = 1
        self.REPEAT_PENALTY = 1.2
        self.SYSTEM_PROMPT = ""
        self.RETRIEVAL_TOP_K = 3
        self.RETRIEVAL_THRESHOLD = 0.3
        self.GROQ_API_KEY = ""
        self.OPENAI_API_KEY = ""
        self.GEMINI_API_KEY = ""
        self.IS_RETRIEVAL = True
        self.FUNCTION_CALLING = False