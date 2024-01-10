class InvalidRequestError(Exception):
    pass


class UserAlreadyExistsError(Exception):
    pass


class UserNotFoundError(Exception):
    pass


class UserDoesNotHaveStripeIdError(Exception):
    pass


class InternalServerError(Exception):
    pass
