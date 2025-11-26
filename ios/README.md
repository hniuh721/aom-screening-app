# AOM Screening iOS App - 完整文件

所有文件已重新创建，可以直接导入到 Xcode 项目。

## 📁 文件位置

所有文件都在：`/Users/yawenwang/aom-screening-app/ios/`

```
ios/
├── App/
│   └── AOMScreeningApp.swift      # 应用入口
├── Models/
│   └── Questionnaire.swift        # 数据模型
├── Services/
│   └── APIService.swift           # API 服务（已配置 IP: 10.0.0.139）
└── Views/
    ├── ContentView.swift          # 主问卷视图
    └── ResultsView.swift          # 结果视图
```

## 🚀 如何在 Xcode 中使用

### 方法 1：删除旧文件，重新添加（推荐）

1. **在 Xcode 中删除旧文件：**
   - 找到 `App/` 文件夹 → 删除 `AOMScreeningApp.swift`
   - 找到 `Models/` 文件夹 → 删除 `Questionnaire.swift`
   - 找到 `Services/` 文件夹 → 删除 `APIService.swift`
   - 找到 `Views/` 文件夹 → 删除 `ContentView.swift` 和 `ResultsView.swift`
   - 右键点击 → Delete → Move to Trash

2. **重新添加文件：**
   - 右键点击项目名称 `AOMScreening`（蓝色图标）
   - 选择 **"Add Files to 'AOMScreening'..."**
   - 导航到：`/Users/yawenwang/aom-screening-app/ios/`
   - 选择以下文件夹：
     - `App/` 文件夹
     - `Models/` 文件夹
     - `Services/` 文件夹
     - `Views/` 文件夹
   - 确保勾选：
     - ✅ **"Copy items if needed"**
     - ✅ **"Create groups"**
     - ✅ **"Add to targets: AOMScreening"**
   - 点击 **Add**

3. **检查应用入口：**
   - 确保 `App/AOMScreeningApp.swift` 中有 `@main`
   - 如果根目录还有默认的 `AOMScreeningApp.swift`，删除它

### 方法 2：直接替换文件内容

如果不想删除文件，可以直接在 Xcode 中打开每个文件，全选（⌘+A），删除，然后粘贴新内容。

## ⚙️ 重要配置

### 1. API 地址

在 `Services/APIService.swift` 第 7 行，确认：
```swift
private let baseURL = "http://10.0.0.139:8000/api"
```

如果你的 Mac IP 地址不同，需要修改这个地址。

**如何查找你的 Mac IP：**
- 在终端运行：`ifconfig | grep "inet " | grep -v 127.0.0.1`
- 或者：系统设置 → 网络 → 查看 Wi-Fi 的 IP 地址

### 2. 网络权限

确保在 Xcode 项目设置中配置了网络权限：
- 项目 → Target → Info → App Transport Security Settings
- 添加：**Allow Local Networking** = `YES`

### 3. 后端 API

确保后端正在运行：
```bash
cd /Users/yawenwang/aom-screening-app/backend
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**重要：** 必须使用 `--host 0.0.0.0`，这样 iOS 模拟器才能访问。

## ✅ 完成后

1. 保存所有文件（⌘+S）
2. 清理构建：⇧⌘K
3. 重新构建：⌘B
4. 运行应用：⌘R

## 🐛 如果还有问题

1. 检查所有文件是否都添加到了项目
2. 检查 API 地址是否正确
3. 检查后端是否正在运行
4. 查看 Xcode 控制台的错误信息

---

**所有文件已准备好，可以直接使用！** 🎉
