# Card Scheduler MVP

## 1. Setup and Running the Application

Follow these steps to set up and run the Card Scheduler application locally. These instructions assume you are working from the root of the repository, and the project files are within a `card_scheduler_project` subdirectory.

### 1.1. Prerequisites
*   Python 3.7+
*   `pip` (Python package installer)
*   `virtualenv` (recommended for creating isolated Python environments)
    *   If not installed, you can typically install it with: `pip install virtualenv`

### 1.2. Setup Steps

1.  **Navigate to Project Directory:**
    If you have cloned a repository, it might already contain the `card_scheduler_project` directory. Otherwise, ensure your project files are within `card_scheduler_project/`.
    ```bash
    cd card_scheduler_project 
    ```
    *(All subsequent commands should be run from within the `card_scheduler_project` directory).*

2.  **Create and Activate a Virtual Environment:**
    It's highly recommended to use a virtual environment to manage project dependencies.
    ```bash
    python3 -m venv venv
    # Or, if you installed virtualenv separately:
    # virtualenv venv
    ```
    Activate the virtual environment:
    *   On macOS and Linux:
        ```bash
        source venv/bin/activate
        ```
    *   On Windows:
        ```bash
        .\venv\Scripts\activate
        ```
    Your terminal prompt should change to indicate that the virtual environment is active (e.g., `(venv) ...`).

3.  **Install Dependencies:**
    Install the required Python packages using `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Initialize the Database:**
    The SQLite database and the `bookings` table need to be initialized before running the application for the first time. This step creates the `database/schedule.db` file.
    ```bash
    python models.py
    ```
    You should see a confirmation message like:
    `Database initialized at /path/to/your/card_scheduler_project/database/schedule.db`
    `Table 'bookings' verified.`

### 1.3. Running the Application

1.  **Start the Flask Development Server:**
    Ensure your virtual environment is still active and you are in the `card_scheduler_project` directory.
    ```bash
    python app.py
    ```
    You should see output similar to:
    ```
     * Serving Flask app 'app'
     * Debug mode: on
     * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
    ```

2.  **Access the Application:**
    Open your web browser and navigate to:
    [http://localhost:5000](http://localhost:5000) (or `http://127.0.0.1:5000`)

    You should now see the Card Scheduler interface and be able to add, view, and delete bookings.

### 1.4. Stopping the Application
To stop the Flask development server, press `CTRL+C` in the terminal where the server is running.

To deactivate the virtual environment (optional, when you're done working):
```bash
deactivate
```

### 1.5. Running with Docker Compose (Recommended)

(Note: These commands use the Docker Compose V2 syntax, `docker compose`. If you have an older version of Docker Compose (V1), you might need to use `docker-compose` with a hyphen.)

This is the recommended way to run the application as it encapsulates the environment and simplifies setup.

**Prerequisites:**
*   Docker Desktop (or Docker Engine + Docker Compose CLI) installed and running. Ensure your Docker Compose version supports the V2 syntax (`docker compose`).

**Instructions:**
All commands should be run from the root of the repository (the directory containing the `docker-compose.yml` file and the `card_scheduler_project/` directory).

1.  **Build and Start Services (First Time or After Changes):**
    This command builds the Docker image for the `web` service (if it doesn't exist or if `Dockerfile` or application code has changed) and starts the service in detached mode (`-d`).
    ```bash
    docker compose up --build -d
    ```

2.  **Start Services (If Already Built):**
    If the image is already built and you just want to start the services:
    ```bash
    docker compose up -d
    ```

3.  **Access the Application:**
    Once the services are running, open your web browser and navigate to:
    [http://localhost:5003](http://localhost:5003)

4.  **View Logs:**
    To view the logs from the `web` service (useful for debugging):
    ```bash
    docker compose logs -f web
    ```
    Press `CTRL+C` to stop following the logs.

5.  **Stopping the Services:**
    To stop and remove the containers, networks, and volumes created by `up`:
    ```bash
    docker compose down
    ```

**Data Persistence:**
*   The `docker-compose.yml` is configured to use a volume that maps the `./scheduler_data` directory (in the project root) to the `/app/database` directory inside the container.
*   This means your SQLite database (`schedule.db`) will be stored in `./scheduler_data` on your host machine and will persist even if you stop or remove the Docker containers. The `scheduler_data` directory will be created automatically if it doesn't exist when the container starts.

## 2. Project Overview and Requirements

### 2.1. Project Overview
This project is a Minimum Viable Product (MVP) for a Card Scheduling application. It allows users to book time slots and view existing bookings. The application uses Flask for the backend, SQLite for the database, and basic HTML/CSS/JavaScript (with Bootstrap) for the frontend.

### 2.2. Product Requirements Document (PRD)

#### 2.2.1. Introduction
A simple web application to manage bookings for a shared resource (e.g., a meeting room, a piece of equipment represented as a "card").

#### 2.2.2. Goals
- Allow users to create new bookings.
- Allow users to view all existing bookings.
- Allow users to delete bookings.
- Provide a simple and intuitive web interface.

#### 2.2.3. User Stories
- (US01) As a user, I want to add a new booking with my name, date, start time, and end time, so that I can reserve a time slot.
- (US02) As a user, I want to see all current bookings, sorted by date and then by start time, so that I can see what times are already taken.
- (US03) As a user, I want to be able to delete a booking, so that I can free up a time slot.
- (US04) As a user, I expect the system to prevent me from submitting incomplete booking information (e.g., missing name or time).
- (US05) As a user, I expect the booking information to be persistent (i.e., not lost if the server restarts).

#### 2.2.4. Functional Requirements
- (FR01) **Booking Creation:**
  - The system must provide a form to input renter's name, booking date, start time, and end time.
  - All fields are mandatory.
  - Upon submission, the booking must be saved to the SQLite database.
- (FR02) **Booking Display:**
  - All bookings must be displayed on the main page.
  - Bookings must be sorted primarily by date (ascending) and secondarily by start time (ascending).
- (FR03) **Database Schema:**
  - A `bookings` table with at least the following fields:
    - `id` (Primary Key, Auto-increment)
    - `renter_name` (Text, Not Null)
    - `booking_date` (Text, Not Null)
    - `start_time` (Text, Not Null)
    - `end_time` (Text, Not Null)
    - `created_at` (Timestamp, Default to current time)
- (FR04) **Booking Deletion:**
  - Each booking listed must have a "Delete" button.
  - Clicking "Delete" should remove the booking from the database.
- (FR05) **Environment Setup:**
  - The application must use Flask.
  - Dependencies should be managed via `requirements.txt`.
  - A Python virtual environment is recommended.

#### 2.2.5. Non-Functional Requirements
- (NF01) **User Interface:** Simple, clean, and intuitive, using Bootstrap for basic styling. A JavaScript confirmation for delete is desirable.
- (NF02) **Database:** SQLite.
- (NF03) **Error Handling:** Basic error handling for form validation (e.g., required fields).

#### 2.2.6. Out of Scope for MVP
- User authentication/authorization.
- Editing existing bookings.
- Conflict detection for bookings.
- Advanced UI features or styling.

#### 2.2.7. Technology Stack
- Backend: Python, Flask
- Database: SQLite
- Frontend: HTML, CSS, JavaScript (Bootstrap)

## 3. Technical Solution Document (技术方案文档)

### 3.1. 系统架构 (System Architecture)
- **应用类型**: 单体Web应用 (Monolithic Web Application)
- **核心框架**: Flask
- **数据库**: SQLite
- **前端**: HTML, CSS (Bootstrap), JavaScript (minimal)
- **部署**: 本地开发服务器 (Flask development server)

### 3.2. 模块设计 (Module Design)
- **`app.py`**: Flask主应用，处理HTTP请求，业务逻辑，数据库交互。
  - 路由: `/` (显示预订), `/add_booking` (添加预订), `/delete_booking/<id>` (删除预订)。
- **`models.py`**: 数据库模型定义 (`bookings`表)，数据库初始化 (`init_db`函数)。
- **`templates/index.html`**: 前端模板，使用Jinja2渲染动态内容，Bootstrap进行样式化。
- **`database/schedule.db`**: SQLite数据库文件。
- **`static/`**: 存放静态文件 (本项目中主要通过CDN使用Bootstrap，此目录为空或含`.gitkeep`)。

### 3.3. 数据库设计 (Database Design) - (FR03)
- 表名: `bookings`
- 字段:
  - `id`: INTEGER, PRIMARY KEY, AUTOINCREMENT
  - `renter_name`: TEXT, NOT NULL
  - `booking_date`: TEXT, NOT NULL (存储格式 YYYY-MM-DD)
  - `start_time`: TEXT, NOT NULL (存储格式 HH:MM)
  - `end_time`: TEXT, NOT NULL (存储格式 HH:MM)
  - `created_at`: TEXT, DEFAULT CURRENT_TIMESTAMP (存储格式 YYYY-MM-DD HH:MM:SS)

### 3.4. 核心功能实现 (Core Functionality Implementation)
- **预订创建 (FR01)**:
  - `index.html`中的表单通过POST请求将数据发送到`/add_booking`。
  - `app.py`中的`add_booking()`函数处理请求：
    - 验证输入 (非空)。
    - 将数据存入`bookings`表。
    - 重定向到主页。
- **预订显示 (FR02)**:
  - `app.py`中的`index()`函数处理`/`的GET请求：
    - 从`bookings`表查询所有记录。
    - 按`booking_date`和`start_time`排序。
    - 将数据传递给`index.html`模板进行渲染。
- **预订删除 (FR04)**:
  - `index.html`中每个预订条目有一个删除按钮，包裹在表单中，通过POST请求到`/delete_booking/<booking_id>`。
  - `app.py`中的`delete_booking()`函数处理请求：
    - 根据`booking_id`从`bookings`表删除记录。
    - 重定向到主页。
  - (NF01) 前端使用JavaScript `confirm()`对话框进行删除确认。

### 3.5. 错误处理 (Error Handling) - (NF03)
- **前端**: HTML表单使用`required`属性进行基本客户端验证。
- **后端**: `app.py`对预订创建请求进行非空字段检查。数据库操作使用`try-except`块捕获潜在的`sqlite3.Error`，并在服务器控制台打印错误信息。对于MVP阶段，不向用户界面显示复杂错误信息。

### 3.6. 安全考虑 (Security Considerations)
- **SQL注入**: 所有数据库查询均使用参数化查询 (例如 `cursor.execute("... VALUES (?, ?, ?, ?)", (var1, ...))`)，有效防止SQL注入。
- **XSS (Cross-Site Scripting)**: Jinja2默认进行HTML转义，有助于防止XSS。用户输入主要显示在表单值和表格内容中，风险较低。未对用户输入进行严格的清理或白名单处理，但在MVP范围内可接受。

### 3.7. 依赖管理 (Dependency Management) - (FR05)
- 使用`requirements.txt`文件列出Python依赖 (主要是Flask)。
- 推荐使用Python虚拟环境 (`venv`或`virtualenv`)。

### 3.8. 项目结构 (Project Structure)
The project files are expected to be within a `card_scheduler_project` directory.
```
card_scheduler_project/
├── app.py                 # Flask主应用文件 (Main Flask application file)
├── models.py              # 数据库交互函数/模型 (Database interaction functions/models)
├── requirements.txt       # Python依赖 (Python dependencies)
├── .gitignore             # Git忽略配置 (Git ignore configuration)
├── venv/                  # Python虚拟环境目录 (Python virtual environment directory)
├── database/
│   └── schedule.db        # SQLite数据库文件 (SQLite database file)
├── static/
│   ├── css/               # (可存放自定义CSS - Can hold custom CSS)
│   │   └── .gitkeep       # (Ensures directory is tracked if empty)
│   └── js/                # (可存放自定义JS - Can hold custom JS)
│       └── .gitkeep       # (Ensures directory is tracked if empty)
└── templates/
    └── index.html         # 主HTML模板 (Main HTML template)
```

### 3.9. 部署策略 (Deployment Strategy)
- **当前阶段**: 使用Flask内置的开发服务器 (`app.run(debug=True)`)。
- **未来考虑**: 对于生产环境，应使用生产级WSGI服务器 (如Gunicorn, uWSGI)配合反向代理 (如Nginx)。

### 3.10. 测试策略 (Testing Strategy)
- **当前阶段**: 手动测试覆盖核心用户场景 (创建、查看、删除预订)。
- **未来考虑**: 单元测试 (针对`models.py`和`app.py`的业务逻辑)，集成测试 (针对Flask应用的请求和响应)。

### 3.11. 潜在改进和未来功能 (Potential Improvements and Future Features) - (参考 PRD 2.2.6 Out of Scope)
- 用户认证与授权。
- 预订编辑功能。
- 预订冲突检测与提醒。
- 更丰富的用户界面和用户体验。
- 使用更强大的数据库系统 (如PostgreSQL, MySQL)。
- API接口开发。
- 详细的日志记录。
- 自动化测试覆盖率提升。
---
**Note:** This README is a comprehensive guide for understanding, setting up, and running the Card Scheduler MVP.
The "Technical Solution Document" part is provided in Chinese as per the original problem description's README structure.
The project structure in section 3.8 reflects the actual state of the `card_scheduler_project` directory, including `.gitkeep` files for empty static directories and the `venv/` directory.
The setup instructions in section 1 are detailed for ease of use and assume commands are run from within the `card_scheduler_project` directory after an initial `cd`.
The README is structured with "Setup and Running" as section 1, "Project Overview and Requirements" as section 2, and "Technical Solution Document" as section 3.
This README file itself should be located at the root of the repository, alongside the `card_scheduler_project/` directory.
