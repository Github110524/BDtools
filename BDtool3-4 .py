import sys
import threading
import tkinter as tk
from tkinter import messagebox, filedialog, StringVar, ttk, Toplevel
import os
import re
import requests
import subprocess
import shutil
import json
from datetime import datetime
import time
import random

# 语言字典 - 包含中英文对照
LANGUAGES = {
    'zh': {
        'app_title': 'BDTools 3.4',
        'url_label': '请输入Bilibili视频网址：',
        'parse_btn': '解析视频',
        'video_info': '视频信息',
        'title_prefix': '标题: ',
        'quality_label': '选择画质：',
        'auto_quality': '自动选择最高画质',
        'choose_dir_btn': '选择保存目录',
        'download_btn': '开始下载',
        'ffmpeg_warning': '未检测到FFmpeg，下载的视频将无声音',
        'url_empty_warning': '请输入视频网址',
        'parsing_video': '正在解析视频...',
        'getting_video_info': '获取视频信息中...',
        'getting_qualities': '获取可用画质中...',
        'parse_complete': '解析完成，请选择画质并开始下载',
        'parse_failed': '解析失败',
        'parse_error_msg': '解析失败: ',
        'no_video_info': '请先解析视频',
        'starting_download': '开始下载...',
        'getting_play_url': '获取播放地址中...',
        'downloading_video': '下载视频流 ({})...',
        'downloading_audio': '下载音频流...',
        'merging_files': '合并文件中...',
        'download_complete': '下载完成！',
        'save_location': '视频已保存到:\n',
        'download_failed': '下载失败',
        'download_error_msg': '下载失败: ',
        'copyright': 'By kimiDDou',
        'version': 'BDTools 3.4',
        'video_stream': '视频流',
        'audio_stream': '音频流',
        'downloading': '下载{}... {}% ({}/{})',
        'downloading_no_size': '下载{}... {}KB',
        'language': '语言',
        'history': '历史记录',
        'history_window_title': '下载历史',
        'history_time': '时间',
        'history_title': '标题',
        'history_quality': '画质',
        'history_path': '保存路径',
        'history_open': '打开文件',
        'history_delete': '删除记录',
        'history_clear': '清空历史',
        'history_empty': '暂无下载历史',
        'history_deleted': '记录已删除',
        'history_cleared': '历史记录已清空',
        'history_open_failed': '打开文件失败',
        'warning': '警告',
        'prompt': '提示',
        'complete': '完成',
        'error': '错误',
        'cannot_parse_bv': '无法解析BV号',
        'api_error': 'API错误',
        'unknown_error': '未知错误',
        'get_quality_failed': '获取画质列表失败',
        'cannot_get_video_stream': '无法获取视频流地址',
        'cannot_get_stream_info': '无法获取视频流信息',
        'format': '格式',
        'unknown': '未知',
        'get_play_info_failed': '获取播放信息失败',
        'merge_failed': '合并失败',
        'cannot_recognize_quality': '无法识别画质选择',
        'open_file': '打开文件',
        'cookie_label': '登录Cookie（用于高清视频）：',
        'get_cookie_btn': '获取Cookie',
        'login_window_title': 'Bilibili登录 - 获取Cookie',
        'login_prompt': '请在下方登录Bilibili，登录成功后将自动获取Cookie',
        'cookie_obtained': 'Cookie获取成功！',
        'cookie_obtain_failed': '获取Cookie失败，请确保已登录',
        'no_cookie_warning': '未登录用户只能下载低画质视频',
        'quality_downgrade': '未登录用户，自动降级到低画质'
    },
    'en': {
        'app_title': 'BDTools 3.4',
        'url_label': 'Enter Bilibili video URL: ',
        'parse_btn': 'Parse Video',
        'video_info': 'Video Information',
        'title_prefix': 'Title: ',
        'quality_label': 'Select Quality: ',
        'auto_quality': 'Auto-select highest quality',
        'choose_dir_btn': 'Choose Save Directory',
        'download_btn': 'Start Download',
        'ffmpeg_warning': 'FFmpeg not detected, downloaded video will have no sound',
        'url_empty_warning': 'Please enter a video URL',
        'parsing_video': 'Parsing video...',
        'getting_video_info': 'Getting video information...',
        'getting_qualities': 'Getting available qualities...',
        'parse_complete': 'Parsing completed, please select quality and start download',
        'parse_failed': 'Parsing failed',
        'parse_error_msg': 'Parsing failed: ',
        'no_video_info': 'Please parse the video first',
        'starting_download': 'Starting download...',
        'getting_play_url': 'Getting playback URL...',
        'downloading_video': 'Downloading video stream ({})...',
        'downloading_audio': 'Downloading audio stream...',
        'merging_files': 'Merging files...',
        'download_complete': 'Download completed!',
        'save_location': 'Video saved to:\n',
        'download_failed': 'Download failed',
        'download_error_msg': 'Download failed: ',
        'copyright': 'By kimiDDou',
        'version': 'BDTools 3.4',
        'video_stream': 'video stream',
        'audio_stream': 'audio stream',
        'downloading': 'Downloading {}... {}% ({}/{})',
        'downloading_no_size': 'Downloading {}... {}KB',
        'language': 'Language',
        'history': 'History',
        'history_window_title': 'Download History',
        'history_time': 'Time',
        'history_title': 'Title',
        'history_quality': 'Quality',
        'history_path': 'Save Path',
        'history_open': 'Open File',
        'history_delete': 'Delete Record',
        'history_clear': 'Clear History',
        'history_empty': 'No download history yet',
        'history_deleted': 'Record deleted',
        'history_cleared': 'History cleared',
        'history_open_failed': 'Failed to open file',
        'warning': 'Warning',
        'prompt': 'Prompt',
        'complete': 'Complete',
        'error': 'Error',
        'cannot_parse_bv': 'Cannot parse BV ID',
        'api_error': 'API error',
        'unknown_error': 'Unknown error',
        'get_quality_failed': 'Failed to get quality list',
        'cannot_get_video_stream': 'Cannot get video stream URL',
        'cannot_get_stream_info': 'Cannot get stream information',
        'format': 'Format',
        'unknown': 'Unknown',
        'get_play_info_failed': 'Failed to get play information',
        'merge_failed': 'Merge failed',
        'cannot_recognize_quality': 'Cannot recognize quality selection',
        'open_file': 'Open File',
        'cookie_label': 'Login Cookie (for HD videos): ',
        'get_cookie_btn': 'Get Cookie',
        'login_window_title': 'Bilibili Login - Get Cookie',
        'login_prompt': 'Please log in to Bilibili below. Cookie will be obtained automatically after successful login',
        'cookie_obtained': 'Cookie obtained successfully!',
        'cookie_obtain_failed': 'Failed to get Cookie, please ensure you are logged in',
        'no_cookie_warning': 'Non-logged-in users can only download low-quality videos',
        'quality_downgrade': 'Not logged in, downgrading to low quality'
    }
}

class BDToolsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # 当前语言设置，默认为中文
        self.current_lang = 'zh'
        
        # 检查FFmpeg是否可用
        self.ffmpeg_available = self.check_ffmpeg()
        
        # 字体大小
        self.default_font = ("宋体", 12) if self.current_lang == 'zh' else ("Arial", 12)
        
        # 视频信息存储
        self.video_info = None
        self.quality_options = []
        self.selected_quality = StringVar(value=self.get_text('auto_quality'))
        
        # 创建默认下载目录（如果不存在）
        self.default_download_dir = self.create_default_download_dir()
        
        # 历史记录文件路径
        self.history_file = os.path.join(os.path.expanduser("~"), "BDTools_history.json")
        
        # 加载历史记录
        self.load_history()

        # 存储用户Cookie
        self.user_cookie = ""
        self.cookie_refresh_time = 0  # 记录Cookie最后刷新时间

        # UI布局
        self.create_ui()

    def create_default_download_dir(self):
        """创建默认下载目录"""
        # 确定桌面路径
        if sys.platform.startswith('win'):
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        else:  # macOS和Linux
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        
        # 创建BDTools Downloads目录
        download_dir = os.path.join(desktop, "BDTools Downloads")
        os.makedirs(download_dir, exist_ok=True)
        return download_dir

    def get_text(self, key):
        """获取当前语言对应的文本"""
        return LANGUAGES[self.current_lang].get(key, key)

    def create_ui(self):
        # 设置窗口标题
        self.title(self.get_text('app_title'))
        self.geometry("800x550")  # 增加宽度以容纳更多内容
        self.resizable(False, False)

        # 左上角大标题
        title_frame = tk.Frame(self)
        title_frame.pack(pady=10, anchor=tk.W, padx=10)
        tk.Label(
            title_frame, 
            text="BDTools 3", 
            font=("微软雅黑", 16, "bold"),
            fg="#333333"
        ).pack()

        # 显示FFmpeg警告（如果需要）
        if not self.ffmpeg_available:
            messagebox.showwarning(self.get_text('warning'), self.get_text('ffmpeg_warning'))

        # 语言选择
        lang_frame = tk.Frame(self)
        lang_frame.pack(pady=5, anchor=tk.E, padx=10)
        tk.Label(lang_frame, text=self.get_text('language') + ":", font=self.default_font).pack(side=tk.LEFT)
        
        self.lang_var = StringVar(value="中文" if self.current_lang == 'zh' else "English")
        lang_combo = ttk.Combobox(lang_frame, textvariable=self.lang_var, 
                                 state="readonly", width=10, font=self.default_font)
        lang_combo['values'] = ["中文", "English"]
        lang_combo.pack(side=tk.LEFT, padx=5)
        lang_combo.bind("<<ComboboxSelected>>", self.change_language)
        
        # URL输入部分
        url_frame = tk.Frame(self)
        url_frame.pack(pady=5, fill=tk.X, padx=10)
        self.url_label = tk.Label(url_frame, text=self.get_text('url_label'), font=self.default_font)
        self.url_label.pack(side=tk.LEFT)
        self.url_entry = tk.Entry(url_frame, width=50, font=self.default_font)
        self.url_entry.pack(side=tk.LEFT, padx=5)
        
        # 解析按钮
        self.parse_btn = tk.Button(url_frame, text=self.get_text('parse_btn'), command=self.parse_video, font=self.default_font)
        self.parse_btn.pack(side=tk.LEFT)
        
        # Cookie输入部分
        cookie_frame = tk.Frame(self)
        cookie_frame.pack(pady=5, fill=tk.X, padx=10)
        self.cookie_label = tk.Label(cookie_frame, text=self.get_text('cookie_label'), font=self.default_font)
        self.cookie_label.pack(side=tk.LEFT)
        self.cookie_entry = tk.Entry(cookie_frame, width=50, font=("宋体", 10) if self.current_lang == 'zh' else ("Arial", 10))
        self.cookie_entry.pack(side=tk.LEFT, padx=5)
        
        # 获取Cookie按钮（新增）
        self.get_cookie_btn = tk.Button(cookie_frame, text=self.get_text('get_cookie_btn'), 
                                       command=self.open_login_window, font=self.default_font)
        self.get_cookie_btn.pack(side=tk.LEFT, padx=5)
        
        # 视频信息显示
        self.info_frame = tk.LabelFrame(self, text=self.get_text('video_info'), font=self.default_font)
        self.info_frame.pack(pady=5, fill=tk.X, padx=10)
        
        self.title_label = tk.Label(self.info_frame, text="", font=self.default_font, wraplength=700)
        self.title_label.pack(pady=5)
        
        # 画质选择
        quality_frame = tk.Frame(self)
        quality_frame.pack(pady=5, fill=tk.X, padx=10)
        self.quality_label = tk.Label(quality_frame, text=self.get_text('quality_label'), font=self.default_font)
        self.quality_label.pack(side=tk.LEFT)
        
        self.quality_combo = ttk.Combobox(quality_frame, textvariable=self.selected_quality, 
                                         state="readonly", width=30, font=self.default_font)
        self.quality_combo.pack(side=tk.LEFT, padx=5)
        
        # 保存位置
        save_frame = tk.Frame(self)
        save_frame.pack(pady=5, fill=tk.X, padx=10)
        self.choose_dir_btn = tk.Button(save_frame, text=self.get_text('choose_dir_btn'), command=self.choose_dir, font=self.default_font)
        self.choose_dir_btn.pack(side=tk.LEFT)
        
        # 设置默认保存位置为BDTools Downloads目录
        self.save_dir = StringVar(value=self.default_download_dir)
        self.save_dir_label = tk.Label(save_frame, textvariable=self.save_dir, fg="gray", font=("宋体", 10) if self.current_lang == 'zh' else ("Arial", 10), wraplength=500)
        self.save_dir_label.pack(side=tk.LEFT, padx=5)
        
        # 下载按钮
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=5, fill=tk.X, padx=10)
        
        self.download_btn = tk.Button(btn_frame, text=self.get_text('download_btn'), command=self.start_download, 
                                    font=self.default_font, state=tk.DISABLED)
        self.download_btn.pack(side=tk.LEFT, padx=5)
        
        # 历史记录按钮
        self.history_btn = tk.Button(btn_frame, text=self.get_text('history'), command=self.show_history, font=self.default_font)
        self.history_btn.pack(side=tk.LEFT, padx=5)
        
        # 状态标签和进度条
        self.status_label = tk.Label(self, text="", fg="blue", font=("宋体", 10) if self.current_lang == 'zh' else ("Arial", 10))
        self.status_label.pack()

        self.progress = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self, variable=self.progress, maximum=100, length=700)
        self.progress_bar.pack(pady=5)
        
        # 详细进度信息
        self.detail_label = tk.Label(self, text="", fg="green", font=("宋体", 9) if self.current_lang == 'zh' else ("Arial", 9))
        self.detail_label.pack()
        
        # 版权信息标签
        self.copyright_label = tk.Label(
            self,
            text=self.get_text('copyright'),
            fg="gray",
            font=("宋体", 8) if self.current_lang == 'zh' else ("Arial", 8)
        )
        self.copyright_label.place(relx=0.0, rely=1.0, anchor="sw", x=10, y=-10)

        # 版本号
        self.version_label = tk.Label(self, text=self.get_text('version'), fg="gray", font=("宋体", 8) if self.current_lang == 'zh' else ("Arial", 8))
        self.version_label.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)

    def open_login_window(self):
        """打开登录窗口获取Cookie（增强版）"""
        try:
            from tkinterweb import HtmlFrame  # 确保导入成功
        except ImportError:
            messagebox.showerror(self.get_text('error'), "tkinterweb库未安装，请先安装该库")
            return

        login_window = Toplevel(self)
        login_window.title(self.get_text('login_window_title'))
        login_window.geometry("1000x700")
        login_window.resizable(True, True)
    
        # 提示标签
        prompt_label = tk.Label(login_window, text=self.get_text('login_prompt'), font=self.default_font)
        prompt_label.pack(pady=10, padx=10, anchor=tk.W)
    
        # 创建网页视图并优化配置
        self.html_frame = HtmlFrame(login_window, horizontal_scrollbar="auto", vertical_scrollbar="auto")
        self.html_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
        # 优化浏览器模拟
        self.html_frame.set_user_agent(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        )
    
        # 加载Bilibili主页
        self.html_frame.load_url("https://www.bilibili.com")

        # 添加刷新按钮
        refresh_btn = tk.Button(login_window, text="刷新页面", command=lambda: self.html_frame.reload())
        refresh_btn.pack(pady=5)
    
        # 状态标签
        self.login_status = tk.Label(login_window, text="等待登录...", fg="blue", font=self.default_font)
        self.login_status.pack(pady=5)
    
        # 定时检查登录状态
        self.login_window = login_window
        self.check_cookie_interval(login_window)

    def check_cookie_interval(self, login_window):
        """定时检查Cookie是否包含必要字段（增强版）"""
        if not login_window.winfo_exists():
            return
        
        try:
            cookies = self.html_frame.get_cookies()

            # 检查必要的Cookie字段
            required_cookies = ['SESSDATA', 'bili_jct', 'DedeUserID']
            if all(key in cookies for key in required_cookies):
                # 格式化Cookie
                cookie_str = '; '.join([f"{k}={v}" for k, v in cookies.items()])
            
                # 更新UI
                self.cookie_entry.delete(0, tk.END)
                self.cookie_entry.insert(0, cookie_str)
                self.user_cookie = cookie_str
                self.cookie_refresh_time = time.time()
            
                self.login_status.config(text=self.get_text('cookie_obtained'), fg="green")
                login_window.after(1000, login_window.destroy)
                messagebox.showinfo(self.get_text('prompt'), self.get_text('cookie_obtained'))
                return
            
            # 检查是否已登录但缺少部分Cookie
            if 'SESSDATA' in cookies:
                self.login_status.config(text=f"已获取部分Cookie，请确保完全登录", fg="orange")
            else:
                self.login_status.config(text=f"等待登录...", fg="blue")
    
        except Exception as e:
            self.login_status.config(text=f"检查Cookie出错: {str(e)}", fg="red")
    
        # 继续检查
        login_window.after(3000, self.check_cookie_interval, login_window)

    def change_language(self, event=None):
        """切换语言并更新界面"""
        selected_lang = self.lang_var.get()
        new_lang = 'zh' if selected_lang == "中文" else 'en'
        
        if new_lang != self.current_lang:
            self.current_lang = new_lang
            # 更新字体
            self.default_font = ("宋体", 12) if new_lang == 'zh' else ("Arial", 12)
            
            # 保存当前输入的URL和标题信息
            current_url = self.url_entry.get()
            current_title = self.title_label.cget("text")
            current_cookie = self.cookie_entry.get()
            
            # 重新创建UI
            for widget in self.winfo_children():
                widget.destroy()
            self.create_ui()
            
            # 恢复保存的信息
            self.url_entry.insert(0, current_url)
            self.title_label.config(text=current_title)
            self.cookie_entry.delete(0, tk.END)
            self.cookie_entry.insert(0, current_cookie)
            
            # 重新设置画质选项
            if self.quality_options:
                quality_names = [f"{q['name']} ({q['qn']})" for q in self.quality_options]
                self.quality_combo['values'] = [self.get_text('auto_quality')] + quality_names
                self.quality_combo.current(0)
            
            # 恢复按钮状态
            if self.video_info:
                self.download_btn.config(state=tk.NORMAL)

    def check_ffmpeg(self):
        """检查FFmpeg是否可用"""
        try:
            result = subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return result.returncode == 0
        except:
            return False

    def choose_dir(self):
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.save_dir.set(dir_path)

    def parse_video(self):
        """解析视频信息并获取可用画质"""
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning(self.get_text('prompt'), self.get_text('url_empty_warning'))
            return
            
        self.parse_btn.config(state=tk.DISABLED)
        self.status_label.config(text=self.get_text('parsing_video'))
        self.progress.set(0)
        
        threading.Thread(target=self.do_parse_video, args=(url,), daemon=True).start()

    def do_parse_video(self, url):
        try:
            # 添加随机延迟避免请求过快
            time.sleep(0.5 + random.random())
            
            bv_id = self.extract_bv(url)
            if not bv_id:
                raise ValueError(self.get_text('cannot_parse_bv'))
            
            # 获取视频基本信息
            self.status_label.config(text=self.get_text('getting_video_info'))
            video_info = self.get_video_info(bv_id)
            self.video_info = video_info
            
            # 获取可用画质
            self.status_label.config(text=self.get_text('getting_qualities'))
            quality_list = self.get_available_qualities(bv_id, video_info['cid'])
            
            # 更新UI
            self.after(0, self.update_ui_after_parse, video_info, quality_list)
            
        except Exception as e:
            self.after(0, self.handle_parse_error, e)
        finally:
            self.after(0, lambda: self.parse_btn.config(state=tk.NORMAL))

    def update_ui_after_parse(self, video_info, quality_list):
        """解析完成后更新UI"""
        self.title_label.config(text=f"{self.get_text('title_prefix')}{video_info['title']}")
        
        # 设置画质选项
        self.quality_options = quality_list
        quality_names = [f"{q['name']} ({q['qn']})" for q in quality_list]
        self.quality_combo['values'] = [self.get_text('auto_quality')] + quality_names
        self.quality_combo.current(0)  # 默认选择自动
        
        # 如果用户未登录，显示警告
        if not self.cookie_entry.get().strip():
            messagebox.showwarning(self.get_text('warning'), self.get_text('no_cookie_warning'))
        
        # 启用下载按钮
        self.download_btn.config(state=tk.NORMAL)
        self.status_label.config(text=self.get_text('parse_complete'))

    def handle_parse_error(self, error):
        """处理解析错误（增强版）"""
        self.status_label.config(text=self.get_text('parse_failed'))
        
        # 显示更友好的错误信息
        error_msg = str(error)
        if "403" in error_msg:
            detailed_msg = "访问被拒绝(403)\n可能原因:\n1. Cookie无效或过期\n2. IP地址被限制\n3. 视频需要登录才能观看"
        elif "404" in error_msg:
            detailed_msg = "视频不存在(404)\n请检查URL是否正确"
        elif "timed out" in error_msg:
            detailed_msg = "连接超时\n请检查网络连接"
        else:
            detailed_msg = error_msg
            
        messagebox.showerror(self.get_text('error'), 
                          f"{self.get_text('parse_error_msg')}{detailed_msg}")

    def start_download(self):
        if not self.video_info:
            messagebox.showwarning(self.get_text('prompt'), self.get_text('no_video_info'))
            return
            
        self.download_btn.config(state=tk.DISABLED)
        self.progress.set(0)
        self.status_label.config(text=self.get_text('starting_download'))
        self.detail_label.config(text="")  # 清空详细信息
        
        # 获取用户选择的画质
        selected = self.selected_quality.get()
        if selected == self.get_text('auto_quality'):
            qn = None  # 自动选择最高画质
        else:
            # 从选择中提取qn值
            match = re.search(r"\((\d+)\)$", selected)
            if match:
                qn = int(match.group(1))
            else:
                qn = None
                messagebox.showwarning(self.get_text('prompt'), 
                                     self.get_text('cannot_recognize_quality'))
        
        threading.Thread(target=self.download_video, args=(qn,), daemon=True).start()

    def get_available_qualities(self, bv_id, cid):
        """获取可用画质列表"""
        api_url = f"https://api.bilibili.com/x/player/playurl?bvid={bv_id}&cid={cid}&fnval=4048"
        headers = self.get_headers(bv_id)
        
        try:
            response = requests.get(api_url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get("code") != 0:
                raise ValueError(f"{self.get_text('api_error')}: {data.get('message', self.get_text('unknown_error'))}")
            
            # 获取支持的画质列表
            accept_quality = data['data']['accept_quality']
            accept_description = data['data']['accept_description']
            
            # 创建画质选项
            quality_options = []
            for i in range(len(accept_quality)):
                quality_options.append({
                    "qn": accept_quality[i],
                    "name": accept_description[i]
                })
            
            # 按画质从高到低排序
            quality_options.sort(key=lambda x: x['qn'], reverse=True)
            return quality_options
            
        except Exception as e:
            raise RuntimeError(f"{self.get_text('get_quality_failed')}: {str(e)}")

    def get_video_info(self, bv_id):
        """获取视频基本信息（标题、cid等） - 增强版"""
        api_url = f"https://api.bilibili.com/x/web-interface/view?bvid={bv_id}"
        
        # 尝试多种方式获取信息
        for attempt in range(3):
            headers = self.get_headers(bv_id)
            
            try:
                response = requests.get(api_url, headers=headers, timeout=10)
                response.raise_for_status()
                data = response.json()
                
                if data.get("code") == 0:
                    return {
                        "title": data['data']['title'],
                        "cid": data['data']['cid'],
                        "bvid": bv_id
                    }
                
                # 处理特定错误
                if data.get("code") == -403:
                    # 尝试刷新Cookie
                    if attempt < 2:
                        self.status_label.config(text="Cookie可能过期，尝试刷新...")
                        # 清除当前Cookie
                        self.user_cookie = ""
                        self.cookie_entry.delete(0, tk.END)
                        time.sleep(1)
                        continue
                    else:
                        raise ValueError("访问被拒绝(403)，请检查Cookie")
                
                error_msg = data.get("message", self.get_text('unknown_error'))
                raise ValueError(f"{self.get_text('api_error')}: {error_msg}")
                
            except requests.exceptions.RequestException as e:
                if attempt < 2:
                    time.sleep(2)  # 等待后重试
                else:
                    raise RuntimeError(f"网络错误: {str(e)}")
        
        raise RuntimeError(f"获取视频信息失败，已尝试3次")

    def download_video(self, qn=None):
        try:
            video_info = self.video_info
            title = video_info['title']
            cid = video_info['cid']
            bv_id = video_info['bvid']
            
            # 清理文件名
            safe_title = re.sub(r'[\\/:*?"<>|]', "_", title)
            save_dir = self.save_dir.get()
            
            # 获取视频播放信息
            self.status_label.config(text=self.get_text('getting_play_url'))
            play_info = self.get_play_info(bv_id, cid, qn)
            
            # 提取视频和音频流
            video_url, audio_url, quality = self.get_streams(play_info)
            
            if not video_url:
                raise ValueError(self.get_text('cannot_get_video_stream'))
            
            # 创建临时目录
            temp_dir = os.path.join(save_dir, "BDTools_temp")
            os.makedirs(temp_dir, exist_ok=True)
            
            # 下载视频流
            video_path = os.path.join(temp_dir, "video.m4s")
            self.status_label.config(text=self.get_text('downloading_video').format(quality))
            self.download_file(video_url, video_path, self.get_text('video_stream'))
            
            # 下载音频流（如果有）
            audio_path = os.path.join(temp_dir, "audio.m4s") if audio_url else None
            if audio_url:
                self.status_label.config(text=self.get_text('downloading_audio'))
                self.download_file(audio_url, audio_path, self.get_text('audio_stream'))
            
            # 合并文件
            final_path = os.path.join(save_dir, f"{safe_title}.mp4")
            self.status_label.config(text=self.get_text('merging_files'))
            
            if audio_path and self.ffmpeg_available:
                # 使用FFmpeg合并音视频
                self.merge_with_ffmpeg(video_path, audio_path, final_path)
            else:
                # 没有音频或FFmpeg不可用时，只保存视频
                if audio_path:
                    messagebox.showwarning(self.get_text('warning'), self.get_text('ffmpeg_warning'))
                shutil.move(video_path, final_path)
            
            # 清理临时文件
            shutil.rmtree(temp_dir, ignore_errors=True)
            
            # 记录下载历史
            self.add_to_history(title, quality, final_path)
            
            self.status_label.config(text=self.get_text('download_complete'))
            messagebox.showinfo(self.get_text('complete'), f"{self.get_text('save_location')}{final_path}")
            
        except Exception as e:
            self.status_label.config(text=self.get_text('download_failed'))
            messagebox.showerror(self.get_text('error'), f"{self.get_text('download_error_msg')}{e}")
            import traceback
            traceback.print_exc()  # 打印详细错误信息到控制台
        finally:
            self.download_btn.config(state=tk.NORMAL)
            self.progress.set(0)

    def get_play_info(self, bv_id, cid, qn=None):
        """
        获取视频播放信息（视频流、音频流地址等），并处理权限验证和重试逻辑
        """
        # 定义API基础URL和重试配置
        max_retries = 3  # 最大重试次数
        retry_delay = 2  # 重试间隔（秒）
        play_info = {}  # 初始化播放信息字典
        
        # 未登录用户默认使用低画质
        is_logged_in = bool(self.cookie_entry.get().strip())
        if not is_logged_in:
            # 未登录用户自动使用低画质
            if qn is None or qn > 32:  # 32是480P
                self.status_label.config(text=self.get_text('quality_downgrade'))
                qn = 32  # 480P
        
        for attempt in range(max_retries):
            try:
                # 1. 构造请求URL（根据qn选择画质）
                if qn is None:
                    # 自动选择最高画质（127对应4K，112对应1080P，根据实际支持降级）
                    api_url = f"https://api.bilibili.com/x/player/playurl?bvid={bv_id}&cid={cid}&qn=127&fnval=4048"
                else:
                    api_url = f"https://api.bilibili.com/x/player/playurl?bvid={bv_id}&cid={cid}&qn={qn}&fnval=4048"
                
                # 2. 获取带Cookie的请求头（确保权限验证）
                headers = self.get_headers(bv_id)
                
                # 3. 发送请求（带超时和证书验证）
                self.status_label.config(text=f"{self.get_text('getting_play_url')}（尝试 {attempt+1}/{max_retries}）")
                response = requests.get(
                    api_url,
                    headers=headers,
                    timeout=15,  # 延长超时时间避免网络波动
                    verify=True  # 启用SSL证书验证（防止被服务器判定为异常请求）
                )
                response.raise_for_status()  # 触发HTTP错误（如403、500）
                
                # 4. 解析API返回数据
                api_data = response.json()
                
                # 5. 验证API返回状态（Bilibili API用code=0表示成功）
                if api_data.get("code") != 0:
                    error_msg = api_data.get("message", self.get_text('unknown_error'))
                    # 特殊处理：若请求的高画质不支持，尝试降级请求
                    if "不支持" in error_msg or "权限" in error_msg:
                        if qn is None:
                            # 自动降级到1080P（qn=112）
                            self.status_label.config(text=f"最高画质不支持，尝试1080P...")
                            qn = 112
                            continue  # 重试请求
                        else:
                            # 尝试降级到下一个较低画质
                            if qn > 16:  # 16是最低画质
                                qn = qn // 2  # 简单降级一半
                                self.status_label.config(text=f"尝试{qn}画质...")
                                continue
                            else:
                                raise ValueError(f"{self.get_text('api_error')}: {error_msg}")
                    else:
                        raise ValueError(f"{self.get_text('api_error')}: {error_msg}")
                
                # 6. 提取核心播放信息并结构化
                play_info = api_data.get("data", {})
                
                # 7. 验证播放信息有效性（必须包含视频流地址）
                if not play_info:
                    raise RuntimeError(self.get_text('cannot_get_stream_info'))
                
                # 8. 处理备用地址（若主地址无效，后续下载可切换备用地址）
                if "dash" in play_info:
                    # 为视频流补充备用地址
                    for video in play_info["dash"].get("video", []):
                        if not video.get("base_url") and video.get("backup_url"):
                            video["base_url"] = video["backup_url"][0]
                    # 为音频流补充备用地址
                    for audio in play_info["dash"].get("audio", []):
                        if not audio.get("base_url") and audio.get("backup_url"):
                            audio["base_url"] = audio["backup_url"][0]
                
                # 9. 验证至少有一种可用的流格式（DASH或FLV）
                has_valid_stream = (
                    ("dash" in play_info and len(play_info["dash"].get("video", [])) > 0) or
                    ("durl" in play_info and len(play_info["durl"]) > 0)
                )
                if not has_valid_stream:
                    raise RuntimeError(self.get_text('cannot_get_stream_info'))
                
                # 10. 成功获取有效播放信息，跳出重试循环
                self.status_label.config(text=f"{self.get_text('getting_play_url')} 成功")
                return play_info
                
            except requests.exceptions.HTTPError as e:
                # 处理403权限错误（优先检查Cookie）
                if response.status_code == 403:
                    error_detail = f"403权限拒绝（可能Cookie失效或IP受限）"
                    # 尝试刷新Cookie（仅当是首次重试时）
                    if attempt == 0 and self.cookie_entry.get().strip():
                        self.status_label.config(text=f"{error_detail}，尝试刷新Cookie...")
                        continue  # 重试请求
                else:
                    error_detail = f"HTTP错误 {response.status_code}"
                
                # 达到最大重试次数则抛出错误
                if attempt == max_retries - 1:
                    raise RuntimeError(f"{self.get_text('get_play_info_failed')}: {error_detail}")
                else:
                    self.status_label.config(text=f"{error_detail}，{retry_delay}秒后重试...")
                    time.sleep(retry_delay)
            
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
                # 处理网络超时或连接错误
                if attempt == max_retries - 1:
                    raise RuntimeError(f"{self.get_text('get_play_info_failed')}: 网络错误 - {str(e)}")
                else:
                    self.status_label.config(text=f"网络超时，{retry_delay}秒后重试...")
                    time.sleep(retry_delay)
            
            except Exception as e:
                # 处理其他未知错误
                if attempt == max_retries - 1:
                    raise RuntimeError(f"{self.get_text('get_play_info_failed')}: {str(e)}")
                else:
                    self.status_label.config(text=f"未知错误，{retry_delay}秒后重试...")
                    time.sleep(retry_delay)
        
        # 若所有重试都失败，抛出最终错误
        raise RuntimeError(self.get_text('get_play_info_failed'))
        
    def get_streams(self, play_info):
        """获取视频和音频流，优先按分辨率排序"""
        if 'dash' in play_info:
            dash = play_info['dash']
            videos = dash.get('video', [])
            audios = dash.get('audio', [])
            
            if videos:
                # 先按高度（分辨率）排序，再按带宽排序
                videos.sort(key=lambda x: (x.get('height', 0), x.get('bandwidth', 0)), reverse=True)
                best_video = videos[0]
                video_url = best_video.get('base_url') or best_video.get('backup_url', [None])[0]
                
                # 获取画质信息
                width = best_video.get('width', 0)
                height = best_video.get('height', 0)
                bandwidth = best_video.get('bandwidth', 0)
                quality = f"{width}x{height} ({bandwidth//1000}Kbps)"
                
                # 选择最高质量的音频流
                audio_url = None
                if audios:
                    audios.sort(key=lambda x: x.get('bandwidth', 0), reverse=True)
                    best_audio = audios[0]
                    audio_url = best_audio.get('base_url') or best_audio.get('backup_url', [None])[0]
                
                return video_url, audio_url, quality
        
        # 如果DASH格式不可用，尝试FLV格式
        if 'durl' in play_info and play_info['durl']:
            # 选择最高质量的FLV格式
            play_info['durl'].sort(key=lambda x: x.get('order', 0), reverse=True)
            best_durl = play_info['durl'][0]
            video_url = best_durl['url']
            quality = f"FLV{self.get_text('format')} ({play_info.get('quality', self.get_text('unknown'))})"
            return video_url, None, quality
        
        raise ValueError(self.get_text('cannot_get_stream_info'))

    def extract_bv(self, url):
        """从URL中提取BV号"""
        match = re.search(r"(BV[a-zA-Z0-9]+)", url)
        return match.group(1) if match else None

    def get_headers(self, bv_id):
        """获取包含完整Cookie和请求头的信息（增强版）"""
        # 优先使用用户输入的Cookie
        user_cookie = self.cookie_entry.get().strip()
        
        # 如果用户没有输入Cookie，尝试使用之前保存的
        if not user_cookie and self.user_cookie:
            user_cookie = self.user_cookie
        
        # 检查Cookie是否需要刷新（每30分钟刷新一次）
        current_time = time.time()
        if user_cookie and (current_time - self.cookie_refresh_time > 1800):
            self.user_cookie = user_cookie
            self.cookie_refresh_time = current_time
            # 更新输入框显示
            self.cookie_entry.delete(0, tk.END)
            self.cookie_entry.insert(0, user_cookie)
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "Referer": f"https://www.bilibili.com/video/{bv_id}" if bv_id else "https://www.bilibili.com",
            "Cookie": user_cookie,
            "Origin": "https://www.bilibili.com",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Sec-Fetch-Dest": "video",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "TE": "trailers",
            "DNT": "1",  # 不要跟踪
            "Upgrade-Insecure-Requests": "1"
        }
        return headers

    def download_file(self, url, path, file_type):
        """下载文件并显示详细进度（增强版，添加重试机制和完整下载逻辑）"""
        max_retries = 3
        retry_delay = 5  # 重试间隔秒数
        
        for attempt in range(max_retries):
            try:
                headers = self.get_headers("")  # 不需要具体BV号
                
                # 对于未登录用户，添加额外的请求头
                if not self.cookie_entry.get().strip():
                    headers.update({
                        "Origin": "https://www.bilibili.com",
                        "Referer": "https://www.bilibili.com/",
                        "Sec-Fetch-Dest": "empty",
                        "Sec-Fetch-Mode": "cors",
                        "Sec-Fetch-Site": "same-site"
                    })
                
                # 检查是否支持断点续传
                resume_download = False
                downloaded_size = 0
                if os.path.exists(path):
                    downloaded_size = os.path.getsize(path)
                    # 发送HEAD请求获取文件总大小
                    head_resp = requests.head(url, headers=headers, timeout=10)
                    head_resp.raise_for_status()
                    total_size = int(head_resp.headers.get('content-length', 0))
                    
                    if downloaded_size < total_size:
                        # 支持断点续传
                        headers['Range'] = f'bytes={downloaded_size}-'
                        resume_download = True
                        self.detail_label.config(text=f"继续下载: 已完成 {downloaded_size/total_size*100:.1f}%")
                    elif downloaded_size == total_size:
                        # 文件已完整下载
                        self.detail_label.config(text=f"{file_type} 已完整下载")
                        return
                    else:
                        # 文件大小异常，删除重新下载
                        os.remove(path)
                        downloaded_size = 0
                
                # 发送GET请求下载文件
                response = requests.get(url, headers=headers, stream=True, timeout=30)
                response.raise_for_status()
                
                # 获取总大小（处理断点续传的情况）
                if not resume_download:
                    total_size = int(response.headers.get('content-length', 0))
                    if downloaded_size > 0 and total_size > 0 and downloaded_size == total_size:
                        self.detail_label.config(text=f"{file_type} 已完整下载")
                        return
                
                # 准备下载
                chunk_size = 8192  # 8KB块
                start_time = time.time()
                last_update_time = start_time
                last_downloaded = downloaded_size
                speed_history = []
                
                with open(path, "ab" if resume_download else "wb") as f:
                    for chunk in response.iter_content(chunk_size=chunk_size):
                        if chunk:
                            f.write(chunk)
                            downloaded_size += len(chunk)
                            
                            # 定期更新进度（每0.5秒更新一次）
                            current_time = time.time()
                            if current_time - last_update_time >= 0.5:
                                # 计算下载速度
                                elapsed = current_time - last_update_time
                                speed = (downloaded_size - last_downloaded) / elapsed / 1024  # KB/s
                                speed_history.append(speed)
                                if len(speed_history) > 5:
                                    speed_history.pop(0)
                                avg_speed = sum(speed_history) / len(speed_history) if speed_history else speed
                                
                                # 计算进度百分比
                                if total_size > 0:
                                    progress = downloaded_size / total_size * 100
                                    self.progress.set(progress)
                                    # 字符串中定义占位符格式，参数传变量
                                    self.detail_label.config(text=
                                        "{} - 速度: {:.1f} KB/s - 剩余: {}"
                                        .format(
                                            self.get_text('downloading').format(file_type, f"{progress:.1f}%", f"{downloaded_size//1024}KB", f"{total_size//1024}KB"),
                                            avg_speed,
                                            self.format_time((total_size-downloaded_size)/(avg_speed*1024) if avg_speed > 0 else 0)
                                        )
                                    )
                                else:
                                    self.detail_label.config(text=
                                        f"{self.get_text('downloading_no_size')} - 速度: {avg_speed:.1f} KB/s"
                                    .format(file_type, downloaded_size//1024))
                                
                                last_update_time = current_time
                                last_downloaded = downloaded_size
                
                # 下载完成检查
                if total_size > 0 and downloaded_size < total_size:
                    raise Exception(f"下载不完整: 仅下载 {downloaded_size} / {total_size} 字节")
                
                self.progress.set(100)
                self.detail_label.config(text=f"{file_type} 下载完成")
                return  # 下载成功，退出重试循环
                
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 403:
                    if attempt < max_retries - 1:
                        self.status_label.config(text=f"下载失败（403错误），{retry_delay}秒后重试 ({attempt+1}/{max_retries})...")
                        time.sleep(retry_delay)
                    else:
                        # 达到最大重试次数，抛出异常
                        raise RuntimeError("403权限错误，需要重新获取播放地址")
                else:
                    if attempt < max_retries - 1:
                        self.status_label.config(text=f"下载失败（HTTP错误），{retry_delay}秒后重试 ({attempt+1}/{max_retries})...")
                        time.sleep(retry_delay)
                    else:
                        raise  # 达到最大重试次数，抛出异常
                
            except Exception as e:
                if attempt < max_retries - 1:
                    self.status_label.config(text=f"下载失败: {str(e)}，{retry_delay}秒后重试 ({attempt+1}/{max_retries})...")
                    time.sleep(retry_delay)
                else:
                    raise  # 达到最大重试次数，抛出异常
        
        # 所有重试失败
        raise Exception(f"下载失败，已尝试{max_retries}次")

    def format_time(self, seconds):
        """将秒数格式化为时:分:秒格式"""
        if seconds <= 0:
            return "计算中..."
        elif seconds < 60:
            return f"{seconds:.1f}秒"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            secs = seconds % 60
            return f"{minutes}分{int(secs)}秒"
        else:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            secs = seconds % 60
            return f"{hours}时{minutes}分{int(secs)}秒"

    def merge_with_ffmpeg(self, video_path, audio_path, output_path):
        """使用FFmpeg合并视频和音频"""
        try:
            cmd = [
                'ffmpeg',
                '-i', video_path,
                '-i', audio_path,
                '-c:v', 'copy',
                '-c:a', 'copy',
                '-y',  # 覆盖已存在文件
                output_path
            ]
            
            # 隐藏FFmpeg控制台窗口（仅Windows）
            startupinfo = None
            if sys.platform.startswith('win'):
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = 0  # 隐藏窗口
            
            process = subprocess.Popen(cmd, 
                                     stdout=subprocess.PIPE, 
                                     stderr=subprocess.PIPE,
                                     startupinfo=startupinfo,
                                     text=True,
                                     encoding='utf-8',
                                     errors='ignore')
            
            # 等待合并完成
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                # 尝试截取关键错误信息
                error_lines = stderr.split('\n')
                error_msg = "\n".join(error_lines[-5:])  # 取最后5行错误信息
                raise RuntimeError(f"FFmpeg{self.get_text('error')}: {error_msg}")
                
        except Exception as e:
            raise RuntimeError(f"{self.get_text('merge_failed')}: {str(e)}")

    def load_history(self):
        """加载下载历史"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
            else:
                self.history = []
        except Exception as e:
            self.history = []
            print(f"加载历史记录失败: {e}")

    def save_history(self):
        """保存下载历史"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存历史记录失败: {e}")

    def add_to_history(self, title, quality, path):
        """添加下载记录到历史"""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        record = {
            'time': now,
            'title': title,
            'quality': quality,
            'path': path
        }
        self.history.insert(0, record)  # 插入到开头，最新的记录在最前
        self.save_history()

    def show_history(self):
        """显示历史记录窗口"""
        history_window = Toplevel(self)
        history_window.title(self.get_text('history_window_title'))
        history_window.geometry("800x500")
        history_window.resizable(True, True)
        
        # 创建表格
        columns = ('time', 'title', 'quality', 'path')
        tree = ttk.Treeview(history_window, columns=columns, show='headings')
        
        # 设置列标题
        tree.heading('time', text=self.get_text('history_time'))
        tree.heading('title', text=self.get_text('history_title'))
        tree.heading('quality', text=self.get_text('history_quality'))
        tree.heading('path', text=self.get_text('history_path'))
        
        # 设置列宽
        tree.column('time', width=150)
        tree.column('title', width=300)
        tree.column('quality', width=150)
        tree.column('path', width=200)
        
        # 添加数据
        if not self.history:
            tree.insert('', 'end', values=(self.get_text('history_empty'), '', '', ''))
        else:
            for record in self.history:
                tree.insert('', 'end', values=(
                    record['time'], 
                    record['title'], 
                    record['quality'], 
                    record['path']
                ))
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(history_window, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)

# 程序入口
if __name__ == "__main__":
    # 提示用户安装依赖
    try:
        from tkinterweb import HtmlFrame
    except ImportError:
        try:
            messagebox.showinfo("安装依赖", "首次运行需要安装tkinterweb库，即将自动安装...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "tkinterweb"])
        except Exception as e:
            messagebox.showerror("安装失败", f"无法自动安装tkinterweb库，请手动运行：\npip install tkinterweb\n错误信息：{str(e)}")
            sys.exit(1)
    
    app = BDToolsApp()
    app.mainloop()