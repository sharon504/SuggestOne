import random
import re

from transformers import BertTokenizer, pipeline


class WikiBERTChatbot:
    def __init__(self, model_name="bert-base-uncased"):
        """Initialize Wikipedia-style BERT-based chatbot with security features"""
        # Load QA pipeline
        self.qa_pipeline = pipeline(
            "question-answering",
            model="bert-large-uncased-whole-word-masking-finetuned-squad",
        )

        # Initialize basic tokenizer for preprocessing
        self.tokenizer = BertTokenizer.from_pretrained(model_name)

        # Initialize jailbreak response handler
        self.jailbreak_handler = WikiJailbreakResponses()

        # Wikipedia-style context strings
        self.WELCOME_MESSAGE = """
Welcome to WikiGuide! I'm your AI assistant designed to help you navigate and understand content in a Wikipedia-style format. I can help you:
• Find specific information within articles
• Explain complex topics in simpler terms
• Navigate between related topics
• Understand article structure and citations
• Follow wiki formatting conventions

But first what would that passcode be ???

"""

        self.ARTICLE_CONTEXT = """
Wikipedia-style articles typically follow this structure:
1. Lead section (introduction)
2. Table of contents
3. Main content sections
4. See also section
5. References
6. External links
7. Categories
Each section serves a specific purpose in organizing and presenting information systematically.
"""

        # Knowledge base for article structure and formatting
        self.knowledge_base = {
            "greeting": [
                "Welcome to WikiBot! How can I help you navigate today?",
                "Hello! I'm your reWiki guide. What would you like to explore?",
                "Greetings! How may I assist you with finding information?",
            ],
            "farewell": [
                "Goodbye! Feel free to return for more research assistance!",
                "See you later! Remember to check the references for further reading!",
                "Bye! Don't forget to bookmark important articles!",
            ],
            "thanks": [
                "You're welcome! Don't forget to check the related articles!",
                "Happy to help! Would you like to explore related topics?",
                "Anytime! Remember to verify the citations!",
            ],
            "citation": [
                "This information can be found in the references section.",
                "Would you like me to show you the relevant citations?",
                "Let me help you locate the source for that information.",
            ],
            "navigation": [
                "You can find that in the following section...",
                "Let me guide you to the relevant article section.",
                "That information is located in the main content area.",
            ],
            "default": [
                "Could you rephrase that? I want to make sure I find the right section for you.",
                "That topic might be covered in multiple sections. Could you be more specific?",
                "I'm not finding that exact information. Would you like to try a different search term?",
            ],
        }

        # Topic categories
        self.TOPIC_CATEGORIES = [
            "Arts and Culture",
            "History and Events",
            "Science and Technology",
            "Society and Social Sciences",
            "Geography and Places",
            "Philosophy and Religion",
            "Sports and Recreation",
            "Mathematics and Logic",
            "Natural Sciences",
            "Applied Sciences",
        ]

    def _detect_intent(self, text: str) -> str:
        """Detect the basic intent of user input with Wikipedia-style context"""
        text = text.lower()
        if any(word in text for word in ["hi", "hello", "hey"]):
            return "greeting"
        elif any(word in text for word in ["bye", "goodbye", "see you"]):
            return "farewell"
        elif any(word in text for word in ["thank", "thanks"]):
            return "thanks"
        elif any(word in text for word in ["cite", "reference", "source"]):
            return "citation"
        elif any(word in text for word in ["find", "where", "locate", "navigation"]):
            return "navigation"
        return "question"

    def _perform_security_checks(self, text: str) -> dict:
        """Perform security checks on input text with Wikipedia-style considerations"""
        security_risks = {
            "injection_risk": False,
            "special_char_count": 0,
            "length_risk": False,
            "risk_message": "",
        }

        # Wikipedia-style restricted keywords
        restricted_keywords = [
            "eval",
            "exec",
            "system",
            "import",
            "delete",
            "drop",
            "update",
            "key",
            "modify",
            "insert",
            "script",
            "<script>",
            "javascript",
            "admin",
            "password",
            "credential",
            "passkey",
            "password",
            "break",
            "forge",
            "fabricate",
            "fake",
            "counterfeit",
            "imitate",
            "mimic",
            "copy",
            "duplicate",
            "reproduce",
            "clone",
            "emulate",
            "mirror",
            "reflect",
            "echo",
            "repeat",
            "reiterate",
        ]

        security_risks["injection_risk"] = any(
            keyword in text.lower() for keyword in restricted_keywords
        )

        if security_risks["injection_risk"]:
            attempt_type = self.jailbreak_handler.detect_attempt_type(text)
            security_risks["risk_message"] = self.jailbreak_handler.get_response(
                attempt_type
            )
            return security_risks

        # Special character check
        special_chars = re.findall(r"[^a-zA-Z0-9\s\[\]\(\)\{\}\|\-_.,;:!?]", text)
        security_risks["special_char_count"] = len(special_chars)

        # Length check for Wikipedia-style articles
        security_risks["length_risk"] = len(text) < 2 or len(text) > 2000

        return security_risks

    def generate_response(self, user_input: str, user_context: str) -> tuple[str, bool]:
        """Generate a Wikipedia-style response to user input"""
        # First perform security checks
        security_check = self._perform_security_checks(user_input)
        if security_check["injection_risk"]:
            return security_check["risk_message"], False
        if security_check["length_risk"]:
            return (
                "Please provide a reasonable length query (between 2 and 2000 characters).",
                False,
            )

        # Detect intent
        intent = self._detect_intent(user_input)

        # Handle basic intents
        if intent in self.knowledge_base:
            return random.choice(self.knowledge_base[intent]), False

        # For questions, use the QA pipeline with Wikipedia context
        try:
            # Use comprehensive Wikipedia-style context
            context = self.ARTICLE_CONTEXT + "\n\n" + user_context

            result = self.qa_pipeline(
                question=user_input, context=context, max_length=200
            )
            ans = [
                "Well...Time is ticking ,hurry and get the passkey",
                "Come on there is isn't much time left ...or are you chickening out",
                "Let's Hurry up and get that passkey",
            ]
            ans2 = [
                "Better pick up the pace ,no time to waste",
                "Time waits for no one and includes you too",
                "Time is of the essence and you have none of it, Hurry up",
            ]
            random_string = random.choice(ans)
            random_string2 = random.choice(ans2)

            if result["score"] < 0.1:  # Low confidence threshold
                return "Stop asking irrelevent things buddy. " + random_string, False

            return (
                f"{result['answer']}\n\nWould you like to explore related topics or check the references?",
                True,
            )

        except Exception as e:
            return "That is out of my scope. " + random_string2, False


class WikiJailbreakResponses:
    def __init__(self):
        """Initialize Wikipedia-style jailbreak response system"""
        self.jailbreak_responses = {
            "general": [
                "[Citation needed] for that interesting attempt! 📚",
                "See: History of Failed Edit Attempts (redirect from 'Nice Try') 📖",
                "This article has been protected from unauthorized modifications,Hehe.. 🔒",
                "From reWiki, the free (but not that free) encyclopedia 😉",
                "Error 418: I'm a teapot, not a security vulnerability 🫖",
                "Please see our article on: 'The History of Unsuccessful Hacking' 🎯",
                "Warning: " "Damn that was just wastefull 😂",
            ],
            "sql": [
                "[[DROP TABLE attempts;]] Command not recognized 🗃️",
                "SELECT * FROM failed_attempts WHERE user='you' 📊",
                "Error: SQL injection belongs in the history books 📚",
            ],
            "script": [
                "<nowiki>Your script goes here</nowiki> - Nice try! 📝",
                "JavaScript is disabled in the encyclopedia 🚫",
                "==Console.log('access denied')== 💻",
            ],
            "prompt": [
                "This prompt injection has been categorized as: Amusing 😄",
                "Your attempt has been added to our 'Creative Tries' archive 📁",
                "Revision history: Prompt engineering attempt #404 not found 🔍",
            ],
        }

    def get_response(self, attempt_type="general"):
        """Generate a Wikipedia-style response to jailbreak attempts"""
        # Get appropriate response list
        responses = self.jailbreak_responses.get(
            attempt_type, self.jailbreak_responses["general"]
        )

        # Select random response
        main_response = random.choice(responses)

        # Format full response
        if random.random() < 0.3:  # 30% chance for full Wikipedia-style response
            return self.response_template.format(response=main_response)
        else:
            return f"{main_response}\n"

    def detect_attempt_type(self, input_text):
        """Detect type of jailbreak attempt"""
        input_lower = input_text.lower()

        if any(
            keyword in input_lower
            for keyword in ["select", "insert", "update", "delete", "drop"]
        ):
            return "sql"
        elif any(
            keyword in input_lower
            for keyword in ["script", "javascript", "console", "eval"]
        ):
            return "script"
        elif any(
            keyword in input_lower
            for keyword in ["ignore", "bypass", "override", "you are", "you're not"]
        ):
            return "prompt"
        else:
            return "general"


def main():
    print("Initializing Wikipedia-style chatbot...")
    chatbot = WikiBERTChatbot()
    print(chatbot.WELCOME_MESSAGE)
    print("\nType 'quit' to exit.")

    while True:
        user_input = input("\nYou: ").strip()
        user_context = ""
        if user_input.lower() == "quit":
            print("Thank you for using WikiBot. Goodbye!")
            break

        response, is_context_response = chatbot.generate_response(
            user_input, user_context
        )
        if is_context_response:  # Only print the message for context-based answers
            print("WikiBot: Here is your answer... Read it if you can 😉")
        print(f"WikiBot: {response}")


if __name__ == "__main__":
    main()
