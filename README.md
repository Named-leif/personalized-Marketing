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
