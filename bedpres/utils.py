def get_bpc_user_dictionary(user):
    """Get a the user information required for bpc from a NablaUser-object"""
    return {"fullname": user.get_full_name(),
            "username": user.username,
            "card_no": user.get_hashed_ntnu_card_number(),
            "year": str(user.get_class_number())}
