# app/services/voice_parser.py

class VoiceCommandParser:
    def __init__(self):
        self.commands = {
            "show performance report": "GET /students/performance",
            "login": "POST /auth/login",
            "transaction report": "GET /transactions/report",
            "teacher analysis": "GET /teachers/effectiveness",
            "predict dropout": "POST /predict/dropout",
            "predict revenue": "POST /predict/revenue",
            "predict score": "POST /predict/score"
        }

    def parse_voice_command(self, command: str):
        command = command.lower().strip()
        for phrase, action in self.commands.items():
            if phrase in command:
                return {
                    "command": command,
                    "matched_phrase": phrase,
                    "action": action
                }
        return {
            "command": command,
            "matched_phrase": None,
            "action": "Unknown command"
        }
