# 驱动签名脚本 (PowerShell版本)
Write-Host "========================================"
Write-Host "驱动签名工具 (PowerShell)"
Write-Host "========================================"
Write-Host ""

# 检查管理员权限
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "[错误] 需要管理员权限运行此脚本" -ForegroundColor Red
    Read-Host "按回车键退出"
    exit 1
}

# 设置变量
$certName = "TestDriverCert"
$driverPath = "bin\hwid_spoofer_kernel.sys"
$driverX64Path = "bin\x64\hwid_spoofer_kernel.sys"

Write-Host "[1/4] 检查驱动文件..."
if (-not (Test-Path $driverPath)) {
    Write-Host "[错误] 驱动文件不存在: $driverPath" -ForegroundColor Red
    Read-Host "按回车键退出"
    exit 1
}
Write-Host "[OK] 驱动文件存在" -ForegroundColor Green

Write-Host ""
Write-Host "[2/4] 查找证书..."
$cert = Get-ChildItem -Path Cert:\LocalMachine\Root | Where-Object { $_.Subject -like "*$certName*" } | Select-Object -First 1

if ($null -eq $cert) {
    Write-Host "[错误] 未找到测试证书: $certName" -ForegroundColor Red
    Write-Host ""
    Write-Host "请先安装证书:"
    Write-Host "1. 双击 TestDriverCert.cer"
    Write-Host "2. 选择'本地计算机'"
    Write-Host "3. 安装到'受信任的根证书颁发机构'"
    Read-Host "按回车键退出"
    exit 1
}
Write-Host "[OK] 找到证书: $($cert.Subject)" -ForegroundColor Green

Write-Host ""
Write-Host "[3/4] 使用 PowerShell 签名驱动..."
try {
    Set-AuthenticodeSignature -FilePath $driverPath -Certificate $cert -TimestampServer "http://timestamp.digicert.com"
    Write-Host "[OK] 主驱动文件签名成功" -ForegroundColor Green
} catch {
    Write-Host "[错误] 签名失败: $_" -ForegroundColor Red
    Read-Host "按回车键退出"
    exit 1
}

Write-Host ""
Write-Host "[4/4] 签名 x64 目录中的驱动..."
if (Test-Path $driverX64Path) {
    try {
        Set-AuthenticodeSignature -FilePath $driverX64Path -Certificate $cert -TimestampServer "http://timestamp.digicert.com"
        Write-Host "[OK] x64 驱动文件签名成功" -ForegroundColor Green
    } catch {
        Write-Host "[警告] x64 驱动签名失败: $_" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "========================================"
Write-Host "[完成] 驱动签名完成!" -ForegroundColor Green
Write-Host "========================================"
Write-Host ""
Write-Host "下一步:"
Write-Host "1. 重新运行 diagnose_driver.py 验证签名"
Write-Host "2. 如果仍有问题,请重启电脑"
Write-Host ""
Read-Host "按回车键退出"