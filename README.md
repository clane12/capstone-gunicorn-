Flask Blog CMS
A full-featured Blog Content Management System built using Flask, SQLAlchemy, Flask-WTF, and Flask-Login. Users can register, log in, comment on posts, and the admin user (first to register) can create, edit, and delete blog posts.

✨ Features
✅ Secure user registration and login system (hashed passwords)
✍️ Rich text editing with CKEditor
👑 Admin-only controls for creating, editing, and deleting posts
💬 Comment system for logged-in users
🖼 Upload blog image via URL
📅 Automatically timestamps posts
🔐 Admin-only decorator for protected routes

📦 Requirements
Python 3.x+

Flask: Web framework

Flask-WTF: Form handling

Flask-Login: User session management

SQLAlchemy: ORM for the database

Flask-CKEditor: Rich text editing

Werkzeug: Password hashing

Bootstrap 5: Styling

🛠 Setup
Clone the repository
git clone https://github.com/your-username/flask-blog-cms.git
cd flask-blog-cms

Create and activate a virtual environment
python -m venv venv
source venv/bin/activate     # On Mac/Linux
venv\Scripts\activate        # On Windows

Install dependencies
pip install -r requirements.txt

Set up environment variables in a .env file
SECRET_KEY="your_flask_secret_key"
DB_SQL="your SQ-lite or PostGRE SQL details"

Run the app
python main.py
Visit: http://localhost:5000

🎮 How It Works
🧑‍💻 User System:
Users can register with name, email, and password.

First user to register becomes the admin.

Admin has special access using a custom @admin_only decorator.

✍️ Post Creation:
Admin can create blog posts with title, subtitle, content, and image URL.

Posts are stored in a SQLite database using SQLAlchemy.

💬 Comments:
Logged-in users can leave comments under any blog post.

Comments are stored in a separate table and linked to posts and users.

🔒 Admin Decorator:
Only admin can access routes like /new-post, /edit-post/<id>, and /delete/<id>.

🚀 How to Use
Register as a new user.

First user becomes admin — you’ll now see New Post, Edit, and Delete buttons.

Create blog posts, and allow others to register to comment.

Use admin-only controls to manage blog content securely.

🧩 Future Enhancements
🎨 Rich Profile Pages: Show user bios, avatars, and post history
🔍 Search Functionality: Let users search through blog posts
📊 Admin Dashboard: Show site stats like total users and posts
📥 Image Upload: Support uploading images instead of only via URL
📬 Email Notifications: Notify users of new posts or replies
