"""Qt实时日志处理器"""
import logging
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QTextCursor, QColor


class QTextEditLogger(QObject, logging.Handler):
    """Qt文本框日志处理器 - 实时显示日志"""
    
    log_signal = pyqtSignal(str, str)  # (message, level)
    
    def __init__(self, text_edit):
        QObject.__init__(self)
        logging.Handler.__init__(self)
        self.text_edit = text_edit
        self.log_signal.connect(self._append_log)
        
        # 日志级别颜色映射
        self.colors = {
            'DEBUG': '#808080',    # 灰色
            'INFO': '#00AA00',     # 绿色
            'WARNING': '#FFA500',  # 橙色
            'ERROR': '#FF0000',    # 红色
            'CRITICAL': '#8B0000'  # 深红色
        }
    
    def emit(self, record):
        """发送日志记录"""
        try:
            msg = self.format(record)
            level = record.levelname
            self.log_signal.emit(msg, level)
        except Exception:
            self.handleError(record)
    
    def _append_log(self, message, level):
        """追加日志到文本框（带颜色）"""
        cursor = self.text_edit.textCursor()
        cursor.movePosition(QTextCursor.End)
        
        # 设置颜色
        color = self.colors.get(level, '#000000')
        self.text_edit.setTextColor(QColor(color))
        
        # 追加文本
        cursor.insertText(message + '\n')
        
        # 滚动到底部
        self.text_edit.setTextCursor(cursor)
        self.text_edit.ensureCursorVisible()