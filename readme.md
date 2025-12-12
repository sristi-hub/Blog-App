# **Blog API — Django REST Framework**

A complete **Blog REST API** built using **Django**, **Django REST Framework**, **JWT Authentication**, and **SQLite**.  
This API provides authentication, blog posts, comments, replies, interactions (like, bookmark, follow), and a role-based moderation system.  
Swagger documentation is included for easy API exploration.

---

## **🚀 Features**

### **🔐 Authentication (Account App)**
- User signup  
- Login / Logout  
- **JWT Authentication** (access & refresh tokens)  
- Email verification  
- Password reset  
- User profile management  

### **📰 Posts API (Posts App)**
- Create, read, update, delete posts  
- Save posts as **drafts**  
- Publish / unpublish  
- **Search posts** by title, content, or author
- **Filter posts** by author, date, ordering  
- Pagination support  
- Only post authors can edit/delete their posts  
- ❌ *Image upload not supported yet*  

### **💬 Comments & Replies (Comments App)**
- Add comments to posts  
- Reply to comments  
- Edit or delete own comments  
- Moderator can remove inappropriate comments  

### **❤️ Interactions (Interactions App)**
- Like / unlike posts  
- Bookmark posts  
- Follow / unfollow users  
- View list of liked posts  
- View list of bookmarked posts  
- Interaction counters (likes, bookmarks, followers)

### **🛡️ Admin & Moderator System**
- **Admin**
  - Full access via Django Admin panel  
  - Can create moderator accounts  
- **Moderator**
  - Can remove posts  
  - Can remove comments  
- **User**
  - Standard API access  

---

## **🛠️ Tech Stack**
- **Backend Framework:** Django, Django REST Framework  
- **Authentication:** JWT (SimpleJWT)  
- **Database:** SQLite  
- **API Documentation:** Swagger (drf-yasg or drf-spectacular)  
- **ORM:** Django ORM  
- **Pagination & Filtering:** DRF filters, search, ordering  

---

## **📂 Project Structure**

```
📦 Blog-API
│
├── account/        # Authentication: Register, Login, JWT, Email Verify, Password Reset
├── posts/          # Blog posts: CRUD, Draft/Publish, Search & Filter
├── comments/       # Comments: Create, List, Replies, Moderation
├── interactions/   # Likes, Bookmarks, Follow System
│
├── project_root/   # Core Django project (settings, urls)
|
├── manage.py
├── requirements.txt
└── README.md

```

---

## **⚙️ Installation & Setup**

### **1️⃣ Clone the repository**
```bash
git clone https://github.com/<sristi-hub>/<Blog-App>.git
cd <Blog-App>
```

### **2️⃣ Create and activate a virtual environment**
```bash
python -m venv env
source env/bin/activate   # macOS/Linux
env\Scripts\activate      # Windows
```

### **3️⃣ Install dependencies**
```bash
pip install -r requirements.txt
```

### **4️⃣ Apply migrations**
```bash
python manage.py migrate
```

### **5️⃣ Create superuser**
```bash
python manage.py createsuperuser
```

### **6️⃣ Start the server**
```bash
python manage.py runserver
```

---
## 📌 API Endpoints 

### 🔐 Authentication (JWT)
```bash
POST    /api/auth/register/
POST    /api/auth/login/
POST    /api/auth/logout/
GET     /api/auth/user/
POST    /api/auth/generate-token/
POST    /api/auth/verify-email/
POST    /api/auth/forgot-password/
POST    /api/auth/password-reset/
```

### 📝 Posts API
```bash
GET     /api/posts/category/
GET     /api/posts/postslist/
GET     /api/posts/postslist/<pk>/
GET     /api/posts/mine-pub-postslist/
GET     /api/posts/mine-draft-postslist/
POST    /api/posts/post-create/
DELETE  /api/posts/post-delete/<pk>/
PUT     /api/posts/post-update/<pk>/
GET     /api/posts/postfilter/
GET     /api/posts/pending-post/
PUT     /api/posts/updatestatus-post<pk>/
```

### 💬 Comments API
```bash
POST    /api/comments/create-comment/<post_id>/
GET     /api/comments/list-comments/<post_id>/
GET     /api/comments/user-comments/
GET     /api/comments/pending-comments/
PUT     /api/comments/changestatus-comments<pk>/
```

### ❤️ Interactions API (Likes, Bookmarks, Follow)
```bash
POST    /api/interactions/like/<post_id>/
GET     /api/interactions/totallike/<post_id>/
GET     /api/interactions/mylikes/
POST    /api/interactions/bookmarks/<post_id>/
GET     /api/interactions/mybookmarks/
POST    /api/interactions/follow/<author_id>/
GET     /api/interactions/myfollowers/
GET     /api/interactions/myfollowings/
```

## **✔️ Future Enhancements**
- Add image upload  
- Categories & tags  
- Notifications  
- Advanced filtering  
- Admin analytics  

## 📘 API Documentation

Your API comes with auto-generated documentation using **drf-spectacular**.

- **Swagger UI:** `/docs/`
- **ReDoc:** `/api/schema/redoc/`
- **OpenAPI Schema:** `/api/schema/`

```python
path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
```

## **👩‍💻 Author**
**Sristi Sharma**  
GitHub: https://github.com/sristi-hub
