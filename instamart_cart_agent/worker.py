from shopping_agent_models import (
    ShoppingItems,
    ShoppingAgent,
    CartAddResult,
    CartValue,
    ClearCartResult,
    ShoppingOperation,
)
import asyncio
from instamart_cart_agent.agent import handle_request
class InstaMartAgent:

    async def cartadd(
        self,
        items: ShoppingItems
    ) -> list[CartAddResult]:

        results = []

        for item in items.items:
            text = f"Add {item.quantity or 1}"
            if item.unit:
                text += f" {item.unit}"
            text += f" of {item.item} to my cart."

            try:
                result = await handle_request(ShoppingOperation.CART_ADD, text, CartAddResult)
                results.append(
                    CartAddResult(
                        item=item.item,
                        success=True,
                        message=str(result),
                    )
                )
            except Exception as exc:
                results.append(
                    CartAddResult(
                        item=item.item,
                        success=False,
                        message=str(exc),
                    )
                )

        return results

    async def view_cart(self) -> ShoppingItems:
        result = await handle_request(ShoppingOperation.VIEW_CART, "", ShoppingItems)
        return result

    async def cartvalue(self) -> CartValue:
        result = await handle_request(ShoppingOperation.CART_VALUE, "", CartValue)
        return result

    async def clear_cart(self) -> ClearCartResult:
        try:
            result = await handle_request(
                ShoppingOperation.CLEAR_CART,
                "",
                ClearCartResult
            )
            return result
        except Exception as exc:
            return ClearCartResult(
                success=False,
                items_removed=0,
                message=str(exc),
            )

instamart_agent: ShoppingAgent = InstaMartAgent()

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    command = input("Command (add to cart,view cart, clear cart,cart value): \n")
    command = command.strip().lower()
    command = "view cart" if command.startswith("view") else "add to cart" if command.startswith("add") else "clear cart" if command.startswith("clear") else "cart value" if command.startswith("cart value") else "unknown"
    request = input("Message: \n")
    response_model = ShoppingItems if command in ("view cart", "add to cart") else ClearCartResult if command == "clear cart" else CartValue if command == "cart value" else None
    if command == "add to cart":
        items = ShoppingItems.parse_raw(request)
        results = asyncio.run(instamart_agent.cartadd(items))
        print(results)
    elif command == "view cart":
        result = asyncio.run(instamart_agent.view_cart())
        print(result)
    elif command == "clear cart":
        result = asyncio.run(instamart_agent.clear_cart())
        print(result)
    elif command == "cart value":
        result = asyncio.run(instamart_agent.cartvalue())
        print(result)