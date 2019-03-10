from http import cookies

C = cookies.SimpleCookie()
# C["rocky"] = "road"
# C["rocky"]["path"] = "/cookie"
# print(C.output(attrs = [], header = "Cookie:"))
C.load("chips=ahoy; vienna=finger")
print(C)
