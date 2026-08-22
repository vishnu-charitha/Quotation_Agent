from backend.agent import agent


def test_agent():

    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": """
                    I need 10 laptops with Intel Core i5,
                    16GB RAM and 512GB SSD.

                    Search suppliers and calculate the final
                    quotation price with 10% profit margin
                    and 18% GST.
                    """
                }
            ]
        }
    )

    print("\n--- AGENT RESPONSE ---\n")

    for message in response["messages"]:
        print(message)