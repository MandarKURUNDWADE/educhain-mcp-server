# test_educhain.py
import os
from dotenv import load_dotenv
from educhain import Educhain, LLMConfig
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()

def test_educhain_setup():
    """Test EduChain setup with Google Gemini API"""
    try:
        # Initialize Gemini model
        gemini_model = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.7
        )
        
        # Create LLM configuration
        gemini_config = LLMConfig(custom_model=gemini_model)
        
        # Initialize EduChain client
        client = Educhain(gemini_config)
        
        # Test MCQ generation
        print("Testing MCQ generation...")
        mcq = client.qna_engine.generate_questions(
            topic="Python Programming Basics",
            num=3,
            question_type="Multiple Choice",
            difficulty_level="Beginner"
        )
        
        print("✅ MCQ Generation Test Passed")
        print(f"Generated {len(mcq.questions)} questions")
        
        # Test lesson plan generation
        print("\nTesting lesson plan generation...")
        lesson = client.content_engine.generate_lesson_plan(
            topic="Python Programming Basics",
            duration="45 minutes",
            grade_level="High School"
        )
        
        print("✅ Lesson Plan Generation Test Passed")
        print(f"Generated lesson plan: {lesson.title}")
        
        return True
        
    except Exception as e:
        print(f"❌ Setup test failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_educhain_setup()
    if success:
        print("\n🎉 EduChain setup completed successfully!")
    else:
        print("\n❌ Please check your configuration and try again.")