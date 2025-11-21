"""获取大漠插件机器码示例"""
from damao_lib import DaMao

# 创建大漠对象（免COM注册，但仍需注册码才能使用完整功能）
# 不提供注册码时，只能使用少数基础功能
dm = DaMao()

print(f"大漠版本: {dm.Ver()}")
print(f"机器码: {dm.GetMachineCode()}")