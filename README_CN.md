# MS Network

[English Version](README.md)

MS Network 是一款为 macOS 用户设计的现代、轻量级网络管理工具。它允许用户轻松修改本地网络配置、安装证书并实时监控网络状态。通过简洁的 Web 界面，用户可以安全地执行系统级网络操作。

## 主要功能
- **网络监控**：实时查看当前活动的网络服务、IP 地址和 DNS 设置。
- **配置管理**：轻松修改 DNS 服务器和 HTTP/HTTPS 代理设置。
- **证书管理**：一键上传并信任本地根证书。
- **一键复原**：自动备份初始网络设置，随时可一键还原，防止配置出错。

## 技术栈
- **后端**：Python 3.15 + Flask
- **前端**：React 18 + Tailwind CSS (现代化 UI)
- **系统集成**：macOS `networksetup` 和 `security` 命令行工具。

## 如何运行
1. 确保已安装 Python 3。
2. 安装依赖：
   ```bash
   pip install flask flask-cors
   ```
3. 启动后端：
   ```bash
   python3 app.py
   ```
4. 在浏览器中打开 `index.html` 或访问 `http://localhost:5000`。

## 许可证
本项目采用 MIT 许可证。详情请参阅 [LICENSE](LICENSE) 文件。
