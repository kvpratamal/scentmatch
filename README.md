# ScentMatch

ScentMatch is an AI-powered agent that recommends products (such as perfumes or scents) to users based on their preferences. It leverages a configurable workflow and language models to generate personalized sales pitches for available products.

## Features
- Configurable system prompt and language model
- Dynamically loads available products from the `products/` directory
- Uses a workflow graph to manage the sales recommendation process
- Generates sales pitches using LLMs based on user information and product descriptions

## Directory Structure

```
src/scentmatch/
├── configuration.py  # Defines agent configuration and available products
├── graph.py          # Builds the workflow graph using LangGraph
├── nodes.py          # Contains the node logic for generating sales pitches
├── state.py          # Defines the workflow state structure
```

## How It Works
1. **Configuration**: The agent loads its configuration, including the system prompt, model, and available products (from the `products/` directory).
2. **Workflow State**: User information is stored in the workflow state.
3. **Sales Node**: The agent selects a random product and loads its description. It then generates a sales pitch using a language model and a prompt template.
4. **Graph Execution**: The workflow is managed using a state graph, progressing from input to sales pitch generation.

## Setup Instructions
**Prepare products**: Place product description `.txt` files and images `.jpg` in a `products/` directory at the project root. Each file should be named after the product (e.g., `rose.txt`). Ensure there is a `sales_prompt.txt` file with the prompt template.

## Usage Example
To use the agent, run your entry point script (e.g., `app.py`). The agent will:
- Accept user information
- Select a product
- Generate and return a personalized sales pitch

## Customization
- **Add products**: Add new `.txt` files to the `products/` directory.
- **Change model or prompt**: Edit the configuration in `configuration.py`.

## License
MIT