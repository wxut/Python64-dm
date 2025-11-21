"""配置向导对话框"""
import sys
import os
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QSpinBox, QPushButton, QWizard,
                             QWizardPage, QTextEdit, QMessageBox)
from PyQt5.QtCore import Qt

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from damao_register.config_manager import ConfigManager


class WelcomePage(QWizardPage):
    """欢迎页"""
    
    def __init__(self):
        super().__init__()
        self.setTitle("欢迎使用大漠免COM注册系统")
        
        layout = QVBoxLayout()
        
        welcome_text = QTextEdit()
        welcome_text.setReadOnly(True)
        welcome_text.setHtml("""
        <h2>欢迎！</h2>
        <p>这是一个大漠插件免COM注册和虚拟机器码注册系统。</p>
        <h3>主要功能：</h3>
        <ul>
            <li>✅ 免COM注册 - 无需regsvr32注册COM组件</li>
            <li>✅ 注册码模式 - 使用注册码激活完整功能</li>
            <li>✅ 虚拟机器码模式 - 使用虚拟机器码注册</li>
            <li>✅ 自动生成硬件配置</li>
            <li>✅ 定时自动注册</li>
        </ul>
        <p>接下来将引导您完成基础配置。</p>
        """)
        layout.addWidget(welcome_text)
        
        self.setLayout(layout)


class RegisterModePage(QWizardPage):
    """注册模式选择页"""
    
    def __init__(self):
        super().__init__()
        self.setTitle("选择注册模式")
        self.setSubTitle("请选择您想使用的注册模式")
        
        layout = QVBoxLayout()
        
        # 注册码输入
        reg_layout = QHBoxLayout()
        reg_layout.addWidget(QLabel("注册码:"))
        self.reg_code_edit = QLineEdit()
        self.reg_code_edit.setPlaceholderText("留空则仅使用基础功能")
        reg_layout.addWidget(self.reg_code_edit)
        layout.addLayout(reg_layout)
        
        # 附加码输入
        add_layout = QHBoxLayout()
        add_layout.addWidget(QLabel("附加码:"))
        self.add_code_edit = QLineEdit()
        self.add_code_edit.setPlaceholderText("可选")
        add_layout.addWidget(self.add_code_edit)
        layout.addLayout(add_layout)
        
        # 说明文本
        info_text = QLabel("""
        <b>注册模式说明：</b><br>
        • <b>未注册状态</b>：不填写注册码，仅可使用基础功能<br>
        • <b>注册码模式</b>：填写注册码，激活完整功能<br>
        • <b>虚拟机器码模式</b>：填写注册码，系统自动生成虚拟机器码
        """)
        info_text.setWordWrap(True)
        layout.addWidget(info_text)
        
        self.setLayout(layout)
        
        # 注册字段
        self.registerField("reg_code", self.reg_code_edit)
        self.registerField("add_code", self.add_code_edit)


class MachineConfigPage(QWizardPage):
    """机器配置页"""
    
    def __init__(self):
        super().__init__()
        self.setTitle("配置虚拟机器")
        self.setSubTitle("设置虚拟机器数量和注册间隔")
        
        layout = QVBoxLayout()
        
        # 机器数量
        count_layout = QHBoxLayout()
        count_layout.addWidget(QLabel("虚拟机器数量:"))
        self.machine_count_spin = QSpinBox()
        self.machine_count_spin.setRange(1, 100)
        self.machine_count_spin.setValue(5)
        count_layout.addWidget(self.machine_count_spin)
        count_layout.addWidget(QLabel("台"))
        count_layout.addStretch()
        layout.addLayout(count_layout)
        
        # 注册间隔
        interval_layout = QHBoxLayout()
        interval_layout.addWidget(QLabel("注册间隔:"))
        self.interval_spin = QSpinBox()
        self.interval_spin.setRange(1, 24)
        self.interval_spin.setValue(2)
        interval_layout.addWidget(self.interval_spin)
        interval_layout.addWidget(QLabel("小时"))
        interval_layout.addStretch()
        layout.addLayout(interval_layout)
        
        # 说明文本
        info_text = QLabel("""
        <b>配置说明：</b><br>
        • <b>虚拟机器数量</b>：系统将为每台虚拟机器生成独立的硬件配置和虚拟机器码<br>
        • <b>注册间隔</b>：系统将按此间隔自动重新注册所有虚拟机器
        """)
        info_text.setWordWrap(True)
        layout.addWidget(info_text)
        
        self.setLayout(layout)
        
        # 注册字段
        self.registerField("machine_count", self.machine_count_spin)
        self.registerField("interval_hours", self.interval_spin)


class SummaryPage(QWizardPage):
    """配置总结页"""
    
    def __init__(self):
        super().__init__()
        self.setTitle("配置完成")
        self.setSubTitle("请确认您的配置")
        
        layout = QVBoxLayout()
        
        self.summary_text = QTextEdit()
        self.summary_text.setReadOnly(True)
        layout.addWidget(self.summary_text)
        
        self.setLayout(layout)
    
    def initializePage(self):
        """初始化页面时更新总结"""
        reg_code = self.field("reg_code")
        add_code = self.field("add_code")
        machine_count = self.field("machine_count")
        interval_hours = self.field("interval_hours")
        
        mode = "未注册状态（基础功能）" if not reg_code else "虚拟机器码注册模式"
        
        summary = f"""
        <h3>配置总结</h3>
        <table border="1" cellpadding="5" cellspacing="0">
            <tr><td><b>注册模式</b></td><td>{mode}</td></tr>
            <tr><td><b>注册码</b></td><td>{reg_code if reg_code else '未设置'}</td></tr>
            <tr><td><b>附加码</b></td><td>{add_code if add_code else '未设置'}</td></tr>
            <tr><td><b>虚拟机器数量</b></td><td>{machine_count} 台</td></tr>
            <tr><td><b>注册间隔</b></td><td>{interval_hours} 小时</td></tr>
        </table>
        <br>
        <p>点击"完成"按钮保存配置并启动系统。</p>
        """
        
        self.summary_text.setHtml(summary)


class ConfigWizard(QWizard):
    """配置向导"""
    
    def __init__(self, config_manager: ConfigManager):
        super().__init__()
        self.config_manager = config_manager
        
        self.setWindowTitle("配置向导")
        self.setWizardStyle(QWizard.ModernStyle)
        self.setOption(QWizard.HaveHelpButton, False)
        
        # 添加页面
        self.addPage(WelcomePage())
        self.addPage(RegisterModePage())
        self.addPage(MachineConfigPage())
        self.addPage(SummaryPage())
        
        # 设置按钮文本
        self.setButtonText(QWizard.FinishButton, "完成")
        self.setButtonText(QWizard.CancelButton, "取消")
        self.setButtonText(QWizard.NextButton, "下一步")
        self.setButtonText(QWizard.BackButton, "上一步")
        
        # 连接完成信号
        self.finished.connect(self.on_finished)
    
    def on_finished(self, result):
        """向导完成时保存配置"""
        if result == QDialog.Accepted:
            # 获取配置值
            reg_code = self.field("reg_code")
            add_code = self.field("add_code")
            machine_count = self.field("machine_count")
            interval_hours = self.field("interval_hours")
            
            # 保存配置
            self.config_manager.set_register_code(reg_code if reg_code else "")
            self.config_manager.set_additional_code(add_code if add_code else "")
            self.config_manager.set_machine_count(machine_count)
            self.config_manager.set_interval_hours(interval_hours)
            
            QMessageBox.information(self, "成功", "配置已保存！\n\n系统将使用新配置启动。")