@echo off
chcp 65001 >nul
echo ========================================
echo 大漠免注册系统启动器（智能版）
echo 自动检测系统架构并选择对应版本
echo ========================================
echo.

echo [1/4] 检查管理员权限...
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 需要管理员权限运行！
    echo 请右键点击此文件，选择"以管理员身份运行"
    echo.
    pause
    exit /b 1
)
echo [✓] 管理员权限检查通过
echo.

echo [2/4] 检测系统架构...
set "ARCH=x64"
if "%PROCESSOR_ARCHITECTURE%"=="x86" (
    if not defined PROCESSOR_ARCHITEW6432 (
        set "ARCH=x86"
        echo [✓] 检测到 32位 系统
    ) else (
        echo [✓] 检测到 64位 系统
    )
) else (
    echo [✓] 检测到 64位 系统
)
echo.

echo [3/4] 配置驱动路径...
set "DRIVER_PATH=bin\%ARCH%\hwid_spoofer_kernel.sys"
set "DLL_PATH=bin\%ARCH%\hwid_api.dll"

if not exist "%DRIVER_PATH%" (
    echo [警告] 未找到 %ARCH% 版本驱动: %DRIVER_PATH%
    echo 使用默认驱动路径...
    set "DRIVER_PATH=bin\hwid_spoofer_kernel.sys"
)

if not exist "%DLL_PATH%" (
    echo [警告] 未找到 %ARCH% 版本DLL: %DLL_PATH%
    echo 使用默认DLL路径...
    set "DLL_PATH=bin\hwid_api.dll"
)

echo [✓] 驱动路径: %DRIVER_PATH%
echo [✓] DLL路径: %DLL_PATH%
echo.

echo [4/4] 启动系统...
if "%ARCH%"=="x86" (
    echo 使用 32位 Python 运行...
    C:\Users\x\AppData\Local\Programs\Python\Python313-32\python.exe main.py
) else (
    echo 使用 64位 Python 运行...
    python main.py
)

if %errorlevel% neq 0 (
    echo.
    echo [错误] 程序运行失败，错误码: %errorlevel%
    echo.
    echo 可能的原因:
    echo 1. Python未安装或未添加到PATH
    echo 2. 缺少依赖包，请运行 install_dependencies.bat
    echo 3. 缺少必要的DLL文件
    echo 4. 驱动文件未编译，请运行 compile_all_drivers.bat
    echo.
    pause
    exit /b %errorlevel%
)

pause