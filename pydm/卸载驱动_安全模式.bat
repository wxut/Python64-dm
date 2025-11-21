@echo off
chcp 65001 >nul
echo ========================================
echo 驱动卸载工具 - 请在安全模式下运行
echo ========================================
echo.

:: 检查管理员权限
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [错误] 需要管理员权限!
    echo 请右键点击此文件,选择"以管理员身份运行"
    pause
    exit /b 1
)

echo [1/4] 停止驱动服务...
sc stop hwid_spoofer_kernel 2>nul
if %errorLevel% equ 0 (
    echo     ✓ 驱动服务已停止
) else (
    echo     - 驱动服务未运行或已停止
)

echo.
echo [2/4] 删除驱动服务...
sc delete hwid_spoofer_kernel 2>nul
if %errorLevel% equ 0 (
    echo     ✓ 驱动服务已删除
) else (
    echo     - 驱动服务不存在或已删除
)

echo.
echo [3/4] 删除驱动文件...
set DRIVER_PATH=%~dp0bin\hwid_spoofer_kernel.sys
if exist "%DRIVER_PATH%" (
    del /f /q "%DRIVER_PATH%" 2>nul
    if %errorLevel% equ 0 (
        echo     ✓ 驱动文件已删除: %DRIVER_PATH%
    ) else (
        echo     ✗ 无法删除驱动文件,可能被占用
    )
) else (
    echo     - 驱动文件不存在
)

echo.
echo [4/4] 清理注册表...
reg delete "HKLM\SYSTEM\CurrentControlSet\Services\hwid_spoofer_kernel" /f >nul 2>&1
if %errorLevel% equ 0 (
    echo     ✓ 注册表项已清理
) else (
    echo     - 注册表项不存在或已清理
)

echo.
echo ========================================
echo 清理完成!
echo ========================================
echo.
echo 建议操作:
echo 1. 重启电脑进入正常模式
echo 2. 不要再使用 hwid_spoofer_kernel.sys 驱动
echo 3. 如需修改硬件ID,请使用虚拟机或官方授权方案
echo.
pause