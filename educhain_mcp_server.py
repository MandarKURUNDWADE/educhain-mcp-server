#!/usr/bin/env python3
"""
EduChain MCP Server - Educational Content Generation with Google Gemini API
Description: MCP server that leverages educhain library to generate educational content
"""

import os
import json
import logging
from typing import Any, Dict, List, Optional, Union
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

# Core MCP and EduChain imports
from mcp.server.fastmcp import FastMCP
from mcp.server.models import InitializationOptions
from mcp.types import Tool, Resource, TextContent, ImageContent

# EduChain and LLM imports
from educhain import Educhain, LLMConfig
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EduChainMCPServer:
    """
    EduChain MCP Server class that integrates educhain with MCP protocol
    """
    
    def __init__(self):
        """Initialize the EduChain MCP Server"""
        self.gemini_model = None
        self.educhain_client = None
        self.mcp_server = None
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize Gemini model and EduChain client"""
        try:
            # Initialize Gemini model
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("GOOGLE_API_KEY environment variable not set")
            
            self.gemini_model = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash-exp",
                google_api_key=api_key,
                temperature=0.7,
                max_tokens=2048
            )
            
            # Create LLM configuration
            gemini_config = LLMConfig(custom_model=self.gemini_model)
            
            # Initialize EduChain client
            self.educhain_client = Educhain(gemini_config)
            
            # Create MCP server
            self.mcp_server = FastMCP("EduChain Educational Content Server")
            
            logger.info("✅ EduChain MCP Server initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize EduChain MCP Server: {str(e)}")
            raise
    
    def setup_tools(self):
        """Set up MCP tools for educational content generation"""
        
        @self.mcp_server.tool()
        def generate_mcq(
            topic: str,
            num_questions: int = 5,
            difficulty_level: str = "Medium",
            custom_instructions: str = ""
        ) -> Dict[str, Any]:
            """
            Generate multiple-choice questions for a given topic
            
            Args:
                topic: The subject/topic for questions
                num_questions: Number of questions to generate (1-10)
                difficulty_level: Difficulty level (Easy, Medium, Hard)
                custom_instructions: Additional instructions for question generation
            
            Returns:
                Dict containing generated MCQ questions
            """
            try:
                logger.info(f"Generating {num_questions} MCQ questions for topic: {topic}")
                
                # Validate inputs
                if not topic.strip():
                    raise ValueError("Topic cannot be empty")
                
                if num_questions < 1 or num_questions > 10:
                    raise ValueError("Number of questions must be between 1 and 10")
                
                # Generate questions using EduChain
                questions = self.educhain_client.qna_engine.generate_questions(
                    topic=topic,
                    num=num_questions,
                    question_type="Multiple Choice",
                    difficulty_level=difficulty_level,
                    custom_instructions=custom_instructions
                )
                
                # Format response
                result = {
                    "success": True,
                    "topic": topic,
                    "num_questions": len(questions.questions),
                    "difficulty_level": difficulty_level,
                    "questions": []
                }
                
                for i, q in enumerate(questions.questions, 1):
                    result["questions"].append({
                        "question_number": i,
                        "question": q.question,
                        "options": q.options,
                        "correct_answer": q.correct_answer,
                        "explanation": q.explanation
                    })
                
                logger.info(f"✅ Successfully generated {len(questions.questions)} MCQ questions")
                return result
                
            except Exception as e:
                logger.error(f"❌ Error generating MCQ questions: {str(e)}")
                return {
                    "success": False,
                    "error": str(e),
                    "topic": topic
                }
        
        @self.mcp_server.tool()
        def generate_lesson_plan(
            topic: str,
            duration: str = "45 minutes",
            grade_level: str = "High School",
            learning_objectives: Optional[List[str]] = None
        ) -> Dict[str, Any]:
            """
            Generate a comprehensive lesson plan for a given topic
            
            Args:
                topic: The subject/topic for the lesson plan
                duration: Duration of the lesson (e.g., "45 minutes", "1 hour")
                grade_level: Target grade level (Elementary, Middle School, High School, College)
                learning_objectives: List of specific learning objectives
            
            Returns:
                Dict containing the generated lesson plan
            """
            try:
                logger.info(f"Generating lesson plan for topic: {topic}")
                
                # Validate inputs
                if not topic.strip():
                    raise ValueError("Topic cannot be empty")
                
                # Generate lesson plan using EduChain
                lesson = self.educhain_client.content_engine.generate_lesson_plan(
                    topic=topic,
                    duration=duration,
                    grade_level=grade_level,
                    learning_objectives=learning_objectives or []
                )
                
                # Format response
                result = {
                    "success": True,
                    "topic": topic,
                    "duration": duration,
                    "grade_level": grade_level,
                    "lesson_plan": {
                        "title": lesson.title,
                        "objectives": lesson.objectives,
                        "materials": lesson.materials,
                        "introduction": lesson.introduction,
                        "main_content": lesson.main_content,
                        "activities": lesson.activities,
                        "assessment": lesson.assessment,
                        "conclusion": lesson.conclusion
                    }
                }
                
                logger.info(f"✅ Successfully generated lesson plan for {topic}")
                return result
                
            except Exception as e:
                logger.error(f"❌ Error generating lesson plan: {str(e)}")
                return {
                    "success": False,
                    "error": str(e),
                    "topic": topic
                }
        
        @self.mcp_server.tool()
        def generate_flashcards(
            topic: str,
            num_cards: int = 10,
            difficulty_level: str = "Medium",
            card_type: str = "Definition"
        ) -> Dict[str, Any]:
            """
            Generate flashcards for a given topic (Bonus Feature)
            
            Args:
                topic: The subject/topic for flashcards
                num_cards: Number of flashcards to generate (1-20)
                difficulty_level: Difficulty level (Easy, Medium, Hard)
                card_type: Type of flashcards (Definition, QA, Concept)
            
            Returns:
                Dict containing generated flashcards
            """
            try:
                logger.info(f"Generating {num_cards} flashcards for topic: {topic}")
                
                # Validate inputs
                if not topic.strip():
                    raise ValueError("Topic cannot be empty")
                
                if num_cards < 1 or num_cards > 20:
                    raise ValueError("Number of cards must be between 1 and 20")
                
                # Generate flashcards using EduChain
                # Note: This uses custom prompt template for flashcard generation
                custom_template = """
                Generate {num} flashcards for the topic: {topic}
                Difficulty level: {difficulty_level}
                Card type: {card_type}
                
                Format each flashcard with:
                - Front: Question or term
                - Back: Answer or definition
                - Category: Subject category
                
                Make sure the flashcards are educational and appropriate for the difficulty level.
                """
                
                questions = self.educhain_client.qna_engine.generate_questions(
                    topic=topic,
                    num=num_cards,
                    question_type="Short Answer",
                    difficulty_level=difficulty_level,
                    custom_instructions=f"Create {card_type} flashcards",
                    prompt_template=custom_template
                )
                
                # Format as flashcards
                result = {
                    "success": True,
                    "topic": topic,
                    "num_cards": len(questions.questions),
                    "difficulty_level": difficulty_level,
                    "card_type": card_type,
                    "flashcards": []
                }
                
                for i, q in enumerate(questions.questions, 1):
                    result["flashcards"].append({
                        "card_number": i,
                        "front": q.question,
                        "back": q.correct_answer,
                        "category": topic,
                        "difficulty": difficulty_level
                    })
                
                logger.info(f"✅ Successfully generated {len(questions.questions)} flashcards")
                return result
                
            except Exception as e:
                logger.error(f"❌ Error generating flashcards: {str(e)}")
                return {
                    "success": False,
                    "error": str(e),
                    "topic": topic
                }
    
    def setup_resources(self):
        """Set up MCP resources for educational content"""
        
        @self.mcp_server.resource("educhain://topic/{topic}")
        def get_topic_overview(topic: str) -> str:
            """
            Get an overview of a specific educational topic
            
            Args:
                topic: The educational topic to get overview for
            
            Returns:
                String containing topic overview
            """
            try:
                logger.info(f"Getting topic overview for: {topic}")
                
                # Use EduChain to generate topic overview
                overview = self.educhain_client.content_engine.generate_lesson_plan(
                    topic=topic,
                    duration="Overview",
                    grade_level="General"
                )
                
                return f"""
                Topic Overview: {topic}
                
                Description: {overview.introduction}
                
                Key Concepts:
                {chr(10).join(f"• {obj}" for obj in overview.objectives)}
                
                Materials Needed:
                {chr(10).join(f"• {mat}" for mat in overview.materials)}
                
                Assessment Methods:
                {overview.assessment}
                """
                
            except Exception as e:
                logger.error(f"❌ Error getting topic overview: {str(e)}")
                return f"Error retrieving overview for {topic}: {str(e)}"
        
        @self.mcp_server.resource("educhain://questions/{topic}")
        def get_sample_questions(topic: str) -> str:
            """
            Get sample questions for a specific topic
            
            Args:
                topic: The educational topic to get sample questions for
            
            Returns:
                String containing sample questions
            """
            try:
                logger.info(f"Getting sample questions for: {topic}")
                
                # Generate sample questions
                questions = self.educhain_client.qna_engine.generate_questions(
                    topic=topic,
                    num=3,
                    question_type="Multiple Choice",
                    difficulty_level="Medium"
                )
                
                result = f"Sample Questions for: {topic}\n\n"
                
                for i, q in enumerate(questions.questions, 1):
                    result += f"Question {i}: {q.question}\n"
                    for j, option in enumerate(q.options, 1):
                        result += f"  {j}. {option}\n"
                    result += f"Correct Answer: {q.correct_answer}\n"
                    result += f"Explanation: {q.explanation}\n\n"
                
                return result
                
            except Exception as e:
                logger.error(f"❌ Error getting sample questions: {str(e)}")
                return f"Error retrieving sample questions for {topic}: {str(e)}"
    
    def run_server(self):
        """Run the MCP server"""
        try:
            # Setup tools and resources
            self.setup_tools()
            self.setup_resources()
            
            logger.info("🚀 Starting EduChain MCP Server...")
            
            # Run the server
            self.mcp_server.run()
            
        except Exception as e:
            logger.error(f"❌ Error running MCP server: {str(e)}")
            raise

# Main execution
if __name__ == "__main__":
    try:
        server = EduChainMCPServer()
        server.run_server()
    except KeyboardInterrupt:
        logger.info("👋 Server stopped by user")
    except Exception as e:
        logger.error(f"💥 Fatal error: {str(e)}")
        exit(1)