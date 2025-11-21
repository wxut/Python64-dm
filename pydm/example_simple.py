"""大漠插件简单使用示例"""
from damao_lib import DaMao

# 重要: 所有功能必须注册后才能使用!
# 请将"your_reg_code"替换为您的注册码

dm = DaMao(reg_code="851935baac5d49b0f99f0a5a250fe62baf78d3", ver_info="vfr")

print(f"版本: {dm.Ver()}")
x, y = dm.GetCursorPos()
print(f"鼠标位置: ({x}, {y})")

dm.MoveTo(100, 100)
print("鼠标已移动到 (100, 100)")

dm.RightClick()
print("执行右键点击")