from Services.UserService import User
from Services.SheduleService import get_shedule

user = User(username="ivachshenko.gennadiy", password="5t8x9m780265_")

shedule = get_shedule(user)
print(shedule)
