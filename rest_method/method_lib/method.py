# coding: utf-8
import asyncio


@asyncio.coroutine
def method(user, benefit_type, *args, **kwargs):
    results = []
    for role in user.roles:
        results.append(role.get_model().calc(benefit_type, *args, **kwargs))
    return results
