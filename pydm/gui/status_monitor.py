"""注册状态监控组件"""
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QLabel, QProgressBar)
from PyQt5.QtCore import QTimer, pyqtSignal
from datetime import datetime, timedelta


class StatusMonitor(QWidget):
    """注册状态监控组件"""
    
    status_changed = pyqtSignal(str, str)  # (status, color)
    
    def __init__(self):
        super().__init__()
        self.next_register_time = None
        self.total_count = 0
        self.success_count = 0
        self.fail_count = 0
        self.init_ui()
        self.init_timer()
    
    def init_ui(self):
        """初始化UI"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # 状态标签
        self.status_label = QLabel("状态: 就绪")
        layout.addWidget(self.status_label)
        
        # 统计信息
        self.stats_label = QLabel("总数: 0 | 成功: 0 | 失败: 0")
        layout.addWidget(self.stats_label)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        layout.addWidget(self.progress_bar)
        
        # 倒计时标签
        self.countdown_label = QLabel("下次注册: --:--:--")
        layout.addWidget(self.countdown_label)
        
        layout.addStretch()
    
    def init_timer(self):
        """初始化定时器"""
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_countdown)
        self.timer.start(1000)  # 每秒更新一次
    
    def set_status(self, status: str, color: str = "black"):
        """设置状态"""
        self.status_label.setText(f"状态: {status}")
        self.status_label.setStyleSheet(f"color: {color}; font-weight: bold;")
        self.status_changed.emit(status, color)
    
    def update_stats(self, total: int, success: int, fail: int):
        """更新统计信息"""
        self.total_count = total
        self.success_count = success
        self.fail_count = fail
        self.stats_label.setText(f"总数: {total} | 成功: {success} | 失败: {fail}")
    
    def set_progress(self, current: int, total: int):
        """设置进度"""
        if total > 0:
            percentage = int((current / total) * 100)
            self.progress_bar.setValue(percentage)
            self.progress_bar.setFormat(f"{current}/{total} ({percentage}%)")
        else:
            self.progress_bar.setValue(0)
            self.progress_bar.setFormat("0/0 (0%)")
    
    def set_next_register_time(self, next_time: datetime):
        """设置下次注册时间"""
        self.next_register_time = next_time
    
    def update_countdown(self):
        """更新倒计时"""
        if self.next_register_time:
            now = datetime.now()
            if now < self.next_register_time:
                delta = self.next_register_time - now
                hours = delta.seconds // 3600
                minutes = (delta.seconds % 3600) // 60
                seconds = delta.seconds % 60
                self.countdown_label.setText(f"下次注册: {hours:02d}:{minutes:02d}:{seconds:02d}")
            else:
                self.countdown_label.setText("下次注册: 即将开始")
        else:
            self.countdown_label.setText("下次注册: --:--:--")
    
    def reset(self):
        """重置状态"""
        self.set_status("就绪", "black")
        self.update_stats(0, 0, 0)
        self.set_progress(0, 0)
        self.next_register_time = None
        self.countdown_label.setText("下次注册: --:--:--")