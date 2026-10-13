# AI Prompts

AI assistant used: ChatGPT (OpenAI)

## 1. Code Review

Prompt:

> Review the Django views `order_create`, `create_checkout_session`, and `payment_success`. Focus on transaction safety, database query efficiency, Stripe integration, duplicate operations, and error handling. Suggest improvements that are appropriate for this project.
## 2. Model Tests

Prompt:

> Generate pytest-django tests for the `Book`, `Order`, and `OrderItem` models using factory-boy. Test string representations, default values, relationships, and `OrderItem.get_cost()`. Add the comment `Generated with AI, reviewed and modified` to each AI-generated test.
## 3. View Docstrings

Prompt:

> Generate concise Python docstrings for all Django views in `catalog/views.py`, `orders/views.py`, and `accounts/views.py`. Describe what each view does without changing its behavior.
## 4. README Documentation

Prompt:

> Improve the README for the Django Bookstore project. Document the main features, Docker setup, testing, coverage, and add an `AI Usage` section describing how AI was used in the project.