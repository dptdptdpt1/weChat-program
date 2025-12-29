# 后台管理界面配置
from sqladmin import Admin, ModelView, BaseView, expose
from wtforms import TextAreaField
from wtforms.widgets import TextArea
from starlette.requests import Request
from starlette.responses import RedirectResponse
from markupsafe import Markup
from app.models.event import Event
from app.models.user import User
from app.models.customer_service import CustomerService
from app.models.uploaded_image import UploadedImage
from app.models.banner import Banner


class MarkdownWidget(TextArea):
    """自定义 Markdown 编辑器 Widget"""
    
    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        kwargs.setdefault('name', field.name)
        
        # 生成 HTML 属性字符串
        html_attrs = ' '.join([f'{k}="{v}"' for k, v in kwargs.items() if k not in ['_form', '_name', '_prefix', '_translations', '_meta']])
        
        # 生成基础 textarea
        html = f'<textarea {html_attrs}>{field._value() or ""}</textarea>'
        
        # 添加 EasyMDE 编辑器脚本
        script = f'''
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/easymde@2.18.0/dist/easymde.min.css">
        <script src="https://cdn.jsdelivr.net/npm/easymde@2.18.0/dist/easymde.min.js"></script>
        <script>
        document.addEventListener('DOMContentLoaded', function() {{
            var textarea = document.getElementById('{field.id}');
            if (textarea && !textarea.easymdeInstance) {{
                var easyMDE = new EasyMDE({{
                    element: textarea,
                    spellChecker: false,
                    placeholder: "使用 Markdown 格式编写内容...",
                    toolbar: [
                        "bold", "italic", "heading", "|",
                        "quote", "unordered-list", "ordered-list", "|",
                        "link", "image", "|",
                        "preview", "side-by-side", "fullscreen", "|",
                        "guide",
                        {{
                            name: "upload-image",
                            action: function(editor) {{
                                var input = document.createElement('input');
                                input.type = 'file';
                                input.accept = 'image/*';
                                input.onchange = function(e) {{
                                    var file = e.target.files[0];
                                    if (!file) return;
                                    
                                    // 显示上传提示
                                    var cm = editor.codemirror;
                                    var stat = editor.getState(cm);
                                    var text = '![上传中...]()';
                                    cm.replaceSelection(text);
                                    
                                    // 上传文件
                                    var formData = new FormData();
                                    formData.append('file', file);
                                    
                                    fetch('/api/upload/image?type=event', {{
                                        method: 'POST',
                                        body: formData
                                    }})
                                    .then(response => response.json())
                                    .then(data => {{
                                        if (data.code === 200) {{
                                            // 替换上传中的文本为实际的图片链接
                                            var content = cm.getValue();
                                            var newContent = content.replace(
                                                '![上传中...]()',
                                                '![图片](' + data.data.url + ')'
                                            );
                                            cm.setValue(newContent);
                                            
                                            // 显示成功提示
                                            alert('图片上传成功！');
                                        }} else {{
                                            alert('上传失败: ' + (data.message || '未知错误'));
                                            // 删除上传中的文本
                                            var content = cm.getValue();
                                            var newContent = content.replace('![上传中...]()', '');
                                            cm.setValue(newContent);
                                        }}
                                    }})
                                    .catch(error => {{
                                        alert('上传失败: ' + error.message);
                                        // 删除上传中的文本
                                        var content = cm.getValue();
                                        var newContent = content.replace('![上传中...]()', '');
                                        cm.setValue(newContent);
                                    }});
                                }};
                                input.click();
                            }},
                            className: "fa fa-upload",
                            title: "上传图片"
                        }}
                    ],
                    status: ["lines", "words", "cursor"],
                    renderingConfig: {{
                        codeSyntaxHighlighting: true
                    }}
                }});
                textarea.easymdeInstance = easyMDE;
            }}
        }});
        </script>
        '''
        
        return Markup(html + script)


class MarkdownField(TextAreaField):
    """Markdown 字段"""
    widget = MarkdownWidget()


class EventAdmin(ModelView, model=Event):
    """赛事管理"""
    
    # 列表页显示的列
    column_list = [
        Event.id,
        Event.title,
        Event.date,
        Event.view_count,
        Event.created_at,
        Event.updated_at
    ]
    
    # 可搜索的列
    column_searchable_list = [Event.title]
    
    # 可排序的列
    column_sortable_list = [
        Event.id,
        Event.date,
        Event.view_count,
        Event.created_at
    ]
    
    # 默认排序
    column_default_sort = [(Event.created_at, True)]  # True = 降序
    
    # 表单中显示的字段
    form_columns = [
        Event.title,
        Event.date,
        Event.content
    ]
    
    # 使用自定义的 Markdown 编辑器
    form_overrides = {
        'content': MarkdownField
    }
    
    # 列表页每页显示数量
    page_size = 20
    
    # 列表页可选的每页数量
    page_size_options = [10, 20, 50, 100]
    
    # 显示名称
    name = "赛事"
    name_plural = "赛事管理"
    icon = "fa-solid fa-futbol"
    
    # 列显示格式化
    column_formatters = {
        Event.content: lambda m, a: (m.content[:50] + '...') if m.content and len(m.content) > 50 else m.content
    }
    
    # 列标签
    column_labels = {
        Event.id: "ID",
        Event.title: "标题",
        Event.date: "赛事日期",
        Event.content: "内容 (Markdown)",
        Event.cover_image: "封面图",
        Event.view_count: "浏览量",
        Event.created_at: "创建时间",
        Event.updated_at: "更新时间"
    }
    
    # 表单说明
    form_args = {
        'title': {
            'description': '赛事标题，如：英超联赛 - 曼联 vs 利物浦'
        },
        'date': {
            'description': '赛事举办日期'
        },
        'content': {
            'description': '使用 Markdown 编辑器编写内容。点击工具栏的上传按钮可以直接上传图片。第一张图片会自动作为封面。'
        }
    }
    
    async def on_model_change(self, data: dict, model: Event, is_created: bool, request: Request) -> None:
        """
        在模型保存前的钩子函数
        自动从内容中提取封面图
        """
        from app.utils.markdown_helper import extract_first_image
        
        # 如果有内容，提取第一张图片作为封面
        if 'content' in data and data['content']:
            model.cover_image = extract_first_image(data['content'])
        
        await super().on_model_change(data, model, is_created, request)


class UserAdmin(ModelView, model=User):
    """用户管理"""
    
    column_list = [
        User.id,
        User.open_id,
        User.nick_name,
        User.created_at,
        User.last_login_at
    ]
    
    column_searchable_list = [User.nick_name, User.open_id]
    
    column_sortable_list = [
        User.id,
        User.created_at,
        User.last_login_at
    ]
    
    column_default_sort = [(User.created_at, True)]
    
    # 只读字段（不允许编辑）
    form_excluded_columns = [
        User.created_at,
        User.last_login_at
    ]
    
    page_size = 20
    page_size_options = [10, 20, 50, 100]
    
    name = "用户"
    name_plural = "用户管理"
    icon = "fa-solid fa-users"
    
    column_labels = {
        User.id: "ID",
        User.open_id: "OpenID",
        User.nick_name: "昵称",
        User.avatar_url: "头像URL",
        User.created_at: "注册时间",
        User.last_login_at: "最后登录"
    }


class CustomerServiceAdmin(ModelView, model=CustomerService):
    """客服配置管理"""
    
    column_list = [
        CustomerService.id,
        CustomerService.qr_code_url,
        CustomerService.online_time,
        CustomerService.updated_at
    ]
    
    form_columns = [
        CustomerService.qr_code_url,
        CustomerService.online_time
    ]
    
    # 只允许编辑，不允许删除和创建（只有一条配置记录）
    can_create = False
    can_delete = False
    
    name = "客服配置"
    name_plural = "客服配置"
    icon = "fa-solid fa-headset"
    
    column_labels = {
        CustomerService.id: "ID",
        CustomerService.qr_code_url: "二维码URL",
        CustomerService.online_time: "在线时间",
        CustomerService.updated_at: "更新时间"
    }


class BannerAdmin(ModelView, model=Banner):
    """顶部滚动栏管理"""
    
    column_list = [
        Banner.id,
        Banner.title,
        Banner.image_url,
        Banner.sort_order,
        Banner.is_active,
        Banner.created_at
    ]
    
    column_searchable_list = [Banner.title]
    
    column_sortable_list = [
        Banner.id,
        Banner.sort_order,
        Banner.is_active,
        Banner.created_at
    ]
    
    column_default_sort = [(Banner.sort_order, False), (Banner.id, False)]
    
    form_columns = [
        Banner.image_url,
        Banner.title,
        Banner.link_url,
        Banner.sort_order,
        Banner.is_active
    ]
    
    page_size = 20
    page_size_options = [10, 20, 50, 100]
    
    name = "轮播图"
    name_plural = "顶部滚动栏"
    icon = "fa-solid fa-images"
    
    column_labels = {
        Banner.id: "ID",
        Banner.image_url: "图片URL",
        Banner.title: "标题",
        Banner.link_url: "跳转链接",
        Banner.sort_order: "排序",
        Banner.is_active: "启用",
        Banner.created_at: "创建时间",
        Banner.updated_at: "更新时间"
    }
    
    form_args = {
        'image_url': {
            'description': '轮播图图片URL，如：/uploads/banners/banner1.jpg。点击赛事内容编辑器的上传按钮上传图片后复制URL'
        },
        'title': {
            'description': '轮播图标题（可选），用于标识轮播图'
        },
        'link_url': {
            'description': '点击轮播图后跳转的链接（可选），留空则不跳转'
        },
        'sort_order': {
            'description': '排序顺序，数字越小越靠前显示。建议使用 10, 20, 30... 便于后续插入'
        },
        'is_active': {
            'description': '是否启用此轮播图。未启用的轮播图不会在前端显示'
        }
    }
    
    column_formatters = {
        Banner.image_url: lambda m, a: f'<a href="{m.image_url}" target="_blank">查看图片</a>',
        Banner.is_active: lambda m, a: '✓ 启用' if m.is_active else '✗ 禁用'
    }


class UploadedImageAdmin(ModelView, model=UploadedImage):
    """上传图片管理"""
    
    column_list = [
        UploadedImage.id,
        UploadedImage.filename,
        UploadedImage.url,
        UploadedImage.type,
        UploadedImage.size,
        UploadedImage.created_at
    ]
    
    column_searchable_list = [UploadedImage.filename, UploadedImage.url]
    
    column_sortable_list = [
        UploadedImage.id,
        UploadedImage.filename,
        UploadedImage.type,
        UploadedImage.size,
        UploadedImage.created_at
    ]
    
    column_default_sort = [(UploadedImage.created_at, True)]
    
    # 只读字段（不允许编辑）
    form_excluded_columns = [
        UploadedImage.created_at
    ]
    
    # 不允许创建（只能通过上传API创建）
    can_create = False
    can_edit = False
    
    page_size = 20
    page_size_options = [10, 20, 50, 100]
    
    name = "图片"
    name_plural = "图片管理"
    icon = "fa-solid fa-image"
    
    column_labels = {
        UploadedImage.id: "ID",
        UploadedImage.filename: "文件名",
        UploadedImage.url: "访问URL",
        UploadedImage.type: "类型",
        UploadedImage.size: "大小(字节)",
        UploadedImage.created_at: "上传时间"
    }
    
    # 列显示格式化
    column_formatters = {
        UploadedImage.size: lambda m, a: f"{m.size_kb} KB",
        UploadedImage.url: lambda m, a: f'<a href="{m.url}" target="_blank">{m.url}</a>'
    }
    
    column_formatters_detail = {
        UploadedImage.url: lambda m, a: f'''
            <div>
                <p><strong>访问URL:</strong> <a href="{m.url}" target="_blank">{m.url}</a></p>
                <p><strong>Markdown语法:</strong> <code>{m.markdown_syntax}</code></p>
                <img src="{m.url}" style="max-width: 400px; margin-top: 10px;" />
            </div>
        '''
    }


class ImageUploadView(BaseView):
    """图片上传页面"""
    
    name = "上传图片"
    icon = "fa-solid fa-upload"
    
    @expose("/upload", methods=["GET", "POST"])
    async def upload_page(self, request: Request):
        """图片上传页面"""
        
        # 处理上传请求
        if request.method == "POST":
            from app.routes.upload import (
                ensure_upload_dir, 
                get_file_extension, 
                generate_filename,
                ALLOWED_EXTENSIONS,
                MAX_FILE_SIZE,
                UPLOAD_DIR
            )
            from app.models.uploaded_image import UploadedImage
            from app.utils.database import SessionLocal
            from datetime import datetime
            
            form = await request.form()
            file = form.get("file")
            upload_type = form.get("type", "event")
            
            error_message = None
            success_data = None
            
            if file and hasattr(file, 'filename'):
                # 验证文件扩展名
                ext = get_file_extension(file.filename)
                if ext not in ALLOWED_EXTENSIONS:
                    error_message = f"不支持的文件格式。允许的格式: {', '.join(ALLOWED_EXTENSIONS)}"
                else:
                    # 读取文件内容
                    contents = await file.read()
                    
                    # 验证文件大小
                    if len(contents) > MAX_FILE_SIZE:
                        error_message = f"文件太大。最大允许 {MAX_FILE_SIZE / 1024 / 1024}MB"
                    else:
                        # 确保上传目录存在
                        ensure_upload_dir()
                        
                        # 生成文件名
                        filename = generate_filename(file.filename)
                        
                        # 确定保存路径
                        if upload_type == "thumbnail":
                            save_dir = UPLOAD_DIR / "thumbnails"
                        else:
                            save_dir = UPLOAD_DIR / "events"
                        
                        file_path = save_dir / filename
                        
                        # 保存文件
                        try:
                            with open(file_path, "wb") as f:
                                f.write(contents)
                            
                            # 返回访问URL
                            url = f"/uploads/{upload_type}s/{filename}"
                            
                            # 保存到数据库
                            db = SessionLocal()
                            try:
                                uploaded_image = UploadedImage(
                                    filename=filename,
                                    url=url,
                                    size=len(contents),
                                    type=upload_type,
                                    created_at=datetime.utcnow()
                                )
                                db.add(uploaded_image)
                                db.commit()
                                db.refresh(uploaded_image)
                                
                                success_data = {
                                    "id": uploaded_image.id,
                                    "url": url,
                                    "filename": filename,
                                    "size": len(contents),
                                    "size_kb": round(len(contents) / 1024, 2),
                                    "type": upload_type,
                                    "markdown": f"![图片描述]({url})"
                                }
                            finally:
                                db.close()
                                
                        except Exception as e:
                            error_message = f"保存文件失败: {str(e)}"
            else:
                error_message = "请选择要上传的图片文件"
            
            # 返回结果页面
            return self._render_upload_page(error_message, success_data)
        
        # GET 请求，显示上传表单
        return self._render_upload_page()
    
    def _render_upload_page(self, error_message=None, success_data=None):
        """渲染上传页面"""
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>上传图片 - 宝利足球赛事通</title>
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
            <style>
                body {
                    background-color: #f5f5f5;
                    padding: 20px;
                }
                .upload-container {
                    max-width: 800px;
                    margin: 0 auto;
                    background: white;
                    padding: 30px;
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
                .upload-area {
                    border: 2px dashed #ddd;
                    border-radius: 8px;
                    padding: 40px;
                    text-align: center;
                    margin: 20px 0;
                    background: #fafafa;
                }
                .upload-area:hover {
                    border-color: #0d6efd;
                    background: #f0f8ff;
                }
                .preview-image {
                    max-width: 100%;
                    max-height: 400px;
                    margin: 20px 0;
                    border-radius: 4px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                }
                .result-box {
                    background: #f8f9fa;
                    padding: 15px;
                    border-radius: 4px;
                    margin: 10px 0;
                    font-family: monospace;
                }
                .copy-btn {
                    margin-left: 10px;
                }
                .back-link {
                    margin-bottom: 20px;
                    display: inline-block;
                }
            </style>
        </head>
        <body>
            <div class="upload-container">
                <a href="/admin" class="back-link">
                    <i class="fas fa-arrow-left"></i> 返回后台首页
                </a>
                
                <h2><i class="fas fa-upload"></i> 上传图片</h2>
                <p class="text-muted">上传图片后，复制 Markdown 语法到赛事内容中使用</p>
                
                <hr>
        """
        
        # 显示错误消息
        if error_message:
            html += f"""
                <div class="alert alert-danger alert-dismissible fade show" role="alert">
                    <i class="fas fa-exclamation-circle"></i> {error_message}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
            """
        
        # 显示成功结果
        if success_data:
            html += f"""
                <div class="alert alert-success" role="alert">
                    <i class="fas fa-check-circle"></i> 图片上传成功！
                </div>
                
                <div class="card mb-3">
                    <div class="card-header">
                        <strong>上传结果</strong>
                    </div>
                    <div class="card-body">
                        <img src="{success_data['url']}" class="preview-image" alt="上传的图片">
                        
                        <div class="mb-3">
                            <label class="form-label"><strong>文件信息</strong></label>
                            <div class="result-box">
                                文件名: {success_data['filename']}<br>
                                大小: {success_data['size_kb']} KB<br>
                                类型: {success_data['type']}<br>
                                ID: {success_data['id']}
                            </div>
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label"><strong>访问 URL</strong></label>
                            <div class="input-group">
                                <input type="text" class="form-control" id="url-input" value="{success_data['url']}" readonly>
                                <button class="btn btn-outline-secondary" type="button" onclick="copyToClipboard('url-input')">
                                    <i class="fas fa-copy"></i> 复制
                                </button>
                            </div>
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label"><strong>Markdown 语法</strong></label>
                            <div class="input-group">
                                <input type="text" class="form-control" id="markdown-input" value="{success_data['markdown']}" readonly>
                                <button class="btn btn-primary" type="button" onclick="copyToClipboard('markdown-input')">
                                    <i class="fas fa-copy"></i> 复制
                                </button>
                            </div>
                            <small class="text-muted">复制此语法到赛事内容中使用</small>
                        </div>
                        
                        <a href="/admin/imageuploadview/upload" class="btn btn-success">
                            <i class="fas fa-plus"></i> 继续上传
                        </a>
                        <a href="/admin/uploadedimage/list" class="btn btn-secondary">
                            <i class="fas fa-images"></i> 查看所有图片
                        </a>
                    </div>
                </div>
            """
        else:
            # 显示上传表单
            html += """
                <form method="post" enctype="multipart/form-data">
                    <div class="mb-3">
                        <label class="form-label"><strong>图片类型</strong></label>
                        <select class="form-select" name="type" id="type-select">
                            <option value="event">赛事图片</option>
                            <option value="thumbnail">缩略图</option>
                        </select>
                        <small class="text-muted">选择图片用途</small>
                    </div>
                    
                    <div class="upload-area">
                        <i class="fas fa-cloud-upload-alt fa-3x text-muted mb-3"></i>
                        <h5>选择图片文件</h5>
                        <p class="text-muted">支持 JPG, PNG, GIF, WebP 格式，最大 5MB</p>
                        <input type="file" class="form-control" name="file" id="file-input" 
                               accept=".jpg,.jpeg,.png,.gif,.webp" required
                               onchange="previewImage(this)">
                    </div>
                    
                    <div id="preview-container" style="display: none;">
                        <label class="form-label"><strong>图片预览</strong></label>
                        <div class="text-center">
                            <img id="preview" class="preview-image" alt="预览">
                        </div>
                    </div>
                    
                    <div class="d-grid gap-2">
                        <button type="submit" class="btn btn-primary btn-lg">
                            <i class="fas fa-upload"></i> 上传图片
                        </button>
                    </div>
                </form>
                
                <hr>
                
                <div class="card">
                    <div class="card-header">
                        <strong><i class="fas fa-info-circle"></i> 使用说明</strong>
                    </div>
                    <div class="card-body">
                        <ol>
                            <li>选择图片类型（赛事图片或缩略图）</li>
                            <li>点击上传区域选择图片文件</li>
                            <li>预览图片无误后，点击"上传图片"按钮</li>
                            <li>上传成功后，复制 Markdown 语法</li>
                            <li>在赛事管理中编辑内容时，粘贴 Markdown 语法</li>
                        </ol>
                        
                        <div class="alert alert-info mb-0">
                            <strong>提示：</strong>内容中的第一张图片会自动作为赛事封面图
                        </div>
                    </div>
                </div>
            """
        
        html += """
            </div>
            
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
            <script>
                function previewImage(input) {
                    if (input.files && input.files[0]) {
                        const reader = new FileReader();
                        reader.onload = function(e) {
                            document.getElementById('preview').src = e.target.result;
                            document.getElementById('preview-container').style.display = 'block';
                        };
                        reader.readAsDataURL(input.files[0]);
                    }
                }
                
                function copyToClipboard(elementId) {
                    const input = document.getElementById(elementId);
                    input.select();
                    document.execCommand('copy');
                    
                    // 显示复制成功提示
                    const btn = event.target.closest('button');
                    const originalHTML = btn.innerHTML;
                    btn.innerHTML = '<i class="fas fa-check"></i> 已复制';
                    btn.classList.add('btn-success');
                    
                    setTimeout(() => {
                        btn.innerHTML = originalHTML;
                        btn.classList.remove('btn-success');
                    }, 2000);
                }
            </script>
        </body>
        </html>
        """
        
        from starlette.responses import HTMLResponse
        return HTMLResponse(content=html)


def setup_admin(app, engine):
    """
    设置后台管理界面
    
    Args:
        app: FastAPI 应用实例
        engine: SQLAlchemy 引擎
    """
    admin = Admin(
        app,
        engine,
        title="宝利足球赛事通 - 后台管理",
        base_url="/admin"
    )
    
    # 注册模型视图
    admin.add_view(EventAdmin)
    admin.add_view(BannerAdmin)
    admin.add_view(CustomerServiceAdmin)
    
    return admin
