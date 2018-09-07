

class InvalidCardNum(Exception):
    pass


def get_bpc_user_dictionary(user):
    """Get a the user information required for bpc from a NablaUser-object

    Raises: InvalidCardNum
    """
    card_no = user.ntnu_card_number
    if not card_no or not card_no.isdigit():
        raise InvalidCardNum(f"User {user} has an invalid cardnumber {card_no}")

    return {"fullname": user.get_full_name(),
            "username": user.username,
            "card_no": user.get_hashed_ntnu_card_number(),
            "year": str(user.get_class_number())}
