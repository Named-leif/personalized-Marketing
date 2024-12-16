# Personalized Content Generation

## Description
The **Personalized Content Generation** system automates the creation of customized marketing strategies through a multi-agent framework. 

The process begins with **user-provided input**:
- Product category
- Product information
- Target communication channels
- Additional notes

The **Manager_LLM** oversees the entire workflow, coordinating tasks among specialized agents.

---

## Workflow
![Workflow Diagram](docs/framework.png)

### Agents and Tasks
1. **Product Researcher**  
   - Identify consumer trends, target audience, and product insights.  
   - **Tool**: SerperDev Tool  

2. **Data Analyst**  
   - Analyze consumer feedback and deliver insights.  

3. **Strategy Agent**  
   - Segment the target audience and recommend channels.

4. **Copy Creator**  
   - Create customized messages and DALL·E prompts.  

5. **Content Creator**  
   - Design visuals based on the communication strategy.  
   - **Tool**: DALL·E Tool

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/USERNAME/Personalized-Content-Generation.git
   cd Personalized-Content-Generation

2. Set up Python enviroment:
   ```bash
   conda create --name content_env python=3.11.10
   conda activate content_env

3. Install dependencies:
   ```bash
   pip install -r requirements.txt

4. Add API keys: Create a .env file in the root directory
   ```bash
   touch .env
   OPENAI_API_KEY=your_openai_api_key
   SERPER_API_KEY=your_serper_api_key
   
5. Run the project:
   ```bash
   python src/trend_content/main.py


