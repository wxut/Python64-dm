"""虚拟机器码管理标签页"""
import sys
import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                             QTableWidgetItem, QPushButton, QMessageBox, QHeaderView,
                             QLineEdit, QLabel, QFileDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QClipboard
from PyQt5.QtWidgets import QApplication

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from damao_register.config_manager import HWIDProfileManager
from damao_register.hwid_generator import HWIDGenerator


class VirtualCodeTab(QWidget):
    """虚拟机器码管理标签页"""
    
    def __init__(self, profile_mgr: HWIDProfileManager):
        super().__init__()
        self.profile_mgr = profile_mgr
        self.init_ui()
        self.load_profiles()
    
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        
        # 工具栏
        toolbar = QHBoxLayout()
        
        self.refresh_btn = QPushButton("🔄 刷新")
        self.refresh_btn.clicked.connect(self.load_profiles)
        toolbar.addWidget(self.refresh_btn)
        
        self.generate_btn = QPushButton("➕ 生成新配置")
        self.generate_btn.clicked.connect(self.generate_new_profile)
        toolbar.addWidget(self.generate_btn)
        
        self.export_btn = QPushButton("📤 导出")
        self.export_btn.clicked.connect(self.export_profiles)
        toolbar.addWidget(self.export_btn)
        
        self.clear_codes_btn = QPushButton("🧹 清理机器码")
        self.clear_codes_btn.clicked.connect(self.clear_all_machine_codes)
        toolbar.addWidget(self.clear_codes_btn)
        
        toolbar.addStretch()
        layout.addLayout(toolbar)
        
        # 表格
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "ID", "厂商", "产品名称", "虚拟机器码", "真实机器码", "注册次数", "操作"
        ])
        
        # 设置列宽
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        header.setSectionResizeMode(4, QHeaderView.Stretch)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)
        
        layout.addWidget(self.table)
        
        # 统计信息
        self.stats_label = QLabel()
        layout.addWidget(self.stats_label)
    
    def load_profiles(self):
        """加载硬件配置"""
        profiles = self.profile_mgr.get_all_profiles()
        self.table.setRowCount(len(profiles))
        
        for row, profile in enumerate(profiles):
            # ID
            self.table.setItem(row, 0, QTableWidgetItem(str(profile.get('id', ''))))
            
            # 厂商
            self.table.setItem(row, 1, QTableWidgetItem(profile.get('manufacturer', '')))
            
            # 产品名称
            self.table.setItem(row, 2, QTableWidgetItem(profile.get('product_name', '')))
            
            # 虚拟机器码
            virtual_code = profile.get('virtual_machine_code', '')
            virtual_item = QTableWidgetItem(virtual_code)
            virtual_item.setToolTip("双击复制")
            self.table.setItem(row, 3, virtual_item)
            
            # 真实机器码
            machine_code = profile.get('machine_code', '未注册')
            self.table.setItem(row, 4, QTableWidgetItem(machine_code))
            
            # 注册次数
            count = self.get_machine_code_count(machine_code)
            self.table.setItem(row, 5, QTableWidgetItem(str(count)))
            
            # 操作按钮
            btn_widget = QWidget()
            btn_layout = QHBoxLayout(btn_widget)
            btn_layout.setContentsMargins(2, 2, 2, 2)
            
            copy_btn = QPushButton("📋")
            copy_btn.setToolTip("复制虚拟机器码")
            copy_btn.clicked.connect(lambda checked, vc=virtual_code: self.copy_to_clipboard(vc))
            btn_layout.addWidget(copy_btn)
            
            delete_btn = QPushButton("🗑️")
            delete_btn.setToolTip("删除配置")
            delete_btn.clicked.connect(lambda checked, pid=profile.get('id'): self.delete_profile(pid))
            btn_layout.addWidget(delete_btn)
            
            self.table.setCellWidget(row, 6, btn_widget)
        
        # 更新统计信息
        self.update_stats(profiles)
        
        # 双击复制虚拟机器码
        self.table.cellDoubleClicked.connect(self.on_cell_double_clicked)
    
    def get_machine_code_count(self, machine_code):
        """获取机器码注册次数"""
        if machine_code == '未注册':
            return 0
        
        try:
            import os
            log_file = "logs/simple_register.log"
            if not os.path.exists(log_file):
                return 0
            
            with open(log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            for line in lines:
                if machine_code in line and ',' in line:
                    parts = line.strip().split(',')
                    if len(parts) >= 3:
                        return int(parts[2])
            return 0
        except:
            return 0
    
    def on_cell_double_clicked(self, row, col):
        """双击单元格事件"""
        if col == 3:  # 虚拟机器码列
            item = self.table.item(row, col)
            if item:
                self.copy_to_clipboard(item.text())
    
    def copy_to_clipboard(self, text):
        """复制到剪贴板"""
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
        QMessageBox.information(self, "成功", f"已复制到剪贴板:\n{text}")
    
    def generate_new_profile(self):
        """生成新配置"""
        profile = HWIDGenerator.generate_profile()
        profile['id'] = len(self.profile_mgr.get_all_profiles()) + 1
        
        if self.profile_mgr.add_profile(profile):
            QMessageBox.information(self, "成功", "新配置已生成")
            self.load_profiles()
        else:
            QMessageBox.warning(self, "失败", "生成配置失败")
    
    def delete_profile(self, profile_id):
        """删除配置"""
        reply = QMessageBox.question(
            self, "确认删除",
            f"确定要删除配置 ID {profile_id} 吗？",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.profile_mgr.remove_profile(profile_id):
                QMessageBox.information(self, "成功", "配置已删除")
                self.load_profiles()
            else:
                QMessageBox.warning(self, "失败", "删除配置失败")
    
    def export_profiles(self):
        """导出配置"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "导出配置", "", "JSON Files (*.json)"
        )
        
        if filename:
            import json
            profiles = self.profile_mgr.get_all_profiles()
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(profiles, f, indent=2, ensure_ascii=False)
                QMessageBox.information(self, "成功", f"配置已导出到:\n{filename}")
            except Exception as e:
                QMessageBox.warning(self, "失败", f"导出失败: {e}")
    
    def clear_all_machine_codes(self):
        """清理所有虚拟机器码配置"""
        reply = QMessageBox.question(
            self, "确认清理",
            "确定要删除所有虚拟机器码配置吗？此操作不可撤销。",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            profiles = self.profile_mgr.get_all_profiles()
            for profile in profiles:
                self.profile_mgr.remove_profile(profile['id'])
            
            QMessageBox.information(self, "成功", "所有虚拟机器码配置已删除")
            self.load_profiles()
    
    def update_stats(self, profiles):
        """更新统计信息"""
        total = len(profiles)
        registered = sum(1 for p in profiles if p.get('machine_code') and p.get('machine_code') != '未注册')
        self.stats_label.setText(f"总配置数: {total} | 已注册: {registered} | 未注册: {total - registered}")