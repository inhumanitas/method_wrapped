# coding: utf-8


async def method(user, benefit_type, *args):
    results = []
    for role in user.roles:
        results.append(await role.get_model().calc(benefit_type, *args))
    return results
