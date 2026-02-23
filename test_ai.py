import sys
import unittest
from dotenv import load_dotenv
load_dotenv()
from ai import analyze_text, PROMPTS

class TestAIIntegration(unittest.TestCase):
    def test_invalid_mode(self):
        with self.assertRaises(ValueError) as cm:
            analyze_text("invalid_mode", "some text")
        self.assertEqual(str(cm.exception), "Modo de análise inválido: invalid_mode")

    def test_empty_text(self):
        with self.assertRaises(ValueError) as cm:
            analyze_text("summary", "")
        self.assertEqual(str(cm.exception), "O texto para análise não pode estar vazio.")

    def test_prompts_exist(self):
        required_modes = [
            "summary", "bullets", "checklist", "qa", "insights", 
            "simplify", "detailed", "chapters", "concepts", "study_plan",
            "translate", "mindmap"
        ]
        for mode in required_modes:
            self.assertIn(mode, PROMPTS)

    def test_real_call(self):
        # This will verify connectivity and model name
        try:
            result = analyze_text("summary", "Olá, isso é um teste de conectividade.")
            self.assertIsInstance(result, str)
            self.assertTrue(len(result) > 0)
            print(f"\nAPI Call Result: {result[:50]}...")
        except Exception as e:
            self.fail(f"API call failed: {e}")

if __name__ == "__main__":
    unittest.main()
