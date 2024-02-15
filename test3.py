import asyncio
from Services.SheduleService import get_shedule


loop = asyncio.get_event_loop()
result = loop.run_until_complete(get_shedule("ivachshenko.gennadiy", "5t8x9m780165_"))
print(result)
