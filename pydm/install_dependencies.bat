@echo off
chcp 65001 >nul
echo ========================================
echo 大漠注册系统 - 依赖安装脚本
echo ========================================
echo.

echo 正在检测系统中的Python安装...
echo.

:: 检查py启动器
where py >nul 2>&1
if %errorlevel% equ 0 (
    echo [1] 使用py启动器安装依赖...
    py -m pip install --upgrade pip
    py -m pip install -r requirements.txt
    echo.
)

:: 检查python命令
where python >nul 2>&1
if %errorlevel% equ 0 (
    echo [2] 使用python命令安装依赖...
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
    echo.
)

:: 检查python3命令
where python3 >nul 2>&1
if %errorlevel% equ 0 (
    echo [3] 使用python3命令安装依赖...
    python3 -m pip install --upgrade pip
    python3 -m pip install -r requirements.txt
    echo.
)

:: 尝试从注册表查找Python安装路径
echo [4] 从注册表查找Python安装...
for /f "tokens=2*" %%a in ('reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Python\PythonCore" /s /v ExecutablePath 2^>nul ^| findstr "ExecutablePath"') do (
    echo 找到Python: %%b
    "%%b" -m pip install --upgrade pip
    "%%b" -m pip install -r requirements.txt
    echo.
)

:: 检查常见安装路径
echo [5] 检查常见Python安装路径...
set "paths=C:\Python27 C:\Python35 C:\Python36 C:\Python37 C:\Python38 C:\Python39 C:\Python310 C:\Python311 C:\Python312"
set "paths=%paths% %LOCALAPPDATA%\Programs\Python\Python37 %LOCALAPPDATA%\Programs\Python\Python38"
set "paths=%paths% %LOCALAPPDATA%\Programs\Python\Python39 %LOCALAPPDATA%\Programs\Python\Python310"
set "paths=%paths% %LOCALAPPDATA%\Programs\Python\Python311 %LOCALAPPDATA%\Programs\Python\Python312"

for %%p in (%paths%) do (
    if exist "%%p\python.exe" (
        echo 找到Python: %%p\python.exe
        "%%p\python.exe" -m pip install --upgrade pip
        "%%p\python.exe" -m pip install -r requirements.txt
        echo.
    )
)

echo ========================================
echo 依赖安装完成！
echo ========================================
echo.
echo 已安装的依赖包：
echo - PyQt5 ^>= 5.15.0
echo - pywin32 ^>= 300
echo.
pause