# EduChain MCP Server 

An MCP (Model Context Protocol) server that integrates the EduChain library with Google Gemini API to provide AI-powered educational content generation.

## Features

- 🎓 **Educational Content Generation**
  - Multiple-choice questions (MCQs) on any academic topic
  - Comprehensive lesson plans with objectives and activities
  - Study flashcards (bonus feature)
  
- 🤖 **AI-Powered**
  - Powered by Google Gemini's advanced language model
  - Customizable difficulty levels and learning objectives
  - Context-aware content generation

- 🔌 **MCP Integration**
  - Seamless integration with Claude Desktop
  - Standardized API endpoints for educational tools
  - Extensible architecture for additional features

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.8 or higher
- Google Gemini API key
- Claude Desktop installed (for testing)
- Node.js (for MCP support in Claude Desktop)

## Installation

To install EduChain MCP Server, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/educhain-mcp-server.git
   cd educhain-mcp-server
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file:
   ```bash
   cp .env.example .env
   ```
   Then edit `.env` and add your Google Gemini API key.

## Usage

### Starting the Server
```bash
python educhain_mcp_server.py
```

### Testing with Claude Desktop
1. Configure Claude Desktop by editing `claude_desktop_config.json`
2. Update the `cwd` path to your project directory
3. Add your Google API key in the environment variables
4. Restart Claude Desktop

### Example Commands
- Generate MCQs: "Create 5 multiple-choice questions about Python loops"
- Get lesson plan: "Provide a 45-minute lesson plan on algebra for high school"
- Create flashcards: "Make 10 definition flashcards about data structures"

## Project Structure

```
educhain-mcp-server/
├── educhain_mcp_server.py      # Main server implementation
├── test_educhain.py            # Setup verification
├── requirements.txt            # Python dependencies
├── .env                        # Environment config (ignored)
├── .env.example                # Environment template
├── claude_desktop_config.json  # Claude config
├── README.md                   # This file
└── .gitignore                  # Git ignore rules
```

## API Documentation

The server provides the following MCP endpoints:

### Tools
- `generate_mcq(topic, num_questions, difficulty_level, custom_instructions)`
- `generate_lesson_plan(topic, duration, grade_level, learning_objectives)`
- `generate_flashcards(topic, num_cards, difficulty_level, card_type)`

### Resources
- `educhain://topic/{topic}` - Get topic overview
- `educhain://questions/{topic}` - Get sample questions

## Troubleshooting

If you encounter issues:

- **Server not starting**: 
  - Verify Python is in your PATH
  - Check all dependencies are installed (`pip list`)
  - Ensure Google API key is valid

- **Tools not appearing in Claude**:
  - Restart Claude Desktop completely
  - Check server logs for errors
  - Verify JSON configuration syntax

## License
This project is licensed under the MIT License
