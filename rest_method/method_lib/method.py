# coding: utf-8
import asyncio


@asyncio.coroutine
def method(user, **kwargs):
    results = []
    for role in user.roles:
        results.append(role.get_model().calc(**kwargs))
    return results
