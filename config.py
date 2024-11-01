
# User API endpoints
BASE_URL = "https://stellarburgers.nomoreparties.site/api"

# User API endpoints
REGISTER_USER_URL = f"{BASE_URL}/auth/register"
LOGIN_USER_URL = f"{BASE_URL}/auth/login"
LOGOUT_USER_URL = f"{BASE_URL}/auth/logout"
RESET_PASSWORD_URL = f"{BASE_URL}/password-reset"
RESET_PASSWORD_CONFIRM_URL = f"{BASE_URL}/password-reset/reset"
USER_INFO_URL = f"{BASE_URL}/auth/user"
REFRESH_TOKEN_URL = f"{BASE_URL}/auth/token"
UPDATE_USER_URL = f"{BASE_URL}/auth/user"
CREATE_ORDER_URL = f"{BASE_URL}/orders"
INGREDIENTS_URL = f"{BASE_URL}/ingredients"
USER_ORDERS_URL = f"{BASE_URL}/orders"
ERROR_MESSAGE_MISSING_INGREDIENTS = "Ingredient ids must be provided"
ERROR_MESSAGE_INVALID_INGREDIENT_HASH = "Internal Server Error"


