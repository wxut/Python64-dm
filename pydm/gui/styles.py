"""GUI样式表定义"""

# 主题颜色
COLORS = {
    'primary': '#2196F3',      # 蓝色
    'success': '#4CAF50',      # 绿色
    'warning': '#FFA500',      # 橙色
    'danger': '#f44336',       # 红色
    'info': '#00BCD4',         # 青色
    'background': '#f5f5f5',   # 浅灰背景
    'surface': '#ffffff',      # 白色表面
    'text': '#212121',         # 深色文本
    'text_secondary': '#757575', # 次要文本
    'border': '#cccccc',       # 边框
}

# 完整样式表
MAIN_STYLE = f"""
/* 全局样式 */
QMainWindow {{
    background-color: {COLORS['background']};
}}

/* 标签页样式 */
QTabWidget::pane {{
    border: 1px solid {COLORS['border']};
    background-color: {COLORS['surface']};
    border-radius: 4px;
}}

QTabBar::tab {{
    background-color: #e0e0e0;
    padding: 10px 20px;
    margin-right: 2px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    font-weight: 500;
}}

QTabBar::tab:selected {{
    background-color: {COLORS['surface']};
    border-bottom: 3px solid {COLORS['primary']};
}}

QTabBar::tab:hover {{
    background-color: #d0d0d0;
}}

/* 按钮样式 */
QPushButton {{
    border: none;
    border-radius: 4px;
    padding: 8px 16px;
    font-weight: 500;
    background-color: {COLORS['primary']};
    color: white;
}}

QPushButton:hover {{
    background-color: #1976D2;
}}

QPushButton:pressed {{
    background-color: #0D47A1;
}}

QPushButton:disabled {{
    background-color: #BDBDBD;
    color: #757575;
}}

/* 输入框样式 */
QLineEdit, QSpinBox {{
    border: 1px solid {COLORS['border']};
    border-radius: 4px;
    padding: 6px 10px;
    background-color: {COLORS['surface']};
}}

QLineEdit:focus, QSpinBox:focus {{
    border: 2px solid {COLORS['primary']};
}}

/* 文本编辑器样式 */
QTextEdit {{
    border: 1px solid {COLORS['border']};
    border-radius: 4px;
    background-color: {COLORS['surface']};
    font-family: 'Consolas', 'Monaco', monospace;
}}

/* 表格样式 */
QTableWidget {{
    border: 1px solid {COLORS['border']};
    border-radius: 4px;
    background-color: {COLORS['surface']};
    gridline-color: #e0e0e0;
}}

QTableWidget::item {{
    padding: 8px;
}}

QTableWidget::item:selected {{
    background-color: {COLORS['primary']};
    color: white;
}}

QHeaderView::section {{
    background-color: #f0f0f0;
    padding: 8px;
    border: none;
    border-bottom: 2px solid {COLORS['primary']};
    font-weight: bold;
}}

/* 进度条样式 */
QProgressBar {{
    border: 1px solid {COLORS['border']};
    border-radius: 4px;
    text-align: center;
    background-color: #e0e0e0;
}}

QProgressBar::chunk {{
    background-color: {COLORS['success']};
    border-radius: 3px;
}}

/* 标签样式 */
QLabel {{
    color: {COLORS['text']};
}}

/* 分组框样式 */
QGroupBox {{
    border: 1px solid {COLORS['border']};
    border-radius: 6px;
    margin-top: 12px;
    padding-top: 12px;
    font-weight: bold;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 8px;
    color: {COLORS['primary']};
}}

/* 状态栏样式 */
QStatusBar {{
    background-color: {COLORS['surface']};
    border-top: 1px solid {COLORS['border']};
}}

/* 滚动条样式 */
QScrollBar:vertical {{
    border: none;
    background-color: #f0f0f0;
    width: 10px;
    margin: 0;
}}

QScrollBar::handle:vertical {{
    background-color: #c0c0c0;
    border-radius: 5px;
    min-height: 20px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: #a0a0a0;
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

/* 工具提示样式 */
QToolTip {{
    background-color: {COLORS['text']};
    color: white;
    border: none;
    border-radius: 4px;
    padding: 6px;
}}
"""

def get_button_style(color_type='primary'):
    """获取特定颜色的按钮样式"""
    color = COLORS.get(color_type, COLORS['primary'])
    return f"""
    QPushButton {{
        background-color: {color};
        color: white;
        border: none;
        border-radius: 4px;
        padding: 8px 16px;
        font-weight: bold;
    }}
    QPushButton:hover {{
        opacity: 0.9;
    }}
    QPushButton:pressed {{
        opacity: 0.8;
    }}
    """